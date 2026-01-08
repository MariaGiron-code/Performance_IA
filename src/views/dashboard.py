import streamlit as st
from src.database import cambiar_contraseña

# Carga del estilo CSS para el dashboard
def local_css(estilo):
    with open(estilo) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


def vista_dashboard():
    # Cargar CSS del dashboard
    local_css("assets/css/dashboard.css")

    # --- VISTA PARA USUARIOS LOGUEADOS (Panel de Control) Dashboard principal ---
    
    try:
        st.sidebar.image("public/logo.png", width=100) 
    except:
        st.sidebar.write("🎓 **EduGuard AI**")
        
    st.sidebar.write(f"Bienvenido, **{st.session_state.user_info['nombre']}**")
    
    opcion = st.sidebar.radio(
        "Navegación",
        ["Realizar Predicción", "Historial de Alumnos", "Cambiar Contraseña"],
        key="nav_radio"
    )
    
    st.sidebar.markdown("---")
    if st.sidebar.button("Cerrar Sesión", key="btn_cerrar_sesion"):
        st.session_state.logged_in = False
        st.session_state.auth_mode = "login" # Resetear para el siguiente inicio
        st.rerun()

    # Secciones del sistema según la opción del radio
    if opcion == "Realizar Predicción":
        st.write("## Análisis de Riesgo Académico")
        # Aquí llamaremos a la función del formulario más adelante
        st.info("El modelo de IA está listo. Pendiente vincular el formulario de datos.")
        
    elif opcion == "Historial de Alumnos":
        st.write("## Historial de Predicciones")
        st.write("Consulta aquí los registros previos almacenados en la nube.")

    elif opcion == "Cambiar Contraseña":
        st.write("## 🔒 Cambiar Contraseña")

        # Formulario de cambio de contraseña
        with st.form("form_cambiar_contraseña"):
            contraseña_actual = st.text_input("Contraseña actual", type="password", key="current_password")
            nueva_contraseña = st.text_input("Nueva contraseña", type="password", key="new_password")
            confirmar_contraseña = st.text_input("Confirmar nueva contraseña", type="password", key="confirm_password")

            submitted = st.form_submit_button("Cambiar Contraseña")

            if submitted:
                if not contraseña_actual or not nueva_contraseña or not confirmar_contraseña:
                    st.error("Todos los campos son obligatorios.")
                elif nueva_contraseña != confirmar_contraseña:
                    st.error("La nueva contraseña y la confirmación no coinciden.")
                elif len(nueva_contraseña) < 6:
                    st.warning("La nueva contraseña debe tener al menos 6 caracteres.")
                else:
                    # Obtener el email del usuario logueado
                    email_usuario = st.session_state.user_info.get('email')

                    if email_usuario:
                        if cambiar_contraseña(email_usuario, contraseña_actual, nueva_contraseña):
                            st.success("Contraseña cambiada exitosamente. Inicia sesión de nuevo.")
                            st.session_state.logged_in = False
                            st.session_state.auth_mode = "login"
                            st.rerun()
                        else:
                            st.error("La contraseña actual es incorrecta.")
                    else:
                        st.error("Error al obtener información del usuario.")
