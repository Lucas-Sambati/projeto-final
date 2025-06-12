import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from db.anac.banco import execute_query

@st.cache_data
def grafico_aeroportos_decolagens():
    df = execute_query("SELECT aeroporto_origem_sigla, natureza, SUM(decolagens) AS decolagens FROM viagens GROUP BY aeroporto_origem_sigla, natureza ORDER BY decolagens DESC", return_df=True)

    total_decolagens = df.groupby('aeroporto_origem_sigla')['decolagens'].sum().reset_index()
    top_empresas = total_decolagens.nlargest(10, 'decolagens')['aeroporto_origem_sigla']
    df_top = df[df['aeroporto_origem_sigla'].isin(top_empresas)]

    fig, ax = plt.subplots(figsize=(10,4))
    sns.barplot( y='aeroporto_origem_sigla', x='decolagens', hue='natureza', data=df_top, ax=ax, order=top_empresas, palette="viridis")
    ax.set_title('Top 10 Aeroportos com Mais Decolagens', fontsize=16)
    ax.set_xlabel('Quantidade de Decolagens', fontsize=12)
    ax.set_ylabel('Aeroportos', fontsize=12)
    st.pyplot(fig)

@st.cache_data
def grafico_aeroportos_maior_carga():
    df = execute_query("""
        SELECT aeroporto_origem_sigla, carga_paga AS carga_total
        FROM viagens
        WHERE carga_paga IS NOT NULL
        GROUP BY aeroporto_origem_sigla
        ORDER BY carga_total DESC
        LIMIT 10;
    """, return_df=True)
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x='carga_total', y='aeroporto_origem_sigla', data=df, palette="viridis")    
    plt.xlabel('carga_paga')
    plt.ylabel('aeroporto_origem_sigla')
    plt.title('Top 10 Aeroportos com Mais Carga Transportada')
    
    st.pyplot(plt)

@st.cache_data
def grafico_aeroportos_mais_passageiros():
    df = execute_query("""
        SELECT aeroporto_origem_sigla, passageiros_pagos AS passageiros_totais
        FROM viagens
        WHERE passageiros_pagos IS NOT NULL
        GROUP BY aeroporto_origem_sigla
        ORDER BY passageiros_totais DESC
        LIMIT 10;
    """, return_df=True)
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x='passageiros_totais', y='aeroporto_origem_sigla', data=df, palette="viridis")    
    plt.xlabel('passageiros_totais')
    plt.ylabel('aeroporto_origem_sigla')
    plt.title('Top 10 Aeroportos com Mais Passageiros Transportados')
    
    st.pyplot(plt)