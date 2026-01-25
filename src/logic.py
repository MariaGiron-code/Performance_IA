# archivo de lógica del proyecto el backend de la aplicación
# se usa para ejecutar la lógica del proyecto
# se usa para ejecutar las funciones necesarias
# se usa para ejecutar las clases necesarias
# se usa para ejecutar las variables necesarias

import joblib
import pandas as pd
import shap

# Mapeo de nombres técnicos a nombres amigables para el usuario
nombres_amigables = {
    'Modo_solicitud': 'Modo de solicitud',
    'Orden_solicitud': 'Orden de solicitud',
    'Carrera': 'Carrera',
    'Asistencia_diurna_nocturna': 'Asistencia diurna/nocturna',
    'Calificacion_previa': 'Calificación previa',
    'Calificacion_madre': 'Calificación madre',
    'Calificacion_padre': 'Calificación padre',
    'Ocupacion_madre': 'Ocupación madre',
    'Ocupacion_padre': 'Ocupación padre',
    'Desplazado': 'Desplazado',
    'Deudor': 'Deudor',
    'Pagos_al_dia': 'Pagos al día',
    'Genero': 'Género',
    'Becado': 'Becado',
    'Edad_al_matricularse': 'Edad al matricularse',
    'Unidades_1er_sem_matriculadas': 'Créditos matriculados 1er sem',
    'Unidades_1er_sem_evaluaciones': 'Créditos evaluados 1er sem',
    'Unidades_1er_sem_aprobadas': 'Créditos aprobados 1er sem',
    'Unidades_1er_sem_nota': 'Nota promedio 1er sem',
    'Unidades_2do_sem_matriculadas': 'Créditos matriculados 2do sem',
    'Unidades_2do_sem_evaluaciones': 'Créditos evaluados 2do sem',
    'Unidades_2do_sem_aprobadas': 'Créditos aprobados 2do sem',
    'Unidades_2do_sem_nota': 'Nota promedio 2do sem',
    'Tasa_desempleo': 'Tasa de desempleo',
    'Tasa_inflacion': 'Tasa de inflación',
    'PIB': 'PIB'
}

def ejecutar_prediccion(datos_dict):
    """
    datos_dict: Diccionario con las 26 variables necesarias para la predicción
    Retorna la probabilidad de que un estudiante sea desertor y las explicaciones SHAP
    """
    try:
        # 1. Cargar el nuevo modelo
        modelo = joblib.load('model/modelo_a.pkl')

        # 2. Convertir a DataFrame asegurando el orden exacto de las columnas
        # Es fundamental que el orden sea el mismo que en entrenamiento.csv
        columnas = [
            'Modo_solicitud', 'Orden_solicitud', 'Carrera', 'Asistencia_diurna_nocturna',
            'Calificacion_previa', 'Calificacion_madre', 'Calificacion_padre',
            'Ocupacion_madre', 'Ocupacion_padre', 'Desplazado', 'Deudor',
            'Pagos_al_dia', 'Genero', 'Becado', 'Edad_al_matricularse',
            'Unidades_1er_sem_matriculadas', 'Unidades_1er_sem_evaluaciones',
            'Unidades_1er_sem_aprobadas', 'Unidades_1er_sem_nota',
            'Unidades_2do_sem_matriculadas', 'Unidades_2do_sem_evaluaciones',
            'Unidades_2do_sem_aprobadas', 'Unidades_2do_sem_nota',
            'Tasa_desempleo', 'Tasa_inflacion', 'PIB'
        ]

        df_input = pd.DataFrame([datos_dict])[columnas]

        # 3. Predicción
        probabilidad = modelo.predict_proba(df_input)[0][1] # Probabilidad de clase 1 (Desertor)

        # 4. Calcular explicaciones con SHAP
        try:
            explainer = shap.TreeExplainer(modelo)
            shap_values = explainer.shap_values(df_input)
            # shap_values[1] para clase positiva (Desertor)
            explicaciones_raw = dict(zip(columnas, shap_values[1][0]))
        except Exception as shap_error:
            print(f"Error calculando SHAP: {shap_error}. Usando explicaciones alternativas.")
            # Fallback: usar feature_importances_ si disponible, sino dict vacío
            if hasattr(modelo, 'feature_importances_'):
                explicaciones_raw = dict(zip(columnas, modelo.feature_importances_))
            else:
                explicaciones_raw = {}

        # Crear explicaciones amigables
        explicaciones_amigables = {nombres_amigables.get(k, k): v for k, v in explicaciones_raw.items()}

        return probabilidad, explicaciones_amigables
    except Exception as e:
        print(f"Error en la predicción: {e}")
        return None, {}