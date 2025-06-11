import streamlit as st
from utils.anac.analise_empresa import grafico_barras, grafico_rpk_empresa, grafico_donut_decolagens, grafico_donut_passageiros, tabela_resumo

st.title("Análise de Empresas Aéreas")

grafico_barras()

grafico_rpk_empresa()

grafico_donut_decolagens()

grafico_donut_passageiros()

tabela_resumo()
