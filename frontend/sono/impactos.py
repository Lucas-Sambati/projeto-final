import streamlit as st
from utils.sono.impactos_utils import (
    show_health_risk_per_occupation, 
    show_occupation_count_chart, 
    show_sleep_disorder_frequency_chart, 
    show_stress_level_heart_rate_chart
)

st.title("Impacto da Profissão na Saúde do Sono")
st.markdown("""
Este dashboard analisa como diferentes profissões se relacionam com a qualidade do sono, níveis de estresse e saúde cardíaca.
""")


st.header("1. Distribuição de Profissionais na Amostra")
with st.container():
    show_occupation_count_chart()

st.divider()

st.header("2. Análise Comparativa por Profissão")
with st.container(border=True):
    col1, col2 = st.columns(2)

    with col1:
        show_sleep_disorder_frequency_chart()

    with col2:
        show_stress_level_heart_rate_chart()

st.divider()

st.header("3. Síntese do Risco de Saúde por Profissão")
with st.container():
    show_health_risk_per_occupation()

    