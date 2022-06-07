from Simulator import ExperimentSimulator

MAX_NUMBER_OF_CLIENTS = 6
number_of_clients = 5

if __name__ == '__main__':
    file_path = '../Datasets/test-data5.txt'
    sim = ExperimentSimulator(file_path, simulations_to_run=10)
    sim.run_simulations()
