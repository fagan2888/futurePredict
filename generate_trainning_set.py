# encoding: UTF-8
__author__ = 'foursking'
import pandas as pd
import numpy as np
from utils.array_manager import ArrayManager
from utils.array_manager import VtBarData

win_percent = 0.01

N = 20
M = 200


def preprocess():

    df = pd.read_csv("./data/XBTUSD_3min.csv")
    close_array = df['close']
    training_length = len(close_array)
    am = ArrayManager(N)

    #generate label
    y = np.zeros(training_length)
    for i in range(len(close_array) - M):

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

            # 当前价格和之前价格变动率
            df.loc[index, "t1"] = (volumn_array[-1] - volumn_array[-2])/volumn_array[-1]
            df.loc[index, "t2"] = (volumn_array[-1] - volumn_array[-3])/volumn_array[-1]
            df.loc[index, "t3"] = (volumn_array[-1] - volumn_array[-4])/volumn_array[-1]
            df.loc[index, "t4"] = (volumn_array[-1] - volumn_array[-5])/volumn_array[-1]

            # 当前价格增长趋势
            # df.loc[index, "t5"] = (volumn_array[-1] - volumn_array[-2])/(volumn_array[-2] - volumn_array[-3])
            # df.loc[index, "t6"] = (volumn_array[-2] - volumn_array[-3])/(volumn_array[-3] - volumn_array[-4])
            # df.loc[index, "t7"] = (volumn_array[-3] - volumn_array[-4])/(volumn_array[-4] - volumn_array[-5])

            df.loc[index, "t8"] = 1 if volumn_array[-1] - volumn_array[-2] > 0 else 0
            df.loc[index, "t9"] = 1 if volumn_array[-1] - volumn_array[-2] < 0 else 0
            df.loc[index, "t10"] = 1 if volumn_array[-2] - volumn_array[-3] > 0 else 0
            df.loc[index, "t11"] = 1 if volumn_array[-2] - volumn_array[-3] < 0 else 0
            df.loc[index, "t12"] = 1 if volumn_array[-3] - volumn_array[-4] > 0 else 0
            df.loc[index, "t13"] = 1 if volumn_array[-3] - volumn_array[-4] < 0 else 0
            df.loc[index, "t14"] = 1 if volumn_array[-4] - volumn_array[-5] > 0 else 0
            df.loc[index, "t15"] = 1 if volumn_array[-4] - volumn_array[-5] < 0 else 0

            df.loc[index, "t16"] = (volumn_array[-1] - max(volumn_array[:-1])) / volumn_array[-1]
            df.loc[index, "t17"] = (volumn_array[-1] - np.mean(volumn_array[:-1])) / volumn_array[-1]

            df.loc[index, "t18"] = (close_array[-1] - close_array[-2])/close_array[-1]
            df.loc[index, "t19"] = (close_array[-1] - close_array[-3])/close_array[-1]
            df.loc[index, "t20"] = (close_array[-1] - close_array[-4])/close_array[-1]
            df.loc[index, "t21"] = (close_array[-1] - close_array[-5])/close_array[-1]

            # 当前价格增长趋势
            # df.loc[index, "t22"] = (close_array[-1] - close_array[-2])/(close_array[-2] - close_array[-3])
            # df.loc[index, "t23"] = (close_array[-2] - close_array[-3])/(close_array[-3] - close_array[-4])
            # df.loc[index, "t24"] = (close_array[-3] - close_array[-4])/(close_array[-4] - close_array[-5])

            df.loc[index, "t25"] = 1 if close_array[-1] - close_array[-2] > 0 else 0
            df.loc[index, "t26"] = 1 if close_array[-1] - close_array[-2] < 0 else 0
            df.loc[index, "t27"] = 1 if close_array[-2] - close_array[-3] > 0 else 0
            df.loc[index, "t28"] = 1 if close_array[-2] - close_array[-3] < 0 else 0
            df.loc[index, "t29"] = 1 if close_array[-3] - close_array[-4] > 0 else 0
            df.loc[index, "t30"] = 1 if close_array[-3] - close_array[-4] < 0 else 0
            df.loc[index, "t31"] = 1 if close_array[-4] - close_array[-5] > 0 else 0
            df.loc[index, "t32"] = 1 if close_array[-4] - close_array[-5] < 0 else 0

            df.loc[index, "t33"] = (close_array[-1] - max(close_array[:-1])) / close_array[-1]
            df.loc[index, "t34"] = (close_array[-1] - np.mean(close_array[:-1])) / close_array[-1]

            ###
            # df.loc[index, "t35"] = (open_array[-1] - open_array[-2])/(open_array[-2] - open_array[-3])
            # df.loc[index, "t36"] = (open_array[-2] - open_array[-3])/(open_array[-3] - open_array[-4])
            # df.loc[index, "t37"] = (open_array[-3] - open_array[-4])/(open_array[-4] - open_array[-5])

            df.loc[index, "t38"] = 1 if open_array[-1] - open_array[-2] > 0 else 0
            df.loc[index, "t39"] = 1 if open_array[-1] - open_array[-2] < 0 else 0
            df.loc[index, "t40"] = 1 if open_array[-2] - open_array[-3] > 0 else 0
            df.loc[index, "t41"] = 1 if open_array[-2] - open_array[-3] < 0 else 0
            df.loc[index, "t42"] = 1 if open_array[-3] - open_array[-4] > 0 else 0
            df.loc[index, "t43"] = 1 if open_array[-3] - open_array[-4] < 0 else 0
            df.loc[index, "t44"] = 1 if open_array[-4] - open_array[-5] > 0 else 0
            df.loc[index, "t45"] = 1 if open_array[-4] - open_array[-5] < 0 else 0

            df.loc[index, "t46"] = (open_array[-1] - max(open_array[:-1])) / open_array[-1]
            df.loc[index, "t47"] = (open_array[-1] - np.mean(open_array[:-1])) / open_array[-1]

    print(df.head(30))
    return df

df = preprocess()
df.reset_index().to_csv("./data/train_M200.csv")


