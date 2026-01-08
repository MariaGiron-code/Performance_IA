import streamlit as st

# Carga del estilo CSS para el dashboard
def local_css(estilo):
    with open(estilo) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def vista_dashboard():
    # Cargar CSS del dashboard
    local_css("assets/css/dashboard.css")

    