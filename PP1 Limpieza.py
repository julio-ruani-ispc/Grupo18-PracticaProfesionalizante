import pandas as pd
import warnings
from pyod.models.iforest import IForest
import re

DF = pd.read_csv("Registros_Composicion_corporal.csv", delimiter = ";")

# Iterar a través de todas las columnas
for column in DF.columns:
    # Verificar si la columna es de tipo object y no es la columna "Fecha"
    if DF[column].dtype == 'object' and column != "Fecha":
        # Reemplazar comas por puntos y convertir a tipo float
        DF[column] = DF[column].str.replace(',', '.').astype(float)


def detectar_anomalias_y_corregir(df, columna, tasa_contaminacion):
    # Llenar valores NaN en la columna con 0
    df[columna].fillna(0, inplace=True)
    warnings.filterwarnings("ignore")
    # Crear un modelo Isolation Forest
    modelo = IForest(contamination=tasa_contaminacion, max_samples=100)
    modelo.fit(df[[columna]])

    # Predecir las anomalías en la columna
    anomalias = modelo.predict(df[[columna]])

    # Agregar una columna al DataFrame indicando si es anómalo o no
    df['EsAnomalo'] = anomalias

    # Función para corregir valores anómalos
    def corregir_valores_anomalos(df):
        for i in range(len(df)):
            if df.loc[i, 'EsAnomalo'] == 1:
                if i > 0 and i < len(df) - 1:
                    # Verificar si el valor siguiente no es anómalo
                    if df.loc[i + 1, 'EsAnomalo'] == 0:
                        valor_anterior = df.loc[i - 1, columna]
                        valor_siguiente = df.loc[i + 1, columna]
                        media_anterior_siguiente = (valor_anterior + valor_siguiente) / 2
                        df.loc[i, columna] = media_anterior_siguiente
                elif i == 0:
                    # Si es el primer valor y es anómalo
                    if df.loc[i + 1, 'EsAnomalo'] == 0:
                        valor_siguiente = df.loc[i + 1, columna]
                        df.loc[i, columna] = valor_siguiente
                elif i == len(df) - 1:
                    # Si es el último valor y es anómalo
                    if df.loc[i - 1, 'EsAnomalo'] == 0:
                        valor_anterior = df.loc[i - 1, columna]
                        df.loc[i, columna] = valor_anterior

    # Llamar a la función para corregir valores anómalos
    corregir_valores_anomalos(df)

    # Mostrar las filas donde se detectaron anomalías
    #anomalias_detectadas = df[df['EsAnomalo'] == 1]
    #print(anomalias_detectadas)

    return df

def calcular_dias_transcurridos(df2, df3, fecha_column, nueva_column):
    # Asegurarse de que la columna de fecha esté en formato DateTime
    df2[fecha_column] = pd.to_datetime(df2[fecha_column], format='%d/%m/%Y')
    df3[fecha_column] = pd.to_datetime(df3[fecha_column], format='%d/%m/%Y')
    # Ordenar el DataFrame por la columna de fecha
    df2 = df2.sort_values(by=[fecha_column])
    df3 = df3.sort_values(by=[fecha_column])

    # Calcular los días transcurridos desde la primera fecha
    df3[nueva_column] = (df3[fecha_column] - df2[fecha_column].iloc[0]).dt.days
    df3[nueva_column] = df3[nueva_column] + 1
    return df3

def mover_columna_a_posicion(dataframe, nombre_columna, posicion):
    columnas = dataframe.columns.tolist()
    if nombre_columna in columnas:
        columnas.remove(nombre_columna)
        columnas.insert(posicion, nombre_columna)
        return dataframe[columnas]
    else:
        return dataframe

def dividir_datos_entrenamiento_prueba(DF, porcprueba, random):
    """
    Divide el DataFrame en conjuntos de entrenamiento y prueba.

    - df_entrenamiento: DataFrame con los datos de entrenamiento.
    - df_prueba: DataFrame con los datos de prueba.
    """

    num_filas_prueba = int(len(DF) * porcprueba)
    df_prueba = DF.sample(n=num_filas_prueba, random_state=random)
    df_entrenamiento = DF.drop(df_prueba.index)

    return df_entrenamiento, df_prueba

DF = detectar_anomalias_y_corregir(DF, 'Grasa %', 0.02)
DF = detectar_anomalias_y_corregir(DF, 'Musculo %', 0.01)
DF = detectar_anomalias_y_corregir(DF, 'BMI', 0.01)
DF = detectar_anomalias_y_corregir(DF, 'Grasa visceral', 0.02)
DF = detectar_anomalias_y_corregir(DF, 'Metabolismo', 0.02)
DF = detectar_anomalias_y_corregir(DF, 'Agua', 0.02)
DF.drop('EsAnomalo', axis=1, inplace=True)

DF = calcular_dias_transcurridos(DF, DF, 'Fecha', 'Dias_Transcurridos')

DF = mover_columna_a_posicion(DF, 'Dias_Transcurridos', 1)

DF.drop('Entrenamiento de fuerza', axis=1, inplace=True)

datos_entrenamiento, datos_prueba = dividir_datos_entrenamiento_prueba(DF, 0.05, 3)


DF.to_csv("Datos_limpieza.csv", sep=";", index=False)
datos_entrenamiento.to_csv("Datos_entrenamiento.csv", sep=";", index=False)
datos_prueba.to_csv("Datos_prueba.csv", sep=";", index=False)



datossrt = []

def convertir_fecha_a_estandar(fecha_original):
    # Diccionario para mapear nombres de meses en español a números
     # Diccionario para mapear nombres de meses en español a números
    meses = {
        'enero': 1,
        'febrero': 2,
        'marzo': 3,
        'abril': 4,
        'mayo': 5,
        'junio': 6,
        'julio': 7,
        'agosto': 8,
        'septiembre': 9,
        'octubre': 10,
        'noviembre': 11,
        'diciembre': 12
    }

    # Dividir la fecha original en partes
    partes = fecha_original.split(', ')
    
    # Obtener el día, mes y año
    dia, mes, año = partes
    mes = mes.split(' ')
    dia = mes[1]
    mes = mes[0]
    # Obtener el número del mes a partir del diccionario
    mes_numero = meses[mes]
    
    # Formatear la fecha en el formato estándar
    fecha_formateada = f'{año}-{mes_numero:02d}-{dia}'
    
    return fecha_formateada

def limpiar_datos(archivo_csv):
    # Ruta al archivo CSV
    # Inicializa una lista para almacenar las líneas relevantes del archivo CSV
    lineas_relevantes = []

    # Indicador para determinar si debes empezar a recolectar líneas
    comenzar_recoleccion = False

    with open(archivo_csv, 'r', encoding='utf-8') as archivo:
        comenzar_recoleccion = False
        lineas_saltar = 0  # Variable para rastrear cuántas líneas has saltado
        for linea in archivo:
            # Comprueba si la línea contiene el indicador
            if ("# Report Details" in linea):
                comenzar_recoleccion = True
                lineas_saltar = 2  # Indica que se deben saltar las siguientes 2 líneas
                continue  # Salta la línea actual que contiene "# Report Details"
            
            if lineas_saltar != 0:
                lineas_saltar -= 1
                continue  # Salta la línea actual
            # Verifica si debes comenzar a recolectar líneas
            if comenzar_recoleccion:
                lineas_relevantes.append(linea)

    # Convierte las líneas recolectadas en un solo texto
    datos_completos = ''.join(lineas_relevantes)

    lineas = datos_completos.split('\n')
    lineas.pop()

    # Procesar cada línea por separado
    for linea in lineas:
        elementos = linea.split('2023",')
        fecha = elementos[0] + "2023"
        fecha = fecha.strip('"')
        fecha = convertir_fecha_a_estandar(fecha)
        elementos.pop(0)
        elementos = elementos[0]
        numeros_con_comas = re.findall(r'"([\d,]+)"', elementos)
        numeros_convertidos = [float(numero.replace(',', '.')) for numero in numeros_con_comas]
        datos_procesados = re.sub(r'"([\d,]+)"', lambda x: str(numeros_convertidos.pop(0)), elementos)
        datos_procesados = datos_procesados.replace(',', ';')
        linea_completa = fecha + ';' + datos_procesados
        
        datossrt.append(linea_completa) 



nombres_columnas = ['Fecha', 'Calorias(kcal)', 'Grasa(g)', 'Sat(g)', 'Carbh(g)', 'Fibra(g)', 'Azucar(g)', 'Proteina(g)', 'Sodio(g)', 'Colesterol(mg)', 'potasio(mg)']
limpiar_datos('FoodDiary_Aug_23_days.csv')
limpiar_datos('FoodDiary_Sep_23_days.csv')
limpiar_datos('FoodDiary_Oct_23_days.csv')

dfaug = pd.DataFrame([item.split(';') for item in datossrt], columns = nombres_columnas)
dfaug['Fecha'] = pd.to_datetime(dfaug['Fecha'])
Columnas_covert = ['Calorias(kcal)', 'Grasa(g)', 'Sat(g)', 'Carbh(g)', 'Fibra(g)', 'Azucar(g)', 'Proteina(g)', 'Sodio(g)', 'Colesterol(mg)', 'potasio(mg)']
for columsn in Columnas_covert:
    dfaug[columsn] = dfaug[columsn].astype(float)

dfaug = calcular_dias_transcurridos(DF, dfaug, 'Fecha', 'Dias_Transcurridos')
dfaug = mover_columna_a_posicion(dfaug, 'Dias_Transcurridos', 1)

merged_df = pd.merge(DF, dfaug, on="Dias_Transcurridos", how="inner")
merged_df.drop('Fecha_y', axis=1, inplace=True)
merged_df= merged_df.rename(columns={'Fecha_x': 'Fecha'})

datos_entrenamiento_unidos, datos_prueba_unidos = dividir_datos_entrenamiento_prueba(merged_df, 0.05, 3)

merged_df.to_csv("Datos_limpieza_unidos.csv", sep=";", index=False)
datos_entrenamiento_unidos.to_csv("Datos_entrenamiento_unidos.csv", sep=";", index=False)
datos_prueba_unidos.to_csv("Datos_prueba_unidos.csv", sep=";", index=False)

