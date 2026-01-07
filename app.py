import streamlit as st
from src.interface import vista_login, vista_registro

# 1. Configuración de página (Página de inicio) como el index.html de una web
st.set_page_config(page_title="EduGuard AI", layout="centered")

# 2. Inicializar el estado de la sesión si no existe
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# 3. Lógica de Navegación Principal
if not st.session_state.logged_in:
    # Menú lateral para usuarios no autenticados
    menu = st.sidebar.selectbox("Selecciona una opción", ["Iniciar Sesión", "Registro"], key="menu_navegacion_principal")
    
    if menu == "Iniciar Sesión":
        vista_login()
    else:
        vista_registro()
else:
    
    # --- VISTA PARA USUARIOS LOGUEADOS ---
    st.sidebar.image("assets/logo.png", width=100) 
    st.sidebar.write(f"Bienvenido, **{st.session_state.user_info['nombre']}**")
    
    opcion = st.sidebar.radio("Navegación", ["Realizar Predicción", "Historial de Alumnos"], key="nav_radio")
    
    if st.sidebar.button("Cerrar Sesión", key="btn_cerrar_sesion"):
        st.session_state.logged_in = False
        st.rerun()

    # Secciones del sistema
    if opcion == "Realizar Predicción":
        st.write("## Análisis de Riesgo Académico")
        # Aquí llamaremos a la función que diseñaremos a continuación
        st.info("Próximamente: Formulario de predicción basado en el dataset.")
        
    elif opcion == "Historial de Alumnos":
        st.write("## Historial de Predicciones")
        st.write("Aquí se mostrarán los datos guardados en Neon.")