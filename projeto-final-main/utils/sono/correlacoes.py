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
    st.pyplot(fig)

def heatmap_stress_sono():
    df = execute_query("SELECT duracao_sono, qualidade_sono, nivel_estresse FROM pessoas;", return_df=True)
    corr = df.corr()
    fig, ax = plt.subplots()
    sns.heatmap(corr, ax=ax, annot=True, cmap="YlGnBu")
    st.pyplot(fig)

def heatmap_obesidade_batimentos_sono():
    df = execute_query("SELECT nivel_IMC, taxa_batimentos, qualidade_sono FROM pessoas;", return_df=True)
    corr = df.corr()
    fig, ax = plt.subplots()
    sns.heatmap(corr, ax=ax, annot=True, cmap="YlGnBu")
    st.pyplot(fig)