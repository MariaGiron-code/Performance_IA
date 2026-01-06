import streamlit as st
from src.database import login, registrar_usuario

# Configuración inicial de la página 
st.set_page_config(page_title="EduGuard AI", layout="centered")

def vista_login():
    st.title("🔑 Iniciar Sesión")
    email = st.text_input("Correo electrónico")
    password = st.text_input("Contraseña", type="password")
    
    if st.button("Entrar"):
        usuario = login(email, password)
        if usuario:
            st.session_state.logged_in = True
            st.session_state.user_info = usuario
            st.rerun() # Recarga la app para entrar 
        else:
            st.error("Credenciales incorrectas")

def vista_registro():
    st.title("📝 Registro de Usuario")
    nombre = st.text_input("Nombre completo")
    email = st.text_input("Correo electrónico")
    password = st.text_input("Contraseña", type="password")
    
    if st.button("Registrarme"):
        if registrar_usuario(nombre, email, password):
            st.success("¡Cuenta creada! Ya puedes iniciar sesión.")
        else:
            st.error("Error al registrar. El email podría ya estar en uso.")

# --- LÓGICA DE NAVEGACIÓN ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    menu = st.sidebar.selectbox("Selecciona una opción", ["Login", "Registro"])
    if menu == "Login":
        vista_login()
    else:
        vista_registro()
else:
    st.sidebar.write(f"Bienvenido, **{st.session_state.user_info['nombre']}**")
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state.logged_in = False
        st.rerun()
    
    # Aquí irán las otras secciones (Predicción e Historial)
    st.write("### ¡Ya estás dentro del sistema!")