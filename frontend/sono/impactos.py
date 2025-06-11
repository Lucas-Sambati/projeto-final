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

with st.container(border=True):
    st.header("1. Distribuição de Profissionais na Amostra")
    show_occupation_count_chart()

st.header("2. Análise Comparativa por Profissão")
col1, col2 = st.columns(2)

with col1:
    with st.container(border=True, height=603):
        st.subheader("Frequência de Distúrbios do Sono")
        show_sleep_disorder_frequency_chart()

with col2:
    with st.container(border=True, height=603):
        st.subheader("Estresse vs. Batimentos Cardíacos")
        show_stress_level_heart_rate_chart()

with st.container(border=True):
    st.header("3. Síntese do Risco de Saúde por Profissão")
    st.markdown("Análise combinada de prevalência de apneia do sono, batimentos cardíacos e nível de estresse.")
    show_health_risk_per_occupation()

    