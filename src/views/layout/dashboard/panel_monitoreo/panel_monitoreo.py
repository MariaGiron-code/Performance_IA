import streamlit as st

def vista_panel_monitoreo():
    st.write("## Panel de Monitoreo")
    st.info("Aquí se mostrará el panel de monitoreo del sistema.")
    # Agregar contenido: estadísticas generales del sistema, gráficos de uso, etc.
    st.metric("predicciones de riesgo alto", 5)
    st.metric("predicciones de riesgo alto", 20)
    st.metric("Predicciones Hoy", 25)