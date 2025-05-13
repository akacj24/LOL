import pandas as pd
import streamlit as st
import plotly.express as px
from datetime import datetime

# Configuración de la página
st.set_page_config(
    page_title="🌆 Análisis de Sensores - Mi Ciudad",
    page_icon="📡",
    layout="wide"
)

# Estilos CSS personalizados
st.markdown("""
    <style>
    html, body, [class*="css"] {
        font-family: 'Segoe UI', sans-serif;
        background-color: #0f172a;
        color: #f1f5f9;
    }
    .main {
        padding: 2rem;
    }
    h1, h2, h3, h4 {
        color: #38bdf8;
    }
    .stTabs [role="tablist"] {
        background-color: #1e293b;
        border-radius: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        color: #f1f5f9;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #38bdf8 !important;
        color: #0f172a !important;
        border-radius: 10px;
    }
    .card {
        background-color: #1e293b;
        padding: 1.5rem;
        border-radius: 1rem;
        box-shadow: 0 0 15px rgba(56, 189, 248, 0.2);
        margin-bottom: 1rem;
    }
    .stButton>button {
        background-color: #38bdf8;
        color: #0f172a;
        border-radius: 0.5rem;
        padding: 0.5rem 1rem;
        font-weight: bold;
        border: none;
    }
    .stButton>button:hover {
        background-color: #0ea5e9;
        color: white;
    }
    .stDataFrame {
        border-radius: 1rem;
        overflow: hidden;
    }
    </style>
""", unsafe_allow_html=True)

# Encabezado
st.title("📡 Análisis de Datos de Sensores en Mi Ciudad")
st.markdown("Bienvenido al panel de control de datos sensoriales urbanos 🌇. Visualiza, explora y analiza la información capturada por sensores ESP32.")

# Mapa base
eafit_location = pd.DataFrame({'lat': [6.2006], 'lon': [-75.5783]})
st.subheader("📍 Ubicación del Sensor")
st.map(eafit_location, zoom=15)

# Carga de archivo CSV
uploaded_file = st.file_uploader('📁 Subir archivo CSV', type='csv')

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        df = df.rename(columns={
            'temperatura {device="ESP32", name="Sensor 1"}': 'temperatura',
            'humedad {device="ESP32", name="Sensor 1"}': 'humedad'
        })
        df['Time'] = pd.to_datetime(df['Time'])
        df = df.set_index('Time')

        # Tabs principales
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Visualización Interactiva", "📈 Estadísticas", "🧪 Filtros", "📘 Info del Sitio"])

        with tab1:
            st.subheader("📊 Visualización Interactiva")

            var = st.radio("¿Qué variable deseas visualizar?", ["temperatura", "humedad", "Ambas"], horizontal=True)
            chart_type = st.selectbox("Tipo de gráfico", ["Línea", "Área", "Dispersión", "Histograma"])

            def plot_plotly(data, y, kind):
                if kind == "Línea":
                    fig = px.line(data, y=y, title=f"{y.capitalize()} - Línea", markers=True)
                elif kind == "Área":
                    fig = px.area(data, y=y, title=f"{y.capitalize()} - Área")
                elif kind == "Dispersión":
                    fig = px.scatter(data, y=y, title=f"{y.capitalize()} - Dispersión")
                else:
                    fig = px.histogram(data, x=y, title=f"{y.capitalize()} - Histograma")
                fig.update_layout(paper_bgcolor="#0f172a", plot_bgcolor="#1e293b", font_color="#f1f5f9")
                st.plotly_chart(fig, use_container_width=True)

            if var == "Ambas":
                plot_plotly(df, "temperatura", chart_type)
                plot_plotly(df, "humedad", chart_type)
            else:
                plot_plotly(df, var, chart_type)

            if st.toggle("📂 Mostrar datos crudos"):
                st.dataframe(df)

        with tab2:
            st.subheader("📈 Análisis Estadístico")

            stat_var = st.selectbox("Variable:", ["temperatura", "humedad"])
            stats = df[stat_var].describe()
            col1, col2 = st.columns(2)

            with col1:
                st.markdown(f"#### 🔢 Resumen de {stat_var.capitalize()}")
                st.dataframe(stats)

            with col2:
                st.markdown(f'<div class="card">', unsafe_allow_html=True)
                st.metric("Media", f"{stats['mean']:.2f}")
                st.metric("Máximo", f"{stats['max']:.2f}")
                st.metric("Mínimo", f"{stats['min']:.2f}")
                st.markdown(f'</div>', unsafe_allow_html=True)

        with tab3:
            st.subheader("🧪 Filtros de Datos")

            filter_var = st.selectbox("Filtrar por:", ["temperatura", "humedad"])
            col1, col2 = st.columns(2)

            with col1:
                min_val = st.slider("Valor mínimo", float(df[filter_var].min()), float(df[filter_var].max()), float(df[filter_var].mean()))
                filtered_min = df[df[filter_var] > min_val]
                st.dataframe(filtered_min)

            with col2:
                max_val = st.slider("Valor máximo", float(df[filter_var].min()), float(df[filter_var].max()), float(df[filter_var].mean()))
                filtered_max = df[df[filter_var] < max_val]
                st.dataframe(filtered_max)

            if st.button("⬇️ Descargar Datos Filtrados"):
                csv = filtered_min.to_csv().encode('utf-8')
                st.download_button("Descargar CSV", data=csv, file_name="datos_filtrados.csv", mime="text/csv")

        with tab4:
            st.subheader("📘 Información del Sitio de Medición")
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("""
                ### 🌍 Ubicación del Sensor  
                - **Lugar**: Universidad EAFIT  
                - **Latitud**: 6.2006  
                - **Longitud**: -75.5783  
                - **Altitud**: ~1.495 msnm  
                """)

            with col2:
                st.markdown("""
                ### ⚙️ Detalles del Sensor  
                - **Tipo**: ESP32  
                - **Variables medidas**: Temperatura, Humedad  
                - **Frecuencia de muestreo**: Configurable  
                - **Ubicación**: Campus universitario  
                """)

    except Exception as e:
        st.error(f"❌ Error procesando el archivo: {e}")
else:
    st.info("📂 Cargue un archivo CSV para comenzar el análisis.")

# Footer
st.markdown("""
---
🎓 Desarrollado por [Tu Nombre] — Universidad EAFIT  
📍 Medellín, Colombia  
""")
