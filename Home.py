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
st.dataframe(df_surveys)
st.dataframe(df_persons)
 




# if uploaded_file is not None:

#     # Selección de variables (preguntas) a analizar
#     columnas = st.multiselect("Selecciona las preguntas a analizar", df.columns)
    
#     if columnas:
#         # Selección del tipo de gráfico a aplicar para todas las preguntas seleccionadas
#         grafico = st.radio("Selecciona el tipo de gráfico", ("Barra", "Histograma", "Torta"))
        
#         # Generar un gráfico para cada variable seleccionada
#         for col in columnas:
#             st.subheader(f"Análisis de: {col}")
#             fig, ax = plt.subplots()
            
#             if grafico == "Barra":
#                 sns.countplot(y=df[col], ax=ax)
#                 ax.set_title(f"Gráfico de Barras para {col}")
#             elif grafico == "Histograma":
#                 sns.histplot(df[col], kde=True, ax=ax)
#                 ax.set_title(f"Histograma para {col}")
#             elif grafico == "Torta":
#                 df[col].value_counts().plot.pie(autopct='%1.1f%%', ax=ax)
#                 ax.set_ylabel('')
#                 ax.set_title(f"Gráfico de Torta para {col}")
            
#             st.pyplot(fig)
