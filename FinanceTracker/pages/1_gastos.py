import streamlit as st
from datetime import datetime
from utils import initialize_session_state, format_currency, save_session_state

# Verificar autenticación
if 'user' not in st.session_state or st.session_state.user is None:
    st.switch_page("app.py")

initialize_session_state()

st.title("📝 Registro de Gastos")

# Gestión de categorías
with st.expander("➕ Gestionar Categorías", expanded=False):
    col1, col2 = st.columns([3, 1])
    with col1:
        nueva_categoria = st.text_input(
            "Nueva categoría",
            placeholder="Ej: Alimentación, Transporte, etc.",
            key="nueva_categoria_gasto"
        )
    with col2:
        if st.button("Agregar", type="primary") and nueva_categoria:
            if nueva_categoria not in st.session_state.categorias:
                st.session_state.categorias.append(nueva_categoria)
                st.session_state.presupuestos[nueva_categoria] = 0
                save_session_state()
                st.success(f"✅ Categoría '{nueva_categoria}' agregada")
                st.rerun()
            else:
                st.error("❌ Esta categoría ya existe")

    if st.session_state.categorias:
        for cat in st.session_state.categorias:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"• {cat}")
            with col2:
                if st.button("🗑️", key=f"del_cat_{cat}"):
                    st.session_state.categorias.remove(cat)
                    del st.session_state.presupuestos[cat]
                    save_session_state()
                    st.rerun()

# Gestión de métodos de pago
with st.expander("💳 Gestionar Métodos de Pago", expanded=False):
    col1, col2 = st.columns([3, 1])
    with col1:
        nuevo_metodo = st.text_input(
            "Nuevo método de pago",
            placeholder="Ej: Efectivo, Tarjeta, etc.",
            key="nuevo_metodo_pago"
        )
    with col2:
        if st.button("Agregar", type="primary") and nuevo_metodo:
            if nuevo_metodo not in st.session_state.metodos_pago:
                st.session_state.metodos_pago.append(nuevo_metodo)
                save_session_state()
                st.success(f"✅ Método de pago '{nuevo_metodo}' agregado")
                st.rerun()
            else:
                st.error("❌ Este método de pago ya existe")

    if st.session_state.metodos_pago:
        for metodo in st.session_state.metodos_pago:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"• {metodo}")
            with col2:
                if st.button("🗑️", key=f"del_met_{metodo}"):
                    st.session_state.metodos_pago.remove(metodo)
                    save_session_state()
                    st.rerun()

# Formulario de registro
with st.form("registro_gasto"):
    fecha = st.date_input("Fecha", datetime.now())
    categoria = st.selectbox("Categoría", st.session_state.categorias)
    monto = st.number_input("Monto", min_value=0.0, step=0.01)
    metodo_pago = st.selectbox("Método de pago", st.session_state.metodos_pago)
    descripcion = st.text_input("Descripción")

    if st.session_state.modo_compartido:
        persona = st.selectbox("Persona", st.session_state.personas)
    else:
        persona = st.session_state.personas[0]

    submitted = st.form_submit_button("Registrar Gasto")

    if submitted:
        nuevo_gasto = {
            'fecha': fecha,
            'categoria': categoria,
            'monto': monto,
            'metodo_pago': metodo_pago,
            'persona': persona,
            'descripcion': descripcion
        }
        st.session_state.gastos.loc[len(st.session_state.gastos)] = nuevo_gasto
        save_session_state()
        st.success("Gasto registrado exitosamente")
        st.rerun()

# Mostrar historial de gastos
st.subheader("Historial de Gastos")
if not st.session_state.gastos.empty:
    st.dataframe(
        st.session_state.gastos.sort_values('fecha', ascending=False),
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("No hay gastos registrados")