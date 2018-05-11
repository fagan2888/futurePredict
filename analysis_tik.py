# encoding: UTF-8
__author__ = 'foursking'

import pandas as pd
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from scipy.stats import skew

df = pd.read_csv("./data/okex.csv")

askPrice = df['askPrice1'].values
bidPrice = df['bidPrice1'].values
dates = df['datetime'].values

print askPrice[0:10]
print bidPrice[0:10]
closePrice = (askPrice + bidPrice) / 2
spreadPrice = askPrice - bidPrice

#M(100-200) 不同的力度哦
#TRIG_PERCENT 不同的力度哦

close_dir = askPrice[1:] - askPrice[:-1]

win_count = 0
loss_count = 0


N = 100
M = 250
K = 100
T = 7
TRIG_PERCENT = 0.0004
UP_TREND = 0.002
MAX_TRIG_PERCENT = 0.002
MAX_TRIGING_LEG = 10
MIN_T = 10
MAX_T = 30
MAX_SPREAD = 5
WIN_TICK = 50

def direction(s):
    dir = 0
    for i in range(len(s) - 1):
        if s[i+1] - s[i] > 0:
            dir += 1
        else:
            dir -= 1
    return 0

for i in range(M, len(askPrice)):

    open_flag =  abs(closePrice[i] - closePrice[i-1]) < MAX_TRIGING_LEG and spreadPrice[i] < 5 and closePrice[i-1] - closePrice[i-2] > 0 and 1.0 * (closePrice[i] - closePrice[i-1]) / (closePrice[i-1] - closePrice[i-2]) > 2 and np.std(closePrice[i-M:i-1]) < 5 and  np.std(closePrice[i-M:i-1]) > 0 \
            and ((closePrice[i] - np.max(closePrice[i-M:i]))/ np.max(closePrice[i-M:i]) > TRIG_PERCENT and (closePrice[i] - np.min(closePrice[i-M:i]))/ np.min(closePrice[i-M:i]) > UP_TREND)

    #open_flag = False

    short_flag = abs(closePrice[i] - closePrice[i-1]) < MAX_TRIGING_LEG and spreadPrice[i] < 5 and closePrice[i-1] - closePrice[i-2] < 0 and 1.0 * (closePrice[i] - closePrice[i-1]) / (closePrice[i-1] - closePrice[i-2]) > 2 and np.std(closePrice[i-M:i-1]) < 5 and np.std(closePrice[i-M:i-1]) > 0 \
            and ((closePrice[i] - np.min(closePrice[i-M:i])) /  np.min(closePrice[i-M:i]) < -TRIG_PERCENT and (closePrice[i] - np.max(closePrice[i-M:i])) /  np.max(closePrice[i-M:i]) < -UP_TREND)
    #short_flag = False

    if open_flag :
        for l in range(i, len(closePrice)):
            if closePrice[l] - closePrice[i] > WIN_TICK:
                win_count += 1
                print 'win'
                print i, l
                print closePrice[i-1], closePrice[i], closePrice[l], dates[i], dates[l]
                break

            if closePrice[l] - closePrice[i] < -WIN_TICK:
                loss_count += 1
                print 'loss'
                print i, l
                print closePrice[i-1], closePrice[i], closePrice[l], dates[i], dates[l]
                break

    if short_flag:
        for l in range(i, len(closePrice)):
            if closePrice[l] - closePrice[i] > WIN_TICK:
                loss_count += 1
                print 'loss'
                print i, l
                print closePrice[i-1], closePrice[i], closePrice[l], dates[i], dates[l]
                break

            if askPrice[l] - askPrice[i] < -WIN_TICK:
                win_count += 1
                print 'win'
                print i, l
                print closePrice[i-1], closePrice[i], closePrice[l], dates[i], dates[l]
                break

print 1.0 * win_count / (win_count + loss_count)
print win_count, loss_count