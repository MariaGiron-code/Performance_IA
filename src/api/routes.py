from typing import Annotated, Dict

from fastapi import APIRouter, Depends, HTTPException, status

from src.api.dependencies import get_current_user
# Importaciones internas del proyecto
from src.api.models import (
    PrediccionRequest,
    PrediccionResponse,
    UsuarioRequest,
    UsuarioResponse,
)
from src.database import (
    guardar_prediccion,
    obtener_estadisticas_monitoreo,
    registrar_usuario,
)
from src.logic import ejecutar_prediccion

# Inicializa el router de FastAPI.
router = APIRouter()


# Rutas de Predicción
@router.post(
    "/predict",
    response_model=PrediccionResponse,
    tags=["Predicciones"],
    summary="Evaluar riesgo de deserción",
)
def predict(
        request: PrediccionRequest,
        current_user: Annotated[Dict, Depends(get_current_user)],
):
    try:
        # 1. Extracción de Datos
        features_data = request.model_dump(exclude={"nombre_estudiante", "umbral"})

        # 2. Ejecución del Modelo
        resultado_prediccion = ejecutar_prediccion(features_data)

        if not resultado_prediccion or resultado_prediccion[0] is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="El modelo no pudo procesar los datos. Verifique los valores numéricos.",
            )

        probabilidad, explicaciones = resultado_prediccion

        # 3. Determina la etiqueta final
        etiqueta = "Desertor" if probabilidad > request.umbral else "No Desertor"

        # 4. Guarda el historial vinculado al usuario actual
        guardado_exitoso = guardar_prediccion(
            usuario_id=current_user["id"],
            nombre_est=request.nombre_estudiante,
            datos_dict=features_data,
            prob=probabilidad,
            resultado=etiqueta,
            umbral=request.umbral,
            explicaciones=explicaciones,
        )

        if not guardado_exitoso:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="La predicción se generó pero falló al guardarse en el historial.",
            )

        return PrediccionResponse(
            prediction=etiqueta, probability=probabilidad, explanations=explicaciones
        )

    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error inesperado en el motor de inferencia: {str(e)}",
        )


# --- Rutas de Usuarios ---
@router.post(
    "/users",
    status_code=status.HTTP_201_CREATED,
    tags=["Usuarios"],
    summary="Registrar nuevo usuario",
)
def create_user(request: UsuarioRequest):
    try:
        exito = registrar_usuario(request.username, request.email, request.password)

        if exito:
            return {"message": "Usuario registrado exitosamente."}
        else:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="El correo electrónico ya está asociado a otra cuenta.",
            )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/users/me",
    response_model=UsuarioResponse,
    tags=["Usuarios"],
    summary="Perfil del usuario actual",
)
def get_user(current_user: Annotated[Dict, Depends(get_current_user)]):
    return current_user


# --- Rutas de Monitoreo ---
@router.get(
    "/monitoreo/stats", tags=["Monitoreo"], summary="Métricas globales del sistema"
)
# Obtiene la info del usuario logueado
def get_monitoreo_stats(_: Annotated[Dict, Depends(get_current_user)]):
    stats = obtener_estadisticas_monitoreo()

    if stats is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="El servicio de monitoreo no está respondiendo.",
        )

    return stats
