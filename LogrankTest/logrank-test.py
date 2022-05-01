import math

import pandas as pd


class LogRankTest:
    def __init__(self, data: pd.DataFrame):
        self.df = data
        self.number_of_subjects = len(df)

    def __get_distinct_time(self):
        return sorted(self.df['time'].unique())

    def __get_subjects_at_risk(self, time, group=None):
        if group is None:
            return len(self.df[df.time >= time])
        return len(self.df[(df.time >= time) & (df.group == group)])

    def __get_number_of_failures(self, time, group=None):
        if group is None:
            return len(self.df[(df.time == time) & (df.Died == 1)])
        return len(self.df[(df.time == time) & (df.Died == 1) & (df.group == group)])

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


if __name__ == '__main__':
    df = pd.read_csv('../Datasets/test-data.txt', sep='\t')
    l = LogRankTest(df)
    res = l.test()
    print(f'group A Z value :{res[0]}, group B Z value:{res[1]}, their sum {res[0] + res[1]}')
    # print()
    # T1 = list(df[df.group == 1].time)
    # T2 = list(df[df.group == 2].time)
    # E1 = list(df[df.group == 1].Died)
    # E2 = list(df[df.group == 2].Died)
    #
    # results = logrank_test(T1, T2, event_observed_A=E1, event_observed_B=E2)
    # results.ascii_print()