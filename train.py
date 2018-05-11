# encoding: UTF-8
__author__ = 'foursking'
import pandas as pd
import numpy as np
from utils.array_manager import ArrayManager
from utils.array_manager import VtBarData
from sklearn import linear_model, datasets
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
from sklearn import preprocessing

df = pd.read_csv("./data/train_M200.csv")
df = df.dropna()

total_length = len(df.index)
train_length = int(total_length * 0.8)

train_df, test_df = df.iloc[:train_length], df.iloc[train_length:]
#columns = filter(lambda x: x.startswith("t"), df.columns.values)
columns = ['t1', 't2', 't3', 't4', 't8', 't9', 't10', 't11', 't12', 't13', 't14', 't15', 't16',
           't17', 't18', 't19', 't20', 't21', 't25', 't26', 't27', 't28', 't29', 't30', 't31',
           't32', 't33', 't34', 't38', 't39', 't40', 't41', 't42', 't43', 't44', 't45', 't46', 't47']

train_X = train_df[columns].values
train_y = train_df['label']

test_X = test_df[columns].values
test_y = test_df['label']

scaler = preprocessing.StandardScaler().fit(train_X)
train_X = scaler.transform(train_X)
test_X = scaler.transform(test_X)

logreg = LogisticRegression(C=1e5)
logreg.fit(train_X, train_y)
y_pred = logreg.predict(test_X)
train_y_pred = logreg.predict(train_X)

model = XGBClassifier()
model.fit(train_X, train_y)

y_pred_xgboost = model.predict(test_X)
print(accuracy_score(train_y, train_y_pred))
print(confusion_matrix(train_y, train_y_pred))
print(accuracy_score(test_y, y_pred))
print(confusion_matrix(test_y, y_pred))

print(accuracy_score(test_y, y_pred_xgboost))
print(confusion_matrix(test_y, y_pred_xgboost))