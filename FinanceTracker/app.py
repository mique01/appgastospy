import streamlit as st
from firebase_config import login_user, register_user

st.set_page_config(
    page_title="Login - Gestión Financiera",
    page_icon="🔐",
    layout="centered"
)

# Verificar autenticación
if 'user' not in st.session_state:
    st.session_state.user = None

# Si no hay usuario autenticado, mostrar login
if st.session_state.user is None:
    st.title("🔐 Acceso al Sistema")

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
                    st.error(str(e))

    with tab2:
        with st.form("register_form"):
            new_email = st.text_input("Correo electrónico")
            new_password = st.text_input("Contraseña", type="password", autocomplete="new-password")
            confirm_password = st.text_input("Confirmar contraseña", type="password", autocomplete="new-password")
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
                        st.error(str(e))
else:
    # Si el usuario está autenticado, redirigir al dashboard
    st.switch_page("pages/dashboard.py")


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