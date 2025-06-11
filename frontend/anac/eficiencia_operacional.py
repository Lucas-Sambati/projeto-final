import streamlit as st
from utils.anac.eficiencia_operacional import *

grafico_combustivel_voos()

st.dataframe(grafico_horas_passageiros())