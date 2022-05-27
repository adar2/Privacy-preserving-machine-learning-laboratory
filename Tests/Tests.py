import math
import os
import random
from math import sqrt

import pandas as pd
from threading import Thread
from LogrankTest.LogrankTest import LogRankTest
from Client.ASY import run_ASY_protocol
from Client.DataServerClient import DataServerClient

MAX_NUMBER_OF_CLIENTS = 6


def run_client(client, file_path, public_key, uid):
    m1, m2 = run_ASY_protocol(file_path, public_key)
    client.submit_results(uid, m1, m2)


if __name__ == '__main__':
    client_files = []
    try:
        file_path = '../Datasets/test-data.txt'
        df = pd.read_csv(file_path)
        logrank_test = LogRankTest(df)
        test_results = logrank_test.test()
        clients = []
        client_threads = []
        number_of_clients = random.randint(1, MAX_NUMBER_OF_CLIENTS)
        with open(file_path, 'r') as data_file:
            headers = data_file.readline()
            data = data_file.readlines()
            lines_per_client = math.floor(len(data) / number_of_clients)
            remaining_lines = len(data) % number_of_clients
            print(
                f'Number of clients:{number_of_clients}, each client get {lines_per_client} rows, the last client gets {lines_per_client + remaining_lines} rows.')
            for i in range(1, number_of_clients + 1):
                if remaining_lines > 0 and i == number_of_clients:
                    lines_per_client += remaining_lines
                client_file_path = f'client_data_{i}.txt'
                with open(client_file_path, 'w') as client_file:
                    client_file.write(headers)
                    for _ in range(lines_per_client):
                        line_to_write = data.pop()
                        if not line_to_write.endswith('\n'):
                            line_to_write += '\n'
                        client_file.write(line_to_write)
                client_files.append(client_file_path)
                clients.append(DataServerClient('https://127.0.0.1:5000'))
        # initialize experiment
        client = clients[0]
        status, uid = client.new_experiment('ExperimentName')
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
        print(results)
        print(f'z* = {z_star}')
        print(f'Non-MPC LogrankTest results : {test_results}')
        print(f'difference between actual Z to Z*:{z_star - test_results[0]}')
    except Exception as e:
        print(e)
    finally:
        # delete test files\
        for file in client_files:
            os.remove(file)
