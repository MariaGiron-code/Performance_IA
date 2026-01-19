import streamlit as st

def vista_panel_monitoreo():
    st.write("## Panel de Monitoreo")
    st.info("Aquí se mostrará el panel de monitoreo del sistema.")
    # Agregar contenido: métricas generales, gráficos de uso, etc.
    st.metric("Usuarios Activos", 150)
    st.metric("Predicciones Hoy", 25)