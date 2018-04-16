__author__ = 'foursking'
import pandas as pd
from utils.array_manager import VtBarData
import numpy as np
kmins = 3

df = pd.read_csv("./data/XBTUSD_1min.csv")

df_new = pd.DataFrame()
xminBar = None

for index, row in df.iterrows():
    if not xminBar:
        xminBar = VtBarData()
        xminBar.open = row['open']
        xminBar.high = row['high']
        xminBar.low = row['low']
        xminBar.close = row['close']
    else:
        xminBar.high = max(xminBar.high, row['high'])
        xminBar.low = min(xminBar.low, row['low'])

    xminBar.close = row['close']
    xminBar.volume += int(row['volume'])

    if not (index+1) % kmins and xminBar:
        row['open'] = xminBar.open
        row['close'] = xminBar.close
        row['high'] = xminBar.high
        row['low'] = xminBar.low
        row['volume'] = xminBar.volume
        df_new = df_new.append(row)
        xminBar = None

df_new.reset_index().to_csv("./data/XBTUSD_3min.csv")