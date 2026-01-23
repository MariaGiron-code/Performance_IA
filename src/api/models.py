# Definición del modelo de datos para la aplicación
from pydantic import BaseModel # Importar BaseModel para definir modelos de datos
from typing import Dict, Any # Importar Any para tipos de datos flexibles y Dict para diccionarios

class PrediccionRequest(BaseModel):
    nombre_estudiante: str
    umbral: float
    Modo_solicitud: int
    Orden_solicitud: int
    Carrera: int
    Asistencia_diurna_nocturna: int
    Calificacion_previa: int
    Calificacion_madre: int
    Calificacion_padre: int
    Ocupacion_madre: int
    Ocupacion_padre: int
    Desplazado: int
    Deudor: int
    Pagos_al_dia: int
    Genero: int
    Becado: int
    Edad_al_matricularse: int
    Unidades_1er_sem_matriculadas: int
    Unidades_1er_sem_evaluaciones: int
    Unidades_1er_sem_aprobadas: int
    Unidades_1er_sem_nota: float
    Unidades_2do_sem_matriculadas: int
    Unidades_2do_sem_evaluaciones: int
    Unidades_2do_sem_aprobadas: int
    Unidades_2do_sem_nota: float
    Tasa_desempleo: float
    Tasa_inflacion: float
    PIB: float

class PrediccionResponse(BaseModel):
    prediction: str  # "Desertor" or "No Desertor"
    probability: float
    explanations: Dict[str, float]  # Diccionario de variable: contribución SHAP

class UsuarioRequest(BaseModel):
    username: str
    password: str
    email: str

class UsuarioResponse(BaseModel):
    id: int
    username: str
    email: str
