from time import process_time
import matplotlib.pyplot as plt
from LogrankTest.LogrankTest import LogRankTest
from Simulator import ExperimentSimulator
import tracemalloc

MAX_NUMBER_OF_CLIENTS = 6
number_of_clients = 5

def generate_data_file(num_of_patients):
    from Datasets.DataGenerator import DataGenerator
    generated_file_name = f'GeneratedData.txt'
    generator = DataGenerator()
    if num_of_patients is not None:
        generator.number_of_patients = num_of_patients
    generator.generate_data(generated_file_name)
    return generated_file_name

def memory_simulations():
    # generate data
    generated_file_name = generate_data_file(250)
    # init simulator
    simulator = ExperimentSimulator()
    simulator.number_of_parties = 5
    simulator.simulations_to_run = 1
    simulator.file_name = generated_file_name

    # perform logrank test
    tracemalloc.start()
    LogRankTest(generated_file_name).test()
    logrank_peak = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()

    # perform ASY test
    tracemalloc.start()
    simulator.run_local_simulations()
    asy_peak = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()

    print(f"LogRank Peak Memory Usage: {logrank_peak/float(1<<10):,.0f} KBs")
    print(f"ASY Protocol Peak Memory Usage: {asy_peak/float(1<<10):,.0f} KBs")


def time_simulations():
    num_of_patients = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000]
    num_of_parties = [2, 5, 10]
    asy_times = []
    logrank_times = []

    for party in num_of_parties:
        for patients in num_of_patients:
            # generate data
            generated_file_name = generate_data_file(patients)
            # init simulator
            simulator = ExperimentSimulator()
            simulator.number_of_parties = party
            simulator.simulations_to_run = 1
            simulator.file_name = generated_file_name

            # perform logrank test
            log_t = process_time()
            LogRankTest(generated_file_name).test()
            logrank_times.append(process_time() - log_t)

            # perform ASY test
            asy_t = process_time()
            simulator.run_local_simulations()
            asy_times.append(process_time() - asy_t)
            print(f'Completed {party} parties {patients} patients')
        plt.plot(num_of_patients, logrank_times, c='r')
        plt.plot(num_of_patients, asy_times, c='g')
        plt.title(f'LogRank vs ASY Performance, Parties: {party}')
        plt.xlabel('Data Size')
        plt.ylabel('Time (Seconds)')
        plt.legend(['LogRank', 'ASY'])
        plt.show()
        logrank_times.clear()
        asy_times.clear()

    print(f'logrank: {logrank_times}')
    print(f'asy: {asy_times}')


if __name__ == '__main__':
    memory_simulations()
