import streamlit as st
from utils.anac.eficiencia_operacional import *

col1, col2, col3 = st.columns(3, gap='medium', border=True)
with col1:
    grafico_combustivel_voos()

with col2:
    grafico_horas_passageiros()

with col3:
    atk_rtk()