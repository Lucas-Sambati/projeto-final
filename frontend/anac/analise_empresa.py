import streamlit as st
from utils.anac.analise_empresa import grafico_barras, grafico_rpk_empresa, grafico_donut_decolagens, grafico_donut_passageiros, tabela_resumo

st.title("Análise de Empresas Aéreas")

col1, col2 = st.columns(2, vertical_alignment="center", border=True, gap="medium")
col3, col4 = st.columns(2, vertical_alignment="center", border=True, gap="medium")

# LINHA 1
with col1:
    grafico_barras()
with col2:
    grafico_rpk_empresa()
# LINHA 2
with col3:
    grafico_donut_decolagens()
with col4:
    grafico_donut_passageiros()

with st.expander("Mostrar Resumo"):
    tabela_resumo()
