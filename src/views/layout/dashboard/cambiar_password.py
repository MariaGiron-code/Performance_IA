import time

import streamlit as st
from sqlalchemy.exc import SQLAlchemyError

from src.database import cambiar_password


def vista_cambiar_pass():
    st.markdown("## Cambiar Contraseña")
    st.info("Por seguridad, deberás iniciar sesión nuevamente tras el cambio.")

    with st.form("form_cambiar_contraseña"):
        current_password = st.text_input(
            "Contraseña actual",
            type="password",
            key="current_password",
            help="Ingresa la contraseña que usaste para entrar hoy.",
        )

        st.write("---")  # Separador visual

        col1, col2 = st.columns(2)
        with col1:
            new_password = st.text_input(
                "Nueva contraseña", type="password", key="new_password"
            )
        with col2:
            confirm_password = st.text_input(
                "Confirmar nueva contraseña", type="password", key="confirm_password"
            )

        # Botón de envío
        submitted = st.form_submit_button(
            "Actualizar Contraseña", use_container_width=True
        )

        if submitted:
            # 1. Validaciones del Frontend
            if not current_password or not new_password or not confirm_password:
                st.warning("⚠️ Todos los campos son obligatorios.")
                return

            if new_password != confirm_password:
                st.error("La nueva contraseña y su confirmación no coinciden.")
                return

            if len(new_password) < 6:
                st.warning("⚠️ La nueva contraseña debe tener al menos 6 caracteres.")
                return

            if current_password == new_password:
                st.warning("⚠️ La nueva contraseña no puede ser igual a la anterior.")
                return

            # 2. Lógica del Backend
            email_usuario = st.session_state.user_info.get("email")

            if not email_usuario:
                st.error("Error de sesión: No se pudo identificar al usuario.")
                return

            try:
                # Llamada a la función de base de datos
                resultado = cambiar_password(
                    email_usuario, current_password, new_password
                )

                if resultado:
                    st.success("¡Contraseña cambiada exitosamente!")
                    st.toast("Redirigiendo al inicio de sesión...", icon="🔒")
                    time.sleep(2)

                    # Cerrar sesión
                    st.session_state.logged_in = False
                    st.session_state.auth_mode = "login"

                    # Limpiar datos sensibles
                    if "user_password" in st.session_state:
                        del st.session_state["user_password"]

                    st.rerun()
                else:
                    st.error(
                        "La contraseña actual es incorrecta o hubo un problema al actualizar."
                    )

            except SQLAlchemyError as e:
                st.error(f"Error de base de datos: {e}")
            except Exception as e:
                st.error(f"Ocurrió un error inesperado: {e}")
