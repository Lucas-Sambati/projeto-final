import streamlit as st
from utils.sono.home import heatmap_geral, boxplot_profissao_stress

st.write("Dashboard")
heatmap_geral()

boxplot_profissao_stress()
