# encoding: UTF-8
__author__ = 'foursking'

import pandas as pd
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from scipy.stats import skew
import talib

df = pd.read_csv("./data/XBTUSD_5min.csv")

high = df['high'].values
low = df['low'].values
open = df['open'].values
close = df['close'].values
dates = df['timestamp'].values
volume = df['volume']

x = range(0, len(close))
y = close

M = 300
#paramater
FAST_MA = 20
SLOW_MA = 100
WIN_PERCENT = 0.01
TRIG_PERCENT = 30
MACD_K = 5

#MACD
macd_slow = 26
macd_fast = 12
macd_period = 9


win_count = 0
loss_count = 0

long_win = []
long_loss = []
short_win = []
short_loss = []

long_win_tick = []
long_loss_tick = []

def sma(close, n):
    """简单均线"""
    result = talib.SMA(close, n)
    return result


# ----------------------------------------------------------------------
def MACD(close, fastPeriod, slowPeriod, signalPeriod):
    """MACD指标"""
    macd, signal, hist = talib.MACD(close, fastPeriod,
                                    slowPeriod, signalPeriod)
    return macd, signal, hist

i = M

while i < len(close):
    ## 1min线平衡，5min线也平衡
    #boll_up5, boll_down5 = boll(close[i-M:i+1], 40, 2)
    #std5 = (boll_up5 - boll_down5) / 4

    #open_flag = (1.0 * (close[i] - boll_up5[-1]) > 0)

    fast = sma(close[i-M:i+1], FAST_MA)
    slow = sma(close[i - M:i + 1], SLOW_MA)
    macd, signal, hist = MACD(close[i - M:i + 1], macd_fast, macd_slow, macd_period)

    long_count = 100
    for j in [-1, -2, -3, -4, -5, -6]:
        if hist[j] < 0:
            break
        else:
            long_count = j

    short_count = 100
    for j in [-1, -2, -3, -4, -5, -6]:
        if hist[j] > 0:
            break
        else:
            short_count = j



    open_flag = (close[i] - close[i-1] > 0 and close[i] - fast[-1] > 0 and close[i] - slow[-1] > TRIG_PERCENT and abs(long_count) < MACD_K
                 and volume[i] > volume[i-1]) and close[i] - open[i] > close[i-1] - open[i-1]
    short_flag =(close[i] - fast[-1] < 0 and close[i] - slow[-1] < -TRIG_PERCENT and abs(short_count) < MACD_K and volume[i] > volume[i-1])
    short_flag = False
    #open_flag = False

    if open_flag:

        for j in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
            if close[i - j] > fast[-1 - j] and open[i - j] < fast[-1-j]:
                WIN_TICK = close[i] - open[i - j]
                break

        print 'win tick'
        print WIN_TICK


        for l in range(i, len(close)):
            if close[l] - close[i] > WIN_TICK:
                win_count += 1
                long_win.append(i)
                print 'win'
                print i, l
                print close[i - 1], close[i], close[l], dates[i], dates[l]
                i = l + 1
                break

            if close[l] - close[i] < -WIN_TICK:
                loss_count += 1
                long_loss.append(i)
                print 'loss'
                print i, l
                print close[i - 1], close[i], close[l], dates[i], dates[l]
                i = l + 1
                break

    if short_flag:


        for j in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
            if close[i - j] < fast[-1 - j] and open[i - j] > fast[-1 - j]:
                WIN_TICK = abs(close[i] - open[i - j])
                break

        print 'win tick'
        print WIN_TICK

        for l in range(i, len(close)):
            if close[l] - close[i] > WIN_TICK:
                loss_count += 1
                print 'loss'
                short_loss.append(i)
                print i, l
                print close[i - 1], close[i], close[l], dates[i], dates[l]
                i = l + 1
                break

            if close[l] - close[i] < - 2 * WIN_TICK:
                win_count += 1
                short_win.append(i)
                print 'win'
                print i, l
                print close[i - 1], close[i], close[l], dates[i], dates[l]
                i = l + 1
                break
        i += 1

    else:
        i += 1

print 1.0 * win_count / (win_count + loss_count)
print win_count, loss_count

plt.plot(x, y, color='blue')
plt.scatter(long_win, [y[i] for i in long_win], marker='+', c='r',s = 100)
plt.scatter(long_loss, [y[i] for i in long_loss], marker='*', c='green',s = 100)
plt.scatter(short_win, [y[i] for i in short_win], marker='+', c='y',s = 100)
plt.scatter(short_loss, [y[i] for i in short_loss], marker='*', c='black',s = 100)
plt.show()

