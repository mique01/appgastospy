import streamlit as st
import pandas as pd
from datetime import datetime
from firebase_config import get_user_data, save_user_data

def initialize_session_state():
    if 'user' not in st.session_state:
        st.session_state.user = None

    # Si el usuario no está autenticado, no inicializar más datos
    if st.session_state.user is None:
        return

    # Cargar datos del usuario desde Firebase
    user_data = get_user_data(st.session_state.user['localId'])

    if user_data:
        # Convertir datos de Firebase a DataFrames
        st.session_state.gastos = pd.DataFrame(user_data.get('gastos', []))
        st.session_state.ingresos = pd.DataFrame(user_data.get('ingresos', []))
        st.session_state.categorias = user_data.get('categorias', [])
        st.session_state.metodos_pago = user_data.get('metodos_pago', [])
        st.session_state.personas = user_data.get('personas', ['Usuario Principal'])
        st.session_state.modo_compartido = user_data.get('modo_compartido', False)
        st.session_state.presupuestos = user_data.get('presupuestos', {})
        st.session_state.comprobantes = pd.DataFrame(user_data.get('comprobantes', []))
    else:
        # Inicializar datos por defecto para nuevo usuario
        st.session_state.gastos = pd.DataFrame(
            columns=['fecha', 'categoria', 'monto', 'metodo_pago', 'persona', 'descripcion']
        )
        st.session_state.ingresos = pd.DataFrame(
            columns=['fecha', 'monto', 'metodo', 'persona', 'descripcion']
        )
        st.session_state.categorias = []
        st.session_state.metodos_pago = []
        st.session_state.personas = ['Usuario Principal']
        st.session_state.modo_compartido = False
        st.session_state.presupuestos = {}
        st.session_state.comprobantes = pd.DataFrame(
            columns=['fecha', 'nombre', 'tipo', 'archivo', 'categoria']
        )

def save_session_state():
    """Guarda el estado actual en Firebase"""
    if st.session_state.user is None:
        return

    user_data = {
        'gastos': st.session_state.gastos.to_dict('records'),
        'ingresos': st.session_state.ingresos.to_dict('records'),
        'categorias': st.session_state.categorias,
        'metodos_pago': st.session_state.metodos_pago,
        'personas': st.session_state.personas,
        'modo_compartido': st.session_state.modo_compartido,
        'presupuestos': st.session_state.presupuestos,
        'comprobantes': st.session_state.comprobantes.to_dict('records')
    }

    save_user_data(st.session_state.user['localId'], user_data)

def format_currency(amount):
    return f"${amount:,.2f}"

def show_empty_state_message():
    st.info("""
    🎉 ¡Bienvenido a tu gestor financiero personal!

    Para comenzar:
    1. Ve a la sección de Preferencias
    2. Configura tus categorías de gastos
    3. Agrega tus métodos de pago
    4. Activa el modo compartido si lo necesitas
    """)