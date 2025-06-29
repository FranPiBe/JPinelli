# -*- coding: utf-8 -*-

import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from RegscorePy import aic,bic
from sklearn import metrics
from sklearn.ensemble import RandomForestRegressor
import pickle



df = pd.read_csv(r"tabla_concatenada_v5.csv",header=0)


X = df[['temp_grano_llenado','tiempo_llenado_muestra_alma','temp_amb_alma',
        'posicion','lona']]


y=df['temp_grano_alma'].values



X_train,X_test,y_train,y_test= train_test_split(X, y,random_state=0)


scaler = StandardScaler().fit(X_train)

X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

clf_RF = RandomForestRegressor(n_estimators=1500, max_depth= 100, 
                               min_samples_split=2,random_state = 1)
clf_RF.fit(X_train, y_train)
y_pred_rf = clf_RF.predict(X_test)

print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred_rf))
print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred_rf))
print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_pred_rf)))
print('R2 score:', metrics.r2_score(y_test, y_pred_rf))

pkl_filename = "pickle_model.pkl"
with open(pkl_filename, 'wb') as file:
    pickle.dump(clf_RF, file)


