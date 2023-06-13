import random

import pandas as pd
import numpy as np

def sample1():
    data = {}
    data['time'] = pd.timedelta_range(start='0 day', periods=10000, freq='10L')
    data['sigma1'] = np.random.normal(20, 1, 10000)
    data['sigma2'] = np.random.normal(20, 2, 10000)

    a = np.random.normal(18, 0.7, 5000)
    b = np.random.normal(22, 0.7, 5000)
    data['double'] = np.concatenate([a,b])

    data_df = pd.DataFrame(data)
    data_df['time'] = data_df['time'].astype(str).str.extract('days (.*)')
    print(data_df)

    data_df.to_csv('src1.csv', index=False)

def sample2():
    data={}
    data['time'] = pd.timedelta_range(start='0 day', periods=10000, freq='10L')
    data['sigma1'] = np.random.normal(20, 1, 10000)
    data['sigma1_noise'] = np.random.normal(20, 1, 10000)

    for i in range (30):
        idx_small = random.randint(0,5000)
        noise_small = random.randint(10, 15)
        idx_large = random.randint(5001,10000)
        noise_large = random.randint(25, 30)
        data['sigma1_noise'][idx_small] = noise_small
        data['sigma1_noise'][idx_large] = noise_large

    data_df = pd.DataFrame(data)
    data_df['time'] = data_df['time'].astype(str).str.extract('days (.*)')
    print(data_df)

    data_df.to_csv('src2.csv', index=False)

if __name__=="__main__":
    sample1()
    sample2()