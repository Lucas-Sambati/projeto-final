import streamlit as st
from db.sono.banco import create_db
from db.anac.banco import create_db_anac

def load_css():
    try:
        with open("style.css") as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.error("Arquivo 'style.css' não encontrado. Crie o arquivo na mesma pasta.")

def main():
    create_db()
    create_db_anac()
    st.set_page_config(layout="wide")
    load_css()    
    
    # SONO
    home_page_sleep = st.Page("frontend/sono/home.py", title="Dashboard", icon="🏠", default=True, url_path="/sono")
    analise_perfil = st.Page("frontend/sono/analise_perfil.py", title="Ánalise de Perfil", icon="🔎", url_path="/analise")
    correlacoes = st.Page("frontend/sono/correlacoes.py", title="Correlações Entre Sono e Estilo de Vida", icon="🔗", url_path="/correlacoes")
    impactos = st.Page("frontend/sono/impactos.py", title="Impacto da Profissão", icon="📈", url_path="/impactos")

    # ANAC
    home_page_anac = st.Page("frontend/anac/home.py", title="Dashboard", icon="🏠", url_path="/anac")
    analise_primaria = st.Page("frontend/anac/analise_primaria.py", title="Análise Primária", icon="🔍", url_path="/analise-primaria")
    rotas_aeroportos = st.Page("frontend/anac/rotas_aeroportos.py", title="Rotas e Aeroportos", icon="✈️", url_path="/rotas")
    eficiencia_operacional = st.Page("frontend/anac/eficiencia_operacional.py", title="Eficiencia Operacional", icon="⚙️", url_path="/eficiencia")
    pages = {
        "Sleep Health and Lifestyle": [home_page_sleep, analise_perfil, correlacoes, impactos],
        "ANAC": [home_page_anac, analise_primaria, rotas_aeroportos, eficiencia_operacional]
    }
    pg = st.navigation(pages)
    pg.run()


if __name__ == "__main__":
    main()