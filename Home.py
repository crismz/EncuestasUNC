import streamlit as st
import pandas as pd



# --- Configuraciones pag ---
st.set_page_config(
    page_title="Mi Aplicación"
)

# Título de la aplicación
st.title("Proyecto condiciones de vida y de trabajo en Córdoba")

df_surveys = pd.read_csv('results-survey.csv')
df_persons = pd.read_csv('results-survey-person.csv')

st.write("Vista previa de los datos:")

st.subheader("Encuestas generales")

# Filtrar según la selección del DNI y/o id de encuesta
# DNI de encuestador: P0S1
# Id de la encuesta:  P0S6

## Selector de encuestador
encuestadores_surveys = df_surveys["P0S1"].astype(str).unique().tolist()
encuestadores_surveys.sort()
opciones_encuestadores_surveys = ["Todos"] + encuestadores_surveys
sel_encuestadores_surveys = st.selectbox("Seleccioná un Encuestador (DNI):", opciones_encuestadores_surveys)
if sel_encuestadores_surveys != "Todos":
    df_filtrado_surveys = df_surveys[df_surveys["P0S1"].astype(str) == sel_encuestadores_surveys]
else:
    df_filtrado_surveys = df_surveys

## Selector de encuesta
encuestas_disponibles_surveys = df_filtrado_surveys["P0S6"].astype(str).unique().tolist()
encuestas_disponibles_surveys.sort()
opciones_encuestas_surveys = ["Todos"] + encuestas_disponibles_surveys
sel_encuestas_surveys = st.selectbox("Seleccioná una Encuesta (ID):", opciones_encuestas_surveys)

## Filtro de datos según la encuesta y encuestador seleccionados
if sel_encuestadores_surveys != "Todos":
    df_filtrado_surveys = df_filtrado_surveys[df_filtrado_surveys["P0S1"].astype(str) == sel_encuestadores_surveys]
if sel_encuestas_surveys != "Todos":
    df_filtrado_surveys = df_filtrado_surveys[df_filtrado_surveys["P0S6"].astype(str) == sel_encuestas_surveys]

## Mostramos dataframe filtrado
st.dataframe(df_filtrado_surveys)


st.subheader("Encuestas de personas")

# Lo mismo pero para la df_persons

## Selector de encuestador
encuestadores_persons = df_persons["P0S1"].astype(str).unique().tolist()
encuestadores_persons.sort()
opciones_encuestadores_persons = ["Todos"] + encuestadores_persons
sel_encuestadores_persons = st.selectbox("Seleccioná un Encuestador (DNI):", opciones_encuestadores_persons)
if sel_encuestadores_persons != "Todos":
    df_filtrado_persons = df_persons[df_persons["P0S1"].astype(str) == sel_encuestadores_persons]
else:
    df_filtrado_persons = df_persons

## Selector de encuesta
encuestas_disponibles_persons = df_filtrado_persons["P0S2"].astype(str).unique().tolist()
encuestas_disponibles_persons.sort()
opciones_encuestas_persons = ["Todos"] + encuestas_disponibles_persons
sel_encuestas_persons = st.selectbox("Seleccioná una Encuesta (ID):", opciones_encuestas_persons)

## Filtro de datos según la encuesta y encuestador seleccionados
if sel_encuestadores_persons != "Todos":
    df_filtrado_persons = df_filtrado_persons[df_filtrado_persons["P0S1"].astype(str) == sel_encuestadores_persons]
if sel_encuestas_persons != "Todos":
    df_filtrado_persons = df_filtrado_persons[df_filtrado_persons["P0S2"].astype(str) == sel_encuestas_persons]

## Mostramos dataframe filtrado
st.dataframe(df_filtrado_persons)
 
