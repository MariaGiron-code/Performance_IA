# Este script es el punto de entrada para ejecutar la API de FastAPI.
# Utiliza uvicorn para servir la aplicación definida en src.api.main:app.
# Configurado para despliegue en Render con puerto dinámico.

import os
import uvicorn

if __name__ == "__main__":
    # Puerto dinámico para Render (usa 8000 por defecto en local)
    port = int(os.environ.get("PORT", 8000))

    # Ejecutar la aplicación FastAPI con uvicorn
    # - app: "src.api.main:app" apunta al módulo y la instancia de FastAPI
    # - host="0.0.0.0": Escucha en todas las interfaces
    # - port: Puerto dinámico de Render
    # - reload=False: No recarga automática en producción
    uvicorn.run("src.api.main:app", host="0.0.0.0", port=port, reload=False)

## DESPUES DE ACABBAR TODO EL DESARROLLOR DE APP SE VA HACER EL DESPLIGUE DE LA API DEL MODELO Y LA APP DE STREAMLIT 
# POR EL MOMENTO LO EJECTAN EN EL LOCAL 
