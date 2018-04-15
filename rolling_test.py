__author__ = 'foursking'

import pandas as pd
import numpy as np
df = pd.DataFrame({'key1':['a','a','b','b','a'],
               'key2':['one','two','one','two','one'],
               'data1':np.nan,
               'data2':np.random.randn(5)})

print(df.head())

df1 = pd.rolling_sum(df,window = 2,min_periods = 1, closed="right")
print(df1.head())