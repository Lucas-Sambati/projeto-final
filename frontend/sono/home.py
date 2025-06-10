import streamlit as st
from utils.sono.home import *

st.title('DASHBOARD')
st.subheader('VISÃO GERAL | SONO, SAÚDE E LIFESTYLE', divider='gray')

st.write('')
st.write('')


col1, col2, col3, col5, col6, col7 = st.columns(6)

with col1:
    colored_metric("PROFISSÃO MAIS ESTRESSANTE", profissao_mais_estressante(), "#0C3C78")
with col2:
    colored_metric("PESSOAS ANALISADAS", qtd_pessoas_analisadas(), "#333333")
with col3:
    colored_metric("MÉDIA DE IDADE", media_idade(), "#333333")

with col5:
    colored_metric("MÉDIA DURAÇÃO SONO", media_duracao_sono(), "#2E7D32")
with col6:
    colored_metric("DISTURBIOS DE SONO", f'{prevalencia_disturbios()}%', "#EF6C00")
with col7:
    colored_metric("RISCO CARDIOVASCULAR", f'{pessoas_com_risco_cardiovascular()}%', "#C62828")
