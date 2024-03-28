# -*- coding: utf-8 -*-


import pandas as pd
import os
import numpy as np
path_root = r"C:\Users\cahernandez\Desktop\AGD\Proyectos\Proyecto Prediccion_perdidas_silos_australianos"
os.chdir(path_root)

df = pd.read_excel(r"planillas/Estructura_tentativa_tabla_V2.xlsx",
                   sheet_name='2020',header=1)

df_alm = df #df.iloc[:,58:64]



matriz = []
for r in range(0,len(df_alm.index)):
#for r in range(0,2):    
    try:

        pista = str(df_alm.iloc[r][56])
        fecha =   pd.to_datetime(df_alm.iloc[r][57]).strftime('%d/%m/%Y')
        doy_extraccion = pd.to_datetime(df_alm.iloc[r][57]).dayofyear    
        lona = df_alm.iloc[r][58]
        ID = df_alm.iloc[r][59]
        hum_grano_extraccion = df_alm.iloc[r][60]
        temp_grano_extraccion = df_alm.iloc[r][61]
        cuerpo_extranio_extraccion = df_alm.iloc[r][62]
        daniado_extraccion = df_alm.iloc[r][63]
    
    
        matriz.append([ID,fecha,doy_extraccion,hum_grano_extraccion,\
                       temp_grano_extraccion, cuerpo_extranio_extraccion,\
                       daniado_extraccion])
        """
        print(ID,fecha,doy_extraccion,hum_grano_extraccion,\
                       temp_grano_extraccion, cuerpo_extranio_extraccion,\
                       daniado_extraccion)
        """
    except:
        pass


cabecera = "ID,fecha_extraccion,doy_extraccion,hum_grano_extraccion,\
temp_grano_extraccion,cuerpo_extranio_extraccion,daniado_extraccion"
np.savetxt('./resultados/extraccion_2020_v1.csv', matriz, delimiter=",", 
           fmt='%s',header = cabecera,comments='')
