import streamlit as st
import requests  # Para consumir la API
import os
from dotenv import load_dotenv

load_dotenv()
API_BASE_URL = os.getenv("URL_API_BACKEND", "http://localhost:8000")

# Carga del estilo CSS 
def local_css(estilo):
    with open(estilo) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
local_css("assets/css/auth.css")


def vista_login():
    # Layout de dos columnas: logo izquierda, formulario derecha
    col_logo, col_form = st.columns([1, 1], gap="large")
    
    # Columna izquierda: Logo
    with col_logo:
        st.markdown('<div class="login-logo-section">', unsafe_allow_html=True)
        st.image("public/logo_app_name.png", width=1000)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Columna derecha: Formulario
    with col_form:
        st.markdown('<div class="login-form-section">', unsafe_allow_html=True)
        
        # Título y subtítulo
        st.markdown('<h1 class="form-title">Iniciar Sesión</h1>', unsafe_allow_html=True)
        st.markdown('<p class="form-subtitle">Ingresa tus credenciales para acceder al sistema</p>', unsafe_allow_html=True)
        
        # Campos de entrada
        email = st.text_input("Correo electrónico", placeholder="correo@ejemplo.com", key="login_email")
        password = st.text_input("Contraseña", type="password", key="login_password")
        
        # Botón de login
        st.markdown('<div class="main-button">', unsafe_allow_html=True)
        if st.button("Iniciar Sesión", use_container_width=True, key="btn_login"):
            if not email or not password:
                st.toast("Por favor, completa todos los campos.")
            else:
                try:
                    # Consumir la API para login
                    response = requests.get(f"{API_BASE_URL}/users/me", auth=(email, password))
                    if response.status_code == 200:
                        user_data = response.json()
                        st.session_state.logged_in = True
                        st.session_state.user_info = {
                            "id": user_data["id"],
                            "nombre": user_data["username"],  # Ajustar si es necesario
                            "email": user_data["email"]
                        }
                        st.session_state.user_password = password  # Almacenar contraseña para llamadas API
                        st.rerun()
                    else:
                        st.error("Credenciales incorrectas. Intenta de nuevo.")
                except requests.exceptions.RequestException as e:
                    st.error(f"Error conectando a la API: {e}")
        st.markdown('</div>', unsafe_allow_html=True)

        # Link de navegación al registro
        st.markdown('<div class="nav-link">', unsafe_allow_html=True)
        st.markdown('¿No tienes cuenta? ', unsafe_allow_html=True)
        if st.button("Regístrate aquí", key="btn_to_registro"):
            st.session_state.auth_mode = "registro"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

def vista_registro():
    # Layout de dos columnas: logo izquierda, formulario derecha
    col_logo, col_form = st.columns([1, 1], gap="large")
    
    # Columna izquierda: Logo
    with col_logo:
        st.markdown('<div class="registro-logo-section">', unsafe_allow_html=True)
        st.image("public/logo_app_name.png", width=1000)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Columna derecha: Formulario
    with col_form:
        st.markdown('<div class="registro-form-section">', unsafe_allow_html=True)
        
        # Título y subtítulo
        st.markdown('<h1 class="form-title">Crear Cuenta</h1>', unsafe_allow_html=True)
        st.markdown('<p class="form-subtitle">Completa el formulario para registrarte</p>', unsafe_allow_html=True)
        
        # Campos de entrada
        nombre = st.text_input("Nombre completo", placeholder="Juan Pérez", key="reg_nombre")
        email = st.text_input("Correo electrónico", placeholder="correo@ejemplo.com", key="reg_email")
        password = st.text_input("Contraseña", type="password", key="reg_password")
        
        # Botón de registro
        st.markdown('<div class="main-button">', unsafe_allow_html=True)
        if st.button("Registrarse", use_container_width=True, key="btn_registro"):
            if not nombre or not email or not password:
                st.error("Todos los campos son obligatorios para el registro.")

            elif "@" not in email:
                st.warning("Por favor, ingresa un correo electrónico válido.")

            else:
                try:
                    # Consumir la API para registro
                    payload = {
                        "username": nombre,  # Usar nombre como username
                        "email": email,
                        "password": password
                    }
                    response = requests.post(f"{API_BASE_URL}/users", json=payload)
                    if response.status_code == 200:
                        # Verificar si es respuesta de éxito
                        response_data = response.json()
                        if "message" in response_data and "Usuario creado" in response_data["message"]:
                            st.success("¡Cuenta creada con éxito! Ahora puedes iniciar sesión.")
                            st.toast("Usuario registrado correctamente")
                        else:
                            st.error(f"Respuesta inesperada: {response_data}")
                    else:
                        error_detail = response.json().get("detail", "Error desconocido")
                        st.error(f"Error en el registro: {error_detail}")
                except requests.exceptions.RequestException as e:
                    st.error(f"Error conectando a la API: {e}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Link de navegación al login
        st.markdown('<div class="nav-link">', unsafe_allow_html=True)
        st.markdown('¿Ya tienes cuenta? ', unsafe_allow_html=True)
        if st.button("Inicia sesión", key="btn_to_login"):
            st.session_state.auth_mode = "login"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)