import pandas as pd
import os
import numpy as np
os.chdir(path_root)


df1 = pd.read_csv(r"resultados/tabla_integrada_2017_v1.csv",header=0)
df2 = pd.read_csv(r"resultados/tabla_integrada_2018_v1.csv",header=0)
df3 = pd.read_csv(r"resultados/tabla_integrada_2019_v1.csv",header=0)
#df4 = pd.read_csv(r"resultados/tabla_integrada_2020_v1.csv",header=0)
df_1 = pd.concat([df1,df2,df3])

print(df_1.head(10))

def agregar_tiempo_llenado_muestra_alma(row):
    doy_llenado = row['DOY_llenado']
    doy_muestra_alma = row['doy_muestra_alma']
    tiempo_llenado_muestra_alma = doy_muestra_alma -  doy_llenado
    if tiempo_llenado_muestra_alma <= 0:
        return 0
    elif tiempo_llenado_muestra_alma >= 0:
        return tiempo_llenado_muestra_alma
    else:
        pass

def agregar_X(row):
    posicion = row['posicion']
    if posicion==-1:
        return 1
    elif posicion==0:
        return 2
    elif posicion==1:
        return 3
    
def agregar_Y(row):
    lona = row['lona']
    return lona
    


df_1['tiempo_llenado_muestra_alma'] = df_1.apply(agregar_tiempo_llenado_muestra_alma, axis=1)
df_1['x'] = df_1.apply(agregar_X, axis=1)
df_1['y'] = df_1.apply(agregar_Y, axis=1)
df_1.to_csv(r"resultados/tabla_concatenada_v3.csv",sep=',',header=True,
          index=False)












