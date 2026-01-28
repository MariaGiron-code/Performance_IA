import logging
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

import joblib
import pandas as pd
import shap

# Configuración y Constantes
logger = logging.getLogger(__name__)

# Define la ruta absoluta al modelo basándose en la ubicación de este archivo.
BASE_DIR = Path(__file__).resolve().parent.parent.parent  # Sube a la raíz del proyecto
MODEL_PATH = BASE_DIR / "scripts" / "model" / "modelo_random_forest.pkl"

# Orden estricto de columnas requerido por el modelo
COLUMN_ORDER = [
    "Modo_solicitud",
    "Orden_solicitud",
    "Carrera",
    "Asistencia_diurna_nocturna",
    "Calificacion_previa",
    "Calificacion_madre",
    "Calificacion_padre",
    "Ocupacion_madre",
    "Ocupacion_padre",
    "Desplazado",
    "Deudor",
    "Pagos_al_dia",
    "Genero",
    "Becado",
    "Edad_al_matricularse",
    "Unidades_1er_sem_matriculadas",
    "Unidades_1er_sem_evaluaciones",
    "Unidades_1er_sem_aprobadas",
    "Unidades_1er_sem_nota",
    "Unidades_2do_sem_matriculadas",
    "Unidades_2do_sem_evaluaciones",
    "Unidades_2do_sem_aprobadas",
    "Unidades_2do_sem_nota",
    "Tasa_desempleo",
    "Tasa_inflacion",
    "PIB",
]

# Diccionario de traducción para presentar resultados legibles al usuario final.
FRIENDLY_NAMES = {
    "Modo_solicitud": "Modo de solicitud",
    "Orden_solicitud": "Orden de solicitud",
    "Carrera": "Carrera",
    "Asistencia_diurna_nocturna": "Horario (Diurno/Nocturno)",
    "Calificacion_previa": "Calificación previa",
    "Calificacion_madre": "Escolaridad Madre",
    "Calificacion_padre": "Escolaridad Padre",
    "Ocupacion_madre": "Ocupación Madre",
    "Ocupacion_padre": "Ocupación Padre",
    "Desplazado": "Condición de Desplazado",
    "Deudor": "Deudor",
    "Pagos_al_dia": "Pagos al día",
    "Genero": "Género",
    "Becado": "Becado",
    "Edad_al_matricularse": "Edad de ingreso",
    "Unidades_1er_sem_matriculadas": "Créditos matriculados (1er Sem)",
    "Unidades_1er_sem_evaluaciones": "Créditos evaluados (1er Sem)",
    "Unidades_1er_sem_aprobadas": "Créditos aprobados (1er Sem)",
    "Unidades_1er_sem_nota": "Promedio (1er Sem)",
    "Unidades_2do_sem_matriculadas": "Créditos matriculados (2do Sem)",
    "Unidades_2do_sem_evaluaciones": "Créditos evaluados (2do Sem)",
    "Unidades_2do_sem_aprobadas": "Créditos aprobados (2do Sem)",
    "Unidades_2do_sem_nota": "Promedio (2do Sem)",
    "Tasa_desempleo": "Tasa de desempleo",
    "Tasa_inflacion": "Tasa de inflación",
    "PIB": "PIB",
}

# Variables Globales (Caché)
_MODEL_CACHE: Optional[Any] = None
_EXPLAINER_CACHE: Optional[Any] = None


# Lógica Interna


# Gestiona la carga del modelo evitando múltiples peticiones de disco.
def _get_resources():
    global _MODEL_CACHE, _EXPLAINER_CACHE

    if _MODEL_CACHE is None:
        if not MODEL_PATH.exists():
            raise FileNotFoundError(f"El modelo no existe en: {MODEL_PATH}")

        logger.info("Cargando modelo en memoria...")
        _MODEL_CACHE = joblib.load(MODEL_PATH)

        # Intenta inicializar SHAP una sola vez para reutilizarlo.
        try:
            logger.info("Inicializando motor de explicabilidad SHAP...")
            _EXPLAINER_CACHE = shap.TreeExplainer(_MODEL_CACHE)
        except Exception as e:
            logger.warning(
                f"No se pudo inicializar SHAP: {e}. Se usará importancia de características simple."
            )
            _EXPLAINER_CACHE = None

    return _MODEL_CACHE, _EXPLAINER_CACHE


# Función Principal
# Orquesta el flujo de predicciones: carga recursos, procesa datos e infiere resultados.
def ejecutar_prediccion(datos_dict: Dict) -> Tuple[Optional[float], Dict[str, float]]:
    try:
        # 1. Obtención de Recursos
        modelo, explainer = _get_resources()

        # 2. Preprocesamiento
        # Convierte el diccionario a DataFrame asegurando el orden estricto de columnas.
        df_input = pd.DataFrame([datos_dict])[COLUMN_ORDER]

        # 3. Inferencia (Predicción)
        probabilidad = modelo.predict_proba(df_input)[0][1]

        if explainer:
            try:
                # Calcula los valores SHAP que corresponden a la clase positiva (Desertor).
                shap_values = explainer.shap_values(df_input)

                # Maneja diferencias en la estructura de retorno de SHAP según la versión.
                vals = (
                    shap_values[1][0]
                    if isinstance(shap_values, list)
                    else shap_values[0]
                )
                explicaciones_raw = dict(zip(COLUMN_ORDER, vals))

            except Exception as shap_err:
                logger.error(f"Error en cálculo SHAP runtime: {shap_err}")
                explicaciones_raw = _get_feature_importances(modelo)
        else:
            explicaciones_raw = _get_feature_importances(modelo)

        # 5. Formato de Salida
        explicaciones_amigables = {
            FRIENDLY_NAMES.get(k, k): v for k, v in explicaciones_raw.items()
        }

        return probabilidad, explicaciones_amigables

    except Exception as e:
        logger.critical(f"Error crítico en ejecutar_prediccion: {e}", exc_info=True)
        return None, {}


def _get_feature_importances(modelo) -> Dict[str, float]:
    if hasattr(modelo, "feature_importances_"):
        return dict(zip(COLUMN_ORDER, modelo.feature_importances_))
    return {}
