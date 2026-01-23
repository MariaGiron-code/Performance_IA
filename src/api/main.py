# Este archivo configura la aplicación principal de FastAPI para la API de predicción de deserción académica.
# Incluye el router de rutas, configura CORS para permitir conexiones desde el frontend de Streamlit,
# y define el punto de entrada para ejecutar el servidor.
# CORS es necesario porque Streamlit (frontend) corre en un puerto diferente (ej. 8501) al de FastAPI (ej. 8000),
# y permite requests cross-origin desde el navegador.

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import router

# Crear la instancia de la aplicación FastAPI
app = FastAPI(
    title="API de Predicción de Deserción Académica",
    description="API REST para realizar predicciones de riesgo de deserción usando un modelo de ML, integrada con Streamlit.",
    version="1.0.0"
)

# Configurar CORS para permitir conexiones desde el frontend de Streamlit
# Esto es esencial para que el frontend (Streamlit en localhost:8501) pueda hacer requests a la API (localhost:8000)
# Sin CORS, el navegador bloquearía las requests por política de same-origin.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],  # Origen del frontend de Streamlit (ajusta si cambias el puerto)
    allow_credentials=True,  # Permitir cookies/credenciales si se usan en el futuro
    allow_methods=["*"],  # Permitir todos los métodos HTTP (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los headers
)

# Incluir el router con todos los endpoints definidos en routes.py
app.include_router(router)

# Punto de entrada para ejecutar el servidor con uvicorn (si se ejecuta directamente)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)