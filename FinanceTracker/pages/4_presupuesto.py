import streamlit as st
import plotly.express as px
from utils import initialize_session_state, format_currency

initialize_session_state()

st.title("💵 Gestión de Presupuesto")

# Configuración de presupuesto
st.subheader("Configurar Presupuesto por Categoría")

for categoria in st.session_state.categorias:
    col1, col2 = st.columns([3, 1])
    with col1:
        nuevo_presupuesto = st.number_input(
            f"Presupuesto para {categoria}",
            min_value=0.0,
            value=float(st.session_state.presupuestos[categoria]),
            key=f"presupuesto_{categoria}"
        )
    with col2:
        if st.button("Guardar", key=f"guardar_{categoria}"):
            st.session_state.presupuestos[categoria] = nuevo_presupuesto
            st.success(f"Presupuesto actualizado para {categoria}")

# Visualización del progreso
st.subheader("Progreso del Presupuesto")

for categoria in st.session_state.categorias:
    presupuesto = st.session_state.presupuestos[categoria]
    gasto_actual = st.session_state.gastos[
        st.session_state.gastos['categoria'] == categoria
    ]['monto'].sum()
    
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        st.write(f"**{categoria}**")
    with col2:
        if presupuesto > 0:
            progreso = (gasto_actual / presupuesto) * 100
            st.progress(min(progreso / 100, 1.0))
    with col3:
        st.write(f"{format_currency(gasto_actual)} / {format_currency(presupuesto)}")

# Gráfico de presupuesto vs gastos
presupuestos_data = []
for categoria in st.session_state.categorias:
    presupuesto = st.session_state.presupuestos[categoria]
    gasto_actual = st.session_state.gastos[
        st.session_state.gastos['categoria'] == categoria
    ]['monto'].sum()
    presupuestos_data.append({
        'categoria': categoria,
        'Presupuesto': presupuesto,
        'Gasto Actual': gasto_actual
    })

fig = px.bar(
    presupuestos_data,
    x='categoria',
    y=['Presupuesto', 'Gasto Actual'],
    title="Presupuesto vs Gasto Actual por Categoría",
    barmode='group'
)
st.plotly_chart(fig, use_container_width=True)
