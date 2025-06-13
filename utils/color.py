import streamlit as st
import plotly.express as px

def get_color():
    modo = st.session_state.get("modo_daltonico", False)
    if modo:
        return px.colors.qualitative.Safe  # Paleta segura para daltônicos
    else:
        return px.colors.diverging.RdBu_r  # Paleta padrão
    
def get_color_correlacoes_sono():
    modo = st.session_state.get("modo_daltonico", False)
    if modo:
        return px.colors.qualitative.Safe  # Paleta segura para daltônicos
    else:
        return 'Blues'  # Paleta padrão