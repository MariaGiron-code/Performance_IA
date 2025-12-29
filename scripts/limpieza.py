# archivo de limpieza de datos
#Importacion de librerias
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

#Importar Dataset
print("Llamando al data Set")
df_dataset= pd.read_csv("dataset.csv")

#visualizar dataset
df_dataset.head()

#Traformación de los valores de la columna target's en datos categoricos
df_dataset['Is_Dropout'] = (df_dataset['Target'] == 'Dropout').astype(int)

df_dataset.head()

#Eliminar columanas que no son validas para este modelo
cols_eliminar=[
    'Target',
        'International',
        'Nacionality',
        'Educational special needs',
        'Marital status',
        'Curricular units 1st sem (credited)',
        'Curricular units 2nd sem (credited)',
        'Curricular units 1st sem (without evaluations)',
        'Curricular units 2nd sem (without evaluations)'
]

df_dataset=df_dataset.drop(cols_eliminar,axis=1)

#Manejo de nulos, duplicados y normalización
# 1. Manejo de Duplicados
# Elimina filas que sean exactamente iguales para evitar sobreajuste
df_proceso= df_dataset.drop_duplicates()
print(f"Registros tras eliminar duplicados: {len(df_proceso)}")

# 2. Manejo de Nulos 
# Se llena las celdas vacías, las llenamos con la mediana
# para no perder la fila completa.
if df_proceso.isnull().values.any():
  df_proceso = df.fillna(df.median(numeric_only=True))
  print("Valores nulos detectados y completados con la mediana.")
else:
  print("No se encontraron valores nulos.")

# 3. Normalización 
# Seleccionamos solo las columnas numéricas para normalizar
columnas_numericas = df_proceso.select_dtypes(include=['float64', 'int64']).columns.drop('Is_Dropout')
scaler = StandardScaler()
df_proceso[columnas_numericas] = scaler.fit_transform(df_proceso[columnas_numericas])
print("Normalización completada exitosamente.")

# 4. Guardar el archivo
dataset_limpio = "dataset_limpio.csv"
df_proceso.to_csv(dataset_limpio, index=False)
print(f"Archivo preprocesado guardado")
