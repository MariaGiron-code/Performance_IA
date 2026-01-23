# Este archivo define las rutas (endpoints) de la API REST utilizando FastAPI.
# La API permite realizar predicciones de riesgo de deserción académica, gestionar usuarios y autenticación.
# Reutiliza funciones existentes de database.py (guardar_prediccion, registrar_usuario) y logic.py (ejecutar_prediccion).
# Utiliza modelos Pydantic de models.py y dependencias de dependencies.py para inyección de DB y autenticación.

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.api.models import PrediccionRequest, PrediccionResponse, UsuarioRequest, UsuarioResponse
from src.api.dependencies import get_db, get_current_user, ejecutar_prediccion
from src.database import guardar_prediccion, registrar_usuario
from typing import Dict

# Crear un router para agrupar los endpoints de la API
router = APIRouter()

# Ruta para hcer predicciones
@router.post("/predict", response_model=PrediccionResponse)
def predict(
    request: PrediccionRequest,
    user: Dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Endpoint para realizar una predicción de riesgo de deserción académica.
    Requiere autenticación básica (HTTP Basic Auth).
    """
    try:
        # Extraer los datos de entrada del request (los 26 campos del modelo )
        # Estos campos corresponden a las variables de entrada del modelo entrenado
        datos = {
            'Modo_solicitud': request.Modo_solicitud,
            'Orden_solicitud': request.Orden_solicitud,
            'Carrera': request.Carrera,
            'Asistencia_diurna_nocturna': request.Asistencia_diurna_nocturna,
            'Calificacion_previa': request.Calificacion_previa,
            'Calificacion_madre': request.Calificacion_madre,
            'Calificacion_padre': request.Calificacion_padre,
            'Ocupacion_madre': request.Ocupacion_madre,
            'Ocupacion_padre': request.Ocupacion_padre,
            'Desplazado': request.Desplazado,
            'Deudor': request.Deudor,
            'Pagos_al_dia': request.Pagos_al_dia,
            'Genero': request.Genero,
            'Becado': request.Becado,
            'Edad_al_matricularse': request.Edad_al_matricularse,
            'Unidades_1er_sem_matriculadas': request.Unidades_1er_sem_matriculadas,
            'Unidades_1er_sem_evaluaciones': request.Unidades_1er_sem_evaluaciones,
            'Unidades_1er_sem_aprobadas': request.Unidades_1er_sem_aprobadas,
            'Unidades_1er_sem_nota': request.Unidades_1er_sem_nota,
            'Unidades_2do_sem_matriculadas': request.Unidades_2do_sem_matriculadas,
            'Unidades_2do_sem_evaluaciones': request.Unidades_2do_sem_evaluaciones,
            'Unidades_2do_sem_aprobadas': request.Unidades_2do_sem_aprobadas,
            'Unidades_2do_sem_nota': request.Unidades_2do_sem_nota,
            'Tasa_desempleo': request.Tasa_desempleo,
            'Tasa_inflacion': request.Tasa_inflacion,
            'PIB': request.PIB
        }

        # Ejecutar la predicción usando la función reutilizada de logic.py
        # Esta función carga el modelo y devuelve la probabilidad de deserción
        probabilidad = ejecutar_prediccion(datos)
        if probabilidad is None:
            raise HTTPException(status_code=400, detail="Error en la predicción. Verifica los campos ingresados.")

        # Determinar el resultado basado en el umbral proporcionado por el usuario
        # Si la probabilidad > umbral, clasifica como "Desertor"; de lo contrario, "No Desertor"
        resultado = "Desertor" if probabilidad > request.umbral else "No Desertor"

        # Guardar la predicción en la base de datos usando la función reutilizada de database.py
        # Asocia la predicción al usuario autenticado
        if not guardar_prediccion(user['id'], request.nombre_estudiante, datos, probabilidad, resultado, request.umbral):
            raise HTTPException(status_code=500, detail="Error al guardar la predicción en la base de datos.")

        # Devolver la respuesta con la predicción y probabilidad
        return PrediccionResponse(prediction=resultado, probability=probabilidad)

    except Exception as e:
        # Manejo de errores generales, devolviendo un error 500 con detalles
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

# Ruta para registrar nuevos usuarios
@router.post("/users", response_model=UsuarioResponse)
def create_user(request: UsuarioRequest, db: Session = Depends(get_db)):
    """
    Endpoint para crear un nuevo usuario.
    No requiere autenticación.
    """
    try:
        # Intentar registrar al usuario usando la función reutilizada de database.py
        if registrar_usuario(request.username, request.email, request.password):
            # Nota: registrar_usuario no devuelve el ID del usuario creado, por lo que no podemos devolver UsuarioResponse completo.
            # En una implementación completa, se podría modificar para devolver el ID o hacer una consulta adicional.
            raise HTTPException(status_code=201, detail="Usuario creado exitosamente.")
        else:
            raise HTTPException(status_code=400, detail="Error al crear el usuario. Posiblemente el email ya existe.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

# Endpoint opcional para obtener información del usuario actual por implementar 
@router.get("/users/me", response_model=UsuarioResponse)
def get_user(user: Dict = Depends(get_current_user)):
    """
    Endpoint para obtener información del usuario autenticado.
    Devuelve el ID, username y email del usuario logueado.
    Útil para verificar la sesión o mostrar datos del perfil.
    """
    return UsuarioResponse(id=user['id'], username=user['nombre'], email=user['email'])