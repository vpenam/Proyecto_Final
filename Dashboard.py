import streamlit as st
import plotly.express as px
import base64
import os
import pandas as pd

st.set_page_config(layout="wide", page_title="Dashboard de Presentación")

st.title("Estado de los Hurtos en Colombia")

# --- Función para cargar imágenes y convertirlas a base64 (para despliegue) ---
def get_image_as_base64(path):
    # Se asume que las imágenes están en el mismo directorio que el script de Streamlit
    if not os.path.exists(path):
        st.error(f"Error: Archivo de imagen no encontrado en {path}. Asegúrate de que está en el mismo directorio que el script de Streamlit.")
        return None
    with open(path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# --- Rutas de los archivos (asumen que están en el mismo directorio que este script) ---
IMAGE_PATHS = {
    "Hurtos por Región": "grafico1_hurtos_region.png",
    "Hurtos por Departamento": "grafico2_hurtos_departamento.png",
    "Autos vs Motos": "grafico3_autos_vs_motos.png",
    "Top 15 Municipios": "grafico4_top15_municipios.png",
    "Tasa de Captura": "grafico5_tasa_captura_por_nivel.png",
    "Eficiencia Policial Ciudades": "grafico6_eficiencia_policial_ciudades.png",
    "Gráfico de Hipótesis": "grafico16_hipotesis.png",
}

INTERACTIVE_HTML_PATH = "grafico7_evolucion_hurtos_interactivo.html"
GEOGRAPHIC_DATA_PATH = "Region_Departamentos_y_municipios_de_Colombia.csv"
CLUSTERING_DATA_PATH = "municipios_clustering_20260316_123316.csv" # Nueva ruta para datos de clustering


st.sidebar.header("Navegación")
page = st.sidebar.radio("Ir a", [
    "Introducción",
    "Visión General de Hurtos",
    "Análisis de Modalidades/Vehículos",
    "Eficiencia y Capturas",
    "Evolución Interactivo", # Se mantiene por si se quiere añadir después
    "Datos Geográficos", # Se mantiene por si se quiere añadir después
    "Análisis de Clustering Geográfico" # Nueva sección
])

if page == "Introducción":
    st.header("Bienvenido al Dashboard de Hurtos")
    st.write("Este dashboard presenta un análisis visual de los datos de hurtos, modalidades y eficiencia policial en Colombia.")
    st.markdown("--- \n_Selecciona una sección en el menú de la izquierda para explorar los gráficos._")

elif page == "Visión General de Hurtos":
    st.header("2. Visión General de Hurtos")
    
    st.subheader("Hurtos por Región")
    img_base64 = get_image_as_base64(IMAGE_PATHS["Hurtos por Región"])
    if img_base64: st.markdown(f"<img src='data:image/png;base64,{img_base64}' style='width:100%; height:auto;'>", unsafe_allow_html=True)

    st.subheader("Hurtos por Departamento")
    img_base64 = get_image_as_base64(IMAGE_PATHS["Hurtos por Departamento"])
    if img_base64: st.markdown(f"<img src='data:image/png;base64,{img_base64}' style='width:100%; height:auto;'>", unsafe_allow_html=True)

    st.subheader("Top 15 Municipios con Mayor Hurto")
    img_base64 = get_image_as_base64(IMAGE_PATHS["Top 15 Municipios"])
    if img_base64: st.markdown(f"<img src='data:image/png;base64,{img_base64}' style='width:100%; height:auto;'>", unsafe_allow_html=True)

elif page == "Análisis de Modalidades/Vehículos":
    st.header("3. Análisis de Modalidades y Vehículos")

    st.subheader("Comparativa Autos vs Motos")
    img_base64 = get_image_as_base64(IMAGE_PATHS["Autos vs Motos"])
    if img_base64: st.markdown(f"<img src='data:image/png;base64,{img_base64}' style='width:100%; height:auto;'>", unsafe_allow_html=True)

elif page == "Eficiencia y Capturas":
    st.header("4. Eficiencia y Capturas")

    st.subheader("Tasa de Captura por Nivel")
    img_base64 = get_image_as_base64(IMAGE_PATHS["Tasa de Captura"])
    if img_base64: st.markdown(f"<img src='data:image/png;base64,{img_base64}' style='width:100%; height:auto;'>", unsafe_allow_html=True)

    st.subheader("Eficiencia Policial en Ciudades")
    img_base64 = get_image_as_base64(IMAGE_PATHS["Eficiencia Policial Ciudades"])
    if img_base64: st.markdown(f"<img src='data:image/png;base64,{img_base64}' style='width:100%; height:auto;'>", unsafe_allow_html=True)

elif page == "Evolución Interactivo":
    st.header("Evolución de Hurtos (Gráfico Interactivo)")
    if os.path.exists(INTERACTIVE_HTML_PATH):
        from streamlit.components.v1 import html as st_html
        with open(INTERACTIVE_HTML_PATH, 'r', encoding='utf-8') as f:
            html_content = f.read()
        st_html(html_content, height=600, scrolling=True)
    else:
        st.error(f"Archivo HTML interactivo no encontrado: {INTERACTIVE_HTML_PATH}")

elif page == "Datos Geográficos":
    st.header("Datos de Regiones, Departamentos y Municipios")
    if os.path.exists(GEOGRAPHIC_DATA_PATH):
        df_geo = pd.read_csv(GEOGRAPHIC_DATA_PATH)
        st.dataframe(df_geo)

        st.subheader("Potencial de Visualización Geográfica con Plotly")
        st.write("El archivo `Region_Departamentos_y_municipios_de_Colombia.csv` proporciona la estructura geográfica de Colombia.")
        st.write("Actualmente, este archivo contiene `REGION`, `DEPARTAMENTO`, `MUNICIPIO`, entre otros, pero no incluye columnas de `Latitud` y `Longitud` para una visualización directa en un mapa interactivo usando `st.map()` o `plotly.express` con puntos específicos.")
        st.info("Mostrando las primeras filas del dataset geográfico.")
        st.dataframe(df_geo.head())

    else:
        st.error(f"Archivo CSV de datos geográficos no encontrado: {GEOGRAPHIC_DATA_PATH}")

elif page == "Análisis de Clustering Geográfico":
    st.header("Análisis de Clustering de Municipios")
    if os.path.exists(CLUSTERING_DATA_PATH):
        df_clustering = pd.read_csv(CLUSTERING_DATA_PATH)
        st.write("Este dataset contiene información de municipios, incluyendo latitud, longitud y métricas de hurtos y eficiencia policial, categorizados por clusters.")

        # Mapa interactivo con Plotly Express
        st.subheader("Mapa Interactivo de Municipios por Hurto Promedio")

        # Asegurarse de que las columnas de latitud y longitud sean numéricas
        df_clustering['latitud'] = pd.to_numeric(df_clustering['latitud'], errors='coerce')
        df_clustering['longitud'] = pd.to_numeric(df_clustering['longitud'], errors='coerce')
        df_clustering.dropna(subset=['latitud', 'longitud'], inplace=True)

        fig = px.scatter_mapbox(
            df_clustering,
            lat="latitud",
            lon="longitud",
            color="hurtos_totales_promedio", # Colorear por hurtos promedio
            size="hurtos_totales_promedio",  # Tamaño del punto por hurtos promedio
            hover_name="Municipio",
            hover_data=["Departamento", "tasa_recuperacion", "tasa_captura", "cluster_kmeans_geo1_robusto_limpio_label"],
            color_continuous_scale=px.colors.sequential.Plasma,
            zoom=4,
            height=600,
            title="Municipios de Colombia con Hurtos Promedio (Clustering)"
        )
        fig.update_layout(mapbox_style="open-street-map")
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Primeras filas del dataset de Clustering")
        st.dataframe(df_clustering.head())

    else:
        st.error(f"Archivo CSV de clustering no encontrado: {CLUSTERING_DATA_PATH}")
