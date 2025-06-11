import streamlit as st
from utils.sono.analise_perfil import tabela_filtragens, grafico_frequencia_categorica, grafico_distribuicao_numerica

st.title("Análise Perfil")
st.divider()
col, _ = st.columns([0.2, 0.8])
with col:
    selecao = st.selectbox("Selecione uma coluna",['idade', 'genero', 'profissao', 'nivel_IMC'])

with st.container(border=True):
    if selecao == "idade":
        grafico_distribuicao_numerica(selecao)
    else: 
        grafico_frequencia_categorica(selecao)


tabela_filtragens()
