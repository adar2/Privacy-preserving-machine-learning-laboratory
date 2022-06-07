import numpy as np
import pandas as pd

number_of_patients = 100000

start_time = 10
end_time = 1000

times = np.random.randint(low=start_time, high=end_time, size=number_of_patients)
Died = np.random.randint(2, size=number_of_patients)
group = np.random.randint(low=1, high=3, size=number_of_patients)

df = pd.DataFrame({"time": times, "Died": Died, "group": group})

df.to_csv('test-data3.txt', index=False)
