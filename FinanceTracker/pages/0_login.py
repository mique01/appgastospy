import streamlit as st
from firebase_config import login_user, register_user
import json

st.set_page_config(
    page_title="Login - Gestión Financiera",
    page_icon="🔐",
    layout="centered"
)

# Estilo personalizado
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .auth-container {
        background-color: white;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        max-width: 400px;
        margin: auto;
    }
    </style>
""", unsafe_allow_html=True)

def main():
    if 'user' not in st.session_state:
        st.session_state.user = None

    if st.session_state.user is not None:
        st.success("Ya has iniciado sesión")
        st.rerun()
        return

    st.title("🔐 Acceso al Sistema")

    # Contenedor principal
    with st.container():
        tab1, tab2 = st.tabs(["Iniciar Sesión", "Registrarse"])
        
        with tab1:
            with st.form("login_form"):
                email = st.text_input("Correo electrónico")
                password = st.text_input("Contraseña", type="password")
                submit_login = st.form_submit_button("Iniciar Sesión", type="primary")

                if submit_login and email and password:
                    try:
                        user = login_user(email, password)
                        if user:
                            st.session_state.user = user
                            st.success("¡Inicio de sesión exitoso!")
                            st.rerun()
                    except Exception as e:
                        st.error(f"Error al iniciar sesión: {str(e)}")

        with tab2:
            with st.form("register_form"):
                new_email = st.text_input("Correo electrónico")
                new_password = st.text_input("Contraseña", type="password")
                confirm_password = st.text_input("Confirmar contraseña", type="password")
                submit_register = st.form_submit_button("Registrarse", type="primary")

                if submit_register and new_email and new_password and confirm_password:
                    if new_password != confirm_password:
                        st.error("Las contraseñas no coinciden")
                    else:
                        try:
                            user = register_user(new_email, new_password)
                            if user:
                                st.session_state.user = user
                                st.success("¡Registro exitoso!")
                                st.rerun()
                        except Exception as e:
                            st.error(f"Error al registrar: {str(e)}")

    # Redirect after successful login/registration
    if st.session_state.user is not None:
        st.switch_page("app.py")

if __name__ == "__main__":
    main()