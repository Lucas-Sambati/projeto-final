import streamlit as st
from utils.sono.home import *

st.title('DASHBOARD')
st.subheader('VISÃO GERAL -> SONO, SAÚDE E LIFESTYLE')
st.divider()

with st.container(border=False):
    col1, col2, col3, col4, col5, col6 = st.columns(6, vertical_alignment="center")

    with col1:
        st.metric("PESSOAS ANALISADAS", qtd_pessoas_analisadas())

    with col2:
        st.metric("MÉDIA DURAÇÃO SONO", media_duracao_sono())

    with col3:
        st.metric("DISTURBIOS DE SONO", f'{prevalencia_disturbios()}%')

    with col4:
        st.metric("RISCO CARDIOVASCULAR", f'{pessoas_com_risco_cardiovascular()}%')

    with col5:
        st.metric("QUALDIADE MÉDIA DO SONO", media_qualidade_sono())

    with col6:
        st.metric("QUALIDADE MÉDIA DO SONO", media_nivel_estresse())

with st.container():
    st.write('')
    st.write('')
    heatmap_geral()    

with st.expander("Mostrar Tabela"):
    st.dataframe(get_df())
