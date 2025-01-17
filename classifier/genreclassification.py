# -*- coding: utf-8 -*-


import librosa
import librosa.display
import IPython.display as ipd
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score
from xgboost import XGBClassifier

df = pd.read_csv("features_30_sec.csv")

df

df.label.value_counts()

features = df.columns[2:59]
features

#Creating Test and Train data
df['is_train'] = np.random.uniform(0, 1, len(df)) <= .75
#View top 10 rows
df.head(10)

#Create dataframes with train and test rows
train, test = df[df['is_train']==True], df[df['is_train']==False]

#show the number of rows in test and train dataframe
print("training data ", len(train))
print("testing data ", len(test))

y = pd.factorize(train['label'])[0]
print(y)

x = pd.factorize(test['label'])[0]
print(x)

target_names = (train['label']).unique()
target_names

#Creating Random Forest Classifier
#clf = RandomForestClassifier(n_jobs=2, random_state=0)
clf = XGBClassifier()
clf.fit(train[features], y)

#Applying trained Classifier to the test
predictions = clf.predict(test[features])
predictions

#viewing predicted probablities of first 10 observation
clf.predict_proba(test[features])[:10]

#mapping names of moods for each music for each predicted mood
preds  = target_names[clf.predict(test[features])]

#View the predicted moods for firat five observations
print(preds[10:20])

#Creating confusion matrix
#crosstab takes two sets of data and forms chart out of it
pd.crosstab(test['label'], preds, rownames=['Actual Label'], colnames=['Predicted Label'])

accuracy = accuracy_score(x, predictions) 
print(accuracy*100)

def predict_genre(feature_set):
  prediction_1 = target_names[clf.predict(feature_set[features])]
  return prediction_1

