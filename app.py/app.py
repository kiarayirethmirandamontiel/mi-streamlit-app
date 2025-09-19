"""
app.py
Streamlit app para EDA y recomendación básica (Crop Recommendation Dataset).
Guarde este archivo en la raíz del proyecto (junto a la carpeta data/).
"""

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

st.set_page_config(page_title="Recomendación de Cultivos", layout="wide")

# -------------------------
# 1) Cargar y validar datos
# -------------------------
DATA_PATH = os.path.join("data", "Crop_recommendation.csv")

@st.cache_data
def cargar_datos(path=DATA_PATH):
    if not os.path.exists(path):
        # Intentar buscar en 'archive' si no está en 'data'
        alt_path = os.path.join("archive", "Crop_recommendation.csv")
        if os.path.exists(alt_path):
            path = alt_path
        else:
            raise FileNotFoundError(f"Archivo no encontrado en 'data' ni en 'archive': {path}")
    df = pd.read_csv(path)
    # Normalizar nombres de columnas (quita espacios)
    df.columns = [c.strip() for c in df.columns]
    # Si la etiqueta de cultivo no se llama 'label', intentar renombrar
    if 'label' not in df.columns and 'Crop' in df.columns:
        df = df.rename(columns={'Crop': 'label'})
    return df

try:
    df = cargar_datos()
except Exception as e:
    st.error(f"Error al cargar datos: {e}")
    st.stop()

# -------------------------
# 2) Interfaz principal
# -------------------------
st.title("🌱 Recomendación de Cultivos - Análisis Exploratorio")
st.markdown("Explora el dataset y prueba filtros. Ajusta el código si los nombres de columna son distintos.")

# Mostrar columnas detectadas
st.write("Columnas del dataset:", list(df.columns))

# -------------------------
# 3) Vista y estadísticas
# -------------------------
st.subheader("Vista previa de los datos")
st.dataframe(df.head())

st.subheader("Estadísticas descriptivas (variables numéricas)")
num_cols = ['N','P','K','temperature','humidity','ph','rainfall']
present_num_cols = [c for c in num_cols if c in df.columns]
st.dataframe(df[present_num_cols].describe().T)

# -------------------------
# 4) Filtro por cultivo
# -------------------------
if 'label' in df.columns:
    cultivo = st.selectbox("Selecciona un cultivo", df["label"].unique())
    df_filtrado = df[df["label"] == cultivo]
    st.subheader(f"Distribución de variables para {cultivo}")
    st.write(df_filtrado.describe())
else:
    st.warning("La columna de etiqueta 'label' no está en el dataset. Verifique los nombres de columna.")

# -------------------------
# 5) Visualizaciones interactivas
# -------------------------
st.subheader("Relación entre variables")
# Permitir solo columnas numéricas para X e Y
opts = present_num_cols if present_num_cols else list(df.select_dtypes(include='number').columns)
columna_x = st.selectbox("Selecciona variable X", opts)
columna_y = st.selectbox("Selecciona variable Y", opts)

fig, ax = plt.subplots()
sns.scatterplot(data=df, x=columna_x, y=columna_y, hue=(df['label'] if 'label' in df.columns else None),
                palette="tab10", alpha=0.7, ax=ax)
ax.set_xlabel(columna_x)
ax.set_ylabel(columna_y)
st.pyplot(fig, use_container_width=True)
