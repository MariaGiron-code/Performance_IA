import os

import uvicorn

if __name__ == "__main__":
    HOST = "0.0.0.0"  # CONSTANTES DE CONFIGURACIÓN
    PORT = int(os.getenv("PORT", 8000))  # PUERTO POR DEFECTO DEL ENTORNO (8000)
    APP_MODULE = "src.api.main:app"

    # Inicia el servidor Uvicorn deshabilitando la recarga automática para producción.
    # Configura el nivel de logs para garantizar visibilidad en el despliegue.
    uvicorn.run(APP_MODULE, host=HOST, port=PORT, log_level="info")
