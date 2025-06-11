import streamlit as st
from utils.anac.home import *

st.title('DASHBOARD')
st.subheader('VISÃO GERAL | AGÊNCIA NACIONAL DE AVIAÇÃO CIVIL', divider='gray')

st.write('')


col1, col2, col3, col4, col5, col6 = st.columns(6)

with col2:
    colored_metric("TOTAL DE VOOS", total_voos(), "#0C3C78")
with col3:
    colored_metric("TOTAL DE PASSAGEIROS", total_passageiros(), "#0C3C78")
with col4:
    colored_metric("DISTÂNCIA VOADA", total_distancia_voada(), "#0C3C78")
with col5:
    colored_metric("EMPRESA COM MAIS VOOS", empresa_com_mais_voos(), "#0C3C78")

st.write('')

aeroportos_unicos()

