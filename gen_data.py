import random

import pandas as pd
import numpy as np

def sample1():
    data = {}
    data['time'] = pd.timedelta_range(start='0 day', periods=1000, freq='s')
    data['sigma1'] = np.sort(np.random.normal(20, 1, 1000))

    data_df = pd.DataFrame(data)
    data_df['time'] = data_df['time'].astype(str).str.extract('days (.*)')
    print(data_df)

    data_df.to_csv('src1.csv', index=False)

def sample2():
    data = {}
    data['time'] = pd.timedelta_range(start='0 day', periods=1000, freq='10L')
    data['sigma1'] = np.sort(np.random.normal(20, 1, 1000))
    data['sigma2'] = np.sort(np.random.normal(20, 2, 1000))[::-1]

    a = np.sort(np.random.normal(17, 1, 500))
    b = np.sort(np.random.normal(23, 1, 500))
    data['double'] = np.concatenate([a,b])

    data_df = pd.DataFrame(data)
    data_df['time'] = data_df['time'].astype(str).str.extract('days (.*)')
    print(data_df)

    data_df.to_csv('src2.csv', index=False)

def sample3():
    data={}
    data['time'] = pd.timedelta_range(start='0 day', periods=100000, freq='10L')
    data['sigma1'] = np.sort(np.random.normal(20, 1, 100000))
    data['sigma1_noise'] = np.sort(np.random.normal(20, 1, 100000))

    for i in range (30):
        idx_small = random.randint(0,50000)
        noise_small = random.randint(10, 15)
        idx_large = random.randint(50001,100000)
        noise_large = random.randint(25, 30)
        data['sigma1_noise'][idx_small] = noise_small
        data['sigma1_noise'][idx_large] = noise_large

    data_df = pd.DataFrame(data)
    data_df['time'] = data_df['time'].astype(str).str.extract('days (.*)')
    print(data_df)

    data_df.to_csv('src3.csv', index=False)

if __name__=="__main__":
    sample1()
    sample2()
    sample3()