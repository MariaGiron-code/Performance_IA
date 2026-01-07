import streamlit as st
from src.database import login, registrar_usuario

# Carga del estilo CSS 
def local_css(estilo):
    with open(estilo) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
local_css("assets/style.css")

# Configuración inicial de la página 
st.set_page_config(page_title="EduGuard AI", layout="centered")

def vista_login():
    
    with st.container():
        st.title("🔑 Iniciar Sesión")
        email = st.text_input("Correo electrónico")
        password = st.text_input("Contraseña", type="password")
        
        if st.button("Entrar"):
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
        st.title("📝 Registro de Usuario")
        nombre = st.text_input("Nombre completo")
        email = st.text_input("Correo electrónico")
        password = st.text_input("Contraseña", type="password")
        
        if st.button("Registrarme"):
            if not nombre or not email or not password:
                st.error(" Todos los campos son obligatorios para el registro.")
            
            elif "@" not in email:
                st.warning("Por favor, ingresa un correo electrónico válido.")
            
            else:
                if registrar_usuario(nombre, email, password):
                    st.success(" ¡Cuenta creada con éxito! Ahora puedes ir al Login.")
                    st.toast("Usuario registrado correctamente") 
                
                else:
                    st.error(" Error: El correo ya está registrado o hubo un problema con la base de datos.")

# --- LÓGICA DE NAVEGACIÓN ---

if "logged_in" not in st.session_state: # Si no hay sesión iniciada, se inicia la sesión
    st.session_state.logged_in = False

if not st.session_state.logged_in: # Si no hay sesión iniciada, se muestra el menú de inicio de sesión y registro
    menu = st.sidebar.selectbox("Selecciona una opción", ["Iniciar Sesión", "Registro"])
    if menu == "Iniciar Sesión":
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