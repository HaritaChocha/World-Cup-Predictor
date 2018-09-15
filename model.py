# %%

# Import modules

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import pickle

# Import dataset
data = pd.read_csv('train_wc.csv')

data = data.reset_index(drop=True)
data.drop(['Unnamed: 0'], inplace = True, axis=1)

# if home team wins = 2, draw = 1 away team wins = 0
data.loc[data.winning_team == data.home_team, 'winning_team']= 2
data.loc[data.winning_team == 'Draw', 'winning_team']= 1
data.loc[data.winning_team == data.away_team, 'winning_team']= 0

data.head()

# Get dummy variables
final = pd.get_dummies(data, prefix=['home_team', 'away_team'],  columns=['home_team', 'away_team'])

# Export final
final.to_csv('final_dummy.csv')

# Set X and y
X = final.drop(['winning_team'], axis=1)
y = final['winning_team']
y.astype('int')


# Seperate train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=25)

# Train Model and predict
logreg = LogisticRegression()
logreg.fit(X_train, y_train)
y_predict = logreg.predict(X_test)

accuracy_logreg = accuracy_score(y_test, y_predict)

filename = 'trained_model.sav'
pickle.dump(logreg, open(filename, 'wb'))

print(accuracy_logreg)