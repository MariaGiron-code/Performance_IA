#Importación de librerias
import numpy as np
import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler

#Importar Dataset
print("Llamando al data Set")
df_dataset= pd.read_csv("dataset.csv")

#visualizar dataset
df_dataset.head()

#Traduccion de columnas en Español
# Diccionario de traducción
columnas_espanol = {
    'Marital status': 'Estado_civil',
    'Application mode': 'Modo_solicitud',
    'Application order': 'Orden_solicitud',
    'Course': 'Carrera',
    'Daytime/evening attendance': 'Asistencia_diurna_nocturna',
    'Previous qualification': 'Calificacion_previa',
    'Nacionality': 'Nacionalidad',
    "Mother's qualification": 'Calificacion_madre',
    "Father's qualification": 'Calificacion_padre',
    "Mother's occupation": 'Ocupacion_madre',
    "Father's occupation": 'Ocupacion_padre',
    'Displaced': 'Desplazado',
    'Educational special needs': 'Necesidades_educativas_especiales',
    'Debtor': 'Deudor',
    'Tuition fees up to date': 'Pagos_al_dia',
    'Gender': 'Genero',
    'Scholarship holder': 'Becado',
    'Age at enrollment': 'Edad_al_matricularse',
    'International': 'Internacional',
    'Curricular units 1st sem (credited)': 'Unidades_1er_sem_acreditadas',
    'Curricular units 1st sem (enrolled)': 'Unidades_1er_sem_matriculadas',
    'Curricular units 1st sem (evaluations)': 'Unidades_1er_sem_evaluaciones',
    'Curricular units 1st sem (approved)': 'Unidades_1er_sem_aprobadas',
    'Curricular units 1st sem (grade)': 'Unidades_1er_sem_nota',
    'Curricular units 1st sem (without evaluations)': 'Unidades_1er_sem_sin_evaluaciones',
    'Curricular units 2nd sem (credited)': 'Unidades_2do_sem_acreditadas',
    'Curricular units 2nd sem (enrolled)': 'Unidades_2do_sem_matriculadas',
    'Curricular units 2nd sem (evaluations)': 'Unidades_2do_sem_evaluaciones',
    'Curricular units 2nd sem (approved)': 'Unidades_2do_sem_aprobadas',
    'Curricular units 2nd sem (grade)': 'Unidades_2do_sem_nota',
    'Curricular units 2nd sem (without evaluations)': 'Unidades_2do_sem_sin_evaluaciones',
    'Unemployment rate': 'Tasa_desempleo',
    'Inflation rate': 'Tasa_inflacion',
    'GDP': 'PIB',
    'Target': 'Objetivo'
}

# Aplicar la traducción
df_dataset = df_dataset.rename(columns=columnas_espanol)

#Separar el dataset en dos grupos

# Casos con resultado final (para entrenar el modelo)
df_entrenamiento = df_dataset[df_dataset['Objetivo'] != 'Enrolled'].copy()

# Casos que siguen inscritos (para evaluarlos después con la IA)
df_inscritos = df_dataset[df_dataset['Objetivo'] == 'Enrolled'].copy()

# Eliminar columna Objetivo en inscritos
df_inscritos = df_inscritos.drop(columns=['Objetivo'] + cols_eliminar)

# Transformación de la columna  Objetivo en datos categoricos
df_entrenamiento['Es_Desertor'] = (df_entrenamiento['Objetivo'] == 'Dropout').astype(int)

#Eliminar columanas que no son tan necesarias para este modelo
cols_eliminar = [
    'Objetivo',
    'Internacional',
    'Nacionalidad',
    'Necesidades_educativas_especiales',
    'Estado_civil',
    'Unidades_1er_sem_acreditadas',
    'Unidades_2do_sem_acreditadas',
    'Unidades_1er_sem_sin_evaluaciones',
    'Unidades_2do_sem_sin_evaluaciones'
]

df_entrenamiento=df_entrenamiento.drop(cols_eliminar,axis=1)

#visualizar los cambios del dataset
df_entrenamiento.head()

#Manejo de nulos, duplicados y normalización
# 1. Manejo de Duplicados
# Elimina filas que sean exactamente iguales para evitar sobreajuste
df_proceso= df_entrenamiento.drop_duplicates()
print(f"Registros tras eliminar duplicados: {len(df_proceso)}")

# 2. Manejo de Nulos
# Eliminar celdas vacías, ajuste con la mediana
if df_proceso.isnull().values.any():
  df_proceso = df.fillna(df.median(numeric_only=True))
  print("Valores nulos detectados y completados con la mediana.")
else:
  print("No se encontraron valores nulos.")

#Guardar Archivos
df_entrenamiento.to_csv('entrenamiento.csv', index=False)
df_inscritos.to_csv('evaluacion.csv', index=False)