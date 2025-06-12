import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from db.anac.banco import execute_query
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

def distribuicao_natureza(filtered_df):
    nature_counts = filtered_df['natureza'].value_counts()
    fig2 = px.pie(
        values=nature_counts.values,
        names=nature_counts.index,
        title="Distribuição por Natureza do Voo"
    )
    st.plotly_chart(fig2, use_container_width=True)

def analise_eficiencia(filtered_df):
     # Fuel consumption vs distance
    st.subheader("Análise de Eficiência")
    
    # Filter out zero values for meaningful analysis
    efficiency_df = filtered_df[
        (filtered_df['litros_combustivel'] > 0) & 
        (filtered_df['distancia_voada_km'] > 0)
    ].copy()
    
    if len(efficiency_df) > 0:
        efficiency_df['fuel_efficiency'] = efficiency_df['litros_combustivel'] / efficiency_df['distancia_voada_km']
        
        fig_efficiency = px.scatter(
            efficiency_df,
            x='distancia_voada_km',
            y='litros_combustivel',
            color='empresa_nacionalidade',
            size='passageiros_pagos',
            title="Consumo de Combustível vs Distância Voada",
            hover_data=['empresa_nome', 'fuel_efficiency'],
            labels={
                'distancia_voada_km': 'Distância Voada (km)',
                'litros_combustivel': 'Combustível (L)'
            }
        )
        st.plotly_chart(fig_efficiency, use_container_width=True)

def evolucao_passageiros_mensal(filtered_df):
    monthly_passengers = filtered_df.groupby(['ano', 'mes']).agg({
                'passageiros_pagos': 'sum',
                'passageiros_gratis': 'sum'
            }).reset_index()
    monthly_passengers['total_passengers'] = monthly_passengers['passageiros_pagos'] + monthly_passengers['passageiros_gratis']
    monthly_passengers["date"] = pd.to_datetime(monthly_passengers["ano"].astype(str) + "-" + monthly_passengers["mes"].astype(str) + "-01", format="%Y-%m-%d", errors="coerce")
            
    fig1 = px.line(
            monthly_passengers,
            x='date',
            y='total_passengers',
            title="Evolução Mensal de Passageiros",
            markers=True
        )
    st.plotly_chart(fig1, use_container_width=True)

def grafico_donut_passageiros():
    df = execute_query("SELECT sigla_empresa, SUM(passageiros_pagos) AS total_passageiros FROM viagens GROUP BY sigla_empresa ORDER BY total_passageiros DESC", return_df=True)
    df['participacao_mercado'] = df['total_passageiros'] / df['total_passageiros'].sum()

    top_empresas = df.nlargest(4, 'participacao_mercado')
    outros = pd.DataFrame({
        'sigla_empresa': ['Outros'],
        'total_passageiros': [df['total_passageiros'].sum() - top_empresas['total_passageiros'].sum()],
        'participacao_mercado': [1 - top_empresas['participacao_mercado'].sum()]
    })

    df_final = pd.concat([top_empresas, outros], ignore_index=True)

    fig = px.pie(
        df_final, 
        names='sigla_empresa', 
        values='participacao_mercado', 
        hole=0.6,  
        color_discrete_sequence = px.colors.diverging.RdBu_r,
    )

    fig.update_traces(textinfo='percent+label') 
    fig.update_layout(
        title='Participação de Mercado por Passageiros',     
        font=dict(family="Arial", size=14, color="#212121"),          
    )

    st.plotly_chart(fig, use_container_width=True)

def tabela_resumo(filtered_df):
    st.dataframe(filtered_df, use_container_width=True)

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