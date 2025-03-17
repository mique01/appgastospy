import streamlit as st
from utils import initialize_session_state

initialize_session_state()

st.title("⚙️ Configuración del Sistema")

# Instrucciones iniciales
if not st.session_state.categorias and not st.session_state.metodos_pago:
    st.info("""
    👋 ¡Bienvenido a la configuración inicial!

    Para comenzar a usar el sistema, configura:
    1. Si compartes gastos, activa el modo compartido
    2. Agrega las personas con las que compartes gastos
    """)

# Contenedor principal con estilo
with st.container():
    st.markdown("""
        <style>
        .configuracion-container {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        </style>
    """, unsafe_allow_html=True)

    # Modo compartido
    st.subheader("🤝 Modo Compartido", divider="gray")
    modo_compartido = st.toggle(
        "Activar gestión de gastos compartidos",
        value=st.session_state.modo_compartido,
        help="Activa esta opción si compartes gastos con otras personas"
    )

    if modo_compartido != st.session_state.modo_compartido:
        st.session_state.modo_compartido = modo_compartido
        st.success("✅ Configuración actualizada")
        st.rerun()

    # Gestión de personas (solo en modo compartido)
    if st.session_state.modo_compartido:
        st.subheader("👥 Gestión de Personas", divider="gray")
        col1, col2 = st.columns([3, 1])
        with col1:
            nueva_persona = st.text_input(
                "Nueva persona",
                placeholder="Nombre de la persona"
            )
        with col2:
            if st.button("Agregar persona", type="primary") and nueva_persona:
                if nueva_persona not in st.session_state.personas:
                    st.session_state.personas.append(nueva_persona)
                    st.success(f"✅ Persona '{nueva_persona}' agregada")
                    st.rerun()
                else:
                    st.error("❌ Esta persona ya existe")

        # Mostrar personas registradas
        if len(st.session_state.personas) > 1:  # Más de 1 porque siempre existe "Usuario Principal"
            st.write("**Personas registradas:**")
            for persona in st.session_state.personas:
                if persona != "Usuario Principal":
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write(f"• {persona}")
                    with col2:
                        if st.button("🗑️", key=f"del_per_{persona}"):
                            st.session_state.personas.remove(persona)
                            st.rerun()