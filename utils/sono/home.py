import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from db.banco import execute_query

def heatmap_geral():
    df = execute_query("SELECT idade, duracao_sono, qualidade_sono, atividade_fisica, nivel_estresse, taxa_batimentos, passos_diarios FROM pessoas;", return_df=True)
    corr = df.corr()
    _, col, _ = st.columns([0.25, 0.5, 0.25], vertical_alignment="center")
    with col:
        st.write("### Correlação entre as colunas")
        fig, ax = plt.subplots(figsize=(7, 7))
        sns.heatmap(corr, ax=ax, annot=True, cmap="Greens", fmt=".2f", linewidths=5)
        plt.tight_layout()
        st.pyplot(fig)

def profissao_mais_estressante():
    return 'Nurse'

def qtd_pessoas_analisadas():
    df = execute_query("SELECT id_pessoas FROM pessoas;", return_df=True)
    return df['id_pessoas'].count()

def media_duracao_sono():
    df = execute_query("SELECT duracao_sono FROM pessoas;", return_df=True)
    
    return int(df['duracao_sono'].mean())

def prevalencia_disturbios():
    df = execute_query('SELECT condicao_sono FROM pessoas', return_df=True)
    
    total_pessoas = len(df)
    
    pessoas_normais = len(df[df['condicao_sono'] == 'Normal'])
    pessoas_com_disturbios = total_pessoas - pessoas_normais
    porcentagem_disturbios = (pessoas_com_disturbios / total_pessoas) * 100
    
    return round(porcentagem_disturbios, 2)  

def pessoas_com_risco_cardiovascular():
    df = execute_query('SELECT pressao_sanguinea FROM pessoas', return_df=True)
    
    total_pessoas = len(df)
    
    pessoas_com_risco = 0
    
    for pressao in df['pressao_sanguinea']:
        try:
            sistolica, diastolica = map(float, pressao.split('/'))
            
            if (sistolica >= 140 or diastolica >= 90):  
                pessoas_com_risco += 1
        except:
            continue
    
    porcentagem_risco = (pessoas_com_risco / total_pessoas) * 100
    
    return round(porcentagem_risco, 2)

def media_idade():
    df = execute_query("SELECT idade FROM pessoas", return_df=True)
    
    return int(df['idade'].mean())

def get_df():
    df = execute_query("SELECT * FROM pessoas", return_df=True)
    return df