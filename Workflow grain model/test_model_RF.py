# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 21:35:31 2020

@author: CAhernandez
"""

import os
import pickle
import numpy as np
os.chdir(r"C:\Users\cahernandez\Desktop\AGD\Proyectos\Proyecto Prediccion_perdidas_silos_australianos\scripts\notebooks\data")



filename = "pickle_model.pkl"
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