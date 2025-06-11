import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from db.anac.banco import execute_query

def grafico_barras():
    df = execute_query("SELECT sigla_empresa, natureza, SUM(decolagens) AS decolagens FROM viagens GROUP BY sigla_empresa, natureza ORDER BY decolagens DESC", return_df=True)

    total_decolagens = df.groupby('sigla_empresa')['decolagens'].sum().reset_index()
    top_empresas = total_decolagens.nlargest(10, 'decolagens')['sigla_empresa']
    df_top = df[df['sigla_empresa'].isin(top_empresas)]

    fig, ax = plt.subplots()
    sns.barplot( y='sigla_empresa', x='decolagens', hue='natureza', data=df_top, ax=ax, order=top_empresas)
    ax.set_title('Top 10 Empresas com Mais Decolagens', fontsize=16)
    ax.set_xlabel('Quantidade de Decolagens', fontsize=12)
    ax.set_ylabel('Empresa', fontsize=12)
    st.pyplot(fig)

def grafico_rpk_empresa():
    df = execute_query("SELECT sigla_empresa, SUM(rpk) AS total_rpk FROM viagens GROUP BY sigla_empresa ORDER BY total_rpk DESC", return_df=True)
    df_top = df.nlargest(20, 'total_rpk')
    fig, ax = plt.subplots()
    sns.barplot(x='total_rpk', y='sigla_empresa', data=df, ax=ax, order=df_top['sigla_empresa'])
    ax.set_title('Empresas com Mais RPK(Revenue Passenger Kilometers)', fontsize=16)
    ax.set_xlabel('RPK Total', fontsize=12)
    ax.set_ylabel('Empresa', fontsize=12)
    st.pyplot(fig)

def grafico_donut_decolagens():
    df = execute_query("SELECT sigla_empresa, SUM(decolagens) AS total_decolagens FROM viagens GROUP BY sigla_empresa ORDER BY total_decolagens DESC", return_df=True)
    df['participacao_mercado'] = df['total_decolagens'] / df['total_decolagens'].sum()

    top_empresas = df.nlargest(4, 'participacao_mercado')
    outros = pd.DataFrame({
        'sigla_empresa': ['Outros'],
        'total_decolagens': [df['total_decolagens'].sum() - top_empresas['total_decolagens'].sum()],
        'participacao_mercado': [1 - top_empresas['participacao_mercado'].sum()]
    })

    df_final = pd.concat([top_empresas, outros], ignore_index=True)

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.pie(
        df_final['participacao_mercado'],
        labels=df_final['sigla_empresa'],
        autopct='%1.1f%%',
        startangle=90,
        wedgeprops={'width': 0.3}
    )
    ax.set_title("Participação de Mercado por Decolagens", fontsize=16)
    st.pyplot(fig)

def grafico_donut_passageiros():
    df = execute_query("SELECT sigla_empresa, SUM(passageiros_pagos) AS total_passageiros FROM viagens GROUP BY sigla_empresa ORDER BY total_passageiros DESC", return_df=True)
    df['participacao_mercado'] = df['total_passageiros'] / df['total_passageiros'].sum()

    top_empresas = df.nlargest(4, 'participacao_mercado')
    outros = pd.DataFrame({
        'sigla_empresa': ['Outros'],
        'total_passageiros': [df['total_passageiros'].sum() - top_empresas['total_passageiros'].sum()],
        'participacao_mercado': [1 - top_empresas['participacao_mercado'].sum()]
    })

    df_final = pd.concat([top_empresas, outros], ignore_index=True)

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.pie(
        df_final['participacao_mercado'],
        labels=df_final['sigla_empresa'],
        autopct='%1.1f%%',
        startangle=90,
        wedgeprops={'width': 0.3}
    )
    ax.set_title("Participação de Mercado por Passageiros", fontsize=16)
    st.pyplot(fig)

def tabela_resumo():
    st.subheader("Tabela de Métricas")
    df_resumo = execute_query("SELECT sigla_empresa, SUM(horas_voadas) AS total_horas_voadas, AVG(litros_combustivel / decolagens) AS combustivel_medio_por_voo, AVG(rpk / assentos) AS ocupacao_media FROM viagens WHERE decolagens > 0 AND assentos > 0 GROUP BY sigla_empresa ORDER BY total_horas_voadas DESC;", return_df=True)
    df_resumo = df_resumo[df_resumo['combustivel_medio_por_voo']> 0]
    st.dataframe(df_resumo)