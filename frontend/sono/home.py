import streamlit as st
from utils.sono.home import *

col1, col2 = st.columns([0.9, 0.12],vertical_alignment="bottom")

with col1:
    st.title('DASHBOARD')
with col2:
    with st.popover("Acessibilidade"):
        modo = st.radio("Modo de Visualização", ["Padrão", "Modo daltônico"], key="acessibilidade_radio")
        st.session_state["modo_daltonico"] = (modo == "Modo daltônico")
        
st.subheader('VISÃO GERAL -> SONO, SAÚDE E LIFESTYLE')
st.divider()

col1, col2, col3, col4, col5, col6 = st.columns(6, vertical_alignment="center", border=False)


with st.container():
    with col1:
        st.metric("PESSOAS ANALISADAS", qtd_pessoas_analisadas())

    with col2:
        st.metric("MÉDIA DURAÇÃO SONO", media_duracao_sono())

    with col3:
        st.metric("DISTURBIOS DE SONO", f'{prevalencia_disturbios()}%')

    with col4:
        st.metric("RISCO CARDIOVASCULAR", f'{pessoas_com_risco_cardiovascular()}%')

    with col5:
        st.metric("QUALIDADE MÉDIA DO SONO", media_qualidade_sono())

    with col6:
        st.metric("NÍVEL MÉDIO DE ESTRESSE", media_nivel_estresse())

with st.container():
    st.write('')
    st.write('')
    heatmap_geral()    

with st.expander("Mostrar Tabela"):
    st.dataframe(get_df())
