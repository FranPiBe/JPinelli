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

from sklearn import metrics
#from dask_ml import metrics
from sklearn.ensemble import RandomForestRegressor
import pickle

os.chdir(r"C:\Users\cahernandez\Desktop\AGD\Proyectos\Proyecto Prediccion_perdidas_silos_australianos\scripts\")


df = dd.read_csv(r"tabla_concatenada_v5.csv",header=0)

X = df[['temp_grano_llenado','hum_grano_llenado','hum_amb_llenado','temp_amb_muestra',
       'daniado_llenado','tiempo_llenado_extraccion','lona']].astype(int)

X = X.to_dask_array(lengths=True)

y = df['daniado_extraccion']
y = y.to_dask_array(lengths=True)


X_train,X_test,y_train,y_test= train_test_split(X, y,random_state=0)

scaler = StandardScaler().fit(X_train)

X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)



          # create local cluster

#================== Hiperparametrizacion de Random Forest ====================

client = Client(processes=False)   

param_grid = { 
    'max_depth': [4, 5, 6],
    'min_samples_leaf': [1, 2],
    'min_samples_split': [4, 5, 6],
    'n_estimators': [990, 1000, 1010]
}

def MAE(y_pred, y_test):
    score = metrics.mean_absolute_error(y_test, y_pred)
    return score

MAE_score = metrics.make_scorer(MAE, greater_is_better = False)

model = RandomForestRegressor()
CV_rfc = GridSearchCV(model, param_grid, cv=3,scoring=MAE_score, n_jobs = -1)

with joblib.parallel_backend('dask'):
    CV_rfc.fit(X_train, y_train)
    
print(CV_rfc.best_params_)   

#=============================================================================


clf_RF = RandomForestRegressor(n_estimators=2000, max_depth= 6,
                               min_samples_leaf=2,min_samples_split=6)
clf_RF.fit(X_train, y_train)
y_pred_rf = clf_RF.predict(X_test)

print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred_rf))
print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred_rf))
print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_pred_rf)))
print('R2 score:', metrics.r2_score(y_test, y_pred_rf))

#============================================================================

import matplotlib.pyplot as plt
import seaborn as sns

# Creating a bar plot
import pandas as pd
feat_impo = clf_RF.feature_importances_
name_columns = ['temp_grano_llenado','hum_grano_llenado','hum_amb_llenado','temp_amb_muestra',
       'daniado_llenado','tiempo_llenado_extraccion','lona']
feature_imp = pd.Series(clf_RF.feature_importances_,index=name_columns).sort_values(ascending=False)
sns.barplot(x=feature_imp, y=feature_imp.index)
# Add labels to your graph

plt.xlabel('Feature Importance Score')
plt.ylabel('Features')
plt.title("Visualizing Important Features")
plt.legend()
plt.show()


#=============================================================================

results = clf_RF.predict(X_test)

mse_all = []
mse = metrics.mean_squared_error(results, np.array(y_test))
mae = metrics.mean_absolute_error(results, np.array(y_test))
rmse =  np.sqrt(metrics.mean_squared_error(results, np.array(y_test)))
r2_score =  metrics.r2_score(results, np.array(y_test))

mse_all.append((type(clf_RF).__name__, mse, mae, rmse,r2_score))
print(mse_all)




plt.scatter(results, np.array(y_test))

pkl_filename = "model_daniado.pkl"
with open(pkl_filename, 'wb') as file:
    pickle.dump(clf_RF, file)


