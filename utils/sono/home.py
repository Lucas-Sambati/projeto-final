import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from db.sono.banco import execute_query

def heatmap_geral():
    df = execute_query("SELECT idade, duracao_sono, qualidade_sono, atividade_fisica, nivel_estresse, taxa_batimentos, passos_diarios FROM pessoas;", return_df=True)
    corr = df.corr()
    fig, ax = plt.subplots()
    sns.heatmap(corr, ax=ax, annot=True, cmap="YlGnBu")
    st.pyplot(fig)

def boxplot_profissao_stress():
    df = execute_query("SELECT profissao,nivel_estresse FROM pessoas;", return_df=True)

    fig = plt.figure(figsize=(10, 6))
    sns.boxplot(data=df, y="nivel_estresse", x="profissao")
    plt.xticks(rotation=45)
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

def colored_metric(label, value, color):
    st.markdown(
        f"""
        <div style="font-weight: bold; font-size: 14px; margin-bottom: 8px;">
            {label}
        </div>
        <div style="color: {color}; font-size: 36px; font-weight: 600;">
            {value}
        </div>
        """,
        unsafe_allow_html=True
    )
    
