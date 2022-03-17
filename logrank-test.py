import math

import numpy as np
import pandas as pd


# import matplotlib.pyplot as plt

class LogRankTest:
    def __init__(self, data: pd.DataFrame):
        self.df = data
        self.number_of_subjects = len(df)

    def __get_distinct_time(self):
        return sorted(self.df['time'].unique())

    def __get_subjects_at_risk(self, time, group=None):
        if group is None:
            return len(self.df[(df.time >= time) & (df.Died == 0)])
        return len(self.df[(df.time >= time) & (df.Died == 0) & (df.group == group)])

    def __get_number_of_failures(self, time, group):
        return len(self.df[(df.time == time) & (df.Died == 1) & (df.group == group)])

    @staticmethod
    def __hyper_geometric(num_of_subjects, num_of_subjects_in_group, num_of_failures):
        return np.random.hypergeometric(num_of_subjects, num_of_failures, num_of_subjects_in_group)

    @staticmethod
    def __hyper_geometric_expectation(num_of_subjects, num_of_subjects_in_group, num_of_failures):
        return (num_of_subjects_in_group / num_of_subjects) * num_of_failures

    @staticmethod
    def __hyper_geometric_variance(num_of_subjects, num_of_subjects_in_group, num_of_failures):
        if num_of_subjects == 1:
            num_of_subjects += 1
        expected_value = LogRankTest.__hyper_geometric_expectation(num_of_subjects, num_of_subjects_in_group,
                                                                   num_of_failures)
        return expected_value * ((num_of_subjects - num_of_failures) / num_of_subjects) * (
                (num_of_subjects - num_of_subjects_in_group) / (num_of_subjects - 1))

    def test(self):
        O_a = 0
        O_b = 0
        E_a = 0
        E_b = 0
        V_a = 0
        V_b = 0
        for time in self.__get_distinct_time():
            subjects_at_risk = self.__get_subjects_at_risk(time)
            for group in [1, 2]:
                group_subjects_at_risk = self.__get_subjects_at_risk(time, group)
                num_of_failures = self.__get_number_of_failures(time, group)
                if group_subjects_at_risk <= 0:
                    continue
                o = self.__hyper_geometric(subjects_at_risk, group_subjects_at_risk, num_of_failures)
                if group == 1:
                    O_a += o
                    E_a += self.__hyper_geometric_expectation(subjects_at_risk, group_subjects_at_risk, o)
                    V_a += self.__hyper_geometric_variance(subjects_at_risk, group_subjects_at_risk, o)
                else:
                    O_b += o
                    E_b += self.__hyper_geometric_expectation(subjects_at_risk, group_subjects_at_risk, o)
                    V_b += self.__hyper_geometric_variance(subjects_at_risk, group_subjects_at_risk, o)
        Z_a = (O_a - E_a) / math.sqrt(V_a)
        Z_b = (O_b - E_b) / math.sqrt(V_b)
        return (Z_a, Z_b)


if __name__ == '__main__':
    df = pd.read_csv('test-data.txt', sep='\t')
    l = LogRankTest(df)
    print(l.test())
