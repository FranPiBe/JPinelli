# -*- coding: utf-8 -*-


import pandas as pd
import os
import numpy as np
path_root = r"C:\Users\cahernandez\Desktop\AGD\Proyectos\Proyecto Prediccion_perdidas_silos_australianos"
os.chdir(path_root)

df = pd.read_excel(r"planillas/Estructura_tentativa_tabla_V2.xlsx",
                   sheet_name='2020',header=1)

df_alm = df.iloc[:,11:56]


"""
for ind_row in df_alm.index:
    for ind_column in 
     print(df_alm['pista.1'][ind_row]) 
"""
matriz = []
for r in range(0,len(df_alm.index)):
#for r in range(0,1):   
    for c in range(3,(len(df_alm.columns)-3)):

        #print(df_alm.columns[c], df_alm.iloc[r][c])
        try:
            pista = str(int(df_alm.iloc[r][0]))
            ID = str(pista +'_'+str(df_alm.columns[c]).replace('L',''))
            
            lona = df_alm.columns[c]
            fecha =   pd.to_datetime(df_alm.iloc[r][1]).strftime('%d/%m/%Y')
            doy_muestra_alma = pd.to_datetime(df_alm.iloc[r][1]).dayofyear
            ubicacion = str(df_alm.iloc[r][2]).lower()
            temperatura = df_alm.iloc[r][c]
            hum_grano_alma = df_alm.iloc[r][-3]
            temp_amb_alma = df_alm.iloc[r][-2]
            hum_amb_alma = df_alm.iloc[r][-1]
            
            """
            print(ID,fecha,doy_muestra_alma,ubicacion,temperatura,
                           hum_grano_alma,temp_amb_alma,hum_amb_alma)
            """
            matriz.append([ID,fecha,doy_muestra_alma,ubicacion,temperatura,
                           hum_grano_alma,temp_amb_alma,hum_amb_alma])
        except:
            pass


cabecera = "ID,fecha_muestra_alma,doy_muestra_alma,ubicacion_alma,\
temp_grano_alma,hum_grano_alma,temp_amb_alma,hum_amb_alma"
np.savetxt('./resultados/almacenamiento_2020_v1.csv', matriz, delimiter=",", 
           fmt='%s',header = cabecera,comments='')        





