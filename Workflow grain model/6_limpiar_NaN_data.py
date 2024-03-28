# -*- coding: utf-8 -*-


import pandas as pd
import os
import numpy as np
path_root = r"C:\Users\cahernandez\Desktop\AGD\Proyectos\Proyecto Prediccion_perdidas_silos_australianos"
os.chdir(path_root)


df = pd.read_csv(r"resultados/tabla_concatenada_v3.csv",header=0)

df = df.dropna()
df.isnull().values

df.to_csv(r"resultados/tabla_concatenada_v5.csv",sep=',',header=True,
          index=False)