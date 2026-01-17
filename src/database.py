import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import bcrypt
import json 

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
    query = text("SELECT id, nombre, email, password_hash from usuarios where email = :email ")

    try:
        with engine.connect() as conn:
            result = conn.execute(query, {"email": email}).fetchone()

            if result:
                user_id, nombre, user_email, hash_almacenado = result
                # Convertir el hash string a bytes para la verificación
                hash_bytes = hash_almacenado.encode('utf-8') if isinstance(hash_almacenado, str) else hash_almacenado

                if bcrypt.checkpw(password.encode('utf-8'), hash_bytes):
                    return {"id": user_id, "nombre": nombre, "email": user_email}  # Login exitoso

                return None  # Contraseña incorrecta

            return None  # Email no encontrado

    except Exception as e:
        print(f"Error al iniciar sesión: {e}")
        return None

def cambiar_contraseña(email, contraseña_actual, nueva_contraseña):
    """Cambia la contraseña del usuario verificando la actual."""
    # Primero, obtener el hash actual
    query_select = text("SELECT password_hash FROM usuarios WHERE email = :email")

    try:
        with engine.connect() as conn:
            result = conn.execute(query_select, {"email": email}).fetchone()

            if result:
                hash_almacenado = result[0]
                # Verificar la contraseña actual
                if bcrypt.checkpw(contraseña_actual.encode('utf-8'), hash_almacenado.encode('utf-8')):
                    # Hashear la nueva contraseña
                    bytes_nueva = nueva_contraseña.encode('utf-8')
                    salida = bcrypt.gensalt()
                    nuevo_hash = bcrypt.hashpw(bytes_nueva, salida).decode('utf-8')

                    # Actualizar en la base de datos
                    query_update = text("UPDATE usuarios SET password_hash = :nuevo_hash WHERE email = :email")
                    with engine.begin() as conn_update:
                        conn_update.execute(query_update, {"nuevo_hash": nuevo_hash, "email": email})
                    return True  # Cambio exitoso
                else:
                    return False  # Contraseña actual incorrecta
            else:
                return False  # Usuario no encontrado

    except Exception as e:
        print(f"Error al cambiar contraseña: {e}")
        return False


# Guardar historial de predicciones
def guardar_prediccion(usuario_id, nombre_est, datos_dict, prob, resultado, umbral):
    """
    Guarda la predicción en la Base de datos. 
    'datos_dict' contiene las 26 variables enviadas al modelo.
    """
    query = text("""
        INSERT INTO historial_predicciones 
        (usuario_id, nombre_estudiante, datos_entrada, probabilidad, resultado_ia, umbral_usado)
        VALUES (:usuario_id, :nombre_est, :datos_json, :prob, :res, :umbral)
    """)
    
    try:
        # Convertimos el diccionario de Python a una cadena JSON para Postgres
        datos_json = json.dumps(datos_dict)
        
        with engine.begin() as conn:
            conn.execute(query, {
                "usuario_id": usuario_id,
                "nombre_est": nombre_est,
                "datos_json": datos_json,
                "prob": prob,
                "res": resultado,
                "umbral": umbral
            })
            return True
    except Exception as e:
        print(f"Error al guardar historial: {e}")
        return False