import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from db.banco import execute_query

query = """
SELECT profissao, condicao_sono, taxa_batimentos, nivel_estresse, genero
FROM pessoas
"""  
df = execute_query(query, return_df=True)

def show_occupation_count_chart():
# CONTAGEM DE PROFISSIONAIS
    fig, ax = plt.subplots(figsize=(10,6))
    sns.countplot(df, y="profissao", ax=ax, hue="profissao", palette="pastel")
    st.pyplot(fig)

def show_sleep_disorder_frequency_chart():
# HEATMAP
    sleep_crosstab = pd.crosstab(
        df['profissao'], 
        df['condicao_sono'],
        normalize='index'
    )

    fig, ax = plt.subplots(figsize=(10,6)) 
    sns.heatmap(
        sleep_crosstab, 
        annot=True, 
        cmap='Pastel1', 
        fmt='.0%',
        linewidths=.5,
        ax=ax
    )
    plt.title('Frequência de Distúrbios do Sono por Profissão')
    plt.ylabel('Profissão')
    plt.xlabel('Distúrbio do Sono')
    plt.tight_layout()
    st.pyplot(fig)

def show_stress_level_heart_rate_chart():
    # GRAFICO DE BARRAS/LINHA ESTRESSE E BATIMENTOS POR PROFISSAO
    agg_df = df.groupby('profissao').agg(
        avg_heart_rate=('taxa_batimentos', 'mean'),
        avg_stress=('nivel_estresse', 'mean')
    ).reset_index().sort_values(by='avg_heart_rate', ascending=False)

    fig, ax1 = plt.subplots(figsize=(10, 8))

    sns.barplot(
        data=agg_df,
        x='avg_heart_rate',
        y='profissao',
        ax=ax1,
        hue='profissao',
        palette="pastel",
        legend=False 
    )
    ax1.set_xlabel('Média de Batimentos Cardíacos', color='royalblue', fontsize=12)
    ax1.set_ylabel('Profissão', fontsize=12)
    ax1.tick_params(axis='x', labelcolor='royalblue')

    ax2 = ax1.twiny()
    sns.lineplot(
        data=agg_df,
        x='avg_stress',
        y='profissao',
        color='crimson',
        marker='o',
        linewidth=2.5,
        ax=ax2,
        label='Nível de Estresse'
    )
    ax2.set_xlabel('Nível Médio de Estresse', color='crimson', fontsize=12)
    ax2.tick_params(axis='x', labelcolor='crimson')
    
    ax1.grid(False)
    ax2.grid(False)

    plt.title('Batimentos Cardíacos e Estresse por Profissão', pad=20, fontsize=16)
    fig.tight_layout()
    st.pyplot(fig)

def show_health_risk_per_occupation():
# GRAFICO SCATTER
    risk_df = df.groupby('profissao').agg(
        sleep_apnea_prevalence=('condicao_sono', lambda x: (x == 'Sleep Apnea').mean()),
        avg_heart_rate=('taxa_batimentos', 'mean'),
        avg_stress=('nivel_estresse', 'mean')
    ).reset_index()

    fig = plt.figure(figsize=(10, 6))
    scatter = sns.scatterplot(
        data=risk_df,
        x='sleep_apnea_prevalence',
        y='avg_heart_rate',
        size='avg_stress',
        sizes=(50, 500),
        hue='profissao',
        palette='pastel',
        alpha=0.8
    )

    highlight = risk_df[risk_df['sleep_apnea_prevalence'] > 0.3]
    for i, row in highlight.iterrows():
        plt.annotate(
            row['profissao'], 
            (row['sleep_apnea_prevalence'], row['avg_heart_rate']),
            xytext=(10, -10),
            textcoords='offset points',
            fontsize=10,
            color='red'
        )

    plt.title('Risco de Saúde por Profissão', fontsize=16)
    plt.xlabel('Prevalência de Apneia do Sono')
    plt.ylabel('Média de Batimentos Cardíacos')
    plt.grid(True, alpha=0.2)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    st.pyplot(fig)