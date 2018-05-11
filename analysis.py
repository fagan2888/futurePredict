__author__ = 'foursking'
import pandas as pd
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

df = pd.read_csv("./data/XBTUSD_1min.csv")
prices_change = df['open'] - df['close']
close_array = df['close'].values
volume_array = df['volume'].values

close_dir = close_array[1:] - close_array[:-1]
volume_dir = volume_array[1:] - volume_array[:-1]
prices_change = prices_change.values


threshold = 30
volume_threshold = 10

win_count = 0
loss_count = 0

for i in range(1, len(prices_change)-1):
    if prices_change[i] > threshold and 1.0 * volume_array[i] / volume_array[i-1] > volume_threshold and  1.0 * volume_array[i-1] / volume_array[i-2] > 0.8 :
        if close_dir[i] > 0:
            win_count += 1
        else:
            loss_count += 1

print 1.0 * win_count / (win_count + loss_count)



#prices_change = df['high'] - df['low']
