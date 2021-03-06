import math

import pandas as pd
from matplotlib import pyplot as plt


class LogRankTest:
    def __init__(self, dataset):
        if isinstance(dataset, str):
            self.df = pd.read_csv(dataset)
        elif isinstance(dataset, pd.DataFrame):
            self.df = dataset
        else:
            raise NotImplementedError
        self.number_of_subjects = len(self.df)

    def __get_distinct_time(self):
        return sorted(self.df['time'].unique())

    def __get_subjects_at_risk(self, time, group=None):
        if group is None:
            return len(self.df[self.df.time >= time])
        return len(self.df[(self.df.time >= time) & (self.df.group == group)])

    def __get_number_of_failures(self, time, group=None):
        if group is None:
            return len(self.df[(self.df.time == time) & (self.df.Died == 1)])
        return len(self.df[(self.df.time == time) & (self.df.Died == 1) & (self.df.group == group)])

    @staticmethod
    def __expectation(num_of_subjects, num_of_subjects_in_group, num_of_failures):
        return (num_of_subjects_in_group / num_of_subjects) * num_of_failures

    @staticmethod
    def __variance(num_of_subjects, num_of_subjects_in_group, num_of_failures):
        if num_of_subjects == 1:
            return 0
        expected_value = LogRankTest.__expectation(num_of_subjects, num_of_subjects_in_group,
                                                   num_of_failures)
        return expected_value * ((num_of_subjects - num_of_failures) / num_of_subjects) * (
                (num_of_subjects - num_of_subjects_in_group) / (num_of_subjects - 1))

    def get_data_graph(self, title='dataset representation'):
        fig = plt.figure()
        times = self.__get_distinct_time()
        remaining_a = [len(self.df[(self.df.time >= time) & (self.df.group == 1)]) / len(self.df) for time in times]
        remaining_b = [len(self.df[(self.df.time >= time) & (self.df.group == 2)]) / len(self.df) for time in times]
        plt.step(times, remaining_a, label="group A", where='pre')
        plt.step(times, remaining_b, label="group B", where='pre')
        plt.title(title)
        plt.xlabel('time')
        plt.ylabel('remaining percent %')
        plt.legend()
        return fig

    def test(self):
        O_a = 0
        O_b = 0
        E_a = 0
        E_b = 0
        V_a = 0
        V_b = 0
        for time in self.__get_distinct_time():
            subjects_at_risk = self.__get_subjects_at_risk(time)
            num_of_failures = self.__get_number_of_failures(time)
            for group in [1, 2]:
                group_subjects_at_risk = self.__get_subjects_at_risk(time, group)
                num_of_failures_in_group = self.__get_number_of_failures(time, group)
                e = self.__expectation(subjects_at_risk, group_subjects_at_risk, num_of_failures)
                v = self.__variance(subjects_at_risk, group_subjects_at_risk, num_of_failures)
                o = num_of_failures_in_group
                if group == 1:
                    O_a += o
                    E_a += e
                    V_a += v
                else:
                    O_b += o
                    E_b += e
                    V_b += v
        Z_a = (O_a - E_a) / math.sqrt(V_a)
        Z_b = (O_b - E_b) / math.sqrt(V_b)
        return (Z_a, Z_b)


def run_logrank_test(file_path: str):
    logrank = LogRankTest(file_path)
    test_results = logrank.test()
    return logrank.get_data_graph(f"Step function for LogRank test, Z={test_results[0]}")


if __name__ == '__main__':
    l = LogRankTest('../Datasets/test-data2.txt')
    res = l.test()
    print(f'group A Z value :{res[0]}, group B Z value:{res[1]}, their sum {res[0] + res[1]}')
    l.get_data_graph()
