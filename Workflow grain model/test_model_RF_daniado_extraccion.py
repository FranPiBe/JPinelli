import os
import pickle
import numpy as np



filename = r"notebooks\data\daniado_orange_v2.pkcls"
model =  pickle.load(open(filename,'rb'))

"""
'temp_grano_llenado','hum_grano_llenado','hum_amb_llenado','temp_amb_muestra',
       'daniado_llenado','tiempo_llenado_extraccion','lona'
"""


TPGRLL = 15
HUMGRLL = 22
HUMAMBLL = 90
TMPAMBLL = 22
DANLL = 5
TPLLEX = 250
LONA = 5

input=np.array([[TPGRLL,HUMGRLL,HUMAMBLL,TMPAMBLL,DANLL,TPLLEX,LONA]]).astype(np.float64)
prediction = model.predict(input)

print(prediction)