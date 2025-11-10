import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# ---------------------------
# CONFIGURACIÓN INICIAL
# ---------------------------
st.set_page_config(page_title="Cotizador de Obra", page_icon="🏗️", layout="wide")

# Estilos personalizados
st.markdown("""
    <style>
    body {background-color: #000000;}
    .main {background-color: #000000;}
    h1, h2, h3, h4, h5, h6, p, label, span, div {
        color: #F7F7F7 !important;
    }
    .stButton>button {
        background-color: #F87B1B;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.6em 1.2em;
    }
    .stButton>button:hover {
        background-color: #ff9635;
        color: #fff;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------
# TÍTULO
# ---------------------------
st.title("🏗️ Proyección y Cotizador de Presupuestos")
st.subheader("Obra blanca y obra negra")

st.divider()

# ---------------------------
# PARTE 1: DATOS GENERALES
# ---------------------------
st.header("📋 Datos generales del proyecto")

col1, col2 = st.columns(2)
with col1:
    tipo_obra = st.radio("Tipo de obra:", ["Obra negra", "Obra blanca"])
    area = st.number_input("Área total (m²):", min_value=0.0, step=1.0)
    calidad = st.selectbox("Nivel de acabados:", ["Económico", "Estándar", "Premium"])
with col2:
    ciudad = st.text_input("Ciudad del proyecto:")
    responsable = st.text_input("Nombre del responsable:")
    contacto = st.text_input("Contacto o correo:")

st.divider()

# ---------------------------
# PARTE 2: SECCIONES DETALLADAS
# ---------------------------
st.header("⚙️ Especificaciones técnicas")

with st.expander("🧱 Estructura y cimentación"):
    estructura = st.selectbox("Tipo de estructura:", ["Concreto reforzado", "Metálica", "Prefabricada"])
    cimentacion = st.selectbox("Tipo de cimentación:", ["Zapatas", "Losas", "Pilotes"])
    refuerzo = st.slider("Cantidad de acero de refuerzo (kg/m²):", 0, 200, 80)

with st.expander("🚿 Hidrosanitarias"):
    puntos_agua = st.slider("Número de puntos de agua:", 0, 20, 5)
    puntos_desague = st.slider("Número de desagües:", 0, 20, 5)
    calentador = st.checkbox("¿Incluye calentador de agua?")

with st.expander("💡 Eléctricas e iluminación"):
    luminarias = st.slider("Cantidad de luminarias:", 0, 50, 12)
    tomas = st.slider("Cantidad de tomas eléctricas:", 0, 30, 10)
    interruptores = st.slider("Cantidad de interruptores:", 0, 20, 8)

with st.expander("🚪 Carpintería, puertas y ventanas"):
    puertas = st.number_input("Número de puertas:", min_value=0, step=1)
    ventanas = st.number_input("Número de ventanas:", min_value=0, step=1)
    tipo_carpinteria = st.selectbox("Tipo de carpintería:", ["Madera", "Aluminio", "PVC"])

with st.expander("🧽 Acabados y pisos"):
    tipo_piso = st.selectbox("Tipo de piso:", ["Cerámica", "Madera laminada", "Porcelanato", "Cemento pulido"])
    paredes = st.selectbox("Tipo de acabado de paredes:", ["Estuco y pintura", "Enchapado", "Texturizado"])
    techos = st.selectbox("Tipo de cielo raso:", ["Drywall", "PVC", "Madera"])

st.divider()

# ---------------------------
# PARTE 3: CÁLCULO DE PRESUPUESTO
# ---------------------------

if st.button("💰 Calcular presupuesto"):
    # Factores base por tipo de obra
    base_costos = {
        "Obra negra": 420000,
        "Obra blanca": 850000
    }

    factor_calidad = {"Económico": 0.8, "Estándar": 1.0, "Premium": 1.3}

    # Costo base
    costo_base = area * base_costos[tipo_obra] * factor_calidad[calidad]

    # Costos adicionales según secciones
    costo_estructura = refuerzo * 5000
    costo_hidrosanitaria = (puntos_agua + puntos_desague) * 80000
    costo_electrica = (luminarias * 50000) + (tomas * 40000) + (interruptores * 30000)
    costo_carpinteria = (puertas * 300000) + (ventanas * 250000)
    costo_acabados = area * 100000

    if calentador:
        costo_hidrosanitaria += 1200000

    total = costo_base + costo_estructura + costo_hidrosanitaria + costo_electrica + costo_carpinteria + costo_acabados

    # ---------------------------
    # RESULTADOS
    # ---------------------------
    st.success(f"💰 **Costo total estimado:** ${total:,.0f} COP")

    st.divider()

    # Detalle de componentes
    detalle = pd.DataFrame({
        "Categoría": ["Base obra", "Estructura", "Hidrosanitaria", "Eléctrica", "Carpintería", "Acabados"],
        "Valor (COP)": [costo_base, costo_estructura, costo_hidrosanitaria, costo_electrica, costo_carpinteria, costo_acabados]
    })

    st.subheader("📊 Desglose de costos")
    st.dataframe(detalle, hide_index=True, use_container_width=True)

    # ---------------------------
    # GRÁFICO DE DISTRIBUCIÓN
    # ---------------------------
    fig = go.Figure(data=[go.Pie(
        labels=detalle["Categoría"],
        values=detalle["Valor (COP)"],
        textinfo="label+percent",
        marker_colors=["#F87B1B", "#1055C9", "#FFAE4D", "#F7F7F7", "#F87B1B", "#1055C9"]
    )])
    fig.update_layout(
        title="Distribución de costos por categoría",
        showlegend=False,
        paper_bgcolor="#000000",
        plot_bgcolor="#000000"
    )
    st.plotly_chart(fig, use_container_width=True)

else:
    st.info("👈 Completa los datos del proyecto y presiona **Calcular presupuesto** para obtener el resultado.")

