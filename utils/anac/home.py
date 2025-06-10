import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from db.anac.banco import execute_query


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
    
def empresa_com_mais_voos():
    df = execute_query("SELECT sigla_empresa, decolagens FROM viagens", return_df=True)
    
    df_empresas_com_mais_voo = df.groupby('sigla_empresa').agg({'decolagens':'sum'}).reset_index().sort_values(by='decolagens', ascending=False)
    
    return df_empresas_com_mais_voo.loc[0, 'sigla_empresa']

def total_voos():
    df = execute_query("SELECT decolagens FROM viagens", return_df=True)
    
    return int(df['decolagens'].sum())

@st.cache_data
def grafico_barras():
    df = execute_query("SELECT atk, rtk FROM viagens WHERE atk and rtk IS NOT NULL", return_df=True)
    
    fig, ax = plt.subplots()
    sns.barplot(x='atk', y='rtk', data=df, ax=ax)
    st.pyplot(fig)
    