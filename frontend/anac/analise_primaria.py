import streamlit as st
from utils.anac.analise_primaria import *
from db.anac.banco import execute_query

df = execute_query("SELECT * FROM viagens", return_df=True)
st.title("✈️ Análise de Dados de Voos ANAC")

# Sidebar filters
st.sidebar.subheader("Filtros")

# 1) Carrega os defaults a partir do DataFrame
default_months = sorted(df['mes'].unique().tolist())
default_nationalities = df['empresa_nacionalidade'].unique().tolist()
default_natures = df['natureza'].unique().tolist()

# 2) Inicializa session_state caso ainda não exista
for key, default in {
    'months': default_months,
    'nationalities': default_nationalities,
    'natures': default_natures
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# 3) Função de reset, que roda ANTES de recriar os widgets
def reset_filters():
    st.session_state.months = default_months
    st.session_state.nationalities = default_nationalities
    st.session_state.natures = default_natures

# 5) Agora os multiselects leem de session_state e você evita reatribuições pós-instanciação
months = st.sidebar.multiselect(
    "Mês:",
    options=default_months,
    default=st.session_state.months,
    key='months'
)

nationalities = st.sidebar.multiselect(
    "Nacionalidade da Empresa:",
    options=default_nationalities,
    default=st.session_state.nationalities,
    key='nationalities'
)

natures = st.sidebar.multiselect(
    "Natureza do Voo:",
    options=default_natures,
    default=st.session_state.natures,
    key='natures'
)

st.sidebar.button("Resetar Filtros", on_click=reset_filters)

# 6) Aplica o filtro
filtered_df = df[
    df['mes'].isin(months) &
    df['empresa_nacionalidade'].isin(nationalities) &
    df['natureza'].isin(natures)
]

col1, col2 = st.columns(2, vertical_alignment="center")
col3, col4 = st.columns(2, vertical_alignment="center")
col5, col6 = st.columns(2, vertical_alignment="center")

# LINHA 1
with st.container(border=True):
    with col1:
        evolucao_passageiros_mensal(filtered_df)
    with col2:
        distribuicao_natureza(filtered_df)

with st.container(border=True):
    with col3:
        atk_rtk(filtered_df)
    with col4:
        grafico_donut_passageiros(filtered_df)

with st.container(border=True):
    with col5:
        grafico_aeroportos_decolagens(filtered_df)
    with col6:
        ask_rpk(filtered_df)
        
analise_eficiencia(filtered_df)

with st.expander("Mostrar Resumo"):
    tabela_resumo(filtered_df)

