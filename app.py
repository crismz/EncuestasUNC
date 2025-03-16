import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# --- Configuraciones pag ---
st.set_page_config(
    page_title="Mi Aplicación"
)

# Título de la aplicación
st.title("Proyecto condiciones de vida y de trabajo en Córdoba")

df = pd.read_csv('results-survey.csv')
st.write("Vista previa de los datos:")
st.dataframe(df)

st.subheader("Control de encuestas")


# --- Ejemplo de gráfico de torta ---
# Teniendo en cuenta que tiene el nombre del encuestador
completadas = 20
no_completadas = 5 

data = [completadas, no_completadas] # Sample data
labels = ['Completas', 'No completas'] # Labels for each slice

# Función para mostrar valores en lugar de porcentajes
def mostrar_valores(pct, valores):
    cantidad = int(round(pct / 100. * sum(valores)))  # Convertir % a cantidad real
    return f"{cantidad}"  # Retorna el número en lugar del porcentaje

fig, ax = plt.subplots(figsize=(6, 6))
# Crear el gráfico de torta con porcentajes dentro de cada sector
ax.pie(data, labels=labels, autopct=lambda pct: mostrar_valores(pct, data), startangle=90, colors=['#66b3ff', '#ff9999'])
plt.title("Encuestas")
st.pyplot(fig) # Show chart


# --- Gráfico de barras para encuestas completadas por encuestador ---
completas_encuestador = {
    'Pedro': 5,
    'Mariela': 3,
    'Pepe': 7,
    'Lucia': 1
}

# Convertir el diccionario en un DataFrame
df_encuestadores = pd.DataFrame(list(completas_encuestador.items()),
                                columns=['Encuestador', 'Encuestas Completadas'])

# Crear el gráfico de barras con Seaborn
fig2, ax2 = plt.subplots(figsize=(8, 4))
sns.barplot(x='Encuestador', y='Encuestas Completadas',
            data=df_encuestadores, palette='viridis', ax=ax2)
ax2.set_title("Encuestas Completadas por Encuestador")
ax2.set_xlabel("Encuestador")
ax2.set_ylabel("Encuestas Completadas")

st.pyplot(fig2)








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