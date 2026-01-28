from typing import Dict, Optional

from pydantic import BaseModel, Field


# Modelos de Entrada (Requests)
class PrediccionRequest(BaseModel):
    # Metadatos de la Petición
    nombre_estudiante: str = Field(
        ...,
        description="Identificador o nombre del estudiante para el reporte.",
        examples=["Juan Pérez"],
    )
    umbral: float = Field(
        0.5,
        ge=0.0,
        le=1.0,
        description="Punto de corte para decidir la clase (0.0 a 1.0). Por defecto 0.5.",
    )

    # Variables Socio-Demográficas
    Genero: int = Field(
        ..., description="1: Masculino, 0: Femenino (según codificación)", examples=[1]
    )
    Edad_al_matricularse: int = Field(
        ..., ge=15, description="Edad del estudiante al ingreso."
    )
    Estado_civil: Optional[int] = Field(
        None, description="Código de estado civil (si aplica)."
    )
    Nacionalidad: Optional[int] = Field(
        None, description="Código de nacionalidad (si aplica)."
    )
    Desplazado: int = Field(..., description="1: Sí, 0: No.")

    # Datos Familiares
    Calificacion_madre: int = Field(..., description="Nivel educativo de la madre.")
    Calificacion_padre: int = Field(..., description="Nivel educativo del padre.")
    Ocupacion_madre: int = Field(..., description="Código de ocupación materna.")
    Ocupacion_padre: int = Field(..., description="Código de ocupación paterna.")

    # Datos de Solicitud
    Modo_solicitud: int = Field(..., description="Modalidad de ingreso.")
    Orden_solicitud: int = Field(
        ..., description="Preferencia en la orden de solicitud."
    )
    Carrera: int = Field(..., description="Código de la carrera seleccionada.")
    Asistencia_diurna_nocturna: int = Field(..., description="1: Diurno, 0: Nocturno.")
    Calificacion_previa: int = Field(
        ..., description="Nota o puntaje previo al ingreso."
    )

    # Factores Económicos
    Becado: int = Field(..., description="1: Tiene beca, 0: No.")
    Deudor: int = Field(..., description="1: Tiene deudas con la institución, 0: No.")
    Pagos_al_dia: int = Field(..., description="1: Pagos al día, 0: Mora.")
    Tasa_desempleo: float = Field(
        ..., description="Tasa de desempleo regional/nacional."
    )
    Tasa_inflacion: float = Field(..., description="Tasa de inflación actual.")
    PIB: float = Field(..., description="Producto Interno Bruto del periodo.")

    # Rendimiento Académico (Primer Semestre)
    Unidades_1er_sem_matriculadas: int = Field(..., ge=0)
    Unidades_1er_sem_evaluaciones: int = Field(..., ge=0)
    Unidades_1er_sem_aprobadas: int = Field(..., ge=0)
    Unidades_1er_sem_nota: float = Field(
        ..., ge=0.0, description="Promedio de notas 1er semestre."
    )

    # Rendimiento Académico (Segundo Semestre)
    Unidades_2do_sem_matriculadas: int = Field(..., ge=0)
    Unidades_2do_sem_evaluaciones: int = Field(..., ge=0)
    Unidades_2do_sem_aprobadas: int = Field(..., ge=0)
    Unidades_2do_sem_nota: float = Field(
        ..., ge=0.0, description="Promedio de notas 2do semestre."
    )


# Esquema para creación - login de usuarios
class UsuarioRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6, description="Contraseña segura.")
    email: str = Field(..., description="Correo electrónico válido.")


# Modelos de Salida (Responses)
class PrediccionResponse(BaseModel):
    prediction: str = Field(..., description="'Desertor' o 'No Desertor'")
    probability: float = Field(..., description="Probabilidad calculada (0-1)")
    explanations: Dict[str, float] = Field(
        ...,
        description="Diccionario de valores SHAP {variable: impacto} para explicabilidad.",
    )


# Respuesta Genérica del usuario
class UsuarioResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True
