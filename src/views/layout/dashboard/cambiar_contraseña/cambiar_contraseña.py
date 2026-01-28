import streamlit as st

from src.database import cambiar_password


def vista_cambiar_contraseña():
    st.write("## 🔒 Cambiar Contraseña")

    # Formulario de cambio de contraseña
    with st.form("form_cambiar_contraseña"):
        contraseña_actual = st.text_input(
            "Contraseña actual", type="password", key="current_password"
        )
        nueva_contraseña = st.text_input(
            "Nueva contraseña", type="password", key="new_password"
        )
        confirmar_contraseña = st.text_input(
            "Confirmar nueva contraseña", type="password", key="confirm_password"
        )

        submitted = st.form_submit_button("Cambiar Contraseña")

        if submitted:
            if (
                    not contraseña_actual
                    or not nueva_contraseña
                    or not confirmar_contraseña
            ):
                st.error("Todos los campos son obligatorios.")
            elif nueva_contraseña != confirmar_contraseña:
                st.error("La nueva contraseña y la confirmación no coinciden.")
            elif len(nueva_contraseña) < 6:
                st.warning("La nueva contraseña debe tener al menos 6 caracteres.")
            else:
                # Obtener el email del usuario logueado
                email_usuario = st.session_state.user_info.get("email")

                if email_usuario:
                    if cambiar_password(
                            email_usuario, contraseña_actual, nueva_contraseña
                    ):
                        st.success(
                            "Contraseña cambiada exitosamente. Inicia sesión de nuevo."
                        )
                        st.session_state.logged_in = False
                        st.session_state.auth_mode = "login"
                        st.rerun()
                    else:
                        st.error("La contraseña actual es incorrecta.")
                else:
                    st.error("Error al obtener información del usuario.")
