import streamlit as st
from db.banco import create_db

def main():
    create_db()

    # SONO
    home_page_sleep = st.Page("frontend/sono/home.py", title="Dashboard", icon="🏠", default=True, url_path="/sono")
    analise_perfil = st.Page("frontend/sono/analise_perfil.py", title="Ánalise de Perfil", icon="🔎", url_path="/analise")
    correlacoes = st.Page("frontend/sono/correlacoes.py", title="Correlações Entre Sono e Estilo de Vida", icon="🔗", url_path="/correlacoes")
    impactos = st.Page("frontend/sono/impactos.py", title="Impacto da Profissão", icon="📈", url_path="/impactos")

    # ANAC
    home_page_anac = st.Page("frontend/anac/home.py", title="Dashboard", icon="🏠", url_path="/anac")
    pages = {
        "Sleep Health and Lifestyle": [home_page_sleep, analise_perfil, correlacoes, impactos],
        "ANAC": [home_page_anac]
    }
    pg = st.navigation(pages)
    pg.run()


if __name__ == "__main__":
    main()