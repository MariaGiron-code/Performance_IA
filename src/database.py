import json
import logging
import os
from typing import Any, Dict, Optional

import bcrypt
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

# --- Configuración Global ---

load_dotenv()

# Configura el sistema de logs para evitar el uso de 'print' en producción.
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Verifica la variable de entorno crítica.
DATABASE_URL = os.getenv("DB_URL")
if not DATABASE_URL:
    raise ValueError("❌ Error: La variable DB_URL no está definida en el entorno.")

# Crea el motor de conexión con pooling activado para eficiencia.
engine = create_engine(DATABASE_URL, pool_pre_ping=True)


# --- Gestión de Usuarios (Auth) ---


def registrar_usuario(nombre: str, email: str, password: str) -> bool:
    """
    Crea un nuevo usuario en la base de datos con contraseña hasheada.
    Retorna False si el email ya existe (IntegrityError).
    """
    # Genera un hash seguro utilizando bcrypt (estándar de la industria).
    bytes_password = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hash_password = bcrypt.hashpw(bytes_password, salt).decode("utf-8")

    query = text("""
                 INSERT INTO usuarios (nombre, email, password_hash)
                 VALUES (:nombre, :email, :password_hash)
                 """)

    try:
        # Usa 'engine.begin' para manejar la transacción automáticamente (commit/rollback).
        with engine.begin() as conn:
            conn.execute(
                query,
                {"nombre": nombre, "email": email, "password_hash": hash_password},
            )
            logger.info(f"Usuario registrado exitosamente: {email}")
            return True

    except IntegrityError:
        logger.warning(f"Intento de registro duplicado para: {email}")
        return False
    except SQLAlchemyError as e:
        logger.error(f"Error de base de datos al registrar usuario: {e}")
        return False


def login(email: str, password: str) -> Optional[Dict[str, Any]]:
    """
    Verifica las credenciales del usuario.
    Retorna un diccionario con los datos del usuario si es exitoso, o None si falla.
    """
    query = text(
        "SELECT id, nombre, email, password_hash FROM usuarios WHERE email = :email"
    )

    try:
        with engine.connect() as conn:
            result = conn.execute(query, {"email": email}).fetchone()

            if not result:
                return None  # Usuario no encontrado

            # Desempaqueta la tupla de resultados.
            user_id, nombre, user_email, hash_almacenado = result

            # Convierte el hash a bytes si es necesario para bcrypt.
            hash_bytes = (
                hash_almacenado.encode("utf-8")
                if isinstance(hash_almacenado, str)
                else hash_almacenado
            )

            # Compara la contraseña plana con el hash almacenado.
            if bcrypt.checkpw(password.encode("utf-8"), hash_bytes):
                return {"id": user_id, "nombre": nombre, "email": user_email}

            return None  # Contraseña incorrecta

    except SQLAlchemyError as e:
        logger.error(f"Error crítico en login: {e}")
        return None


def cambiar_contraseña(
        email: str, contraseña_actual: str, nueva_contraseña: str
) -> bool:
    """
    Actualiza la contraseña del usuario previa validación de la actual.
    """
    query_select = text("SELECT password_hash FROM usuarios WHERE email = :email")
    query_update = text(
        "UPDATE usuarios SET password_hash = :nuevo_hash WHERE email = :email"
    )

    try:
        with engine.begin() as conn:
            # 1. Verificación
            result = conn.execute(query_select, {"email": email}).fetchone()
            if not result:
                return False

            hash_almacenado = result[0]
            if isinstance(hash_almacenado, str):
                hash_almacenado = hash_almacenado.encode("utf-8")

            if not bcrypt.checkpw(contraseña_actual.encode("utf-8"), hash_almacenado):
                return False

            # 2. Actualización
            bytes_nueva = nueva_contraseña.encode("utf-8")
            nuevo_hash = bcrypt.hashpw(bytes_nueva, bcrypt.gensalt()).decode("utf-8")

            conn.execute(query_update, {"nuevo_hash": nuevo_hash, "email": email})
            logger.info(f"Contraseña actualizada para: {email}")
            return True

    except SQLAlchemyError as e:
        logger.error(f"Error al cambiar contraseña: {e}")
        return False


# --- Historial y Analítica ---


def guardar_prediccion(
        usuario_id: int,
        nombre_est: str,
        datos_dict: Dict,
        prob: float,
        resultado: str,
        umbral: float,
        explicaciones: Dict,
) -> bool:
    """
    Persiste el resultado de la inferencia y los datos de entrada (JSONB) para auditoría.
    """
    query = text("""
                 INSERT INTO historial_predicciones
                 (usuario_id, nombre_estudiante, datos_entrada, probabilidad, resultado_ia, umbral_usado, explicaciones)
                 VALUES (:uid, :nombre, :datos, :prob, :res, :umbral, :expl)
                 """)

    try:
        with engine.begin() as conn:
            conn.execute(
                query,
                {
                    "uid": usuario_id,
                    "nombre": nombre_est,
                    # SQLAlchemy maneja JSON nativamente en dialectos modernos,
                    # pero json.dumps asegura compatibilidad con tipos TEXT o JSON genéricos.
                    "datos": json.dumps(datos_dict),
                    "prob": float(prob),
                    "res": resultado,
                    "umbral": float(umbral),
                    "expl": json.dumps(explicaciones),
                },
            )
            return True
    except SQLAlchemyError as e:
        logger.error(f"Error guardando predicción: {e}")
        return False


def obtener_estadisticas_monitoreo() -> Optional[Dict[str, Any]]:
    """
    Calcula métricas globales y recupera el historial reciente.
    Optimización: Realiza agregaciones en SQL para reducir latencia de red.
    """
    # Consulta optimizada: Calcula total y riesgo en una sola pasada.
    query_agregada = text("""
                          SELECT COUNT(*)                                                   as total,
                                 SUM(CASE WHEN resultado_ia = 'Desertor' THEN 1 ELSE 0 END) as total_riesgo
                          FROM historial_predicciones
                          """)

    query_historial = text("""
                           SELECT nombre_estudiante, resultado_ia, probabilidad
                           FROM historial_predicciones
                           ORDER BY fecha_prediccion DESC LIMIT 10
                           """)

    try:
        with engine.connect() as conn:
            # 1. Obtener métricas agregadas
            metrics = conn.execute(query_agregada).fetchone()
            total = metrics[0] or 0
            riesgo = metrics[1] or 0

            # 2. Obtener historial reciente
            historial_raw = conn.execute(query_historial).fetchall()

            # Formatear respuesta
            historial = [
                {"nombre": row[0], "resultado": row[1], "probabilidad": float(row[2])}
                for row in historial_raw
            ]

            tasa = (riesgo / total * 100) if total > 0 else 0

            return {
                "total_evaluados": total,
                "total_riesgo": riesgo,
                "tasa_riesgo": round(tasa, 2),
                "historial": historial,
            }

    except SQLAlchemyError as e:
        logger.error(f"Error obteniendo estadísticas: {e}")
        return None
