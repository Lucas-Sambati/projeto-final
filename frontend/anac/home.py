import streamlit as st
from utils.anac.home import *

st.title('DASHBOARD')
st.subheader('VISÃO GERAL | AGÊNCIA NACIONAL DE AVIAÇÃO CIVIL')
st.divider()

_, col2, col3, col4, col5, _ = st.columns([0.05, 0.225, 0.225, 0.225, 0.225, 0.05])

with col2:
    st.metric("TOTAL DE VOOS", total_voos())
with col3:
    st.metric("TOTAL DE PASSAGEIROS", total_passageiros())
with col4:
    st.metric("DISTÂNCIA VOADA", total_distancia_voada())
with col5:
    st.metric("EMPRESA COM MAIS VOOS", empresa_com_mais_voos())

st.write("## Rotas")
with st.container(border=True):
    aeroportos_unicos()

