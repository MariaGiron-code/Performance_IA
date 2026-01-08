import streamlit as st
from src.views.auth import vista_login, vista_registro

# 1. Configuración de página (index.html de la app)
st.set_page_config(page_title="EduGuard AI", page_icon="public/logo.png", layout="centered")


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
    # --- VISTA PARA USUARIOS LOGUEADOS (Panel de Control) Dashboard principal ---
  
    try:
        st.sidebar.image("public/logo.png", width=100) 
    except:
        st.sidebar.write("🎓 **EduGuard AI**")
        
    st.sidebar.write(f"Bienvenido, **{st.session_state.user_info['nombre']}**")
    
    opcion = st.sidebar.radio(
        "Navegación", 
        ["Realizar Predicción", "Historial de Alumnos"], 
        key="nav_radio"
    )
    
    st.sidebar.markdown("---")
    if st.sidebar.button("Cerrar Sesión", key="btn_cerrar_sesion"):
        st.session_state.logged_in = False
        st.session_state.auth_mode = "login" # Resetear para el siguiente inicio
        st.rerun()

    # Secciones del sistema según la opción del radio
    if opcion == "Realizar Predicción":
        st.write("## 🔍 Análisis de Riesgo Académico")
        # Aquí llamaremos a la función del formulario más adelante
        st.info("El modelo de IA está listo. Pendiente vincular el formulario de datos.")
        
    elif opcion == "Historial de Alumnos":
        st.write("## 📚 Historial de Predicciones")
        st.write("Consulta aquí los registros previos almacenados en la nube.")