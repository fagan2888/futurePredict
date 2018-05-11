# encoding: UTF-8
__author__ = 'foursking'

import pandas as pd
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from scipy.stats import skew
import talib

df = pd.read_csv("./data/XBTUSD_1min.csv")

high = df['high'].values
low = df['low'].values
open = df['open'].values
close = df['close'].values
dates = df['timestamp'].values
volume = df['volume']

#paramater
M = 100
WIN_PERCENT = 0.01
TRIG_PERCENT = 0.4

win_count = 0
loss_count = 0

# ----------------------------------------------------------------------
def boll(close, n, dev, array=False):
    """布林通道"""
    mid = talib.SMA(close, n)
    std = talib.STDDEV(close, n)

    up = mid + std * dev
    down = mid - std * dev

    return up, down

i = M
while i < len(close):
    ## 1min线平衡，5min线也平衡
    boll_up5, boll_down5 = boll(close[i-M:i+1], 40, 2)
    std5 = (boll_up5 - boll_down5) / 4

    open_flag = (1.0 * (close[i] - boll_up5[-1]) > 0)

    if open_flag:
        for l in range(i, len(close)):
            if 1.0 * (close[l] - close[i]) / close[i] > WIN_PERCENT:
                win_count += 1
                print 'win'
                print i, l
                print close[i - 1], close[i], close[l], dates[i], dates[l]
                i = l + 1
                break

            if 1.0 * (close[l] - close[i]) / close[i] < -WIN_PERCENT:
                loss_count += 1
                print 'loss'
                print i, l
                print close[i - 1], close[i], close[l], dates[i], dates[l]
                i = l + 1
                break

    # if short_flag:
    #     for l in range(i, len(closePrice)):
    #         if closePrice[l] - closePrice[i] > WIN_TICK:
    #             loss_count += 1
    #             print 'loss'
    #             print i, l
    #             print closePrice[i - 1], closePrice[i], closePrice[l], dates[i], dates[l]
    #             break
    #
    #         if askPrice[l] - askPrice[i] < -WIN_TICK:
    #             win_count += 1
    #             print 'win'
    #             print i, l
    #             print closePrice[i - 1], closePrice[i], closePrice[l], dates[i], dates[l]
    #             break
        i += 1

    else:
        i += 1

print 1.0 * win_count / (win_count + loss_count)
print win_count, loss_count



