from pathlib import Path

import streamlit as st

# Gestión de Rutas Absolutas
BASE_DIR = Path(__file__).parent.parent.parent.parent.parent
CSS_PATH = BASE_DIR / "public" / "css" / "dashboard.css"
LOGO_PATH = BASE_DIR / "public" / "logo.png"


def local_css(file_path):
    try:
        with open(file_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        print(f"Advertencia: No se encontró {file_path}")


def vista_dashboard():
    local_css(CSS_PATH)  # Se carga el CSS

    # --- SIDEBAR (Menú Lateral) ---
    with st.sidebar:
        # 1. Logo con manejo de errores
        if LOGO_PATH.exists():
            st.image(str(LOGO_PATH), width=100)
        else:
            st.markdown("### 🎓 **EduGuard AI**")

        # 2. Saludo seguro
        nombre_usuario = st.session_state.get("user_info", {}).get("nombre", "Usuario")
        st.write(f"Bienvenido, **{nombre_usuario}**")

        # 3. Menú de navegación
        opcion = st.radio(
            "Menú de opciones",
            [
                "Panel de Monitoreo",
                "Nueva Predicción",
                "Métricas del modelo",
                "Perfil",
                "Cambiar Contraseña",
            ],
            key="nav_dashboard",
        )

        st.markdown("---")

        # 4. Botón de Logout
        if st.button(
                "Cerrar Sesión", key="btn_cerrar_sesion", use_container_width=True
        ):
            # Limpiar variables críticas
            keys_to_clear = ["logged_in", "user_info", "user_password"]
            for key in keys_to_clear:
                if key in st.session_state:
                    del st.session_state[key]

            st.session_state.auth_mode = "login"
            st.rerun()

    # ROUTER (Carga de Vistas)
    if opcion == "Panel de Monitoreo":
        from panel_monitoreo.panel_monitoreo import vista_panel_monitoreo

        vista_panel_monitoreo()

    elif opcion == "Nueva Predicción":
        from prediccion.nueva_prediccion import vista_nueva_prediccion

        vista_nueva_prediccion()

    elif opcion == "Métricas del modelo":
        from metricas.metricas_modelo import vista_metricas_modelo

        vista_metricas_modelo()

    elif opcion == "Perfil":
        st.title("Perfil de Usuario")
        st.info("Esta funcionalidad estará disponible próximamente.")

    elif opcion == "Cambiar Contraseña":
        from cambiar_contraseña.cambiar_contraseña import vista_cambiar_contraseña

        vista_cambiar_contraseña()
