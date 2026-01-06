import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import bcrypt

load_dotenv() 

# usamos la URL de la base de datos
DATABASE_URL = os.getenv("DB_URL")

# Creamos el motor de SQLAlchemy
engine = create_engine(DATABASE_URL)

# FUNCIONES DEL SISTEMA

def registrar_usuario(nombre, email, password):
    ## 1. Crear el 'hash' de la contraseña
    # Transformamos la contraseña en una cadena de caracteres irreconocible
    bytes_password = password.encode('utf-8')
    salida = bcrypt.gensalt()
    hash_password = bcrypt.hashpw(bytes_password, salida).decode('utf-8')

    query = text("""
            INSERT INTO usuarios (nombre, email, password_hash)
            VALUES (:nombre, :email, :password_hash)
    """)

    try:
        with engine.begin() as conn:
            conn.execute(query, {
                "nombre": nombre,
                "email": email,
                "password_hash": hash_password
            })
            return True

    except Exception as e: 
        print(f"Error en el registro del usuario: {e}")
        return False


def login(email, password):
    query = text("SELECT id, nombre, password_hash from usuarios where email = :email ")

    try:
        with engine.connect() as conn:
            result = conn.execute(query, {"email": email}).fetchone()

            if result:
                user_id, nombre, hash_almacenado = result
                # Convertir el hash string a bytes para la verificación
                hash_bytes = hash_almacenado.encode('utf-8') if isinstance(hash_almacenado, str) else hash_almacenado
                
                if bcrypt.checkpw(password.encode('utf-8'), hash_bytes):
                    return {"id": user_id, "nombre": nombre}  # Login exitoso
                
                return None  # Contraseña incorrecta
            
            return None  # Email no encontrado
    
    except Exception as e:
        print(f"Error al iniciar sesión: {e}")
        return None

def guardar_prediccion(usuario_id, nombre_est, nota, asist, socio, umbral, prob, es_riesgo):
    """Guarda una nueva predicción en Neon usando SQLAlchemy."""
    query = text("""
        INSERT INTO historial_predicciones 
        (usuario_id, nombre_estudiante, nota_promedio, asistencia_porcentaje, 
         nivel_socioeconomico, umbral_decision, probabilidad_riesgo, es_riesgo_alto)
        VALUES (:usuario_id, :nombre_est, :nota, :asist, :socio, :umbral, :prob, :es_riesgo)
    """)
    
    try:
        with engine.begin() as conn: # .begin() hace el commit automáticamente
            conn.execute(query, {
                "usuario_id": usuario_id,
                "nombre_est": nombre_est,
                "nota": nota,
                "asist": asist,
                "socio": socio,
                "umbral": umbral,
                "prob": prob,
                "es_riesgo": es_riesgo
            })
            print(" Predicción guardada exitosamente en Neon.")
    except Exception as e:
        print(f"Error al guardar en la base de datos: {e}") 
