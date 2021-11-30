import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

def filtrar_weekly(weekly, num):

    num_weeklies = weekly.groupby(['Email con el que nos comunicamos contigo']).count()['#']
    alumnos_completos = num_weeklies[num_weeklies.sort_values(ascending=False) > num].index.tolist()

    return weekly[weekly['Email con el que nos comunicamos contigo'].isin(alumnos_completos)]


def filtrar_completos(weekly):

    formato_full = weekly['¿En qué horario estás cursando tu programa?'] == 'Full-time'
    ultima_full = weekly['semana'] == 14

    formato_part = weekly['¿En qué horario estás cursando tu programa?'] == 'Part-time'
    ultima_part = weekly['semana'] == 25

    alumnos_completos = weekly.loc[(formato_full & ultima_full) | (formato_part & ultima_part)]['Email con el que nos comunicamos contigo'].tolist()
    return weekly[weekly['Email con el que nos comunicamos contigo'].isin(alumnos_completos)]

def formato(agrupados_vert,bootcamps, formato):

    st.subheader(formato)

    plot_info(agrupados_vert, bootcamps, formato, '¿Cómo te ha resultado el ritmo de la clase esta semana?')
    plot_info(agrupados_vert, bootcamps, formato,
                 '¿Cómo describirías la dificultad de la materia de la última semana?')
    plot_info(agrupados_vert, bootcamps, formato, '¿Qué puntuación general le darías a esta última semana?')


def plot_info(agrupados_vert, bootcamps, formato, pregunta):

    with st.beta_expander(pregunta):
        idx = pd.IndexSlice
        st.subheader(pregunta)

        fig = plt.figure(figsize=(18, 6))
        fig.show()
        ax = fig.add_subplot(111)

        for bootcamp in bootcamps:
            try:
                datos = agrupados_vert.loc[idx[formato, bootcamp, :]]
                ax.plot(datos.index.get_level_values(2),
                         datos[(pregunta, 'mean')].tolist(), marker='',
                         linewidth=1, alpha=0.9, label=bootcamp)
            except:
                st.write(f'No hay alumnos de {bootcamp} que hayan finalizado los weeklies.')
        plt.legend(loc=2)
        st.pyplot(fig)