# -*- coding: utf-8 -*-

import os
import pandas as pd
import dask.dataframe as dd
import numpy as np
#from sklearn.preprocessing import StandardScaler
from dask_ml.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression

from dask_ml.model_selection import train_test_split

from dask.distributed import Client
import joblib
#from sklearn.model_selection import GridSearchCV
from dask_ml.model_selection import GridSearchCV
from RegscorePy import aic,bic

#from sklearn import metrics
from dask_ml import metrics
from sklearn.ensemble import RandomForestRegressor
import pickle



df = dd.read_csv(r"tabla_concatenada_v5.csv",header=0)


X = df[['temp_grano_llenado','tiempo_llenado_muestra_alma','temp_amb_alma',
        'posicion','lona']].astype(int)
X = X.to_dask_array(lengths=True)

y=df['temp_grano_alma'].astype(int)
y = y.to_dask_array(lengths=True)


X_train,X_test,y_train,y_test= train_test_split(X, y,random_state=0)




scaler = StandardScaler().fit(X_train)

X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)



client = Client(processes=False)             # create local cluster

#================== Hiperparametrizacion de Random Forest ====================
param_grid = { 
    'n_estimators': [100, 500,1000,1500,2000],
    'max_depth' : [10,50,100,200]
}

def MAE(y_pred, y_test):
    score = metrics.mean_absolute_error(y_test, y_pred)
    return score

MAE_score = metrics.make_scorer(MAE, greater_is_better = False)

model = RandomForestRegressor()
CV_rfc = GridSearchCV(model, param_grid, cv=3,scoring=MAE_score, n_jobs = -1)

with joblib.parallel_backend('dask'):
    CV_rfc.fit(X_train, y_train)

"""
{'max_depth': 100, 'max_features': 1, 'min_samples_split': 2, 'n_estimators': 1500, 'random_state': 1}
"""
#=============================================================================
print(CV_rfc.best_params_)



clf_RF = RandomForestRegressor(n_estimators=1500, max_depth= 100, 
                               min_samples_split=2,random_state = 1)
clf_RF.fit(X_train, y_train)
y_pred_rf = clf_RF.predict(X_test)

print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred_rf))
print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred_rf))
print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_pred_rf)))
print('R2 score:', metrics.r2_score(y_test, y_pred_rf))

#============================================================================

results = clf_RF.predict(X_test)

mse_all = []
mse = metrics.mean_squared_error(results, np.array(y_test))
mae = metrics.mean_absolute_error(results, np.array(y_test))
rmse =  np.sqrt(metrics.mean_squared_error(results, np.array(y_test)))
r2_score =  metrics.r2_score(results, np.array(y_test))

mse_all.append((type(clf_RF).__name__, mse, mae, rmse,r2_score))
print(mse_all)




plt.scatter(results, np.array(y_test))

filename = 'model_V1.sav'
model =  pickle.load(open(filename,'rb'))

"""
'temp_grano_llenado','tiempo_llenado_muestra_alma','temp_amb_alma',
        'posicion','lona'
"""
TPLL = 17
TLLMALM = 182
TEMPALBALMA = 20
POS = 0
LONA = 15
input=np.array([[TPLL,TLLMALM,TEMPALBALMA,POS,LONA]]).astype(np.float64)
prediction = model.predict(input)
#pred = '{0:.{1}f}'.format(prediction[0][0], 2)
print(int(prediction))


