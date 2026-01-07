import streamlit as st
from src.database import login, registrar_usuario

# Carga del estilo CSS 
def local_css(estilo):
    with open(estilo) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
local_css("assets/style.css")


def vista_login():
    # Contenedor principal con estilo de tarjeta
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Logo usando la imagen logo_app_name.png
    st.markdown('<div class="logo-container">', unsafe_allow_html=True)
    st.image("public/logo_app_name.png", width=200)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Título y subtítulo
    st.markdown('<h1 class="form-title">Iniciar Sesión</h1>', unsafe_allow_html=True)
    st.markdown('<p class="form-subtitle">Ingresa tus credenciales para acceder al sistema</p>', unsafe_allow_html=True)
    
    # Campos de entrada
    email = st.text_input("Correo electrónico", placeholder="correo@ejemplo.com", key="login_email")
    password = st.text_input("Contraseña", type="password", key="login_password")
    
    # Botón de login
    if st.button("Iniciar Sesión", use_container_width=True, key="btn_login"):
        if not email or not password:
            st.toast("Por favor, completa todos los campos.")
        else:
            usuario = login(email, password)
            if usuario:
                st.session_state.logged_in = True
                st.session_state.user_info = usuario
                st.rerun()
            else:
                st.error("Credenciales incorrectas.")

    # Link de navegación al registro
    st.markdown('<div class="nav-link">', unsafe_allow_html=True)
    st.markdown('¿No tienes cuenta? ', unsafe_allow_html=True)
    if st.button("Regístrate aquí", key="btn_to_registro"):
        st.session_state.auth_mode = "registro"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def vista_registro():
    # Contenedor principal con estilo de tarjeta
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Logo usando la imagen logo_app_name.png
    st.markdown('<div class="logo-container">', unsafe_allow_html=True)
    st.image("public/logo_app_name.png", width=200)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Título y subtítulo
    st.markdown('<h1 class="form-title">Crear Cuenta</h1>', unsafe_allow_html=True)
    st.markdown('<p class="form-subtitle">Completa el formulario para registrarte</p>', unsafe_allow_html=True)
    
    # Campos de entrada
    nombre = st.text_input("Nombre completo", placeholder="Juan Pérez", key="reg_nombre")
    email = st.text_input("Correo electrónico", placeholder="correo@ejemplo.com", key="reg_email")
    password = st.text_input("Contraseña", type="password", key="reg_password")
    
    # Botón de registro
    if st.button("Registrarse", use_container_width=True, key="btn_registro"):
        if not nombre or not email or not password:
            st.error("Todos los campos son obligatorios para el registro.")
        
        elif "@" not in email:
            st.warning("Por favor, ingresa un correo electrónico válido.")
        
        else:
            if registrar_usuario(nombre, email, password):
                st.success("¡Cuenta creada con éxito! Ahora puedes ir al Login.")
                st.toast("Usuario registrado correctamente") 
            
            else:
                st.error("Error: El correo ya está registrado o hubo un problema con la base de datos.")
    
    # Link de navegación al login
    st.markdown('<div class="nav-link">', unsafe_allow_html=True)
    st.markdown('¿Ya tienes cuenta? ', unsafe_allow_html=True)
    if st.button("Inicia sesión", key="btn_to_login"):
        st.session_state.auth_mode = "login"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)