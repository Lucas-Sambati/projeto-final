import streamlit as st
from utils.anac.home import *

st.title('DASHBOARD')
st.subheader('VISÃO GERAL | AGÊNCIA NACIONAL DE AVIAÇÃO CIVIL', divider='gray')

st.write('')
st.write('')


col1, col2, col3, col5, col6, col7 = st.columns(6)

with col1:
    colored_metric("EMPRESA COM MAIS VOOS", empresa_com_mais_voos(), "#0C3C78")
with col2:
    colored_metric("EMPRESA COM MAIS VOOS", empresa_com_mais_voos(), "#0C3C78")

