import streamlit as st
from utils.sono.impactos_utils import show_health_risk_per_occupation, show_occupation_count_chart, show_sleep_disorder_frequency_chart, show_stress_level_heart_rate_chart 

st.title("Impacto da Profissão na Saúde do Sono")
show_occupation_count_chart()
show_sleep_disorder_frequency_chart()
show_stress_level_heart_rate_chart()
show_health_risk_per_occupation()

    