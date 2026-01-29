# 🎓 EduGuard AI: Sistema de Predicción de Deserción Académica

**EduGuard AI** es una solución integral basada en Inteligencia Artificial diseñada para detectar tempranamente el riesgo de deserción
estudiantil. Mediante el uso de modelos de Machine Learning (Random Forest) y una interfaz web interactiva, permitimos a las instituciones
educativas identificar estudiantes en riesgo y tomar medidas preventivas basadas en datos.

---

## 🔗 Enlaces del Proyecto

| Recurso                      | Enlace                                                                                   |
|------------------------------|------------------------------------------------------------------------------------------|
| **🌐 Sistema en Producción** | [Ver Aplicación Web](https://www.google.com/search?q=AQU%C3%8D_TU_ENLACE_AL_SISTEMA_WEB) |
| **📺 Demo en Video**         | [Ver en YouTube](https://www.google.com/search?q=AQU%C3%8D_TU_ENLACE_DE_YOUTUBE)         |
| **📄 Informe Técnico**       | [Ver PDF en Drive](https://www.google.com/search?q=AQU%C3%8D_TU_ENLACE_DE_GOOGLE_DRIVE)  |

---

## 🏛️ Equipo de Desarrollo

Proyecto desarrollado como parte de las actividades académicas en la **Escuela Politécnica Nacional (EPN)**.

* **Girón María Paula**
* **Ganchala Eduardo**
* **Simbaña Alexis**
* **Ortiz Josué**

---

## 🚀 Características del Sistema

El sistema cuenta con una arquitectura moderna dividida en Frontend (Streamlit) y Backend (FastAPI + Base de Datos), ofreciendo las siguientes
funcionalidades:

### 1. 🔐 Autenticación Segura

* Login y Registro de usuarios con validación de credenciales.
* Diseño responsivo y amigable (CSS personalizado).
* Gestión de sesiones seguras.

### 2. 📊 Dashboard de Monitoreo

* Visualización de KPIs en tiempo real (Estudiantes evaluados, Tasa de riesgo).
* Gráficos interactivos de distribución de riesgo.
* Historial de las últimas evaluaciones con indicadores visuales.
* **Optimización:** Implementación de caché (TTL) para evitar saturación de la API.

### 3. 🔮 Módulo de Predicción (Core)

* Formulario intuitivo dividido en tres dimensiones: **Socio-demográfica, Académica y Entorno**.
* **Control de Sensibilidad:** Slider para ajustar el umbral de decisión del modelo (falsos positivos vs. falsos negativos).
* **Explicabilidad (XAI):** Gráficos que muestran qué variables influyeron más en la decisión (e.g., promedio del 1.er semestre, desempleo
  regional).
* Integración directa con Base de Datos para guardar cada predicción.

### 4. 📈 Métricas del Modelo

* Transparencia total sobre el rendimiento del algoritmo.
* Visualización de Matriz de Confusión, Accuracy, Recall y F1-Score.
* Carga optimizada del modelo `.pkl` mediante `st.cache_resource`.

---

## 🛠️ Tecnologías Utilizadas

* **Lenguaje:** Python 3.14+
* **Frontend:** Streamlit, Plotly, CSS3.
* **Backend:** FastAPI (API REST), SQLAlchemy (ORM).
* **Base de Datos:** PostgreSQL / SQLite.
* **Machine Learning:** Scikit-Learn (Random Forest), Joblib, Pandas.

---

## 🌿 Gestión de Ramas y Despliegue

Para este proyecto se ha seguido una estrategia de ramificación específica para asegurar la estabilidad en producción:

* `main`: Rama principal que contiene la base del desarrollo colaborativo del equipo.
* `jossu`: **Rama de Producción y Optimización**.
* Esta rama fue creada a partir de `main` para implementar mejoras de rendimiento críticas.

---

### **Optimizaciones incluidas en esta rama:**

* Refactorización del manejo de conexiones a Base de Datos (SQLAlchemy Transactions).
* Implementación de sistemas de Caché (`st.cache_data`) para reducir latencia.
* Mejoras en la experiencia de usuario (UX) y validaciones de formularios.
* Corrección de rutas relativas para despliegue en la nube.

> **Nota:** La versión desplegada en el enlace de producción corresponde al código estable de la rama `jossu`.

---

## ⚙️ Instalación y Ejecución Local

Si deseas correr este proyecto en tu máquina local:

1. **Clonar el repositorio:**

```bash
git clone https://github.com/MariaGiron-code/Performance_IA.git
cd Performance_IA

```

2. **Crear entorno virtual:**

```bash
python -m venv venv
source venv/bin/activate
venv\Scripts\activate       # En Windows

```

3. **Instalar dependencias:**

```bash
pip install -r requirements.txt

```

4. **Configurar variables de entorno:**
   Crea un archivo `.env` en la raíz y configura la URL del backend:

```env
URL_API_BACKEND=http://localhost:8000
DB_URL="postgresql://usuario:contraseña@localhost:5432/postgres"

```

5. **Ejecutar la aplicación:**

```bash
streamlit run src/main.py

```

---

© 2026 - Escuela Politécnica Nacional - Fundamentos de Inteligencia Artificial

