import streamlit as st
import pandas as pd
import functions as ft
st.set_page_config(layout='wide')

csv = st.sidebar.file_uploader("CSV:")
try:
    weekly = pd.read_csv(csv, sep = ';', parse_dates = [22])
except:
    st.warning("Introduce el csv del weekly.")
    st.stop()
weekly['fecha inicio promocion'] = pd.to_datetime(weekly['fecha inicio promocion'], format='%d/%m/%Y')
weekly['semana'] = ((weekly['Submit Date (UTC)'] - weekly['fecha inicio promocion']) / 7).dt.days

completos = st.slider("Numero mínimo de weeklies que ha realizado un alumno para aparecer en la gráfica.", max_value=30)

if completos:
    weekly = ft.filtrar_weekly(weekly, completos)


agrupados_vert = weekly.groupby(['¿En qué horario estás cursando tu programa?',
                                 '¿Qué programa estás cursando?',
                                 'semana']).agg({'¿Cómo te ha resultado el ritmo de la clase esta semana?': 'mean',
                                                 '¿Cómo describirías la dificultad de la materia de la última semana?': 'mean',
                                                 '¿Qué puntuación general le darías a esta última semana?': ['mean', 'count']})


#st.subheader('Filtrar bootcamp:')
bootcamps = st.multiselect('selecciona los bootcamps que te interesan (si no añades ninguno apareceran todos):',
                           options=weekly['¿Qué programa estás cursando?'].unique().tolist())


if bootcamps == list():
    bootcamps = weekly['¿Qué programa estás cursando?'].unique().tolist()

ft.formato(agrupados_vert, bootcamps, 'Full-time')

ft.formato(agrupados_vert, bootcamps, 'Part-time')




#formato = st.selectbox('selecciona formato:', options=weekly['¿En qué horario estás cursando tu programa?'].unique().tolist())
#metrica = st.multiselect('selecciona metrica:', options=['¿Cómo te ha resultado el ritmo de la clase esta semana?',
#                                                       '¿Cómo describirías la dificultad de la materia de la última semana?',
#                                                       '¿Qué puntuación general le darías a esta última semana?'])
#agrupados_clase = weekly.groupby(['¿En qué horario estás cursando tu programa?',
#                                  '¿Qué programa estás cursando?',
#                                  '¿Cuál es el código de la edición de tu programa?',
#                                  'semana']).agg({'¿Cómo te ha resultado el ritmo de la clase esta semana?': 'mean',
#                                                  '¿Cómo describirías la dificultad de la materia de la última semana?': 'mean',
#                                                  '¿Qué puntuación general le darías a esta última semana?': ['mean', 'count']})
