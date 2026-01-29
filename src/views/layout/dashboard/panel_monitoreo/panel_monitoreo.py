import os
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import requests
import streamlit as st
from dotenv import load_dotenv

# Configuración Inicial
load_dotenv()
API_BASE_URL = os.getenv("URL_API_BACKEND", "http://localhost:8000")

# Gestión de rutas para imágenes
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent
ICONO_PATH = BASE_DIR / "public" / "analytics(2).png"


# Función de Carga de Datos con Caché
@st.cache_data(ttl=60, show_spinner="Sincronizando con el servidor...")
def obtener_metricas(api_url, auth_tuple):
    try:
        response = requests.get(
            f"{api_url}/monitoreo/stats", auth=auth_tuple, timeout=5
        )
        if response.status_code == 200:
            return response.json()
        return None
    except requests.exceptions.RequestException:
        return None


def vista_panel_monitoreo():
    st.markdown('<div class="monitoreo-container">', unsafe_allow_html=True)

    # ENCABEZADO
    col_icono, col_titulo = st.columns([1, 10])
    with col_icono:
        if ICONO_PATH.exists():
            st.image(str(ICONO_PATH), width=60)
        else:
            st.write("📊")

    with col_titulo:
        st.title("Tablero de Control")
        st.markdown(
            "Monitor de riesgo académico en tiempo real • **Actualización automática cada 60s**"
        )

    # Validación de sesión
    if "user_info" not in st.session_state or "user_password" not in st.session_state:
        st.error("⚠️ Sesión no válida. Por favor reinicia sesión.")
        return

    email = st.session_state.user_info["email"]
    password = st.session_state.user_password

    # OBTENCIÓN DE DATOS
    data = obtener_metricas(API_BASE_URL, (email, password))

    if not data:
        st.error(
            "No se pudo conectar con el servidor de análisis. Verifica tu conexión."
        )
        return

    # TARJETAS DE MÉTRICAS (KPIs)
    total = data.get("total_evaluados", 0)
    riesgo = data.get("total_riesgo", 0)
    seguros = total - riesgo
    tasa = data.get("tasa_riesgo", 0.0)

    # Estilo visual de tarjetas
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    kpi1.metric("Estudiantes Evaluados", total, help="Total histórico de predicciones")
    kpi2.metric(
        "Alerta de Deserción",
        riesgo,
        delta=f"{tasa:.1f}% Tasa Riesgo",
        delta_color="inverse",
        help="Estudiantes marcados como posibles desertores",
    )
    kpi3.metric("Estudiantes Seguros", seguros, delta="Bajo Riesgo")
    kpi4.metric(
        "Precisión del Modelo",
        "92%",
        help="Métrica estática basada en validación cruzada",
    )

    st.markdown("---")

    # VISUALIZACIÓN GRÁFICA
    c_grafico, c_tabla = st.columns([2, 3], gap="medium")

    with c_grafico:
        st.subheader("Distribución de Riesgo")
        if total > 0:
            labels = ["Alto Riesgo (Desertor)", "Bajo Riesgo (Retenido)"]
            values = [riesgo, seguros]
            colors = ["#EF4444", "#3B82F6"]

            fig = go.Figure(
                data=[
                    go.Pie(
                        labels=labels,
                        values=values,
                        hole=0.5,
                        marker=dict(colors=colors),
                        textinfo="percent+label",
                        textposition="inside",
                        showlegend=False,
                    )
                ]
            )
            fig.update_layout(margin=dict(t=20, b=20, l=20, r=20), height=300)
            st.plotly_chart(fig)
        else:
            st.info("Esperando datos para generar gráficos...")

    with c_tabla:
        st.subheader("Últimas Evaluaciones")
        historial = data.get("historial", [])

        if historial:
            df_hist = pd.DataFrame(historial)

            if "nombre_estudiante" in df_hist.columns:
                df_hist = df_hist.rename(
                    columns={
                        "nombre_estudiante": "Estudiante",
                        "resultado_ia": "Diagnóstico",
                        "probabilidad": "Riesgo",
                    }
                )
            elif "nombre" in df_hist.columns:
                df_hist = df_hist.rename(
                    columns={
                        "nombre": "Estudiante",
                        "resultado": "Diagnóstico",
                        "probabilidad": "Riesgo",
                    }
                )

            # Configuración avanzada de la tabla
            st.dataframe(
                df_hist[["Estudiante", "Diagnóstico", "Riesgo"]].head(10),
                height=300,
                hide_index=True,
                column_config={
                    "Riesgo": st.column_config.ProgressColumn(
                        "Nivel de Riesgo",
                        format="%.2f",
                        min_value=0,
                        max_value=1,
                    ),
                    "Diagnóstico": st.column_config.TextColumn(
                        "Predicción IA", width="medium"
                    ),
                },
            )
        else:
            st.info("No hay historial reciente.")
            st.markdown("Ve a **'Nueva Predicción'** para comenzar.")

    st.markdown("</div>", unsafe_allow_html=True)
