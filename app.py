import streamlit as st
from src.views.auth import vista_login, vista_registro
from src.views.dashboard import vista_dashboard

# 1. Configuración de página (index.html de la app)
st.set_page_config(page_title="EduGuard AI", page_icon="public/logo.png", layout="centered")

# Cargar Font Awesome para iconos
st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">', unsafe_allow_html=True)

# 2. Inicializar el estado de la sesión
# 'logged_in' controla si el usuario entró al sistema
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# 'auth_mode' controla si mostramos Login o Registro (Navegación interna)
if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "login"

# 3. Lógica de Navegación Principal
if not st.session_state.logged_in:
    
    # Dependiendo de auth_mode, llamamos a una vista o la otra
    if st.session_state.auth_mode == "login":
        vista_login()
    else:
        vista_registro()

else:
    # Usuario logueado - Mostrar dashboard
    vista_dashboard()
