from utils.anac.rotas_aeroportos import *
import streamlit as st

st.title("Top 10 Aeroportos por categoria")
grafico_aeroportos_maior_carga()
st.write("""
Vemos que o aeroporto com mais carga transportada foi o Aeroporto Internacional Murtala Muhammed, da Nigéria
""")

grafico_aeroportos_mais_passageiros()
st.write("""
Vemos que o aeroporto com mais passageiros transportados foi o Aeroporto Internacional de Hamad, do Catar
""")