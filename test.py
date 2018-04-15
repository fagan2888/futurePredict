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


def preprocess():

    df = pd.read_csv("./data/XBTUSD_1min.csv")
    close_array = df['close']
    training_length = len(close_array)
    am = ArrayManager(N)

    #generate label
    y = np.zeros(training_length)
    for i in range(len(close_array)):
        if i > 50:
            break

        for j in range(i + 1, i + M):
            if close_array[j] / close_array[i] > (1 + win_percent):
                y[i] = 1
                break

            if close_array[j] / close_array[i] < (1 - win_percent):
                y[i] = -1
                break

    print(close_array[0:20])
    print(y[0:20])

    df['label'] = y

    #generate feature
    # 前20的方差

    for index, row in df.iterrows():
        if index > 50:
            break
        #
        bar = VtBarData()
        bar.close = row['close']
        bar.open = row['open']
        bar.low = row['low']
        bar.high = row['high']
        bar.volume = row['volume']

        am.updateBar(bar)
        #
        if am.inited:
            volumn_array = am.volume
            open_array = am.open
            close_array = am.close

            df.loc[index, "t1"] = (volumn_array[-1] - volumn_array[-2])/volumn_array[-1]
            df.loc[index, "t2"] = (volumn_array[-1] - volumn_array[-3])/volumn_array[-1]
            df.loc[index, "t3"] = (volumn_array[-1] - max(volumn_array[:-1])) / volumn_array[-1]
            df.loc[index, "t4"] = (volumn_array[-1] - np.mean(volumn_array[:-1])) / volumn_array[-1]

            df.loc[index, "t5"] = (close_array[-1] - close_array[-2])/close_array[-1]
            df.loc[index, "t6"] = (close_array[-1] - close_array[-3])/close_array[-1]
            df.loc[index, "t7"] = (close_array[-1] - min(close_array[:-1])) / close_array[-1]
            df.loc[index, "t8"] = (close_array[-1] - max(close_array[:-1])) / close_array[-1]
            df.loc[index, "t9"] = (close_array[-1] - np.mean(close_array[:-1])) / close_array[-1]

            df.loc[index, "t10"] = (close_array[-1] - min(open_array[:-1])) / close_array[-1]
            df.loc[index, "t11"] = (close_array[-1] - max(open_array[:-1])) / close_array[-1]
            df.loc[index, "t12"] = (close_array[-1] - np.mean(open_array[:-1])) / close_array[-1]

            # 波动

    print(df.head(30))
    return df

preprocess()


