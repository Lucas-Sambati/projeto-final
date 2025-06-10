import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from db.banco import execute_query

def heatmap_exercicio_sono():
    df = execute_query("SELECT duracao_sono, qualidade_sono, atividade_fisica, passos_diarios FROM pessoas;", return_df=True)
    corr = df.corr()
    fig, ax = plt.subplots()
    sns.heatmap(corr, ax=ax, annot=True, cmap="YlGnBu")
    plt.title('Correlação entre Exercicios e Qualidade/Duração do sono')
    st.pyplot(fig)

def heatmap_stress_sono():
    df = execute_query("SELECT duracao_sono, qualidade_sono, nivel_estresse FROM pessoas;", return_df=True)
    corr = df.corr()
    fig, ax = plt.subplots()
    sns.heatmap(corr, ax=ax, annot=True, cmap="YlGnBu")
    plt.title('Correlação entre Estresse e Qualidade/Duracao do sono')
    st.pyplot(fig)

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
    fig, ax = plt.subplots()
    sns.heatmap(corr, ax=ax, annot=True, cmap="YlGnBu", 
                xticklabels=['Nível IMC', 'Taxa Batimentos', 'Qualidade Sono'],
                yticklabels=['Nível IMC', 'Taxa Batimentos', 'Qualidade Sono'])
    plt.title('Correlação entre IMC, Batimentos e Qualidade do Sono')
    st.pyplot(fig)