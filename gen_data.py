from datetime import timedelta

import pandas as pd
import numpy as np

data = {}


data['time'] = pd.timedelta_range(start='0 day', periods=2000, freq='s')
data['sigma1'] = np.random.normal(20, 1, 2000)
data['sigma2'] = np.random.normal(20, 2, 2000)

a = np.random.normal(18, 0.7, 1000)
b = np.random.normal(22, 0.7, 1000)
data['double'] = np.concatenate([a,b])

data_df = pd.DataFrame(data)
data_df['time'] = data_df['time'].astype(str).str.extract('days (.*)')
print(data_df)

data_df.to_csv('src1.csv', index=False)