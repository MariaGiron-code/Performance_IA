import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routes import router

# Configuración de la Aplicación
app = FastAPI(
    title="EduGuard AI API",
    description="API REST para la predicción de deserción académica utilizando modelos de Machine Learning.",
    version="1.0.0",
)

# Configuración de CORS
origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:8501").split(",")

# Middleware de CORS para permitir que el frontend se comunique con la API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Lista de URLs permitidas (Frontend).
    allow_credentials=True,  # Permite el uso de cookies/autenticación.
    allow_methods=["*"],  # Permite todos los verbos HTTP (GET, POST, etc.).
    allow_headers=["*"],  # Permite todos los encabezados.
)

# Rutas y Endpoints
app.include_router(router)


# Endpoint de verificación de estado (Health Check).
@app.get("/", tags=["Estado"])
async def health_check():
    """Retorna el estado operativo del servicio."""
    return {"status": "online", "service": "EduGuard AI API"}
