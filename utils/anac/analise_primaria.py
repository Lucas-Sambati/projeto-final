import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from db.anac.banco import execute_query
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from utils.color import get_color

def distribuicao_natureza(filtered_df):
    nature_counts = filtered_df['natureza'].value_counts()
    fig2 = px.pie(
        values=nature_counts.values,
        names=nature_counts.index,
        color_discrete_sequence=get_color(),
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
            color_discrete_sequence=get_color(),
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
            color_discrete_sequence=get_color(),
            title="Evolução Mensal de Passageiros",
            markers=True
        )
    st.plotly_chart(fig1, use_container_width=True)

def grafico_donut_passageiros(df):
    df_agg = (
        df.groupby('sigla_empresa', as_index=False)['passageiros_pagos']
        .sum()
        .rename(columns={'passageiros_pagos': 'total_passageiros'})
        .sort_values(by='total_passageiros', ascending=False)
    )

    df_agg['participacao_mercado'] = df_agg['total_passageiros'] / df_agg['total_passageiros'].sum()

    top_empresas = df_agg.nlargest(4, 'participacao_mercado')
    outros = pd.DataFrame({
        'sigla_empresa': ['Outros'],
        'total_passageiros': [df_agg['total_passageiros'].sum() - top_empresas['total_passageiros'].sum()],
        'participacao_mercado': [1 - top_empresas['participacao_mercado'].sum()]
    })

    df_final = pd.concat([top_empresas, outros], ignore_index=True)

    fig = px.pie(
        df_final, 
        names='sigla_empresa', 
        values='participacao_mercado', 
        hole=0.6,  
        color_discrete_sequence = get_color(),
    )

    fig.update_traces(textinfo='percent+label') 
    fig.update_layout(
        title='Participação de Mercado por Passageiros',     
        font=dict(family="Arial", size=14, color="#212121"),          
    )

    st.plotly_chart(fig, use_container_width=True)

def tabela_resumo(filtered_df):
    st.dataframe(filtered_df, use_container_width=True)

def grafico_horas_passageiros(df):
    df_filtrado = df[df['horas_voadas'].notnull() & df['passageiros_pagos'].notnull()][['horas_voadas', 'passageiros_pagos']]
    df_filtrado['horas_voadas'] = df_filtrado['horas_voadas'].str.replace(',', '.').astype(float)

    df_agg = df_filtrado.groupby('horas_voadas', as_index=False)['passageiros_pagos'].mean().sort_values('horas_voadas')

    fig = px.line(
        df_agg,
        x='horas_voadas',
        y='passageiros_pagos',
        title='Variação Mensal de Horas Voadas vs Passageiros',
        color_discrete_sequence=get_color(),
        labels={
            'horas_voadas': 'Horas Voadas',
            'passageiros_pagos': 'Número de Passageiros'
        }
    )
    
    st.plotly_chart(fig, use_container_width=True)

def atk_rtk(df):
    df_filtered = df[
        df['atk'].notnull() & 
        df['rtk'].notnull() & 
        df['decolagens'].notnull()
    ].copy()

    df_filtered = df_filtered[(df_filtered['atk'] > 5000000) & (df_filtered['rtk'] > 5000000)]
    df_sorted = df_filtered.sort_values('decolagens', ascending=False)
    df_top = df_sorted.drop_duplicates(subset='sigla_empresa').head(10)

    labels = df_top['sigla_empresa']
    atk = df_top['atk']
    rtk = df_top['rtk']

    # Paleta RdBu_r: vermelho e azul
    colors = get_color()
    # Vamos usar um vermelho próximo de colors[0] e azul próximo de colors[-1]
    color_atk = colors[0]    # tom vermelho
    color_rtk = colors[-1]   # tom azul

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=labels,
        y=atk,
        name='ATK',
        marker_color=color_atk,
    ))

    fig.add_trace(go.Bar(
        x=labels,
        y=rtk,
        name='RTK',
        marker_color=color_rtk,
    ))

    fig.update_layout(
        barmode='group',
        title='Fator de Utilização de Carga',
        xaxis_title='Empresa',
        yaxis_title='ATK e RTK',
        xaxis_tickangle=-45,
        template='simple_white',
        width=900,
        height=600,
        legend=dict(title='Legenda')
    )
    
    fig.update_layout(
    annotations=[
            dict(
                x=0.02, y=1.08,
                xref='paper', yref='paper',
                text="<b></b><br>"
                    f"<span style='color:{colors[0]}'>■</span> ATK - Capacidade total de transporte de carga disponível (passageiro e peso)<br>"
                    f"<span style='color:{colors[-1]}'>■</span> RTK - Quanto da capacidade total (ATK) está sendo usado",
                showarrow=False,
                align='left',
                font=dict(size=14),
                bordercolor="black",
                borderwidth=1,
                borderpad=4,
                bgcolor="white",
                opacity=0.8
            )
        ]
    )


    st.plotly_chart(fig, use_container_width=True)
    
def grafico_aeroportos_decolagens(df):
    df_agg = (
        df.groupby(['aeroporto_origem_sigla', 'natureza'], as_index=False)['decolagens']
        .sum()
        .rename(columns={'decolagens': 'decolagens'})
        .sort_values(by='decolagens', ascending=False)
    )

    total_decolagens = df_agg.groupby('aeroporto_origem_sigla')['decolagens'].sum().reset_index()
    top_empresas = total_decolagens.nlargest(10, 'decolagens')['aeroporto_origem_sigla']
    df_top = df_agg[df_agg['aeroporto_origem_sigla'].isin(top_empresas)]
    
    fig = px.bar(
            df_top,
            x='decolagens',
            y='aeroporto_origem_sigla',
            orientation='h',
            title=f"Top 10 Aeroportos com Mais Decolagens",
            color='natureza',
            barmode='group',
            color_discrete_sequence=get_color(),
            height=600
        )
    fig.update_yaxes(autorange="reversed")
    st.plotly_chart(fig, use_container_width=True)

    
def ask_rpk(df):
    df_filtered = df[
        df['ask'].notnull() & 
        df['rpk'].notnull() & 
        df['decolagens'].notnull()
    ].copy()

    df_filtered = df_filtered[(df_filtered['ask'] > 5000000) & (df_filtered['rpk'] > 5000000)]
    df_sorted = df_filtered.sort_values('decolagens', ascending=False)
    df_top = df_sorted.drop_duplicates(subset='sigla_empresa').head(10)

    labels = df_top['sigla_empresa']
    ask = df_top['ask']
    rpk = df_top['rpk']

    # Paleta RdBu_r: vermelho e azul
    colors = get_color()
    # Vamos usar um vermelho próximo de colors[0] e azul próximo de colors[-1]
    color_ask = colors[0]    # tom vermelho
    color_rpk = colors[-1]   # tom azul

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=labels,
        y=ask,
        name='APK',
        marker_color=color_ask,
    ))

    fig.add_trace(go.Bar(
        x=labels,
        y=rpk,
        name='RPK',
        marker_color=color_rpk,
    ))

    fig.update_layout(
        barmode='group',
        title='Fator de Utilização de Carga',
        xaxis_title='Empresa',
        yaxis_title='APK e RPK',
        xaxis_tickangle=-45,
        template='simple_white',
        width=900,
        height=600,
        legend=dict(title='Legenda')
    )
    
    fig.update_layout(
    annotations=[
            dict(
                x=0.02, y=1.08,
                xref='paper', yref='paper',
                text="<b></b><br>"
                    f"<span style='color:{colors[0]}'>■</span> APK - Capacidade total de assentos disponíveis por Km<br>"
                    f"<span style='color:{colors[-1]}'>■</span> RPK - Quanto da capacidade total (APK) está sendo usado",
                showarrow=False,
                align='left',
                font=dict(size=14),
                bordercolor="black",
                borderwidth=1,
                borderpad=4,
                bgcolor="white",
                opacity=0.8
            )
        ]
    )


    st.plotly_chart(fig, use_container_width=True)
    
