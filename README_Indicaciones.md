# EduGuard AI - Predictor de Deserción Estudiantil

Sistema de Inteligencia Artificial para predecir el riesgo de abandono escolar.

## Equipo de Desarrollo (Sprints)

Para avanzar más rápido en el proyecto, se ha dividido en 5 sprints, cada uno será responsable de un Sprint en específico o varios dependiendo de como avancemos.

### Kevin == (Sprint 1 - Desarrollo del Modelo)
* **Responsabilidad:** Preparación de la materia prima del proyecto.
* **Tareas:** * Búsqueda y selección del dataset en Kaggle o otras fuentes o librerias propias de python para obtener los datos.
  * Análisis Exploratorio de Datos (EDA) para entender las variables.
  * Ejecución del script `scripts/limpieza.py` (Manejo de nulos, duplicados y normalización).
  * Selección del algoritmo de IA a utilizar para entrenar el modelo (tener en cuenta el tipo de algoritmos ausar ya que depende del prósito de la app y los tipos de datos y resultados que vayamos a dar).

###  María y Eduardo == (Sprint 2 - Entrenamiento)
* **Responsabilidad:** Transformar los datos en un sistema inteligente funcional.
* **Tareas:** * Codificación del script `scripts/entrenamiento.py`.
  * División de datos en conjuntos de entrenamiento y prueba (Train/Test Split).
  * Evaluación del modelo mediante métricas (Accuracy, Precision, Recall).
  * Exportación del modelo final a la carpeta `models/` en formato `.pkl`.

### María == Integrante 3: Backend (Sprint 3 - Lógica y Base de Datos)
* **Responsabilidad:** Crear el "cerebro" y el sistema de almacenamiento de la App.
* **Tareas:** * Desarrollo de `src/logic.py` para cargar el modelo y procesar las predicciones.
  * Configuración de la base de datos SQL en la nube (Supabase/PostgreSQL).
  * Desarrollo de `src/database.py` para gestionar el historial de consultas.
  * Implementación de validaciones de datos de entrada.

### Josué y Eduardo == Integrante 4: Frontend  (Sprint 4 - Interfaz de Usuario)
* **Responsabilidad:** Crear la experiencia visual y conectar todas las piezas.
* **Tareas:** * Diseño de la interfaz en `app.py` usando Streamlit (Sidebar, Tabs, Formularios).
  * Integración de las funciones de lógica y base de datos en la interfaz.
  * Creación de visualizaciones dinámicas de los resultados.
  * Pruebas de usabilidad y corrección de errores visuales.

**DOCUMENTAR TODO LO QUE VAYAN HACIENDO PARA QUE DESPUÉS SEA MÁS FÁCIL HACER LA DOCUMENTACIÓN GENERAL Y HACER CON TIMEPO CADA PARTE PARA QUE LOS DEMÁS PUEDAN HACER SUS PARTES PORFA** 

*Importante!!!: El **Sprint 5 (Despliegue y Documentación)** será realizado de forma colaborativa por todo el equipo una vez finalizadas las tareas individuales.*

## Cómo ejecutar
1. Crear entorno virtual: `python -m venv venv`
2. Activa el entorno para trabjar: `source venv/bin/activate` (o `venv\Scripts\activate` en Windows)
3. Instalar: `pip install -r requirements.txt`
4. Correr: `streamlit run app.py`