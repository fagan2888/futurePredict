__author__ = 'foursking'
import pandas as pd
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from datetime import datetime

df = pd.read_csv("./data/bitmex_future.csv")

askPrice = df['askPrice1'].values
bidPrice = df['bidPrice1'].values
dates = df['datetime'].values
dates = [datetime.strptime(x, '%Y-%m-%dT%H:%M:%S.%fZ') for x in dates]

print askPrice[0:10]
print bidPrice[0:10]
closePrice = (askPrice + bidPrice) / 2
spreadPrice = askPrice - bidPrice


close_dir = askPrice[1:] - askPrice[:-1]

win_count = 0
loss_count = 0

N = 100
M = 600
T = 7
TRIG_PERCENT = 0.0004
MAX_TRIGING_LEG = 20
MIN_T = 10
MAX_T = 30
MAX_SPREAD = 5
WIN_TICK = 30



def direction(s):
    dir = 0
    for i in range(len(s) - 1):
        if s[i+1] - s[i] > 0:
            dir += 1
        else:
            dir -= 1
    return 0


for N in [ 50,  100,  200, 250, 300, 400, 500]:
    for UP_TREND in [0.0012, 0.0015, 0.002, 0.0023, 0.0025, 0.003]:
        for TRIG_PERCENT in [-1, 0 ]:
            for WIN_TICK in [30, 55, 80]:
                win_count = 0
                loss_count = 0
                for i in range(M, len(askPrice)):

                    K = i - M
                    for k in range(K, i):
                        if (dates[i] - dates[k]).seconds < N:
                            K = k
                            break

                    # print i, K

                    open_flag = abs(closePrice[i] - closePrice[i - 1]) < MAX_TRIGING_LEG and spreadPrice[i] < 2 and \
                                closePrice[i - 1] - closePrice[i - 2] > 0 and 1.0 * (
                    closePrice[i] - closePrice[i - 1]) / (closePrice[i - 1] - closePrice[i - 2]) > 1 and np.std(
                        closePrice[K:i - 1]) < 5 and np.std(closePrice[K:i - 1]) > 0 \
                                and (
                                1.0 * (closePrice[i] - np.max(closePrice[K:i])) / np.max(closePrice[K:i]) > TRIG_PERCENT
                                and 1.0 * (closePrice[i] - np.min(closePrice[K:i])) / np.min(closePrice[K:i]) > UP_TREND
                                and 1.0 * (closePrice[i - 1] - np.min(closePrice[K:i - 1])) / np.min(
                                    closePrice[K:i - 1]) < UP_TREND
                                # and np.mean(closePrice[i-MA_SHORT:i+1]) > np.mean(closePrice[i-MA_LONG:i+1])
                                )
                    # open_flag = False

                    short_flag = abs(closePrice[i] - closePrice[i - 1]) < MAX_TRIGING_LEG and spreadPrice[i] < 2 and \
                                 closePrice[i - 1] - closePrice[i - 2] < 0 and 1.0 * (
                    closePrice[i] - closePrice[i - 1]) / (closePrice[i - 1] - closePrice[i - 2]) > 1 and np.std(
                        closePrice[K:i - 1]) < 5 and np.std(closePrice[K:i - 1]) > 0 \
                                 and (1.0 * (closePrice[i] - np.min(closePrice[K:i])) / np.min(
                        closePrice[K:i]) < -TRIG_PERCENT and
                                      1.0 * (closePrice[i] - np.max(closePrice[K:i])) / np.max(
                                          closePrice[K:i]) < -UP_TREND and
                                      1.0 * (closePrice[i - 1] - np.max(closePrice[K:i - 1])) / np.max(
                                          closePrice[K:i - 1]) > -UP_TREND)
                    # short_flag = False

                    # if dates[i] == '2018-04-23T15:07:00.289Z':
                    #     print closePrice[i-M:i]

                    if open_flag:
                        for l in range(i, len(closePrice)):
                            if closePrice[l] - closePrice[i] > WIN_TICK:
                                win_count += 1
                                # print 'win'
                                # print i, l
                                # print closePrice[i - 1], closePrice[i], closePrice[l], dates[i], dates[l]
                                break

                            if closePrice[l] - closePrice[i] < -WIN_TICK:
                                loss_count += 1
                                # print 'loss'
                                # print i, l
                                # print closePrice[i - 1], closePrice[i], closePrice[l], dates[i], dates[l]
                                break

                    if short_flag:
                        for l in range(i, len(closePrice)):
                            if closePrice[l] - closePrice[i] > WIN_TICK:
                                loss_count += 1
                                # print 'loss'
                                # print i, l
                                # print closePrice[i - 1], closePrice[i], closePrice[l], dates[i], dates[l]
                                break

                            if askPrice[l] - askPrice[i] < -WIN_TICK:
                                win_count += 1
                                # print 'win'
                                # print i, l
                                # print closePrice[i - 1], closePrice[i], closePrice[l], dates[i], dates[l]
                                break

                print N, TRIG_PERCENT, UP_TREND, WIN_TICK, win_count, loss_count
                print 1.0 * win_count / (win_count + loss_count)
                print win_count, loss_count