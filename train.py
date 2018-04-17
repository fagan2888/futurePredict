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

df = pd.read_csv("./data/train_M5.csv")
df = df.dropna()

total_length = len(df.index)
train_length = int(total_length * 0.8)

train_df, test_df = df.iloc[:train_length], df.iloc[train_length:]
train_X = train_df[['t1', 't2', 't3', 't4', 't5', 't6', 't7', 't8', 't9', 't10', 't11', 't12' ]].values
train_y = train_df['label']

test_X = test_df[['t1', 't2', 't3', 't4', 't5', 't6', 't7', 't8', 't9', 't10', 't11', 't12' ]].values
test_y = test_df['label']

logreg = LogisticRegression(C=1e5)
logreg.fit(train_X, train_y)
y_pred = logreg.predict(test_X)
train_y_pred = logreg.predict(train_X)

# model = XGBClassifier()
# model.fit(X, y)

#y_pred_xgboost = model.predict(X)
print(accuracy_score(train_y, train_y_pred))
print(confusion_matrix(train_y, train_y_pred))
print(accuracy_score(test_y, y_pred))
print(confusion_matrix(test_y, y_pred))

# print(accuracy_score(y, y_pred_xgboost))
# print(confusion_matrix(y, y_pred_xgboost))