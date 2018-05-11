__author__ = 'foursking'
import pandas as pd
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

df = pd.read_csv("./data/spread.txt")
x = df['x'].values


import matplotlib.pylab as plt
plt.figure(figsize=(21, 12))
plt.hist(x, bins=50)
# plt.hist(df['title'].apply(lambda x: len(x)), bins=50)
plt.grid()
plt.savefig('distribution.png')

print df.iloc[[2]]