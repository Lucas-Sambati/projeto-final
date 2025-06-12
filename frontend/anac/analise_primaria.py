import streamlit as st
from utils.anac.analise_primaria import grafico_donut_passageiros, tabela_resumo, evolucao_passageiros_mensal, distribuicao_natureza, analise_eficiencia, atk_rtk, grafico_horas_passageiros
from db.anac.banco import execute_query

df = execute_query("SELECT * FROM viagens", return_df=True)
st.title("✈️ Análise de Dados de Voos ANAC")

# Sidebar filters
st.sidebar.subheader("Filtros")

# Year filter
years = st.sidebar.multiselect(
    "Ano:",
    options=sorted(df['ano'].unique()),
    default=sorted(df['ano'].unique())
)

# Month filter
months = st.sidebar.multiselect(
    "Mês:",
    options=sorted(df['mes'].unique()),
    default=sorted(df['mes'].unique())
)

# Company nationality filter
nationalities = st.sidebar.multiselect(
    "Nacionalidade da Empresa:",
    options=df['empresa_nacionalidade'].unique(),
    default=df['empresa_nacionalidade'].unique()
)

# Flight nature filter
natures = st.sidebar.multiselect(
    "Natureza do Voo:",
    options=df['natureza'].unique(),
    default=df['natureza'].unique()
)

# Apply filters
filtered_df = df[
    (df['ano'].isin(years)) &
    (df['mes'].isin(months)) &
    (df['empresa_nacionalidade'].isin(nationalities)) &
    (df['natureza'].isin(natures))
]

col1, col2 = st.columns(2, vertical_alignment="center")
col3, col4 = st.columns(2, vertical_alignment="center")

# LINHA 1
with st.container(border=True):
    with col1:
        evolucao_passageiros_mensal(filtered_df)
    with col2:
        distribuicao_natureza(filtered_df)

with st.container(border=True):
    with col3:
        grafico_horas_passageiros()
    with col4:
        grafico_donut_passageiros()

atk_rtk()
analise_eficiencia(filtered_df)

with st.expander("Mostrar Resumo"):
    tabela_resumo(filtered_df)

