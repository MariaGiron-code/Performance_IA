import os
import time
from pathlib import Path

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
API_BASE_URL = os.getenv("URL_API_BACKEND", "http://localhost:8000")

# Gestión de Rutas
BASE_DIR = Path(__file__).parent.parent.parent.parent
CSS_PATH = BASE_DIR / "public" / "css" / "auth.css"


def local_css(file_path):
    try:
        with open(file_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning(f"No se encontró el archivo de estilos en: {file_path}")


# Se carga el CSS usando la ruta absoluta calculada
local_css(CSS_PATH)


def vista_login():
    col_logo, col_form = st.columns([1, 1], gap="large")

    with col_logo:
        st.markdown('<div class="login-logo-section">', unsafe_allow_html=True)
        st.image("public/logo_app_name.png", width="stretch")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_form:
        st.markdown('<div class="login-form-section">', unsafe_allow_html=True)
        st.markdown(
            '<h1 class="form-title">Iniciar Sesión</h1>', unsafe_allow_html=True
        )
        st.markdown(
            '<p class="form-subtitle">Ingresa tus credenciales para acceder al sistema</p>',
            unsafe_allow_html=True,
        )

        with st.form("login_form"):
            email = st.text_input(
                "Correo electrónico",
                placeholder="correo@ejemplo.com",
                key="login_email",
            )
            password = st.text_input(
                "Contraseña", type="password", key="login_password"
            )

            st.markdown('<div class="main-button">', unsafe_allow_html=True)
            submit_login = st.form_submit_button("Iniciar Sesión", width="stretch")
            st.markdown("</div>", unsafe_allow_html=True)

        if submit_login:
            if not email or not password:
                st.toast("Por favor, completa todos los campos.")
            else:
                try:
                    response = requests.get(
                        f"{API_BASE_URL}/users/me", auth=(email, password)
                    )

                    if response.status_code == 200:
                        user_data = response.json()
                        st.session_state.logged_in = True
                        st.session_state.user_info = {
                            "id": user_data["id"],
                            "nombre": user_data["username"],
                            "email": user_data["email"],
                        }
                        st.session_state.user_password = password
                        st.rerun()
                    else:
                        st.error("Credenciales incorrectas o error en el servidor.")
                except requests.exceptions.RequestException as e:
                    st.error(f"Error de conexión: {e}")

        # Navegación (fuera del form)
        st.markdown('<div class="nav-link">', unsafe_allow_html=True)
        st.markdown("¿No tienes cuenta? ", unsafe_allow_html=True)
        if st.button("Regístrate aquí", key="btn_to_registro"):
            st.session_state.auth_mode = "registro"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)


def vista_registro():
    col_logo, col_form = st.columns([1, 1], gap="large")

    with col_logo:
        st.markdown('<div class="registro-logo-section">', unsafe_allow_html=True)
        st.image("public/logo_app_name.png", width="stretch")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_form:
        st.markdown('<div class="registro-form-section">', unsafe_allow_html=True)
        st.markdown('<h1 class="form-title">Crear Cuenta</h1>', unsafe_allow_html=True)
        st.markdown(
            '<p class="form-subtitle">Completa el formulario para registrarte</p>',
            unsafe_allow_html=True,
        )

        with st.form("register_form"):
            nombre = st.text_input(
                "Nombre completo", placeholder="Juan Pérez", key="reg_nombre"
            )
            email = st.text_input(
                "Correo electrónico", placeholder="correo@ejemplo.com", key="reg_email"
            )
            password = st.text_input("Contraseña", type="password", key="reg_password")

            st.markdown('<div class="main-button">', unsafe_allow_html=True)
            submit_registro = st.form_submit_button("Registrarse", width="stretch")
            st.markdown("</div>", unsafe_allow_html=True)

        if submit_registro:
            if not nombre or not email or not password:
                st.error("Todos los campos son obligatorios.")
            elif "@" not in email:
                st.warning("Correo electrónico inválido.")
            else:
                try:
                    payload = {"username": nombre, "email": email, "password": password}
                    response = requests.post(f"{API_BASE_URL}/users", json=payload)

                    # 200 (OK) y 201 (Created)
                    if response.status_code in [200, 201]:
                        st.success("¡Cuenta creada con éxito!")
                        st.toast("Redirigiendo al inicio de sesión...", icon="✅")
                        time.sleep(2)
                        st.session_state.auth_mode = "login"
                        st.rerun()
                    else:
                        try:
                            error_detail = response.json().get(
                                "detail", "Error desconocido"
                            )
                        except:
                            # Si falla el parseo JSON (ej. error 500 html)
                            error_detail = f"Error {response.status_code}"
                        st.error(f"No se pudo crear la cuenta: {error_detail}")

                except requests.exceptions.RequestException as e:
                    st.error(f"Error conectando a la API: {e}")

        # Navegación
        st.markdown('<div class="nav-link">', unsafe_allow_html=True)
        st.markdown("¿Ya tienes cuenta? ", unsafe_allow_html=True)
        if st.button("Inicia sesión", key="btn_to_login"):
            st.session_state.auth_mode = "login"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
