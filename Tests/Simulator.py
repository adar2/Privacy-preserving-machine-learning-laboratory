import os
import string
from math import sqrt
from threading import Thread

import numpy as np
import pandas as pd
from PyQt5.QtCore import QThread, pyqtSignal, QObject
from matplotlib import pyplot as plt
from phe import paillier

from Client.ASY import run_ASY_protocol
from Common.Constants import KEY_SIZE
from LogrankTest.LogrankTest import LogRankTest

NAME_LENGTH = 10


def generate_experiment_name():
    return ''.join(np.random.choice(list(string.ascii_uppercase + string.digits)) for _ in range(NAME_LENGTH))


class Signal(QObject):
    inner = pyqtSignal(object)


class ExperimentSimulator(QThread):
    def __init__(self, file_name="", number_of_parties=5, simulations_to_run=100):
        super(ExperimentSimulator, self).__init__()
        self.number_of_parties = number_of_parties
        self.file_name = file_name
        self.simulations_to_run = simulations_to_run
        self.data = None
        self.public_key = None
        self.private_key = None
        self.D = None
        self.U = None
        self.figure_signal = Signal()
        self.progress_signal = Signal()

    def run(self):
        self.figure_signal.inner.emit(self.run_simulations())

    def run_local_simulations(self):
        self.data = pd.read_csv(self.file_name)
        self.public_key, self.private_key = paillier.generate_paillier_keypair(n_length=KEY_SIZE)
        z_star = self.__run_simulation()

    def run_simulations(self):
        self.data = pd.read_csv(self.file_name)
        self.public_key, self.private_key = paillier.generate_paillier_keypair(n_length=KEY_SIZE)
        logrank_test = LogRankTest(self.data)
        logrank_test_result = logrank_test.test()
        original_z = logrank_test_result[0]
        simulation_results = []
        for i in range(self.simulations_to_run + 1):
            completion_percent = round((i / self.simulations_to_run) * 100)
            self.progress_signal.inner.emit(completion_percent)
            if i == self.simulations_to_run:
                break
            z_star = self.__run_simulation()
            delta = z_star - original_z
            simulation_results.append(delta)
        fig = plt.figure()
        plt.hist(simulation_results, alpha=0.5)
        plt.title(f'z* - z: data size={len(self.data)}, {self.number_of_parties} parties , original z={original_z}')
        plt.xlabel('z* - z')
        plt.ylabel('count')
        return fig

    def __run_client(self, file_path, public_key):
        m1, m2 = run_ASY_protocol(file_path, public_key)
        self.D += m1
        self.U += m2

    def __get_client_files(self):
        client_files = []
        shuffled = self.data.sample(frac=1)
        splitted_data = np.array_split(shuffled, self.number_of_parties)
        for i in range(self.number_of_parties):
            client_file_name = f'client-data-file{i + 1}.txt'
            client_file = splitted_data[i]
            client_file.to_csv(client_file_name, index=False)
            client_files.append(client_file_name)
        return client_files

    def __run_simulation(self):
        self.D = self.public_key.encrypt(0)
        self.U = self.public_key.encrypt(0)
        client_files = self.__get_client_files()
        try:
            client_threads = []
            for file_path in client_files:
                client_thread = Thread(target=self.__run_client, args=(file_path, self.public_key))
                client_thread.start()
                client_threads.append(client_thread)
            for client_thread in client_threads:
                client_thread.join()
            D = self.private_key.decrypt(self.D)
            U = self.private_key.decrypt(self.U)
            z_star = D / sqrt(U)
            return z_star
        except Exception as e:
            print(e)
        finally:
            for file in client_files:
                os.remove(file)
