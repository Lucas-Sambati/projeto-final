import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from db.sono.banco import execute_query
from io import BytesIO
import plotly.express as px
import plotly.graph_objects as go

@st.cache_data
def grafico_distribuicao_numerica(coluna_numerica):
    df = execute_query(f"SELECT {coluna_numerica} FROM pessoas;", return_df=True)
    
    df["idade_agrupada"] = (df[coluna_numerica] // 5) * 5
    frequencias = df["idade_agrupada"].value_counts().sort_index()

    hist_df = pd.DataFrame({
        "Idade": frequencias.index,
        "Frequencia": frequencias.values
    })
        
    fig = px.bar(
            hist_df,
            x='Idade',
            y='Frequencia',
            orientation='v',
            title=f"Distribuição de Pessoas por {coluna_numerica}",
            color_discrete_sequence=px.colors.diverging.RdBu_r,
            height=600
        )
    st.plotly_chart(fig, use_container_width=True)

def grafico_frequencia_categorica(coluna_categorica):
    df = execute_query(f"SELECT {coluna_categorica} FROM pessoas;", return_df=True)

    contagem = df[coluna_categorica].value_counts().reset_index()
    contagem.columns = [coluna_categorica, 'Frequência']

    fig = px.bar(
            contagem,
            x='Frequência',
            y=coluna_categorica,
            orientation='h',
            color=coluna_categorica,
            color_discrete_sequence=px.colors.diverging.RdBu_r,
            title=f"Distribuição de Pessoas por {coluna_categorica}",
            height=600
        )
    st.plotly_chart(fig, use_container_width=True)
    

def tabela_filtragens():
    df = execute_query("SELECT idade, genero, profissao, nivel_IMC, condicao_sono, nivel_estresse FROM pessoas;", return_df=True)

    with st.container():
        min_idade_df = df['idade'].min()
        max_idade_df = df['idade'].max()

        col1, col2 = st.columns(2)
        col3, col4 = st.columns(2)

        with col1:
            opcoes_genero = df['genero'].unique()
            genero_selecionado = st.multiselect(
                "Gênero",
                options=opcoes_genero,
                default=None
            )
        with col2:
            opcoes_profissao = df['profissao'].unique()
            profissao_selecionada = st.multiselect(
                "Profissão",
                options=opcoes_profissao,
                default=None
            )
        with col3:
            opcoes_imc = df['nivel_IMC'].unique()
            imc_selecionado = st.multiselect(
                "Categoria IMC",
                options=opcoes_imc,
                default=None
            )
        with col4:
            opcoes_disturbio = df['condicao_sono'].unique()
            disturbio_selecionado = st.multiselect(
                "Distúrbio do Sono",
                options=opcoes_disturbio,
                default=None
            )

        _, slider, _ = st.columns([0.01, 0.98, 0.01])
        with slider:
            faixa_etaria = st.slider(
            "Faixa Etária",
            min_idade_df,
            max_idade_df,
            (min_idade_df, max_idade_df),
            1
            )

    condicao_final = pd.Series(True, index=df.index)

    condicao_idade = (df['idade'] >= faixa_etaria[0]) & (df['idade'] <= faixa_etaria[1])
    condicao_final = condicao_final & condicao_idade

    if genero_selecionado:
        condicao_final = condicao_final & (df['genero'].isin(genero_selecionado))

    if profissao_selecionada:
        condicao_final = condicao_final & (df['profissao'].isin(profissao_selecionada))

    if imc_selecionado:
        condicao_final = condicao_final & (df['nivel_IMC'].isin(imc_selecionado))

    if disturbio_selecionado:
        condicao_final = condicao_final & (df['condicao_sono'].isin(disturbio_selecionado))

    df_filtrado = df[condicao_final]

    st.dataframe(df_filtrado, use_container_width=True)
