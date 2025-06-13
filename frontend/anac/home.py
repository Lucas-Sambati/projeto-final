import streamlit as st
from utils.anac.home import *

col1, col2 = st.columns([0.9, 0.12],vertical_alignment="bottom")

with col1:
    st.title('DASHBOARD')
with col2:
    with st.popover("Acessibilidade"):
        modo = st.radio("Modo de Visualização", ["Padrão", "Modo daltônico"], key="acessibilidade_radio")
        st.session_state["modo_daltonico"] = (modo == "Modo daltônico")
        
st.subheader('VISÃO GERAL | AGÊNCIA NACIONAL DE AVIAÇÃO CIVIL')
st.divider()

col2, col3, col4, col5, col6 = st.columns(5)

with col2:
    st.metric("TOTAL DE VOOS", total_voos())
with col3:
    st.metric("TOTAL DE PASSAGEIROS", total_passageiros())
with col4:
    st.metric("DISTÂNCIA VOADA", total_distancia_voada())
with col5:
    st.metric("EMPRESA COM MAIS VOOS", empresa_com_mais_voos())
with col6:
    st.metric("VOOS IMPRODUTIVOS (%)", voos_improdutivos())

st.divider()
st.write("## Rotas")

query_params = st.query_params
reset_triggered = "reset" in query_params

if reset_triggered:
    st.query_params.clear()

options = st.radio("Filtrar por", ["aeroporto", "país"], horizontal=True)
origin_airport = None
destination_airport = None
origin_country = None
destination_country = None
col1, col2, col3 = st.columns([0.45, 0.45, 0.1], vertical_alignment="bottom")
match options:
    case "aeroporto":
        origin_airport = col1.selectbox(
            "Aeroporto de Origem",
            [""] + get_origin_airport_options(),
            index=0 if reset_triggered else None,
            key="origin_airport"
        )
        destination_airport = col2.selectbox(
            "Aeroporto de Destino",
            [""] + get_destination_airport_options(),
            index=0 if reset_triggered else None,
            key="destination_airport"
        )
    case "país":
        origin_country = col1.selectbox(
            "País de Origem",
            [""] + get_origin_country_options(),
            index=0 if reset_triggered else None,
            key="origin_country"
        )

        destination_country = col2.selectbox(
            "País de Destino",
            [""] + get_destination_country_options(),
            index=0 if reset_triggered else None,
            key="destination_country"
        )

if col3.button("Resetar Filtros"):
    st.query_params["reset"] = "true"
    st.rerun()

def parse_code(option):
    return option.split(" - ")[0] if option else None

with st.container(border=True):
    draw_filtered_map(
        origin_airport=parse_code(origin_airport),
        destination_airport=parse_code(destination_airport),
        origin_country=origin_country if parse_code(origin_country) else None,
        destination_country=destination_country if parse_code(destination_country) else None
    )



