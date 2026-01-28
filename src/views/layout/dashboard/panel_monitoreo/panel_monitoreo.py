import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go

def vista_panel_monitoreo():
    st.markdown('<div class="monitoreo-container">', unsafe_allow_html=True)
    col_icono , col_titulo = st.columns([2, 8])
    
    with col_icono:
        st.image("public/analytics(2).png")
    
    with col_titulo:
        st.title("Tablero de Control y Monitoreo")
        st.write("Visión general del estado de riesgo académico detectado por EduGuard AI.")

    if "user_info" not in st.session_state:
        st.warning("Debes iniciar sesión para ver los datos.")
        return
        
    email = st.session_state.user_info["email"]
    password = st.session_state.user_password

    # --- 1. OBTENCIÓN DE DATOS (API) ---
    with st.spinner("Actualizando métricas en tiempo real..."):
        try:
            response = requests.get("https://eduguard-ai.onrender.com/monitoreo/stats", auth=(email, password))
            
            if response.status_code != 200:
                st.error("No se pudieron cargar los datos del servidor.")
                return
                
            data = response.json()
            
        except Exception as e:
            st.error(f"Error de conexión: {e}")
            return

    # --- 2. TARJETAS DE MÉTRICAS (KPIs) ---
    total = data["total_evaluados"]
    riesgo = data["total_riesgo"]
    seguros = total - riesgo
    tasa = data["tasa_riesgo"]

    col1, col2, col3, col4 = st.columns(4)
    
    col1.metric("Estudiantes Evaluados", total, delta="Total histórico")
    col2.metric("Detectados en Riesgo", riesgo, delta=f"{tasa:.1f}% del total", delta_color="inverse")
    col3.metric("Sin Riesgo", seguros, delta_color="normal")
    col4.metric("Precisión Estimada", "92%", help="Basado en validación del modelo") # Dato estático del modelo

    st.divider()

    # --- 3. GRÁFICOS VISUALES ---
    c1, c2 = st.columns([1, 1])

    with c1:
        st.subheader("Distribución de Riesgo")
        if total > 0:
            # Gráfico de Dona
            labels = ['En Riesgo (Desertor)', 'Sin Riesgo (No Desertor)']
            values = [riesgo, seguros]
            colors = ['#C41A1A', '#172BA3'] # Rojo y Azul
            
            fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.4, marker=dict(colors=colors))])
            fig.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=300)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No hay datos suficientes.")

    with c2:
        st.subheader("Tendencias")
        # Convertimos el historial a DataFrame para facilitar visualización
        historial = data.get("historial", [])
        if historial:
            df_hist = pd.DataFrame(historial)
            st.dataframe(
                df_hist[["nombre", "resultado", "probabilidad"]].style.format({"probabilidad": "{:.2%}"}),
                use_container_width=True,
                height=300,
                hide_index=True
            )
        else:
            st.info("Aún no se han realizado predicciones.")

    st.markdown('</div>', unsafe_allow_html=True)