import streamlit as st
from db.banco import create_db

def main():
    create_db()
    st.set_page_config(layout="wide")
    st.markdown(
        """
        <style>
        .stApp { background-color: #F5F7FA; color: #212121; }
        </style>
        """,
        unsafe_allow_html=True,
    )
    
    home_page_sleep = st.Page("frontend/sono/home.py", title="Dashboard", icon="🏠", default=True)
    analise_perfil = st.Page("frontend/sono/analise_perfil.py", title="Ánalise de Perfil", url_path="sono-analise")
    correlacoes = st.Page("frontend/sono/correlacoes.py", title="Correlações Entre Sono e Estilo de Vida", url_path="sono-correlacoes")
    impactos = st.Page("frontend/sono/impactos.py", title="Impacto da Profissão", url_path="sono-impactos")

    home_page_anac = st.Page("frontend/anac/home.py", title="Dashboard", icon="🏠", url_path="anac-home")
    pages = {
        "SONO": [home_page_sleep, analise_perfil, correlacoes, impactos],
        "ANAC": [home_page_anac]
    }
    pg = st.navigation(pages)
    pg.run()


if __name__ == "__main__":
    main()