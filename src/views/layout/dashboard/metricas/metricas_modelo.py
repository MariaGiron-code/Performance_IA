import streamlit as st

def vista_metricas_modelo():
    st.write("## Métricas del Modelo")
    st.info("Aquí se mostrarán las métricas de rendimiento del modelo de IA.")
    # Agregar métricas: accuracy, precision, recall, etc.
    st.metric("Accuracy", "85%")
    st.metric("Precision", "82%")
    st.metric("Recall", "78%")