
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

from Home import df_surveys
from Home import df_persons

# --- Barra de progreso encuestas  ---
# Teniendo en cuenta que tiene el nombre del encuestador
total = 1000
completadas = df_surveys['submitdate'].notnull().sum() 

data = [total, completadas] # Sample data
labels = ['Total', 'Completadas'] # Labels for each slice

st.write(f"Progreso: {completadas} de {total} encuestas completadas.")
st.progress(completadas / total)


# --- Gráfico de barras para encuestas completadas por encuestador ---
# Conteo de encuestas completadas por encuestador
completas_encuestador = df_surveys['P0S1'].value_counts()

# Convertir el diccionario en un DataFrame
df_encuestadores = pd.DataFrame(list(completas_encuestador.items()),
                                columns=['Encuestador', 'Encuestas Completadas'])
# Llevamos a string la columna de Encuestador
df_encuestadores['Encuestador'] = df_encuestadores['Encuestador'].apply(lambda x: str(int(x)) if pd.notnull(x) else "")

# Crear el gráfico de barras
fig2 = px.bar(
    df_encuestadores,
    x='Encuestas Completadas',
    y='Encuestador',
    orientation='h',  # Para barras horizontales
    title='Encuestas Completadas por Encuestador',
    labels={'Encuestas Completadas': 'Encuestas Completadas', 'Encuestador': 'Encuestador'},
    color_continuous_scale='Viridis' # Paleta de colores
)

fig2.update_yaxes(tickformat='d', type='category')

# Mostrar el gráfico en Streamlit
st.plotly_chart(fig2, use_container_width=True)


# --- Gráfico de barras para encuestas bien cargadas por encuestador ---
df_persons_count = df_persons.groupby(["P0S1", "P0S2"]).size().reset_index(name="conteo_filas")
df_persons_count.columns = ['Encuestador', 'Encuesta', 'Cantidad']

df_surveys_encuestas = df_surveys[['P0S1', 'P0S6', 'P2']].copy()
df_surveys_encuestas.columns = ['Encuestador', 'Encuesta', "Cantidad_mencionada"]

df_merged = df_surveys_encuestas.merge(df_persons_count, on=["Encuestador", 'Encuesta'], how="left")
df_merged["coinciden"] = df_merged["Cantidad_mencionada"] == df_merged["Cantidad"]

df_summary = df_merged.groupby(["Encuestador", "coinciden"]).size().reset_index(name="Cantidad")

df_summary["Estado"] = df_summary["coinciden"].map({True: "Bien Cargadas", False: "Mal Cargadas"})

df_plot = df_summary[['Encuestador', 'Estado', 'Cantidad']]

fig = px.bar(
    df_plot,
    x='Cantidad',
    y='Encuestador',
    color='Estado',
    orientation='h',
    hover_data=['Cantidad'],  # Muestra la cantidad en el tooltip
    labels={'Encuestador': 'Encuestador', 'Cantidad': 'Cantidad'},
    title='Coincidencia de personas de Encuesta por Encuestador',
    color_discrete_map={'Bien Cargadas': 'green', 'Mal Cargadas': 'red'}  # Colores personalizados
)
fig.update_yaxes(tickformat='d', type='category')
# Mostrar el gráfico en Streamlit
st.plotly_chart(fig)

df_discrepancias = df_merged[df_merged["coinciden"] == False]
if not df_discrepancias.empty:
    st.warning("⚠️ Existen encuestas mal cargadas.")
    st.dataframe(df_discrepancias)
else:
    st.success("✅ Todas las encuestas están bien cargadas.")