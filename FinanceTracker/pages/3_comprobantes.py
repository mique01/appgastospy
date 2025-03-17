import streamlit as st
from datetime import datetime
from utils import initialize_session_state, save_session_state
import io

# Verificar autenticación
if 'user' not in st.session_state or st.session_state.user is None:
    st.switch_page("app.py")

initialize_session_state()

st.title("📄 Gestión de Comprobantes")

with st.form("subir_comprobante"):
    fecha = st.date_input("Fecha", datetime.now())
    nombre = st.text_input("Nombre del comprobante")
    categoria = st.selectbox("Categoría", st.session_state.categorias)
    tipo = st.selectbox("Tipo de comprobante", ["Factura", "Recibo", "Ticket", "Otro"])
    archivo = st.file_uploader("Subir comprobante", type=['pdf', 'png', 'jpg', 'jpeg'])
    
    submitted = st.form_submit_button("Guardar Comprobante")
    
    if submitted and archivo is not None:
        nuevo_comprobante = {
            'fecha': fecha,
            'nombre': nombre,
            'tipo': tipo,
            'archivo': archivo.getvalue(),
            'categoria': categoria
        }
        st.session_state.comprobantes.loc[len(st.session_state.comprobantes)] = nuevo_comprobante
        st.success("Comprobante guardado exitosamente")
        st.rerun()

# Mostrar comprobantes
st.subheader("Comprobantes Guardados")
if not st.session_state.comprobantes.empty:
    for idx, comprobante in st.session_state.comprobantes.iterrows():
        with st.expander(f"{comprobante['fecha']} - {comprobante['nombre']}"):
            st.write(f"Tipo: {comprobante['tipo']}")
            st.write(f"Categoría: {comprobante['categoria']}")
            if comprobante['archivo'] is not None:
                st.download_button(
                    "Descargar comprobante",
                    comprobante['archivo'],
                    file_name=comprobante['nombre'],
                    mime="application/octet-stream"
                )
else:
    st.info("No hay comprobantes guardados")