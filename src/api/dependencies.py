from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import os
from dotenv import load_dotenv
from src.database import login  # Reutilizar función de login para autenticación
from src.logic import ejecutar_prediccion  # Reutilizar función de predicción

# Archivo de dependencias para FastAPI: carga de base de datos y autenticación
# Dedicado a inyección de datos y dependencias comunes
load_dotenv()

DATABASE_URL = os.getenv("DB_URL")

# Crear el motor de SQLAlchemy
engine = create_engine(DATABASE_URL)

# Crear SessionLocal para dependencias
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependencia para obtener la sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Instancia de HTTPBasic para autenticación
security = HTTPBasic()

# Dependencia para obtener el usuario actual autenticado
def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    user = login(credentials.username, credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
            headers={"WWW-Authenticate": "Basic"},
        )
    return user 