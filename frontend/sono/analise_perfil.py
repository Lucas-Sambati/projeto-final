import streamlit as st
from utils.sono.analise_perfil import tabela_filtragens, grafico_frequencia_categorica, grafico_distribuicao_numerica

col1, col2 = st.columns([0.9, 0.12],vertical_alignment="bottom")

with col1:
    st.title('Análise Perfil')
with col2:
    with st.popover("Acessibilidade"):
        modo = st.radio("Modo de Visualização", ["Padrão", "Modo daltônico"], key="acessibilidade_radio")
        st.session_state["modo_daltonico"] = (modo == "Modo daltônico")

st.divider()
col, _ = st.columns([0.2, 0.8])
with col:
    selecao = st.selectbox("Selecione uma coluna",['idade', 'genero', 'profissao', 'nivel_IMC'])

with st.container():
    if selecao == "idade":
        grafico_distribuicao_numerica(selecao)
    else: 
        grafico_frequencia_categorica(selecao)

with st.expander("Mostrar Filtragem"):
    tabela_filtragens()
