from pathlib import Path  # Cargar rutas

import streamlit as st

from src.views.auth.auth import vista_login, vista_registro
from src.views.layout.dashboard.dashboard import vista_dashboard


def setup_assets():
    # Carga la ruta CSS mediante la librería para evitar conflictos con diferentes SO.
    css_path = Path("assets/css/dashboard.css")

    if css_path.exists():
        with open(css_path, encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # Importa dependencias de iconos externos.
    st.markdown(
        '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">',
        unsafe_allow_html=True,
    )


def initialize_session():
    # Setea los valores iniciales de un usuario.
    defaults = {"logged_in": False, "auth_mode": "login"}
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


# Define el comportamiento de la ventana al arrancar (y mostrarse en el navegador).
st.set_page_config(
    page_title="EduGuard AI",
    page_icon="public/logo.png",
    layout="centered",
    initial_sidebar_state="collapsed",
)

setup_assets()
initialize_session()

# Determina qué vista renderizar basándose en el estado de autenticación.
if not st.session_state.logged_in:
    # Cambio entre la ventana de registro / inicio de sesión.
    if st.session_state.auth_mode == "login":
        vista_login()
    else:
        vista_registro()
else:
    # Despliega el panel principal tras una autenticación exitosa.
    vista_dashboard()
