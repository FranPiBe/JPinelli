# -*- coding: utf-8 -*-


import pandas as pd
import os
import numpy as np

path_root = r"C:\Users\cahernandez\Desktop\AGD\Proyectos\Proyecto Prediccion_perdidas_silos_australianos"
os.chdir(path_root)

df = pd.read_excel(r"planillas/Estructura_tentativa_tabla_V2.xlsx",
                   sheet_name='2020',header=1)

df_alm = df#df.iloc[:,[0:10,36]]

matriz = []
for r in range(0,len(df_alm.index)):
#for r in range(0,2):
    #print(df_alm.columns[c], df_alm.iloc[r][c])
    try:
        pista = str(df_alm.iloc[r][0])
        
        fecha_llenado = pd.to_datetime(df_alm.iloc[r][1]).strftime('%d/%m/%Y')
        doy_llenado = pd.to_datetime(df_alm.iloc[r][1]).dayofyear
        lona = str(df_alm.iloc[r][2])
        ID = str(df_alm.iloc[r][3])
        hum_grano_muestra = str(df_alm.iloc[r][4])
        temp_grano_muestra = str(df_alm.iloc[r][5])
        hum_amb_muestra = str(df_alm.iloc[r][6])
        temp_amb_muestra = str(df_alm.iloc[r][7])
        cuerpo_extraño_llenado =  str(df_alm.iloc[r][8])
        daniado_llenado =  str(df_alm.iloc[r][9])
        

        
        """
        print(ID,pista,fecha_llenado,doy_llenado,hum_grano_muestra,
                       temp_grano_muestra,hum_amb_muestra,temp_amb_muestra,
                       cuerpo_extraño_llenado, daniado_llenado)
        """
        
        matriz.append([ID,pista,fecha_llenado,doy_llenado,hum_grano_muestra,
                       temp_grano_muestra,hum_amb_muestra,temp_amb_muestra,
                       cuerpo_extraño_llenado, daniado_llenado])
        
    except:
        pass
    

cabecera = "ID,pista,fecha_llenado,DOY_llenado,hum_grano_llenado,\
temp_grano_llenado,hum_amb_llenado,temp_amb_muestra,cuerpo_extranio_llenado,daniado_llenado"
np.savetxt('./resultados/llenado_2020_v1.csv', matriz, delimiter=",", 
           fmt='%s',header = cabecera,comments='')        

