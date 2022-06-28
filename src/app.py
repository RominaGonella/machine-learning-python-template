### ejecutar en consola
#!pip install pandas
#!pip install matplotlib
#!pip install seaborn
#!pip install folium

# importo librerias
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datautils.analysis import *
import folium 
from folium.plugins import MarkerCluster

# cargo datos desde la web
df_airbnb = pd.read_csv('https://raw.githubusercontent.com/4GeeksAcademy/data-preprocessing-project-tutorial/main/AB_NYC_2019.csv')

# describo el data frame
df_airbnb.info()

# el data frame contiene 16 columnas y 48895 filas
# las columnas que contienen NA son: name, host_name, last_review y reviews_per_month

# miro aleatoriamente 5 filas para entender el data set
df_airbnb.sample(3)

### edito los tipos de variables

# variables a pasar a categorical: name, host_name, neighbourhood_group, neighbourhood, room_type
df_airbnb['name'] = pd.Categorical(df_airbnb['name'])
df_airbnb['host_name'] = pd.Categorical(df_airbnb['host_name'])
df_airbnb['neighbourhood_group'] = pd.Categorical(df_airbnb['neighbourhood_group'])
df_airbnb['neighbourhood'] = pd.Categorical(df_airbnb['neighbourhood'])
df_airbnb['room_type'] = pd.Categorical(df_airbnb['room_type'])

# variables a pasar a fecha: last_review
df_airbnb['last_review'] = pd.to_datetime(df_airbnb['last_review'])

# el resto deben ser numéricas

# vuelvo a mirar los datos a ver si se ven igual
df_airbnb.sample(3)

# vuelvo a ver los tipos de variables
df_airbnb.info()

# describo variables numéricas (cuantitativas)
df_airbnb.describe()

# cosas que llaman la atención:
# hay datos raros en latitud y longitud (cercanos a cero)
# hay casos con precio = 0

# me fijo si el id se repite
print('la cantidad de id distintos en '+ str(len(df_airbnb)) + ' filas es ' + str(df_airbnb['id'].nunique()))

# el id no se repite, creo que identifica una propiedad distinta

# me fijo si el name se repite
print('la cantidad de name distintos en '+ str(len(df_airbnb)) + ' filas es ' + str(df_airbnb['name'].nunique()))

# el name sí se repite, pero pueden haber varias propiedades con el mismo nombre

#### entiendo que la unidad de análisis es cada propiedad distinta, es decir, cada fila identifica una propiedad, pueden haber varias propiedades con un mismo anfitrión

# me fijo en casos con precio 0
print(f'hay {sum(df_airbnb["price"] == 0)} alojamientos con precio 0')

# los elimino del dataset
df_airbnb = df_airbnb[df_airbnb['price'] != 0]

# algunos datos del data set:
print(f'cantidad de alojamientos distintos: {len(df_airbnb)}')
print('')
print(f'cantidad de nombres de alojamientos distintos: {df_airbnb["name"].nunique()}, es decir se repiten {len(df_airbnb)-df_airbnb["name"].nunique()} nombres de alojamientos')
print('')
print(f'cantidad de anfitriones distintos: {df_airbnb["host_id"].nunique()}')
print('')
print(f'cantidad de nombres de anfitriones distintos: {df_airbnb["host_name"].nunique()}, es decir se repiten {len(df_airbnb)-df_airbnb["host_name"].nunique()} nombres de anfitriones')
print('')
print(f'cantidad de grupos de vecindarios distintos: {df_airbnb["neighbourhood_group"].nunique()}')
print('')
print(f'Estos son los grupos de vecindarios: {df_airbnb["neighbourhood_group"].unique()}')
print('')
print(f'cantidad de vecindarios distintos: {df_airbnb["neighbourhood"].nunique()}')
print('')
print(f'cantidad de tipos de cuartos distintos: {df_airbnb["room_type"].nunique()}')
print('')
print(f'Estos son los tipos de cuartos: {df_airbnb["room_type"].unique()}')
print('')
print(f'Las fechas de las últimas reseñas varían entre {df_airbnb["last_review"].min().date()} y {df_airbnb["last_review"].max().date()}')

# cantidad de alojamientos por tipo
hist_rooms = df_airbnb['room_type'].value_counts()
hist_rooms = pd.DataFrame({'room_type': hist_rooms.index, 'frecuencia': hist_rooms.values})

fig=plt.figure(figsize=(15,5))
plt.bar(hist_rooms['room_type'].astype(str), hist_rooms['frecuencia'])
plt.title('Cantidad de alojamientos en 2019 por tipo')
plt.xlabel('tipo de alojamiento')
plt.ylabel('cantidad')

plt.show()

## los más frecuentes son apartamento o casa entera, o cuarto privado. El menos frecuente es cuarto compartido

# distribución del precio del alojamiento
sns.boxplot(x = df_airbnb['price'])
plt.show()

## los precios llegan a 10000, máas de 500 aprox ya se considera outlier

# distribución del precio del alojamiento (menores a 500)
sns.boxplot(x = df_airbnb['price'][df_airbnb['price'] < 500])
plt.show()

## el precio mediano es de aprox 100 dólares por alojamiento y día

# histograma del precio del alojamiento (precio por noche menor a 500 usd)
sns.histplot(x = df_airbnb['price'][df_airbnb['price'] < 500])
plt.show()

# precio del alojamiento según tipo (menores a 500 usd)
sns.boxplot(x = df_airbnb['room_type'][df_airbnb['price'] < 500], y = df_airbnb['price'][df_airbnb['price'] < 500])
plt.show()

## en general el precio de un alojamiento entero es superior al de una habitación privada, y este es superior al de una habitación compartida
## el precio también depende del vecindario

# cantidad de alojamientos por vecindario
bar_vec = df_airbnb['neighbourhood_group'].value_counts()
bar_vec = pd.DataFrame({'vec': bar_vec.index, 'frec': bar_vec.values})

fig=plt.figure(figsize=(15,5))
plt.bar(bar_vec['vec'].astype(str), bar_vec['frec'])
plt.title('Cantidad de alojamientos en 2019 por grupo de vecindario')
plt.xlabel('vecindario (grupo)')
plt.ylabel('cantidad')

plt.show()

# la mayoría de los alojamientos están en Manhattan o Brooklyn

### precio según vecindario y tipo de alojamiento

fig, axes = plt.subplots(3, 2, figsize = (18, 10))

fig.suptitle('Precio de alojamientos según grupo de vecindario y tipo')

sns.boxplot(ax = axes[0, 0], data = df_airbnb[(df_airbnb['neighbourhood_group'] == 'Bronx') & (df_airbnb['price'] < 500)], x = 'room_type', y = 'price')
sns.boxplot(ax = axes[0, 1], data = df_airbnb[(df_airbnb['neighbourhood_group'] == 'Brooklyn') & (df_airbnb['price'] < 500)], x = 'room_type', y = 'price')
sns.boxplot(ax = axes[1, 0], data = df_airbnb[(df_airbnb['neighbourhood_group'] == 'Manhattan') & (df_airbnb['price'] < 500)], x = 'room_type', y = 'price')
sns.boxplot(ax = axes[1, 1], data = df_airbnb[(df_airbnb['neighbourhood_group'] == 'Queens') & (df_airbnb['price'] < 500)], x = 'room_type', y = 'price')
sns.boxplot(ax = axes[2, 0], data = df_airbnb[(df_airbnb['neighbourhood_group'] == 'Staten Island') & (df_airbnb['price'] < 500)], x = 'room_type', y = 'price')
axes[2, 1].axis('off')
axes[0, 0].set_title('Bronx')
axes[0, 1].set_title('Brooklyn')
axes[1, 0].set_title('Manhattan')
axes[1, 1].set_title('Queens')
axes[2, 0].set_title('Staten Island')
axes[0, 0].set_xlabel('')
axes[0, 1].set_xlabel('')
axes[1, 0].set_xlabel('')
axes[1, 1].set_xlabel('')
axes[0, 0].set_xlabel('')

fig.show()

## la diferencia entre los tipos de alojamiento observada en el total se mantiene en cada grupo de vecindario

# mediana del precio en cada vecindario
vec_median = df_airbnb[['price', 'neighbourhood_group']].groupby('neighbourhood_group').agg('median').sort_values('price', ascending = False)
print(vec_median)

# precio según vecindario
sns.boxplot(x = df_airbnb['neighbourhood_group'][df_airbnb['price'] < 500],y = df_airbnb['price'][df_airbnb['price'] < 500], order = vec_median.index)
plt.show()

# los precios más altos están en general en Manhattan, le sigue Brooklyn
# los precios en Bronx, Queens y Staten Islands se distribuyen de forma muy similar

# anfitriones según cantidad de alojamientos que poseen
anfit = df_airbnb.groupby('host_id').size()
anfit = pd.DataFrame({'host_id': anfit.index, 'frecuencia': anfit.values}).sort_values('frecuencia', ascending = False)
anfit = pd.merge(anfit, df_airbnb[['host_id', 'host_name']], on = 'host_id', how = 'left')
anfit = anfit.drop_duplicates()
anfit = anfit[['host_id', 'host_name', 'frecuencia']]

# top 10 anfitriones con más alojamientos
print('estos son los 10 anfitriones con más alojamientos y la cantidad que poseen:')
print(anfit.head(10))

print('')

## el anfitrión con más alojamientos posee 327

anfit['grup_frec'] = '1'
mask = anfit['frecuencia'] == 2
anfit.loc[mask, 'grup_frec'] = '2'
mask = anfit['frecuencia'] > 2
anfit.loc[mask, 'grup_frec'] = '3 o más'

anfit2 = anfit.groupby('grup_frec').size()
anfit2 = pd.DataFrame({'grup_anfit': anfit2.index, 'frecuencia': anfit2.values})
anfit2['porcentaje'] = round(100*anfit2['frecuencia']/sum(anfit2['frecuencia']), 2)
print(anfit2)

## el 86% de los anfitriones sólo tiene 1 alojamiento

# disponibilidad de los alojamientos: asumo que 'availability_365' representa la cantidad de días que el
# alojamiento estuvo disponible en el año

fig, ax = plt.subplots(1, 2)
# histograma de la disponibilidad en días
sns.histplot(ax = ax[0], x = df_airbnb['availability_365'])
sns.boxplot(ax = ax[1], x = df_airbnb['availability_365'])
fig.show()

# al parecer muchos alojamientos no estuvieron disponibles muchos días en el año

print(df_airbnb['availability_365'].describe())
# el promedio de días disponible es 112, pero más del 25% de los casos no tuvo disponibilidad en todo el año

print()
print(f'El {round(100*sum(df_airbnb["availability_365"] == 0)/len(df_airbnb), 2)}% de los alojamientos no tuvo disponibilidad en 2019')

# disponibilidad media según grupo de vecindario
vec_median_avail = df_airbnb[['availability_365', 'neighbourhood_group']].groupby('neighbourhood_group').agg('median').sort_values('availability_365', ascending = False)
print(vec_median_avail)

# grafico disponibilidad según grupo de vecindario
sns.boxplot(x = 'neighbourhood_group', y = 'availability_365', data = df_airbnb, order = vec_median_avail.index)
plt.show()

## los vecindarios con mayor disponibilidad son los de menor precio mediano

# los 100 alojamientos con más reseñas
aloj = df_airbnb[['id', 'name', 'number_of_reviews', 'latitude', 'longitude']].sort_values('number_of_reviews', ascending = False).head(100)
print(aloj)

# mapa: distribución territorial de los 100 alojamientos con más reseñas

map = folium.Map()

for i in range(len(aloj)):
    lat = aloj["latitude"].to_list()[i]
    lon = aloj["longitude"].to_list()[i]
    folium.Marker(location=[lat, lon], icon=folium.Icon(color="red", icon="check", prefix="fa")).add_to(map)
map

# guardo data set limpio
df_airbnb.to_csv('../data/processed/datos_limpios_airbnb.csv')
