import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from db.anac.banco import execute_query
from io import BytesIO
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

@st.cache_data
def grafico_combustivel_voos():
    df = execute_query("SELECT passageiros_pagos, litros_combustivel, distancia_voada_km FROM viagens WHERE passageiros_pagos and litros_combustivel and distancia_voada_km IS NOT NULL", return_df=True)
    
    df = df[df['distancia_voada_km'] > 0]
    
    df['eficiencia_litro_por_km'] = df['litros_combustivel'] / df['distancia_voada_km']

    fig = px.scatter(
        df,
        x='distancia_voada_km',
        y='litros_combustivel',
        size='passageiros_pagos',
        title="Eficiência de Combustível vs Distância dos Voos",
        labels={
            'distancia_voada_km': 'Distância Voada (km)',
            'combustivel_litros': 'Combustível (L)'
        }
    )
    st.plotly_chart(fig, use_container_width=True)
        
@st.cache_data
def grafico_horas_passageiros():
    df = execute_query("SELECT horas_voadas, passageiros_pagos FROM viagens WHERE horas_voadas and passageiros_pagos IS NOT NULL", return_df=True)
    df['horas_voadas'] = df['horas_voadas'].str.replace(',', '.').astype(float)

    df_agg = df.groupby('horas_voadas', as_index=False)['passageiros_pagos'].mean().sort_values('horas_voadas')

    fig = px.line(
        df_agg,
        x='horas_voadas',
        y='passageiros_pagos',
        title='Variação Mensal de Horas Voadas vs Passageiros',
        labels={
            'horas_voadas': 'Horas Voadas',
            'passageiros_pagos': 'Número de Passageiros'
        }
    )
    
    st.plotly_chart(fig, use_container_width=True)



@st.cache_data
def atk_rtk():    
    df = execute_query(
        "SELECT sigla_empresa, atk, rtk, decolagens FROM viagens "
        "WHERE atk IS NOT NULL AND rtk IS NOT NULL AND decolagens IS NOT NULL",
        return_df=True
    )

    df = df[(df['atk']>5000000) & (df['rtk'] >5000000)]
    df_sorted = df.sort_values('decolagens', ascending=False)
    df_top = df_sorted.drop_duplicates(subset='sigla_empresa').head(10)

    labels = df_top['sigla_empresa']
    atk = df_top['atk']
    rtk = df_top['rtk']

    x = np.arange(len(labels))  # posições no eixo X
    width = 0.35  # largura das barras

    fig, ax = plt.subplots(figsize=(12,7))

    # Barras lado a lado
    bar1 = ax.bar(x - width/2, atk, width, label='ATK', color='red')
    bar2 = ax.bar(x + width/2, rtk, width, label='RTK', color='blue')

    # Configurações do eixo X
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=45, ha='right')

    # Títulos e legendas
    ax.set_title('Top 10 Empresas com Mais RPK (Revenue Passenger Kilometers)', fontsize=16)
    ax.set_xlabel('Empresa', fontsize=12)
    ax.set_ylabel('ATK e RTK', fontsize=12)
    ax.legend()

    sns.despine()
    plt.tight_layout()

    # Exibe no Streamlit
    st.pyplot(fig)
    st.write('''
    Barra vermelha (ATK) Capacidade disponível total\n
    Barra azul (RTK) Demanda efetiva
    ''')