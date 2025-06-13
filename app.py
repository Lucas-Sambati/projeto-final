import streamlit as st
from db.sono.banco import create_db
from db.anac.banco import create_db_anac
import plotly.express as px


def load_css():
    try:
        with open("style.css") as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.error("Arquivo 'style.css' não encontrado. Crie o arquivo na mesma pasta.")





def define_paginas():
    # Definição das páginas (só após acessibilidade estar definida)
    home_page_sleep = st.Page("frontend/sono/home.py", title="Dashboard", icon="🏠", default=True, url_path="/sono")
    analise_perfil = st.Page("frontend/sono/analise_perfil.py", title="Ánalise de Perfil", icon="🔎", url_path="/analise")
    correlacoes = st.Page("frontend/sono/correlacoes.py", title="Correlações Entre Sono e Estilo de Vida", icon="🔗", url_path="/correlacoes")
    impactos = st.Page("frontend/sono/impactos.py", title="Impacto da Profissão", icon="📈", url_path="/impactos")

    home_page_anac = st.Page("frontend/anac/home.py", title="Dashboard", icon="🏠", url_path="/anac")
    analise_primaria = st.Page("frontend/anac/analise_primaria.py", title="Análise Primária", icon="🔍", url_path="/analise-primaria")

    return {
        "Sleep Health and Lifestyle": [home_page_sleep, analise_perfil, correlacoes, impactos],
        "ANAC": [home_page_anac, analise_primaria]
    }


def main():
    create_db()
    create_db_anac()
    st.set_page_config(layout="wide")
    load_css()

    # Acessibilidade ANTES da definição das páginas

    # Só depois disso criamos e executamos as páginas
    pages = define_paginas()
    pg = st.navigation(pages)
    pg.run()


if __name__ == "__main__":
    main()
