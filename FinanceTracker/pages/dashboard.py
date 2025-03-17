import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils import initialize_session_state, format_currency, show_empty_state_message

# Verificar autenticación
if 'user' not in st.session_state or st.session_state.user is None:
    st.switch_page("app.py")

st.set_page_config(
    page_title="Dashboard - Gestión Financiera",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configuración de tema personalizado
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stMetric {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .st-emotion-cache-1r6slb0 {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

initialize_session_state()

# Botón de cierre de sesión en la barra lateral
with st.sidebar:
    if st.button("Cerrar Sesión"):
        st.session_state.user = None
        st.rerun()

st.title("📊 Dashboard Financiero")

if not st.session_state.categorias:
    show_empty_state_message()
else:
    # Balance general
    st.subheader("Resumen General", divider="gray")
    col1, col2, col3 = st.columns(3)

    total_ingresos = st.session_state.ingresos['monto'].sum()
    total_gastos = st.session_state.gastos['monto'].sum()
    balance = total_ingresos - total_gastos

    with col1:
        st.metric(
            "Balance Total",
            format_currency(balance),
            delta=format_currency(balance) if balance != 0 else None,
            delta_color="normal"
        )

    with col2:
        st.metric("Total Ingresos", format_currency(total_ingresos))

    with col3:
        st.metric("Total Gastos", format_currency(total_gastos))

    # Gráficos
    st.subheader("Análisis Detallado", divider="gray")
    col1, col2 = st.columns(2)

    with col1:
        fig_balance = go.Figure(data=[
            go.Bar(
                name='Ingresos',
                x=['Total'],
                y=[total_ingresos],
                marker_color='#2ecc71'
            ),
            go.Bar(
                name='Gastos',
                x=['Total'],
                y=[total_gastos],
                marker_color='#e74c3c'
            )
        ])
        fig_balance.update_layout(
            title="Balance de Ingresos vs Gastos",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            barmode='group'
        )
        st.plotly_chart(fig_balance, use_container_width=True)

    with col2:
        if not st.session_state.gastos.empty:
            gastos_por_categoria = st.session_state.gastos.groupby('categoria')['monto'].sum()
            fig_categorias = px.pie(
                values=gastos_por_categoria.values,
                names=gastos_por_categoria.index,
                title="Distribución de Gastos por Categoría",
                hole=0.4
            )
            fig_categorias.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_categorias, use_container_width=True)
        else:
            st.info("Aún no hay gastos registrados para mostrar la distribución.")
