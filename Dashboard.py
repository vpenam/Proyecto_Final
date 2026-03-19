import pandas as pd
import streamlit as st
import base64
import os

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


st.sidebar.header("Navegación")
page = st.sidebar.radio("Ir a", [
    "Introducción",
    "Visión General de Hurtos",
    "Análisis de Modalidades/Vehículos",
    "Eficiencia y Capturas",
    "Evolución Interactivo", # Se mantiene por si se quiere añadir después
    "Datos Geográficos" # Se mantiene por si se quiere añadir después
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

        st.subheader("Visualización Simple de Datos Geográficos")
        # Un ejemplo si tuviera columnas de latitud y longitud
        if 'Latitud' in df_geo.columns and 'Longitud' in df_geo.columns:
            st.map(df_geo, latitude='Latitud', longitude='Longitud')
        else:
            st.info("El archivo CSV no contiene columnas 'Latitud' y 'Longitud' para una visualización directa en un mapa de Streamlit. Mostrando las primeras filas.")
            st.dataframe(df_geo.head())
    else:
        st.error(f"Archivo CSV de datos geográficos no encontrado: {GEOGRAPHIC_DATA_PATH}")
