import streamlit as st
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
        "Menú de opciones",
        ["Panel de Monitoreo","Nueva Predicción", "Métricas del modelo", "Cambiar Contraseña"],
        key="nav_dashboard"
    )
    
    st.sidebar.markdown("---")
    if st.sidebar.button("Cerrar Sesión", key="btn_cerrar_sesion"):
        st.session_state.logged_in = False
        st.session_state.auth_mode = "login" # Resetear para el siguiente inicio
        st.rerun()

    # Secciones del sistema según la opción seleccionada
    if opcion == "Panel de Monitoreo":
        from .panel_monitoreo.panel_monitoreo import vista_panel_monitoreo
        vista_panel_monitoreo()
        
    elif opcion == "Nueva Predicción":
        from .prediccion.nueva_prediccion import vista_nueva_prediccion
        vista_nueva_prediccion()
        
    elif opcion == "Métricas del modelo":
        from .metricas.metricas_modelo import vista_metricas_modelo
        vista_metricas_modelo()
        
    elif opcion == "Cambiar Contraseña":
        from .cambiar_contraseña.cambiar_contraseña import vista_cambiar_contraseña
        vista_cambiar_contraseña()