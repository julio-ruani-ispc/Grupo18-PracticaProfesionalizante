#Importamos librerias
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D


#Cargamos el dataset principal y unificado
ruta_archivo = "dataset_inspección/Datos_limpieza_unidos.csv"
data_df = pd.read_csv(ruta_archivo, delimiter = ";")
data_df.head(10)

#Exploración de los datos
data_df.head()
data_df.info()
data_df.describe()

#INSPECCIÓN DE LOS GRAFICOS
#Relación entre peso y grasa
plt.scatter(data_df['Grasa %'], data_df['Peso'])
plt.xlabel('Grasa %')
plt.ylabel('Peso')
plt.title('Relación entre Grasa % y Peso')
plt.show()

#Relaciones entre múltiples pares de variables al mismo tiempo.Matriz de diagramas de dispersión
sns.pairplot(data_df, vars=['Peso', 'Grasa %', 'Musculo %', 'Calorias(kcal)'])
plt.show()

#Relación en tendencias temporales
plt.plot(data_df['Dias_Transcurridos'], data_df['Peso'])
plt.xlabel('Dias Transcurridos')
plt.ylabel('Peso')
plt.title('Tendencia del Peso a lo largo del Tiempo')
plt.xticks(rotation=45)
plt.show()

#Relación entre Calorias y peso
plt.scatter(data_df['Calorias(kcal)'], data_df['Peso'])
plt.xlabel('Calorías (kcal)')
plt.ylabel('Peso')
plt.title('Relación entre Calorías y Peso')
plt.show()

#Relación Proteinas y Musculos
plt.scatter(data_df['Proteina(g)'], data_df['Musculo %'])
plt.xlabel('Proteína (g)')
plt.ylabel('Musculo %')
plt.title('Relación entre Proteína y Musculo %')
plt.show()

#Densidad de la distribución conjunta del peso y la grasa
sns.kdeplot(data=data_df, x='Peso', y='Grasa %', cmap='Blues', fill=True)
plt.xlabel('Peso')
plt.ylabel('Grasa %')
plt.title('Distribución Conjunta de Peso y Grasa %')
plt.show()

#Correlación entre todas las variables numéricas
correlacion = data_df[['Peso', 'Grasa %', 'Musculo %', 'BMI', 'Grasa visceral', 'Metabolismo', 'Agua']].corr()
sns.heatmap(correlacion, annot=True, cmap='coolwarm')
plt.title('Correlación entre Variables Numéricas')
plt.show()

#Relación de porcentajes de grasa y musculo en base al BMI
plt.scatter(data_df['Grasa %'], data_df['Musculo %'], s=data_df['BMI'] * 10, alpha=0.5)
plt.xlabel('Grasa %')
plt.ylabel('Músculo %')
plt.title('Relación entre Grasa % y Músculo % con Tamaño de Burbuja basado en BMI')
plt.show()

#Relación de porcentajes de grasa y musculo en base al BMI (3D)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(data_df['Grasa %'], data_df['Musculo %'], data_df['BMI'], s=data_df['BMI'] * 10, alpha=0.5)
ax.set_xlabel('Grasa %')
ax.set_ylabel('Músculo %')
ax.set_zlabel('BMI')
plt.title('Gráfico de Burbujas 3D')
plt.show()

#Proporción entre grasa, musculo,y agua
labels = ['Grasa', 'Musculo', 'Agua']
sizes = data_df[['Grasa %', 'Musculo %', 'Agua']].loc[0].values
colors = ['lightcoral', 'lightskyblue', 'lightgreen']
plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', wedgeprops=dict(width=0.4))
plt.title('Composición Corporal')
plt.axis('equal')
plt.show()

#ANÁLISIS DE DATOS ATÍPICOS
#Valor atípico del Peso
plt.boxplot(data_df['Peso'])
plt.title('Diagrama de Caja de Peso')
plt.show()

#Valores atípicos de grasa
sns.boxplot(x=data_df['Grasa %'])
plt.title('Diagrama de Caja de Grasa %')
plt.xlabel('Grasa %')
plt.show()

#Valores atípicos de BMI
sns.boxplot(x=data_df['BMI'])
plt.title('Diagrama de Caja de BMI')
plt.xlabel('BMI')
plt.show()

#Valores atípicos de Carbohidratos
umbral_carbohidratos = 100  # Define tu umbral
data_df['Carbh(g) Atípico'] = data_df['Carbh(g)'] > umbral_carbohidratos
sns.countplot(x='Carbh(g) Atípico', data=data_df)
plt.title('Valores Atípicos en Carbh(g)')
plt.xlabel('Valores Atípicos')
plt.show()

#DISTRIBUCIÓN DE PROBABILIDAD DE MUESTRAS
#Distribución de peso
plt.hist(data_df['Peso'], bins=20, color='skyblue', edgecolor='black')
plt.xlabel('Peso')
plt.ylabel('Frecuencia')
plt.title('Distribución de Peso')
plt.show()

#Distribución de Grasa
sns.kdeplot(data=data_df['Grasa %'], fill=True, color='skyblue')
plt.xlabel('Grasa %')
plt.ylabel('Densidad')
plt.title('Distribución de Probabilidad de Grasa %')
plt.show()

#Distribución de Metabolismo
plt.hist(data_df['Metabolismo'], bins=20, color='lightgreen', edgecolor='black')
plt.xlabel('Metabolismo')
plt.ylabel('Frecuencia')
plt.title('Distribución de Metabolismo')
plt.show()

#Distribución de Agua
sns.kdeplot(data=data_df['Agua'], fill=True, color='lightblue')
plt.xlabel('Agua')
plt.ylabel('Densidad')
plt.title('Distribución de Probabilidad de Agua')
plt.show()

#Distribución de Proteina
plt.hist(data_df['Proteina(g)'], bins=20, color='lightcoral', edgecolor='black')
plt.xlabel('Proteina(g)')
plt.ylabel('Frecuencia')
plt.title('Distribución de Proteina(g)')
plt.show()

#Distribución de Colesterol
sns.kdeplot(data=data_df['Colesterol(mg)'], fill=True, color='lightgreen')
plt.xlabel('Colesterol(mg)')
plt.ylabel('Densidad')
plt.title('Distribución de Probabilidad de Colesterol(mg)')
plt.show()
