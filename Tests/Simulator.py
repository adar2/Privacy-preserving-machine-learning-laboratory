import os
import string
from math import sqrt
from threading import Thread

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from Client.ASY import run_ASY_protocol
from Client.DataServerClient import DataServerClient
from LogrankTest.LogrankTest import LogRankTest
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

NAME_LENGTH = 10


def generate_experiment_name():
    return ''.join(np.random.choice(list(string.ascii_uppercase + string.digits)) for _ in range(NAME_LENGTH))


def run_client(client, file_path, public_key, uid):
    m1, m2 = run_ASY_protocol(file_path, public_key)
    client.submit_results(uid, m1, m2)


class ExperimentSimulator:
    def __init__(self, file_name, number_of_parties=5, simulations_to_run=100,
                 data_server_url='https://127.0.0.1:5000'):
        self.file_name = ''
        self.number_of_parties = number_of_parties
        self.simulations_to_run = simulations_to_run
        self.data = pd.read_csv(file_name)
        self.data_server_url = data_server_url

    def run_simulations(self):
        logrank_test = LogRankTest(self.data)
        logrank_test_result = logrank_test.test()
        original_z = logrank_test_result[0]
        simulation_results = []
        for _ in range(self.simulations_to_run):
            z_star = self.__run_simulation()
            delta = z_star - original_z
            print(f'z* = {z_star}, z = {original_z}')
            print(f'difference between actual Z to Z*:{delta}')
            simulation_results.append(delta)
        plt.hist(simulation_results, alpha=0.5)
        plt.title(f'z* - z: data size={len(self.data)}, {self.number_of_parties} parties , original z={original_z}')
        plt.xlabel('z* - z')
        plt.ylabel('count')
        plt.show()

    def __get_clients_and_files(self):
        client_files = []
        clients = []
        shuffled = self.data.sample(frac=1)
        splitted_data = np.array_split(shuffled, self.number_of_parties)
        for i in range(self.number_of_parties):
            client_file_name = f'client-data-file{i + 1}.txt'
            client_file = splitted_data[i]
            client_file.to_csv(client_file_name, index=False)
            client_files.append(client_file_name)
            clients.append(DataServerClient(self.data_server_url))
        return client_files, clients

    def __run_simulation(self):
        client_files, clients = self.__get_clients_and_files()
        try:
            client_threads = []
            # initialize experiment
            client = clients[0]
            status, uid = client.new_experiment(generate_experiment_name())
            _, public_key = client.get_public_key_from_uid(uid)
            # make clients act simultaneously
            for client, file_path in zip(clients, client_files):
                client_thread = Thread(target=run_client, args=(client, file_path, public_key, uid))
                client_thread.start()
                client_threads.append(client_thread)
            for client_thread in client_threads:
                client_thread.join()
            results = client.get_results(uid)[1]
            D = results['D']
            U = results['U']
            z_star = D / sqrt(U)
            return z_star
        except Exception as e:
            print(e)
        finally:
            for file in client_files:
                os.remove(file)
