
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


st.header("Encuestas Completas")

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


# --- Gráfico de barras para encuestas bien cargadas por encuestador (igualdad personas cargadas con mencionadas) ---
st.header("Coincidencia personas encuesta vs personas cargadas")

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

df_discrepancias = df_merged[df_merged["coinciden"] == False].copy()
df_discrepancias = df_discrepancias.rename(columns={
    "Cantidad_mencionada": "Cantidad Personas Hogar",
    "Cantidad": "Cantidad Personas Cargadas"
})

# Selectbox para elegir encuestador
encuestadores = df_discrepancias["Encuestador"].astype(str).unique().tolist()
encuestadores.sort()
opciones = ["Todos"] + encuestadores

sel = st.selectbox("Seleccioná un Encuestador (DNI):", opciones)

# Filtrar según la selección
if sel != "Todos":
    df_filtrado_disc = df_discrepancias[df_discrepancias["Encuestador"].astype(str) == sel]
else:
    df_filtrado_disc = df_discrepancias

if not df_discrepancias.empty:
    st.warning("⚠️ Existen encuestas mal cargadas.")
    st.dataframe(df_filtrado_disc)
else:
    st.success("✅ Todas las encuestas están bien cargadas.")


# --- Gráfico de barras para encuestas bien cargadas por encuestador (datos inconsistentes)---

# --- Validación de reglas por encuesta ---

# Reglas:
#   Regla A: si P7S8 == 2 ==> P7S10 == 2
#   Regla B: si P7S10 == 1  ==>  P7S12 debe estar en [8,9,10,12]
#   Regla C: si P7S10 == 2 ==> P7S12 no debe ser 8
#   Regla D: si P7S8 == 2 ==> P7S15[A1], P7S15[A2], P7S15[A3] no tienen que ser Sí
#   Regla E: si P7S13 == 'Profesional' o P7S13 == 'Técnico' ==> si P3S0 de encuesta Persona == Sí y P3S5 == 6. 'Universitario o terciario completo'
#   Regla F: si P7S12 == 'Servicio doméstico' <==> P7S13 == 'Servicio doméstico en hogares particulares'
#   Regla G: si P9S3 == 'Suficientes para cubrir los gastos del hogar y les permite ahorrar' ==> P9S8 == 'No'
#   Regla H: si P9S3 == 'Insuficientes para cubrir los gastos del hogar' ==> P9S13 == 'No'


df_copy = df_surveys.copy()  # tu DataFrame original
df_personas_copy = df_persons.copy()  # tu DataFrame original

# Juntar los DataFrames por la columna 'P0S6' (Encuesta)
df_copy = df_copy.merge(df_personas_copy[['P0S2', 'P3S0', 'P3S5']], left_on='P0S6',right_on='P0S2', how='left')

# Eliminamos las filas donde el P3S0 es "No"
df_copy = df_copy[df_copy["P3S0"] == "Sí"].copy()

# Booleanos de error
df_copy["Error_A"] = (df_copy["P7S8"] == 'para su propia actividad/ negocio/empresa?') & (df_copy["P7S10"] != 'en el sector privado')  # Regla A
df_copy["Error_B"] = (df_copy["P7S10"] == 'en el sector público-estatal') & (~df_copy["P7S12"].isin(['Administración pública, defensa y seguridad social',
                                                                                                      'Enseñanza',
                                                                                                      'Servicios sociales y de salud',
                                                                                                      'Otros servicios comunitarios, sociales y personales']))   # Regla B
df_copy["Error_C"] = (df_copy["P7S10"] == 'en el sector privado') & (df_copy["P7S12"] == 'Administración pública, defensa y seguridad social')  # Regla C
df_copy["Error_D"] = (df_copy["P7S8"] == 'para su propia actividad/ negocio/empresa?') & (
                        (df_copy["P7S15[A1]"] == 'Sí') | (df_copy["P7S15[A2]"] == 'Sí') | (df_copy["P7S15[A3]"] == 'Sí'))  # Regla D
df_copy["Error_E"] = (
                        (df_copy["P7S13"] == 'Profesional') | (df_copy["P7S13"] == 'Técnico')
                     ) & ~(df_copy["P3S5"] == '6. Universitario o terciario completo')  # Regla E
df_copy["Error_F"] = ((df_copy["P7S12"] == 'Servicio doméstico') & ~(df_copy["P7S13"] == 'Servicio doméstico en hogares particulares')
                      ) | (~(df_copy["P7S13"] == 'Servicio doméstico en hogares particulares') & (df_copy["P7S12"] == 'Servicio doméstico'))  # Regla F
df_copy["Error_G"] = (df_copy["P9S3"] == 'Suficientes para cubrir los gastos del hogar y les permite ahorrar') & (df_copy["P9S8"] != 'No')  # Regla G
df_copy["Error_H"] = (df_copy["P9S3"] == 'Insuficientes para cubrir los gastos del hogar') & (df_copy["P9S13"] != 'No')  # Regla H

# Filtramos sólo las encuestas con al menos un error
df_errors = df_copy[df_copy["Error_A"] | 
                    df_copy["Error_B"] | 
                    df_copy["Error_C"] |
                    df_copy["Error_D"] |
                    df_copy["Error_E"] |
                    df_copy["Error_F"] |
                    df_copy["Error_G"] |
                    df_copy["Error_H"]].copy()

def determine_error_type(row):
    if row["Error_A"]:
        return "Error P7S8(actividad propia) → P7S10(trabajo no privado)"
    elif row["Error_B"]:
        return "Error P7S10(sector público) → P7S12(trabajos no públicos)"
    elif row["Error_C"]:
        return "Error P7S10(sector privado) → P7S12(un trabajo público)"
    elif row["Error_D"]:
        return "Error P7S8(actividad propia) → P7S15(A1,A2,A3)(trabajo propio)"
    elif row["Error_E"]:
        return "Error P7S13(Profesional/Técnico) → P3S5(Universitario o terciario completo)"
    elif row["Error_F"]:
        return "Error P7S12(Servicio doméstico) ↔ P7S13(Servicio doméstico en hogares particulares)"
    elif row["Error_G"]:
        return "Error P9S3(Suficiente ingresos) → P9S8(Usa ahorros)"
    elif row["Error_H"]:
        return "Error P9S3(Insuficiente ingresos) → P9S13(Compra dolares)"
    else:
        return "No Error"

df_errors["Tipo_Error"] = df_errors.apply(determine_error_type, axis=1)

# --- Resumen por encuestador ---
df_summary = (
    df_errors
    .groupby(["P0S1","Tipo_Error"], as_index=False)            
    .agg(Cantidad=("Tipo_Error","size"))                           
)

df_summary.rename(columns={"P0S1":"Encuestador"}, inplace=True)

          
st.header("Errores de validación por encuestador")
st.text("Se buscan inconsistencias en las respuestas de la encuesta. Por ejemplo: si el encuestador responde que trabaja en el sector privado, pero luego indica que su trabajo es en el sector público y viceversa, o si dice que trabaja en su propia actividad, pero luego menciona que fue suspendido, etc.")

# --- Gráfico interactivo con Plotly Express ---
fig = px.bar(
    df_summary,
    x="Cantidad",
    y="Encuestador",
    color="Tipo_Error",
    orientation="h",                                       
    title="Encuestas con errores por encuestador",
    labels={"Cantidad":"Nº de encuestas","Encuestador":"Encuestador"},
)
fig.update_yaxes(tickformat='d', type='category')       

st.plotly_chart(fig, use_container_width=True)


st.subheader("Filtro por Encuestador")

# Prepara la lista de opciones
encuestadores = df_errors['P0S1'].unique().tolist()
encuestadores.sort()
opciones = ['Todos'] + encuestadores

# Widget
sel = st.selectbox("Seleccioná un Encuestador (DNI):", opciones)

# Filtrar
if sel != 'Todos':
    df_filtrado_err = df_errors[df_errors['P0S1'] == sel]
else:
    df_filtrado_err = df_errors

# Mostrar tabla detallada
st.subheader("Detalle de encuestas con errores")
st.dataframe(df_filtrado_err[[
    "P0S1","P0S6","P7S8","P7S10","P7S12", "P7S13", "P7S15[A1]", "P7S15[A2]", "P7S15[A3]", "P3S5", "P9S3", "P9S8", "P9S13", "Tipo_Error"
]].rename(columns={
    "P0S1":"Encuestador",
    "P0S6":"Encuesta",
    "P3S5":"Nivel educativo PSH"
}))


# --- Gráfico de barras para ingresos y suficiencia de ingresos ---

st.header("Ingresos y suficiencia de ingresos")
st.text("Se busca determinar si el ingreso mencionado tiene coherencia con la suficiencia de ingresos.")

# Hacemos una copia del DataFrame original y mostramos solamente las columnas de encuestador, encuestas, P9S2 y P9S3
# Ademas al igual que antes damos el filtro por encuestador

df_ingresos = df_surveys[["P0S1", "P0S6", "P9S2A1", "P9S2A2", "P9S3"]].copy()  # Filtramos las columnas necesarias
df_ingresos.rename(columns={"P0S1": "Encuestador", "P0S6": "Encuesta", "P9S2A1": "Ingreso_valor", "P9S2A2": "Ingreso_opcion", "P9S3": "Suficiencia"}, inplace=True)

# Prepara la lista de opciones
encuestadores = df_ingresos['Encuestador'].unique().tolist()
encuestadores.sort()
opciones = ['Todos'] + encuestadores

# Widget
sel = st.selectbox("Seleccioná un Encuestador (DNI):", opciones)

# Filtrar
if sel != 'Todos':
    df_filtrado_ing = df_ingresos[df_ingresos['Encuestador'] == sel]
else:
    df_filtrado_ing = df_ingresos

# Mostrar tabla detallada
st.subheader("Detalle de encuestas con ingresos y suficiencia")
st.dataframe(df_filtrado_ing[[
    "Encuestador","Encuesta","Ingreso_valor", "Ingreso_opcion", "Suficiencia"
]])