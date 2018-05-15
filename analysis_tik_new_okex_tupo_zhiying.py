# encoding: UTF-8
__author__ = 'foursking'

import pandas as pd
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from scipy.stats import skew
import matplotlib
from scipy import optimize

def f_1(x, A, B):
    return A*x + B

df = pd.read_csv("./data/okex.csv")

askPrice = df['askPrice1'].values
bidPrice = df['bidPrice1'].values
dates = df['datetime'].values

print askPrice[0:10]
print bidPrice[0:10]
closePrice = (askPrice + bidPrice) / 2
spreadPrice = askPrice - bidPrice

x = range(0, len(closePrice))
y = closePrice

close_dir = askPrice[1:] - askPrice[:-1]

win_count = 0
loss_count = 0

N = 600
M = 1000
MIN_T = 2000

TRIG_PERCENT = -1
UP_TREND = 0.004
DOWN_TREND = 0.002
MAX_SPREAD = 3
MAX_TRIGING_LEG = 5

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

i = N
count = 0
wait_signal = False
open_flag = False
WAIT_TIME = 400

last_open_win = False
last_short_win = False

short_lose = []
short_win = []
open_win = []
open_loss = []

i = M
while i < len(closePrice)- 100:

    WIN_PERCENT = 0.012
    LOS_PERCENT = 0.006

    count += 1
    open_flag = False

    # open_flag =  abs(spreadPrice[i]) < MAX_SPREAD and abs(closePrice[i] - closePrice[i-1]) < 10 \
    #              and (1.0 * (closePrice[i] - np.max(closePrice[i-M:i-N]))/ np.max(closePrice[i-M:i-N]) > 0.01
    #              and 1.0 * (closePrice[i-1] - np.max(closePrice[i-M:i-N]))/ np.max(closePrice[i-M:i-N]) < 0.01
    #              and 1.0 * (closePrice[i] - np.min(closePrice[i-N:i]))/ np.min(closePrice[i-N:i]) > UP_TREND)

    # open_flag =  abs(spreadPrice[i]) < MAX_SPREAD and abs(closePrice[i] - closePrice[i-1]) < 10 \
    #              and (1.0 * (closePrice[i] - np.max(closePrice[i-M:i]))/ np.max(closePrice[i-M:i]) > 0
    #              and 1.0 * (closePrice[i-1] - np.min(closePrice[i - N:i-1])) / np.min(closePrice[i - N:i-1]) < UP_TREND
    #              and 1.0 * (closePrice[i] - np.min(closePrice[i-N:i]))/ np.min(closePrice[i-N:i]) > UP_TREND)
    #print len(closePrice[i-M:i-N+1])
    #A1, B1 = optimize.curve_fit(f_1, range(0, M-N), closePrice[i-M:i-N])[0]
    #print A1

    max_index = np.argmax(closePrice[i-M:i-N])
    min_index = np.argmin(closePrice[i-M:i-N])
    max_value = closePrice[i-M+max_index]
    min_value = closePrice[i-M+min_index]

    # if min_index > 0:
    #     first_max_value = np.max(closePrice[i-M: i-M+min_index])
    # else:
    #     first_max_value = min_value



    # open_flag = abs(spreadPrice[i-1]) < MAX_SPREAD and abs(closePrice[i-1] - closePrice[i-2]) < 5 \
    #             and closePrice[i] - closePrice[i-1] > 0 \
    #             and (closePrice[i - 2] - np.min(closePrice[i-N:i-2])) / np.min(closePrice[i-N:i-2]) > UP_TREND \
    #             and closePrice[i] - np.max(closePrice[i-M:i]) > 0 and closePrice[i-1] - np.max(closePrice[i-M:i-1]) < 0



    open_flag = abs(spreadPrice[i-1]) < MAX_SPREAD and abs(closePrice[i-1] - closePrice[i-2]) < 5 \
                and closePrice[i] - closePrice[i-1] > 0 \
                and (closePrice[i - 2] - np.min(closePrice[i-N:i-2])) / np.min(closePrice[i-N:i-2]) < UP_TREND \
                and (closePrice[i - 1] - np.min(closePrice[i-N:i-2])) / np.min(closePrice[i-N:i-2]) > UP_TREND \
                # and np.std(closePrice[i-M:i-N]) < 5




            # open_flag =  closePrice[i] - closePrice[i-1] > 0 and abs(spreadPrice[i-1]) < MAX_SPREAD and abs(closePrice[i-1] - closePrice[i-2]) < 5 \
    #              and min_index - max_index > 500 \
    #              and (max_value - min_value) / min_value > UP \
    #              and (closePrice[i-1] - min_value) / min_value > UP_TREND \
    #              and (closePrice[i-2] - min_value) / min_value < UP_TREND \
    #              and M - min_index < N

        #wait 5 miao


    #open_flag = False

    # open_flag =  abs(closePrice[i] - closePrice[i-1]) < MAX_TRIGING_LEG and spreadPrice[i] < 2 and np.std(closePrice[i-M:i-1]) < 4 \
    #         and (1.0 * (closePrice[i] - np.max(closePrice[i-M:i]))/ np.max(closePrice[i-M:i]) > TRIG_PERCENT
    #              and 1.0* (closePrice[i] - np.min(closePrice[i-M:i]))/ np.min(closePrice[i-M:i]) > UP_TREND
    #              and 1.0* (closePrice[i-1] - np.min(closePrice[i-M:i-1]))/ np.min(closePrice[i-M:i-1]) < UP_TREND)


    short_flag =  abs(closePrice[i] - closePrice[i-1]) < 10 and spreadPrice[i] < 3 and np.std(closePrice[i-M:i-1]) < 5 \
                  and (closePrice[i-1] - np.min(closePrice[i - M:i-1]) > 0 and
                  1.0 * (closePrice[i] - np.max(closePrice[i-N:i])) / np.max(closePrice[i-N:i]) < -DOWN_TREND)

    short_flag = False

    # short_flag = abs(closePrice[i] - closePrice[i-1]) < MAX_TRIGING_LEG and spreadPrice[i] < MAX_SPREAD and closePrice[i-1] - closePrice[i-2] < 0 and 1.0 * (closePrice[i] - closePrice[i-1]) / (closePrice[i-1] - closePrice[i-2]) > 2 and np.std(closePrice[i-M:i-2]) < 4.5 \
    #         and (1.0 * (closePrice[i] - np.min(closePrice[i-M:i])) /  np.min(closePrice[i-M:i]) < -TRIG_PERCENT and
    #              1.0 * (closePrice[i] - np.max(closePrice[i-M:i])) /  np.max(closePrice[i-M:i]) < -UP_TREND  and
    #              1.0 * (closePrice[i-1] - np.max(closePrice[i-M:i-1]))/ np.max(closePrice[i-M:i-1]) > -UP_TREND)



    # if dates[i] == '2018-04-23T15:07:00.289Z':
    #     print closePrice[i-M:i]
#
    if open_flag :
        for l in range(i, len(closePrice)):

            #如果刚开始就盈利那么正常止损止盈
            # #如果刚开始亏，减少止损阈值
            # if l - i > WAIT_TIME:
            #     if np.mean(closePrice[i:l]) < closePrice[i]:
            #         LOS_PERCENT = 0.003
            # if l - i > MIN_T:
            #     WIN_PERCENT = 0.005
            #     LOS_PERCENT = 0.005



            if 1.0 * (closePrice[l] - closePrice[i]) / closePrice[i] >  WIN_PERCENT:
                if last_open_win:
                    open_win.append(i)
                    win_count += 1

                last_open_win = True
                print 'open win'
                print i, l
                i = l + 1
                print closePrice[i-1], closePrice[i], closePrice[l], dates[i], dates[l]
                break

            if 1.0 * (closePrice[l] - closePrice[i]) / closePrice[i] < -LOS_PERCENT:
                if last_open_win:
                    open_loss.append(i)
                    loss_count += 1

                last_open_win = True
                print 'open loss'
                print i, l
                i = l + 1
                print closePrice[i-1], closePrice[i], closePrice[l], dates[i], dates[l]
                break
        i += 1

    elif short_flag:
        for l in range(i, len(closePrice)):

            if 1.0*(closePrice[l] - closePrice[i]) / closePrice[i] > WIN_PERCENT:
                if last_short_win:
                    short_lose.append(i)
                    loss_count += 1
                last_short_win = True
                print 'short loss'
                print i, l
                print closePrice[i-1], closePrice[i], closePrice[l], dates[i], dates[l]
                break

            if 1.0*(closePrice[l] - closePrice[i]) / closePrice[i] < - WIN_PERCENT:
                if last_short_win:
                    short_win.append(i)
                    win_count += 1
                last_short_win = True
                print 'short win'
                print i, l
                print closePrice[i-1], closePrice[i], closePrice[l], dates[i], dates[l]
                break
        i += 1
    else:
        i += 1

print 1.0 * win_count / (win_count + loss_count)
print win_count, loss_count

plt.plot(x, y, color='blue')
plt.scatter(open_win, [y[i] for i in open_win], marker='+', c='red',s = 300)
plt.scatter(open_loss, [y[i] for i in open_loss], marker='*', c='green',s = 300)
plt.scatter(short_win, [y[i] for i in short_win], marker='+', c='red',s = 300)
plt.scatter(short_lose, [y[i] for i in short_lose], marker='*', c='green',s = 300)
plt.show()


