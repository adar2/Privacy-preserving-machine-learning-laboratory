import pandas as pd
from phe import PaillierPublicKey


def get_df_from_file(file) -> pd.DataFrame:
    return pd.read_csv(file)


def run_ASY_protocol(file, public_key: PaillierPublicKey):
    df = get_df_from_file(file)
    time_set = sorted(df['time'].unique())
    groups = df["group"].unique()
    O_a = 0
    O_b = 0
    E_a = 0
    E_b = 0
    V_a = 0
    V_b = 0
    for time in time_set:
        subjects_at_risk = len(df[df.time >= time])
        num_of_failures = len(df[(df.time == time) & (df.Died == 1)])
        for group in groups:
            group_subjects_at_risk = len(df[(df.time >= time) & (df.group == group)])
            group_num_of_failures = len(df[(df.time == time) & (df.Died == 1) & (df.group == group)])
            e = (group_subjects_at_risk / subjects_at_risk) * num_of_failures
            if subjects_at_risk == 1:
                v = 0
            else:
                v = e * ((subjects_at_risk - num_of_failures) / subjects_at_risk) * (
                        (subjects_at_risk - group_subjects_at_risk) / (subjects_at_risk - 1))
            o = group_num_of_failures
            if group == 1:
                O_a += o
                E_a += e
                V_a += v
            else:
                O_b += o
                E_b += e
                V_b += v

    m1 = public_key.encrypt(O_a - E_a)
    m2 = public_key.encrypt(V_a)
    return m1, m2
