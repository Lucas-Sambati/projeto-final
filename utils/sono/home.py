import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from db.sono.banco import execute_query
import plotly.express as px
import plotly.graph_objects as go

@st.cache_data
def heatmap_geral():
    df = execute_query("SELECT idade, duracao_sono, qualidade_sono, atividade_fisica, nivel_estresse, taxa_batimentos, passos_diarios FROM pessoas;", return_df=True)
    
    st.subheader("MATRIZ DE CORRELAÇÕES")
    numeric_cols = ['idade', 'duracao_sono', 'qualidade_sono', 'atividade_fisica', 
                   'nivel_estresse', 'taxa_batimentos', 'passos_diarios']
    corr_matrix = df[numeric_cols].corr()
    
    fig_corr = px.imshow(
        corr_matrix,
        text_auto=True,
        aspect="auto",
        color_continuous_scale='RdBu_r'
    )
    st.plotly_chart(fig_corr, use_container_width=True)

@st.cache_data
def profissao_mais_estressante():
    return 'Nurse'

@st.cache_data
def qtd_pessoas_analisadas():
    df = execute_query("SELECT id_pessoas FROM pessoas;", return_df=True)
    return df['id_pessoas'].count()

@st.cache_data
def media_duracao_sono():
    df = execute_query("SELECT duracao_sono FROM pessoas;", return_df=True)
    
    return f'{float(df['duracao_sono'].mean()):.1f}h'

@st.cache_data
def prevalencia_disturbios():
    df = execute_query('SELECT condicao_sono FROM pessoas', return_df=True)
    
    total_pessoas = len(df)
    
    pessoas_normais = len(df[df['condicao_sono'] == 'Normal'])
    pessoas_com_disturbios = total_pessoas - pessoas_normais
    porcentagem_disturbios = (pessoas_com_disturbios / total_pessoas) * 100
    
    return round(porcentagem_disturbios, 2)  

@st.cache_data
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

@st.cache_data
def media_qualidade_sono():
    df = execute_query("SELECT qualidade_sono FROM pessoas", return_df=True)
    
    return f'{df['qualidade_sono'].mean():.1f}/10'

@st.cache_data
def media_nivel_estresse():
    df = execute_query("SELECT nivel_estresse FROM pessoas", return_df=True)
    
    return f'{df['nivel_estresse'].mean():.1f}/10'

@st.cache_data
def get_df():
    df = execute_query("SELECT * FROM pessoas", return_df=True)
    return df
