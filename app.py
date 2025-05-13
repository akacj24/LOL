import pandas as pd
import streamlit as st
import plotly.express as px
from datetime import datetime

# Configuración de página
st.set_page_config(page_title="🌿 Análisis de Sensores Naturales", page_icon="🦜", layout="wide")

# Estilos personalizados con temática natural
st.markdown("""
    <style>
    /* Fondo con imagen temática natural */
    body {
        background-image: url("https://images.unsplash.com/photo-1600596541240-8d210f492f28?auto=format&fit=crop&w=1920&q=80");
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
    }

    .main {
        background-color: rgba(255, 255, 255, 0.06);
        backdrop-filter: blur(8px);
        border-radius: 1.5rem;
        padding: 2rem 4rem;
        margin: 2rem;
        box-shadow: 0 0 40px rgba(0,0,0,0.4);
    }

    h1 {
        font-size: 3.5rem;
        color: #fefae0;
        text-align: center;
        text-shadow: 2px 2px 4px #1b4332;
        margin-bottom: 2rem;
    }

    h2, h3 {
        color: #d8f3dc;
        text-shadow: 1px 1px 3px #081c15;
    }

    .stTabs [role="tablist"] {
        background-color: rgba(8, 28, 21, 0.6);
        border-radius: 10px;
        padding: 0.5rem;
    }

    .stTabs [data-baseweb="tab"] {
        color: #b7e4c7 !important;
        font-weight: 600;
    }

    .stTabs [aria-selected="true"] {
        background-color: #95d5b2 !important;
        color: #081c15 !important;
        border-radius: 10px;
    }

    .stButton>button {
        background-color: #40916c;
        color: white;
        font-weight: bold;
        padding: 0.6rem 1.4rem;
        border-radius: 10px;
        border: none;
        transition: 0.3s ease;
    }

    .stButton>button:hover {
        background-color: #1b4332;
        transform: scale(1.05);
    }

    .metric-container {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 1rem;
        padding: 1.2rem;
        box-shadow: 0 0 10px rgba(0,0,0,0.3);
    }

    .block-container {
        padding-top: 0 !important;
    }

    .stDataFrame {
        border-radius: 1rem;
        overflow: hidden;
    }
    </style>
""", unsafe_allow_html=True)

# Encabezado principal
st.markdown("# 🦜 Análisis de Sensores Ambientales en la Ciudad")

# Mapa de ubicación
eafit_location = pd.DataFrame({'lat': [6.2006], 'lon': [-75.5783]})
st.subheader("📍 Sensor en Universidad EAFIT")
st.map(eafit_location, zoom=15)

# Carga de archivo
uploaded_file = st.file_uploader("📁 Suba su archivo CSV", type='csv')

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        df = df.rename(columns={
            'temperatura {device="ESP32", name="Sensor 1"}': 'temperatura',
            'humedad {device="ESP32", name="Sensor 1"}': 'humedad'
        })
        df['Time'] = pd.to_datetime(df['Time'])
        df = df.set_index('Time')

        tab1, tab2, tab3, tab4 = st.tabs(["🌱 Visualización", "🌡️ Estadísticas", "🔍 Filtros", "🌍 Sitio"])

        with tab1:
            st.subheader("🌿 Visualización Interactiva")
            var = st.radio("Variable a visualizar:", ["temperatura", "humedad", "Ambas"], horizontal=True)
            tipo = st.selectbox("Tipo de gráfico", ["Línea", "Área", "Dispersión", "Histograma"])

            def grafico(data, y, tipo):
                if tipo == "Línea":
                    fig = px.line(data, y=y, markers=True)
                elif tipo == "Área":
                    fig = px.area(data, y=y)
                elif tipo == "Dispersión":
                    fig = px.scatter(data, y=y)
                else:
                    fig = px.histogram(data, x=y)

                fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(255,255,255,0.05)',
                    font_color='#d8f3dc',
                    title=f"{y.capitalize()} - {tipo}",
                    title_font_size=22
                )
                st.plotly_chart(fig, use_container_width=True)

            if var == "Ambas":
                grafico(df, "temperatura", tipo)
                grafico(df, "humedad", tipo)
            else:
                grafico(df, var, tipo)

        with tab2:
            st.subheader("🌡️ Estadísticas del Sensor")
            variable = st.selectbox("Selecciona variable", ["temperatura", "humedad"])
            stats = df[variable].describe()

            col1, col2 = st.columns(2)
            with col1:
                st.markdown("### 📊 Resumen")
                st.dataframe(stats)

            with col2:
                st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                st.metric("Media", f"{stats['mean']:.2f}")
                st.metric("Máximo", f"{stats['max']:.2f}")
                st.metric("Mínimo", f"{stats['min']:.2f}")
                st.markdown('</div>', unsafe_allow_html=True)

        with tab3:
            st.subheader("🔍 Filtros")
            f_var = st.selectbox("Filtrar por variable", ["temperatura", "humedad"])
            col1, col2 = st.columns(2)

            with col1:
                min_val = st.slider("Valor mínimo", float(df[f_var].min()), float(df[f_var].max()), float(df[f_var].mean()))
                filtered_min = df[df[f_var] > min_val]
                st.dataframe(filtered_min)

            with col2:
                max_val = st.slider("Valor máximo", float(df[f_var].min()), float(df[f_var].max()), float(df[f_var].mean()))
                filtered_max = df[df[f_var] < max_val]
                st.dataframe(filtered_max)

            if st.button("⬇️ Descargar CSV filtrado"):
                csv = filtered_min.to_csv().encode('utf-8')
                st.download_button("Descargar", data=csv, file_name="filtrado.csv", mime="text/csv")

        with tab4:
            st.subheader("🌍 Información del Sitio de Medición")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("""
                ### 📌 Ubicación  
                - Universidad EAFIT  
                - Lat: 6.2006  
                - Lon: -75.5783  
                - Altitud: ~1.495 msnm  
                """)

            with col2:
                st.markdown("""
                ### 🛠️ Sensor  
                - Tipo: ESP32  
                - Medidas: Temperatura, Humedad  
                - Frecuencia: Configurable  
                - Entorno: Tropical urbano  
                """)

    except Exception as e:
        st.error(f"❌ Error cargando archivo: {e}")
else:
    st.info("📂 Sube un archivo CSV para comenzar el análisis.")

# Footer
st.markdown("""
---
🧬 Desarrollado para visualización ambiental de sensores urbanos  
🌱 Universidad EAFIT — Medellín, Colombia  
""")
