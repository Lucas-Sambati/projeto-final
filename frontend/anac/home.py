import streamlit as st
from utils.anac.home import *

st.title('DASHBOARD')
st.subheader('VISÃO GERAL | AGÊNCIA NACIONAL DE AVIAÇÃO CIVIL')
st.divider()

st.write('')


col2, col3, col4, col5, col6 = st.columns(5)

with col2:
    st.metric("TOTAL DE VOOS", total_voos())
with col3:
    st.metric("TOTAL DE PASSAGEIROS", total_passageiros())
with col4:
    st.metric("DISTÂNCIA VOADA", total_distancia_voada())
with col5:
    st.metric("EMPRESA COM MAIS VOOS", empresa_com_mais_voos())
with col6:
    st.metric("VOOS IMPRODUTIVOS (%)", voos_improdutivos())

st.write("## Rotas")
with st.container(border=True):
    aeroportos_unicos()



