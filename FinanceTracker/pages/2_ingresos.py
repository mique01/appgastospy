import streamlit as st
from datetime import datetime
from utils import initialize_session_state, format_currency, save_session_state

# Verificar autenticación
if 'user' not in st.session_state or st.session_state.user is None:
    st.switch_page("app.py")

initialize_session_state()

st.title("💰 Registro de Ingresos")

# Gestión de métodos de pago
with st.expander("➕ Gestionar Métodos de Pago", expanded=False):
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

with st.form("registro_ingreso"):
    fecha = st.date_input("Fecha", datetime.now())
    monto = st.number_input("Monto", min_value=0.0, step=0.01)
    metodo = st.selectbox("Método de ingreso", st.session_state.metodos_pago)
    descripcion = st.text_input("Descripción")

    if st.session_state.modo_compartido:
        persona = st.selectbox("Persona", st.session_state.personas)
    else:
        persona = st.session_state.personas[0]

    submitted = st.form_submit_button("Registrar Ingreso")

    if submitted:
        nuevo_ingreso = {
            'fecha': fecha,
            'monto': monto,
            'metodo': metodo,
            'persona': persona,
            'descripcion': descripcion
        }
        st.session_state.ingresos.loc[len(st.session_state.ingresos)] = nuevo_ingreso
        save_session_state()
        st.success("Ingreso registrado exitosamente")
        st.rerun()

# Mostrar historial de ingresos
st.subheader("Historial de Ingresos")
if not st.session_state.ingresos.empty:
    st.dataframe(
        st.session_state.ingresos.sort_values('fecha', ascending=False),
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("No hay ingresos registrados")