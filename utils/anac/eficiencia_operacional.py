import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from db.anac.banco import execute_query
from io import BytesIO

@st.cache_data
def grafico_combustivel_voos():
    df = execute_query("SELECT litros_combustivel, distancia_voada_km FROM viagens WHERE litros_combustivel and distancia_voada_km IS NOT NULL", return_df=True)
    
    df = df[df['distancia_voada_km'] > 0]
    
    fig, ax = plt.subplots(figsize=(12, 6))
    df['eficiencia_litro_por_km'] = df['litros_combustivel'] / df['distancia_voada_km']
    sns.scatterplot(data=df, x='distancia_voada_km', y='eficiencia_litro_por_km', ax=ax)
    ax.set_title('Eficiência de Combustível vs Distância dos Voos')
    ax.set_xlabel('Distância Voada (km)', fontsize=12)
    ax.set_ylabel('Perca de Eficiência (litros/km)', fontsize=12)
    
    buf = BytesIO()
    fig.savefig(buf, format="png", dpi=100, bbox_inches='tight')
    buf.seek(0)

    st.image(buf, width=1000)  

    plt.close(fig)

@st.cache_data
def grafico_horas_passageiros():
    df = execute_query("SELECT horas_voadas, passageiros_pagos FROM viagens WHERE horas_voadas and passageiros_pagos IS NOT NULL", return_df=True)
    df['horas_voadas'] = df['horas_voadas'].str.replace(',', '.').astype(float)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(data=df, x='horas_voadas', y='passageiros_pagos', ax=ax)
    ax.set_title('Variação Mensal de Horas Voadas vs Passageiros')
    ax.set_xlabel('Horas Voadas', fontsize=12)
    ax.set_ylabel('Número de Passageiros', fontsize=12)
    
    buf = BytesIO()
    fig.savefig(buf, format="png", dpi=100, bbox_inches='tight')
    buf.seek(0)

    st.image(buf, width=1000)  

    plt.close(fig)
    


    