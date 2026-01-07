import streamlit as st
from src.database import login, registrar_usuario

# Carga del estilo CSS 
def local_css(estilo):
    with open(estilo) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
local_css("assets/style.css")


def vista_login():
    
    with st.container():
        st.title(" Iniciar Sesión")
        email = st.text_input("Correo electrónico", key="login_email")
        password = st.text_input("Contraseña", type="password", key="login_password")
        
        if st.button("Entrar", key="btn_login"):
            if not email or not password:
                st.toast(" Por favor, completa todos los campos.")
            else:
                usuario = login(email, password)
                if usuario:
                    st.success(f"¡Bienvenido de nuevo, {usuario['nombre']}!")
                    st.balloons()
                    st.session_state.logged_in = True
                    st.session_state.user_info = usuario
                    st.rerun()
                else:
                    st.error(" Correo o contraseña incorrectos. Inténtalo de nuevo.")

def vista_registro():
    
    with st.container():
        st.title(" Registro de Usuario")
        nombre = st.text_input("Nombre completo", key="reg_nombre")
        email = st.text_input("Correo electrónico", key="reg_email")
        password = st.text_input("Contraseña", type="password", key="reg_password")
        
        if st.button("Registrarme", key="btn_registro"):
            if not nombre or not email or not password:
                st.toast(" Todos los campos son obligatorios para el registro.")
            
            elif "@" not in email:
                st.warning("Por favor, ingresa un correo electrónico válido.")
            
            else:
                if registrar_usuario(nombre, email, password):
                    st.success(" ¡Cuenta creada con éxito! Ahora puedes ir al Login.")
                    st.toast("Usuario registrado correctamente") 
                
                else:
                    st.error(" Error: El correo ya está registrado o hubo un problema con la base de datos.")