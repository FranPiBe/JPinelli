#!/usr/bin/env python
# coding: utf-8

# In[204]:


# !pip install geopandas
# !pip install matplotlib
# !pip install contextily
# !pip install folium 
# !pip install matplotlib 
# !pip install mapclassify
# !pip install matplotlib-scalebar
# !pip install mplcursors
get_ipython().system('pip install geog')


# In[1]:


import geopandas as gpd
from shapely.geometry import Point
from shapely.wkt import loads
import pandas as pd
import matplotlib.pyplot as plt
import contextily as ctx
from matplotlib_scalebar.scalebar import ScaleBar
from shapely.geometry import LineString
import matplotlib.patches as mpatches


# In[2]:


radiobases = gpd.read_file("C:/Users/jpinelli/rb.csv")

rutas_nacionales = gpd.read_file("C:/Users/jpinelli/Downloads/_3_4_1_1_6_rutas_nacionales_dnv18_view/_3_4_1_1_6_rutas_nacionales_dnv18_view.shp")
radiobases_coord = gpd.GeoDataFrame(
    radiobases, geometry=gpd.points_from_xy(radiobases.longitud, radiobases.latitud), crs="EPSG:4326"
)
RN = rutas_nacionales[["FNA", "geometry","Sentido"]]
radiobases_coord['radio_de_cobertura'] = radiobases_coord['radio_de_cobertura'].astype(float)
radiobases_coord=radiobases_coord.drop_duplicates()
rutas_nacionales=rutas_nacionales.drop_duplicates()
RN=RN.drop_duplicates()


# In[4]:


fig , fila = plt.subplots(1, figsize=(10,10))
radiobases_coord.plot(ax=fila, alpha=0.8)
fig.suptitle("Planta de Telefónica",y=0.9)
fila.set_axis_off()
ctx.add_basemap(fila, source=ctx.providers.OpenStreetMap.Mapnik, crs=radiobases_coord.crs.to_string())
fila.set_xlim(radiobases_coord.total_bounds[0]-1, radiobases_coord.total_bounds[2]+1)
fila.set_ylim(radiobases_coord.total_bounds[1]-1, radiobases_coord.total_bounds[3]+1)
fila.set_aspect('equal')
plt.show() #coord


# In[3]:


RB = radiobases_coord.to_crs("EPSG:32614")
RB.geometry = RB.geometry.buffer(RB['radio_de_cobertura']*1000)
RB = RB.to_crs(crs=4326) 
RB = RB.drop_duplicates()


# In[5]:


# sitios_seleccionados
sitios_seleccionados = RB[RB['sitio'].isin(['BA014','BA015','BA016','BA018','BA019'])]

# Crea una figura de tamaño 10x10
fig, ax = plt.subplots(figsize=(10, 10))

# Dibuja los primeros 10 sitios y sus radios de cobertura en el mapa
sitios_seleccionados.geometry.plot(ax=ax, facecolor='lightblue', edgecolor='black', linewidth=1.3, alpha=0.15)

# Mapa de fondo
ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik, crs=sitios_seleccionados.crs.to_string())

for idx, sitio in sitios_seleccionados.iterrows():
    x, y = sitio.geometry.centroid.x, sitio.geometry.centroid.y
    latitud = float(sitio['latitud'])
    longitud = float(sitio['longitud'])
    label = f"Sitio: {sitio['sitio']} \n Radio: {sitio['radio_de_cobertura']:.2f}"
    plt.text(x, y, label, ha='center', va='center', fontsize=12, color='black')

    
ax.set_xlim(sitios_seleccionados.total_bounds[0], sitios_seleccionados.total_bounds[2])
ax.set_ylim(sitios_seleccionados.total_bounds[1], sitios_seleccionados.total_bounds[3])
ax.set_aspect('equal')

# Muestra el mapa con los sitios y etiquetas
plt.show() #Sites view


# In[4]:


RN = RN.to_crs(RB.crs)
radiobases_con_rutas = gpd.sjoin(RB, RN, how='inner', predicate='intersects')
radiobases = gpd.read_file("C:/Users/jpinelli/rb2.csv")
radiobases = radiobases.rename(columns=lambda x: x.replace('a.', ''))
radiobases_con_rutas = pd.merge(radiobases_con_rutas, radiobases[['sitio', 'rsh_sector']], on='sitio', how='left')
radiobases_con_rutas = radiobases_con_rutas.drop_duplicates()
radiobases_con_rutas[radiobases_con_rutas['sitio']=='BA014']


# In[7]:


indices_seleccionados = [174, 175]
seleccion = RN.iloc[indices_seleccionados]
# sitios_seleccionados = gdf.iloc[1:6]
sitios_seleccionados = RB[RB['sitio'].isin(['BA014'])]
# Crea una figura de tamaño 10x10
fig, ax = plt.subplots(figsize=(10, 10))

# Dibuja los sitios y sus radios de cobertura en el mapa
sitios_seleccionados.geometry.plot(ax=ax, facecolor='lightblue', edgecolor='black', linewidth=1, alpha=1)
seleccion.plot(ax=ax)
# Mapa de fondo
ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik, crs=sitios_seleccionados.crs.to_string())

for idx, sitio in sitios_seleccionados.iterrows():
    x, y = sitio.geometry.centroid.x, sitio.geometry.centroid.y
    label = f"Sitio: {sitio['sitio']}, Radio: {sitio['radio_de_cobertura']}"
    plt.text(x, y-0.2, label, ha='center', va='center', fontsize=12, color='black')

# Agregar etiquetas a cada ruta
for idx, ruta in seleccion.iterrows():
    x, y = ruta.geometry.centroid.x, ruta.geometry.centroid.y
    label = ruta['FNA']
    ax.annotate(label, (x, y), ha='center', va='center', fontsize=12, color='black')

    
ax.set_xlim(seleccion.total_bounds[0], seleccion.total_bounds[2])
ax.set_ylim(seleccion.total_bounds[1], seleccion.total_bounds[3])
ax.set_aspect('equal')

# Muestra el mapa con los sitios y etiquetas
plt.show() #Sites and highway view
print(seleccion['geometry'].to_crs('EPSG:22173').length)


# In[8]:


fig, (ax2,ax1) = plt.subplots(1, 2, figsize=(20, 20))


gpd.GeoDataFrame({'geometry': seleccion.geometry.unary_union.intersection(sitios_seleccionados.geometry)}, crs=sitios_seleccionados.crs.to_string()).plot(ax=ax1, color='black')
gpd.GeoDataFrame({'geometry': seleccion.geometry.unary_union.intersection(sitios_seleccionados.geometry)}, crs=sitios_seleccionados.crs.to_string()).boundary.plot(ax=ax1,facecolor='red')
sitios_seleccionados.plot(ax=ax1, alpha=0.15)
sitios_seleccionados.plot(ax=ax2, alpha=1.0,facecolor='red')
seleccion.plot(ax=ax2,)

ctx.add_basemap(ax=ax1, source=ctx.providers.OpenStreetMap.Mapnik, crs=sitios_seleccionados.crs.to_string())
ctx.add_basemap(ax=ax2, source=ctx.providers.OpenStreetMap.Mapnik, crs=seleccion.crs.to_string())

ax1.set_axis_off()
ax2.set_axis_off()
ax1.set_xlim(sitios_seleccionados.total_bounds[0], sitios_seleccionados.total_bounds[2])
ax1.set_ylim(sitios_seleccionados.total_bounds[1], sitios_seleccionados.total_bounds[3])
ax1.set_aspect('equal')
ax2.set_xlim(seleccion.total_bounds[0], seleccion.total_bounds[2])
ax2.set_ylim(seleccion.total_bounds[1], seleccion.total_bounds[3])
ax2.set_aspect('equal')

# Ajusta los espacios entre subfiguras
fig.tight_layout()

# Ajusta los márgenes superior e inferior de la figura
fig.subplots_adjust()

plt.show() #Intersection view
print(gpd.GeoDataFrame({'geometry': seleccion.geometry.unary_union.intersection(sitios_seleccionados.geometry)}, crs=sitios_seleccionados.crs.to_string()).to_crs('EPSG:22173').length)


# In[9]:


RB


# In[10]:


RN


# In[11]:


rutas_nacionales


# In[12]:


radiobases_con_rutas


# In[13]:


# Crea una figura y subfiguras
fig, (fila1, fila2, fila3) = plt.subplots(1, 3, figsize=(10, 10))

# Grafica el la planta de telefónica en la primera subfigura
RB.plot(ax=fila1, alpha=1)
fila1.set_title('RB en planta')
fila1.set_axis_off()
ctx.add_basemap(fila1, source=ctx.providers.OpenStreetMap.Mapnik, crs=RB.crs.to_string())
fila1.set_xlim(RN.total_bounds[0], RN.total_bounds[2])
fila1.set_ylim(RN.total_bounds[1], RN.total_bounds[3])
fila1.set_aspect('equal')

# Grafica el las rutas nacionales en la segunda subfigura
RN.plot(ax=fila2, alpha=1)
fila2.set_title('Rutas Nacionales')
fila2.set_axis_off()
ctx.add_basemap(fila2, source=ctx.providers.OpenStreetMap.Mapnik, crs=RN.crs.to_string())
fila2.set_xlim(RN.total_bounds[0], RN.total_bounds[2])
fila2.set_ylim(RN.total_bounds[1], RN.total_bounds[3])
fila2.set_aspect('equal')

# Grafica las radiobases con rutas en la tercera subfigura
radiobases_con_rutas.plot(ax=fila3, column='rsh_sector',  alpha=1, legend=True)
fila3.set_title('radiobases con rutas')
fila3.set_axis_off()
ctx.add_basemap(fila3, source=ctx.providers.OpenStreetMap.Mapnik, crs=radiobases_con_rutas.crs.to_string())
fila3.set_xlim(radiobases_con_rutas.total_bounds[0], radiobases_con_rutas.total_bounds[2])
fila3.set_ylim(radiobases_con_rutas.total_bounds[1], radiobases_con_rutas.total_bounds[3])
fila3.set_aspect('equal')

# Título general de la figura
fig.suptitle("Radiobases en rutas",ha='center',va='center', y=0.15)

# Ajusta los espacios entre subfiguras
fig.tight_layout()

# Ajusta los márgenes superior e inferior de la figura
fig.subplots_adjust()

# Muestra la figura
plt.show() #GeoJoin with categories view


# In[7]:


fig , fila = plt.subplots(1, figsize=(10,10))
RN.plot(figsize = (10,10), ax=fila, alpha=0.8)
fig.suptitle("Rutas Nacionales", y=0.1)
fila.set_axis_off()
ctx.add_basemap(fila, source=ctx.providers.OpenStreetMap.Mapnik, crs=RN.crs.to_string())
fila.set_xlim(RN.total_bounds[0], RN.total_bounds[2])
fila.set_ylim(RN.total_bounds[1], RN.total_bounds[3])
fila.set_aspect('equal') 

plt.show()#Highways view


# In[16]:


ruta_seleccionada='RN 0009'
# Filtrar las radiobases que coinciden con la FNA "RN 009" en ambas direcciones
radiobases_filtradas = radiobases_con_rutas[(radiobases_con_rutas['FNA'] == ruta_seleccionada)]
# Crea una figura y subfigura
fig, ax = plt.subplots(figsize=(10, 10))

# Grafica las radiobases filtradas en la subfigura
radiobases_filtradas.plot(ax=ax, column='rsh_sector',  alpha=1, legend=True)

# Grafica el las rutas nacionales en la misma subfigura
# RB.plot(ax=ax, alpha=0.3)
RN[(RN['FNA'] == ruta_seleccionada) & (RN['Sentido'] == 'A')].plot(ax=ax, alpha=0.3, color='purple', linewidth=0.5)
RN[(RN['FNA'] == ruta_seleccionada) & (RN['Sentido'] == 'D')].plot(ax=ax, alpha=0.3, color='orange', linewidth=0.5)
limites = RN[(RN['FNA'] == ruta_seleccionada) & (RN['Sentido'] == 'A')].boundary

# Configuraciones adicionales de la subfigura
ax.set_title(f'Radiobases que cruzan con {ruta_seleccionada}')
ax.set_axis_off()
ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik, crs=limites.crs.to_string())
ax.set_xlim(limites.bounds.minx.values[0]-0.1, limites.bounds.maxx.values[0]+0.1)
ax.set_ylim(limites.bounds.miny.values[0]-0.1, limites.bounds.maxy.values[0]+0.1)
ax.set_aspect('equal')


# Muestra la figura
plt.show() #Highway n 9 view


# In[18]:


# Tiro columnas innecesarias
radiobases_con_rutas_f=radiobases_con_rutas[["sitio","latitud","longitud","radio_de_cobertura","FNA","Sentido"]]

# Guardar el DataFrame resultante en formato CSV
radiobases_con_rutas_f.to_csv('resultado.csv', index=False)


# In[20]:


# Calcular la cuenta de valores distintos de 'sitio' por 'index_right'
count_df = radiobases_con_rutas.groupby('index_right')['sitio'].nunique().reset_index()
# Fusionar 'gdf2' y 'count_df' en base a la columna 'index_right'
merged_gdf = RN.merge(count_df, how='left', left_index=True, right_on='index_right')

# Seleccionar las columnas deseadas
new_df = merged_gdf.loc[:, ['FNA', 'geometry', 'sitio']]

# Convertir el DataFrame en un GeoDataFrame
new_gdf = gpd.GeoDataFrame(new_df, geometry='geometry')
new_gdf = new_gdf.drop_duplicates()
# Crea el ax
fig, (ax1,ax2) = plt.subplots(1,2,figsize=(20, 10))
# Configurar los parámetros de la leyenda
legend_kwds = {'label': "Sitio", 'orientation': "vertical", 'shrink': 0.5}
# Colorear según el campo 'sitio' usando una escala de colores
new_gdf.plot('sitio',ax=ax1, cmap='plasma', linewidth=0.8,  legend=True,legend_kwds=legend_kwds)
# Agregar el mapa de fondo utilizando OpenStreetMap
ctx.add_basemap(ax1, source=ctx.providers.OpenStreetMap.Mapnik, crs=new_gdf.crs.to_string())
radiobases_con_rutas.plot(ax=ax2, column='rsh_sector',  alpha=1, legend=True)
ctx.add_basemap(ax2, source=ctx.providers.OpenStreetMap.Mapnik, crs=radiobases_con_rutas.crs.to_string())
# Agregar título al gráfico
plt.title('Mapa coloreado por sitio')
# Configura el aspecto del gráfico
# Ajustar el tamaño de los ejes para que tengan las mismas dimensiones
ax1.set_xlim(ax2.get_xlim())
ax1.set_ylim(ax2.get_ylim())
ax1.set_aspect('equal')
ax1.set_title('Rutas grupos')
ax2.set_aspect('equal')
ax2.set_title('RB en rutas')
# Ajusta los espacios entre subfiguras
fig.tight_layout()

# Ajusta los márgenes superior e inferior de la figura
fig.subplots_adjust()

# Mostrar el gráfico
plt.show() #Highway choroplet
new_gdf.loc[new_gdf['sitio'].idxmax(),['FNA', 'sitio']]


# In[21]:


# Crear una figura con dos subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))

# Graficar el GeoDataFrame en el primer subplot
merged_gdf[merged_gdf['sitio'].isnull()].drop_duplicates().plot(ax=ax1, figsize=(10, 10))
ctx.add_basemap(ax1, source=ctx.providers.OpenStreetMap.Mapnik, crs=merged_gdf.crs.to_string())
ax1.set_title('Rutas con 0 radiobases')

# Obtener los valores únicos de la columna 'sitio'
valores_unicos = merged_gdf[merged_gdf['sitio'].isnull()]['FNA'].unique()

# Mostrar la lista de valores únicos en el segundo subplot
ax2.text(0, 0.5, '\n'.join(valores_unicos), fontsize=12)
ax2.set_axis_off()

# Ajustar los espacios entre subplots
plt.subplots_adjust(wspace=0.1)

# Mostrar la figura
plt.show() #Highway insight discovery


# In[22]:


# Crea un indicador
new_gdf['RB_por_km'] = (new_gdf.geometry.to_crs("EPSG:22173").length) / new_gdf['sitio']
new_gdf = new_gdf.drop_duplicates()

# Crea el ax
fig, (ax1,ax2) = plt.subplots(1,2,figsize=(20, 10))
# Configurar los parámetros de la leyenda
legend_kwds = {'label': "km/rb", 'orientation': "vertical", 'shrink': 0.5}
# Colorear según el campo 'sitio' usando una escala de colores
new_gdf.plot('RB_por_km',ax=ax1, cmap='plasma', linewidth=0.8,  legend=True,legend_kwds=legend_kwds)
# Agregar el mapa de fondo utilizando OpenStreetMap
ctx.add_basemap(ax1, source=ctx.providers.OpenStreetMap.Mapnik, crs=new_gdf.crs.to_string())
radiobases_con_rutas.plot(ax=ax2, column='rsh_sector',  alpha=1, legend=True)
ctx.add_basemap(ax2, source=ctx.providers.OpenStreetMap.Mapnik, crs=radiobases_con_rutas.crs.to_string())
# Agregar título al gráfico
plt.title('Mapa coloreado por km/rb')
# Configura el aspecto del gráfico
# Ajustar el tamaño de los ejes para que tengan las mismas dimensiones
ax1.set_xlim(ax2.get_xlim())
ax1.set_ylim(ax2.get_ylim())
ax1.set_aspect('equal')
ax1.set_title('Rutas grupos')
ax2.set_aspect('equal')
ax2.set_title('RB en rutas')
# Mostrar el gráfico
plt.show()#Highway insight discovery2
new_gdf.loc[new_gdf['RB_por_km'].idxmax(),['FNA', 'RB_por_km']]


# In[28]:


# select count(distinct a.ani) q_anis, a.sitio, case when c.fna = '' then null when c.fna is not null then c.fna else null end as ruta
# from sandbox_datascientist.lp_ani_sitio_mes_temp  a 
# inner join access_data.ABT_Suscripcion_Movil_m b on a.ani=b.valor_recurso_primario_cd and (a.mes-1)=b.periodo_nr
#         left join sandbox_datascientist.jfp_radiobases_con_rutas c on a.sitio=c.sitio
#         where  producto_principal_de='Movil' and tipo_cliente_de in ('Individuo','Empresa') 
#         and oper_baja_fl=0
# and a.minutos>0 and a.mb_total>0
# group by a.sitio, case when c.fna = '' then null when c.fna is not null then c.fna else null end;

qc_sit_rut = pd.read_csv("C:/Users/jpinelli/q_anis xsitio x ruta.csv")
qc_sit_rut = qc_sit_rut.rename(columns=lambda x: x.replace('a.', ''))
qc_sit_rut = qc_sit_rut.dropna(subset=['sitio'])


# In[29]:


merged_gdf2 = RN.merge(qc_sit_rut, how='left', left_on='FNA', right_on='ruta')
merged_gdf2 = merged_gdf2.groupby(['FNA','geometry','Sentido']).agg({'q_anis': 'mean'})
merged_gdf2 = merged_gdf2.reset_index()
merged_gdf3 = radiobases_con_rutas.merge(qc_sit_rut, how='left', left_on='sitio', right_on='sitio')

# Seleccionar las columnas deseadas
merged_gdf2 = merged_gdf2.loc[:, ['FNA', 'geometry', 'q_anis']]
anis_sitio = merged_gdf3[merged_gdf3['q_anis'] < merged_gdf3['q_anis'].mean()]

# Convertir el DataFrame en un GeoDataFrame
new_gdf2 = gpd.GeoDataFrame(merged_gdf2, geometry='geometry')
new_gdf2 = new_gdf2.set_crs(RN.crs)
# Crea el ax
fig, (ax1,ax2) = plt.subplots(1,2,figsize=(20, 10))
# Configurar los parámetros de la leyenda
legend_kwds = {'label': "q_anis", 'orientation': "vertical", 'shrink': 0.5}
# Colorear según el campo 'sitio' usando una escala de colores
new_gdf2.plot('q_anis',ax=ax1, cmap='plasma', linewidth=0.8,  legend=True,legend_kwds=legend_kwds)
# Agregar el mapa de fondo utilizando OpenStreetMap
ctx.add_basemap(ax1, source=ctx.providers.OpenStreetMap.Mapnik, crs=new_gdf2.crs.to_string())
anis_sitio.plot(ax=ax2, column='q_anis',  alpha=1, legend=True)
ctx.add_basemap(ax2, source=ctx.providers.OpenStreetMap.Mapnik, crs=merged_gdf3.crs.to_string())
# Agregar título al gráfico
plt.title('Rutas coloreadas por q_anis')
# Configura el aspecto del gráfico
# Ajustar el tamaño de los ejes para que tengan las mismas dimensiones
ax1.set_xlim(new_gdf2.total_bounds[0], new_gdf2.total_bounds[2])
ax1.set_ylim(new_gdf2.total_bounds[1], new_gdf2.total_bounds[3])
ax2.set_xlim(anis_sitio.total_bounds[0], anis_sitio.total_bounds[2])
ax2.set_ylim(anis_sitio.total_bounds[1], anis_sitio.total_bounds[3])
ax1.set_aspect('equal')
ax1.set_title('Rutas grupos')
ax2.set_aspect('equal')
ax2.set_title('RB en rutas')
# Ajusta los espacios entre subfiguras
fig.tight_layout()

# Ajusta los márgenes superior e inferior de la figura
fig.subplots_adjust()

# Mostrar el gráfico
plt.show()#Highway insight discovery3


# In[ ]:




