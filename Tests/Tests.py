from math import sqrt

from Client.ASY import run_ASY_protocol
from Client.DataServerClient import DataServerClient

if __name__ == '__main__':
    file_path = '../Datasets/test-data2.txt'
    client = DataServerClient('https://127.0.0.1:5000')
    status, uid, public_key = client.new_experiment('ExperimentName')
    m1, m2 = run_ASY_protocol(file_path, public_key)
    client.submit_results(uid, m1, m2)
    results = client.get_results(uid)
    D = results['D']
    U = results['U']
    print(results)
    print(f'z* = {D / sqrt(U)}')
