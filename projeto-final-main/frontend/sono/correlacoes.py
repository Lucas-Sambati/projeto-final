import streamlit as st
from utils.sono.correlacoes import heatmap_exercicio_sono, heatmap_stress_sono, heatmap_obesidade_batimentos_sono

st.write("Dashboard")
heatmap_exercicio_sono()

heatmap_stress_sono()

heatmap_obesidade_batimentos_sono()
