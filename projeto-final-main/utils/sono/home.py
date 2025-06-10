import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from db.banco import execute_query

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
    