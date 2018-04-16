# encoding: UTF-8
__author__ = 'foursking'
import pandas as pd
import numpy as np
from utils.array_manager import ArrayManager
from utils.array_manager import VtBarData

win_percent = 0.01
loss_percent = 0.01

N = 20
M = 20
k_min = 1

df = pd.read_csv("./data/XBTUSD_3min.csv")
print(len(df.index))
print(df.iloc[0:5])