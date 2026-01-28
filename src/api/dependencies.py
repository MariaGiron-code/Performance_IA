import os
from typing import Annotated, Generator

from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

# Importaciones internas
from src.database import login

# Se cargan las variables de entorno
load_dotenv()

# Configuración de la BDD
DB_URL = os.getenv("DB_URL")

if not DB_URL:
    raise ValueError("Error Crítico: La variable de entorno 'DB_URL' no está definida.")

# Configuración del motor SQL.
engine = create_engine(DB_URL, pool_pre_ping=True)

# Fábrica de sesiones para las peticiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Crea una petición para la BDD
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Define el tipo para insertar dependencias.
db_dependency = Annotated[Session, Depends(get_db)]

# Seguridad y Autenticación
security = HTTPBasic()


# Valida las credenciales del usuario
def get_current_user(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    user = login(credentials.username, credentials.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales de acceso inválidas",
            headers={"WWW-Authenticate": "Basic"},
        )
    return user


# Define el tipo ingresar al usuario actual
user_dependency = Annotated[dict, Depends(get_current_user)]
