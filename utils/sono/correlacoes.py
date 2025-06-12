import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from db.sono.banco import execute_query
import plotly.express as px
import plotly.graph_objects as go

@st.cache_data
def heatmap_exercicio_sono():
    df = execute_query("SELECT duracao_sono, qualidade_sono, atividade_fisica, passos_diarios FROM pessoas;", return_df=True)
    corr = df.corr()
    fig_corr = px.imshow(
        corr,
        text_auto=True,
        aspect="auto",
        title="Correlação entre Variáveis Sono e Atividades Físicas",
        color_continuous_scale='Blues'
    )
    st.plotly_chart(fig_corr, use_container_width=True)

@st.cache_data
def heatmap_stress_sono():
    df = execute_query("SELECT duracao_sono, qualidade_sono, nivel_estresse FROM pessoas;", return_df=True)
    corr = df.corr()
    
    fig_corr = px.imshow(
        corr,
        text_auto=True,
        aspect="auto",
        title="Correlação entre Variáveis Sono e Estresse",
        color_continuous_scale='Blues'
    )
    st.plotly_chart(fig_corr, use_container_width=True)

@st.cache_data
def heatmap_obesidade_batimentos_sono():
    df = execute_query("SELECT nivel_IMC, taxa_batimentos, qualidade_sono FROM pessoas;", return_df=True)
    imc_mapping = {
        'Underweight': 0,
        'Normal': 1,
        'Overweight': 2,
        'Obese': 3
    }
    df['nivel_IMC_num'] = df['nivel_IMC'].map(imc_mapping)
    df_numeric = df[['nivel_IMC_num', 'taxa_batimentos', 'qualidade_sono']]
    corr = df_numeric.corr()
    fig_corr = px.imshow(
        corr,
        text_auto=True,
        aspect="auto",
        title="Correlação entre Variáveis Sono e Saúde",
        color_continuous_scale='Blues'
    )
    st.plotly_chart(fig_corr, use_container_width=True)