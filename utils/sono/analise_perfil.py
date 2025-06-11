import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from db.sono.banco import execute_query
from io import BytesIO

def grafico_distribuicao_numerica(coluna_numerica):
    df = execute_query(f"SELECT {coluna_numerica} FROM pessoas;", return_df=True)

    fig, ax = plt.subplots(figsize=(10, 6))

    sns.histplot(data=df, x=coluna_numerica, kde=True, ax=ax,
                 color="#4CAF50",
                 edgecolor="black", bins=15)

    ax.set_title(f'Distribuição de {coluna_numerica.replace("_", " ").title()}', fontsize=16) 
    ax.set_xlabel(f'{coluna_numerica.replace("_", " ").title()}', fontsize=12)
    ax.set_ylabel('Frequência', fontsize=12)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    buf = BytesIO()
    fig.savefig(buf, format="png", dpi=100, bbox_inches='tight')
    buf.seek(0)

    st.image(buf, width=1000)  

    plt.close(fig)

def grafico_frequencia_categorica(coluna_categorica):
    df = execute_query(f"SELECT {coluna_categorica} FROM pessoas;", return_df=True)

    contagem = df[coluna_categorica].value_counts().reset_index()
    contagem.columns = [coluna_categorica, 'Frequência']

    fig, ax = plt.subplots(figsize=(10, 6))

    sns.barplot(x='Frequência', y=coluna_categorica, data=contagem, ax=ax,
                palette="pastel", 
                orient='h')

    ax.set_title(f'Frequência por {coluna_categorica.replace("_", " ").title()}', fontsize=16)
    ax.set_xlabel('Número de Pessoas', fontsize=12)
    ax.set_ylabel(f'{coluna_categorica.replace("_", " ").title()}', fontsize=12)
    ax.tick_params(axis='y', labelsize=10) 
    ax.invert_yaxis() 

    buf = BytesIO()
    fig.savefig(buf, format="png", dpi=100, bbox_inches='tight')
    buf.seek(0)

    st.image(buf, width=1000)  

    plt.close(fig)

def tabela_filtragens():
    df = execute_query("SELECT idade, genero, profissao, nivel_IMC, condicao_sono, nivel_estresse FROM pessoas;", return_df=True)

    with st.container(border=True):
        min_idade_df = df['idade'].min()
        max_idade_df = df['idade'].max()
        faixa_etaria = st.slider(
            "Faixa Etária",
            min_idade_df,
            max_idade_df,
            (min_idade_df, max_idade_df),
            1
        )

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
