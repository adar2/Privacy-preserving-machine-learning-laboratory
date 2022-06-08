import numpy as np
import pandas as pd


class DataGenerator:
    def __init__(self, number_of_patients=200, start_time=10, end_time=1000):
        self.number_of_patients = number_of_patients
        self.start_time = start_time
        self.end_time = end_time

    def generate_data(self, file_name):
        times = np.random.randint(low=self.start_time, high=self.end_time, size=self.number_of_patients)
        died = np.random.randint(2, size=self.number_of_patients)
        group = np.random.randint(low=1, high=3, size=self.number_of_patients)
        df = pd.DataFrame({"time": times, "Died": died, "group": group})
        df.to_csv(file_name, index=False)
