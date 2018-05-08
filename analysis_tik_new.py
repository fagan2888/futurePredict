# encoding: UTF-8
__author__ = 'foursking'

import pandas as pd
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from scipy.stats import skew

df = pd.read_csv("./data/bitmex_future.csv")

askPrice = df['askPrice1'].values
bidPrice = df['bidPrice1'].values
dates = df['datetime'].values

print askPrice[0:10]
print bidPrice[0:10]
closePrice = (askPrice + bidPrice) / 2
spreadPrice = askPrice - bidPrice


close_dir = askPrice[1:] - askPrice[:-1]

win_count = 0
loss_count = 0

LONG_M = 2000
M = 400
TRIG_PERCENT = -1
UP_TREND = 0.002
MAX_TRIG_PERCENT = 0.002
MAX_TRIGING_LEG = 10
MAX_SPREAD = 2
WIN_TICK = 55


def direction(s):
    dir = 0
    for i in range(len(s) - 1):
        if s[i+1] - s[i] > 0:
            dir += 1
        else:
            dir -= 1
    return dir

def trend(s):
    A = abs(s[-1] - s[1])
    S = 0
    for i in range(len(s) - 1):
        S += abs(s[i+1] - s[i-1])
    return 1.0 * A / S

for i in range(M, len(askPrice)):

    open_flag =  abs(closePrice[i] - closePrice[i-1]) < MAX_TRIGING_LEG and spreadPrice[i] < MAX_SPREAD and closePrice[i-1] - closePrice[i-2] > 0 and 1.0 * (closePrice[i] - closePrice[i-1]) / (closePrice[i-1] - closePrice[i-2]) > 1 and np.std(closePrice[i-M:i-1]) < 4 \
            and (1.0 * (closePrice[i] - np.max(closePrice[i-M:i]))/ np.max(closePrice[i-M:i]) > TRIG_PERCENT
                 and 1.0* (closePrice[i] - np.min(closePrice[i-M:i]))/ np.min(closePrice[i-M:i]) > UP_TREND
                 and 1.0* (closePrice[i-1] - np.min(closePrice[i-M:i-1]))/ np.min(closePrice[i-M:i-1]) < UP_TREND)

    # open_flag =  abs(closePrice[i] - closePrice[i-1]) < MAX_TRIGING_LEG and spreadPrice[i] < 2 and np.std(closePrice[i-M:i-1]) < 4 \
    #         and (1.0 * (closePrice[i] - np.max(closePrice[i-M:i]))/ np.max(closePrice[i-M:i]) > TRIG_PERCENT
    #              and 1.0* (closePrice[i] - np.min(closePrice[i-M:i]))/ np.min(closePrice[i-M:i]) > UP_TREND
    #              and 1.0* (closePrice[i-1] - np.min(closePrice[i-M:i-1]))/ np.min(closePrice[i-M:i-1]) < UP_TREND)


    short_flag = abs(closePrice[i] - closePrice[i-1]) < MAX_TRIGING_LEG and spreadPrice[i] < MAX_SPREAD and closePrice[i-1] - closePrice[i-2] < 0 and 1.0 * (closePrice[i] - closePrice[i-1]) / (closePrice[i-1] - closePrice[i-2]) > 1 and np.std(closePrice[i-M:i-1]) < 4 \
            and (1.0 * (closePrice[i] - np.min(closePrice[i-M:i])) /  np.min(closePrice[i-M:i]) < -TRIG_PERCENT and
                 1.0 * (closePrice[i] - np.max(closePrice[i-M:i])) /  np.max(closePrice[i-M:i]) < -UP_TREND  and
                 1.0 * (closePrice[i-1] - np.max(closePrice[i-M:i-1]))/ np.max(closePrice[i-M:i-1]) > -UP_TREND)


    #short_flag = False

    # if dates[i] == '2018-04-23T15:07:00.289Z':
    #     print closePrice[i-M:i]

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