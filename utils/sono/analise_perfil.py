import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from db.sono.banco import execute_query

def grafico_idade(col):
    df = execute_query(f"SELECT {col} FROM pessoas;", return_df=True)
    fig, ax = plt.subplots(figsize=(10,6))
    sns.histplot(y=col, data=df, ax=ax)
    ax.set_title(f'Frequência de {col}')
    st.pyplot(fig)

def grafico_profissao_stress(col):
    df = execute_query(f"SELECT {col}, nivel_estresse FROM pessoas;", return_df=True)
    fig, ax = plt.subplots()
    sns.barplot(x='nivel_estresse', y=col, data=df, ax=ax)
    ax.set_xlabel('Nível Médio de Estresse')
    ax.set_ylabel(f'{col}')
    ax.set_title(f'Nível Médio de Estresse por {col}')
    st.pyplot(fig)

def grafico_imc_por_profissao():
    df = execute_query("SELECT profissao, nivel_IMC FROM pessoas;", return_df=True)
    fig, ax = plt.subplots(figsize=(12,8))
    sns.boxplot(x='profissao', y='nivel_IMC', data=df, ax=ax)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    ax.set_title('Distribuição de IMC por Profissão')
    st.pyplot(fig)

def tabela_filtragens():
    df = execute_query("SELECT idade, genero, profissao, nivel_IMC, condicao_sono, nivel_estresse FROM pessoas;", return_df=True)

    faixa_etaria = st.slider("Faixa Etária", df['idade'].min(), df['idade'].max(), (df['idade'].min(), df['idade'].max()), 1)
    genero = st.multiselect("Gênero", options=df['genero'].unique(), default=df['genero'].unique())
    profissao = st.multiselect("Profissão", options=df['profissao'].unique(), default=df['profissao'].unique())
    imc = st.multiselect("Categoria IMC", options=df['nivel_IMC'].unique(), default=df['nivel_IMC'].unique())
    disturbio = st.multiselect("Distúrbio do Sono", options=df['condicao_sono'].unique(), default=df['condicao_sono'].unique())

    df_filtrado = df[
        (df['idade'] >= faixa_etaria[0]) & (df['idade'] <= faixa_etaria[1]) &
        (df['genero'].isin(genero)) &
        (df['profissao'].isin(profissao)) &
        (df['nivel_IMC'].isin(imc)) &
        (df['condicao_sono'].isin(disturbio))
    ]

    st.dataframe(df_filtrado)