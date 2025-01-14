# -*- coding: utf-8 -*-


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import seaborn as sns # Seaborn for data visualization

# Load the data
df = pd.read_csv('data_moods.csv') #change address accordingly
# print(df)

# from google.colab import drive
# drive.mount('/content/drive')

# Feature engineering
X = df.loc[:, 'popularity':'time_signature']
max_len = max(X['length'])
X['length'] = X['length']/max(X['length'])

# Mapping class label to respected integer
y = df['mood'].map({'Happy': 0, 'Sad': 1, 'Energetic': 2, 'Calm':3})
target_names = ['Happy', 'Sad', 'Energetic', 'Calm']

from xgboost import XGBClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import GradientBoostingClassifier
# from lightgbm import LGBMClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# Splitting training data and testing data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)




clf = XGBClassifier()
clf.fit(X_train, y_train)
predictions = clf.predict(X_test)
accuracy = accuracy_score(predictions, y_test)
print(accuracy)
print(classification_report(predictions, y_test, target_names=target_names))

def predict_emotion(features1):
    pred = clf.predict(features1)
    return target_names[pred[0]]



