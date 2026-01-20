# Este script es el punto de entrada para ejecutar la API de FastAPI.
# Utiliza uvicorn para servir la aplicación definida en src.api.main:app.
# Ejecuta el servidor en modo reload para desarrollo, permitiendo recargas automáticas al cambiar el código.
# Para producción, quita reload=True y ajusta host/port según necesites.

import uvicorn

if __name__ == "__main__":
    # Ejecutar la aplicación FastAPI con uvicorn
    # - app: "src.api.main:app" apunta al módulo y la instancia de FastAPI
    # - host="0.0.0.0": Escucha en todas las interfaces (accesible desde otros dispositivos en la red)
    # - port=8000: Puerto por defecto para FastAPI
    # - reload=True: Recarga automática en desarrollo al detectar cambios en el código
    uvicorn.run("src.api.main:app", host="0.0.0.0", port=8000, reload=True)

## DESPUES DE ACABBAR TODO EL DESARROLLOR DE APP SE VA HACER EL DESPLIGUE DE LA API DEL MODELO Y LA APP DE STREAMLIT 
# POR EL MOMENTO LO EJECTAN EN EL LOCAL 
