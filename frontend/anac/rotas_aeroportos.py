from utils.anac.rotas_aeroportos import *
import streamlit as st

st.markdown("""
<style>
.big-font {
    margin: auto;
    font-size:24px !important;
    padding:0px 48px 16px 48px;
    text-align:justify;
    align-items: center;
    align-content: center;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

st.title("Top 10 Aeroportos por categoria")

col0 = st.columns(1, gap='medium', border=True)[0]
with col0:
    grafico_aeroportos_decolagens()

col1, col2 = st.columns(2, gap='medium', border=True)
with col1:
    grafico_aeroportos_maior_carga()
    st.markdown('<p class="big-font">Vemos que o aeroporto com mais carga transportada foi o Aeroporto Internacional Murtala Muhammed, da Nigéria</p>', unsafe_allow_html=True)

with col2:
    grafico_aeroportos_mais_passageiros()
    st.markdown('<p class="big-font">Vemos que o aeroporto com mais passageiros transportados foi o Aeroporto Internacional de Hamad, do Catar</p>', unsafe_allow_html=True)
