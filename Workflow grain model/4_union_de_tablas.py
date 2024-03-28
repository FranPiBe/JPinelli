# -*- coding: utf-8 -*-


import pandas as pd
import os
import numpy as np
path_root = r"C:\Users\cahernandez\Desktop\AGD\Proyectos\Proyecto Prediccion_perdidas_silos_australianos"
os.chdir(path_root)

df1 = pd.read_csv(r"resultados/almacenamiento_2020_v1.csv",header=0)
df2 = pd.read_csv(r"resultados/extraccion_2020_v1.csv",header=0)
df3 = pd.read_csv(r"resultados/llenado_2020_v1.csv",header=0)

df_result1 = pd.merge(df1,df2,left_on='ID',right_on='ID')

df = pd.merge(df_result1,df3,left_on='ID',right_on='ID',)


def agregar_tiempo_llenado_extraccion(row):
    doy_llenado = row['DOY_llenado']
    doy_extraccion = row['doy_extraccion']
    dias_llenado_extraccion = doy_extraccion -  doy_llenado
    if dias_llenado_extraccion <= 0:
        return 0
    elif dias_llenado_extraccion >= 0:
        return dias_llenado_extraccion
    else:
        pass
        
def agregar_DEW(row):
    temp = row['temp_amb_alma']
    rh = row['hum_amb_alma']
    es = 6.11 * np.exp((2.5e6 / 461) * (1 / 273 - 1 / (273 + temp)))
    vpd = ((100 - rh) / 100) * es
    return vpd



def posicion(row):
    if row['ubicacion_alma']=='izquierda':
        return -1
    elif row['ubicacion_alma']=='centro':
        return 0
    elif row['ubicacion_alma']=='derecho':
        return 1
    else:
        pass
    
def agregar_lona(row):
    lona = str(row['ID']).split('_')[1]
    return lona

df['posicion'] = df.apply(posicion, axis=1)
df['tiempo_llenado_extraccion'] = df.apply(agregar_tiempo_llenado_extraccion, axis=1)
df['DEW_amb_alma'] = df.apply(agregar_DEW, axis=1)
df['lona'] = df.apply(agregar_lona, axis=1)
df.to_csv(r"resultados/tabla_integrada_2020_v1.csv",sep=',',header=True,
          index=False)











