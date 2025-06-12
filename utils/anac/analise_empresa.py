import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from db.anac.banco import execute_query
import plotly.express as px
import plotly.graph_objects as go

def grafico_barras():
    df = execute_query("SELECT sigla_empresa, natureza, SUM(decolagens) AS decolagens FROM viagens GROUP BY sigla_empresa, natureza ORDER BY decolagens DESC", return_df=True)

    total_decolagens = df.groupby('sigla_empresa')['decolagens'].sum().reset_index()
    top_empresas = total_decolagens.nlargest(10, 'decolagens')['sigla_empresa']
    df_top = df[df['sigla_empresa'].isin(top_empresas)]
    
    fig = px.bar(
            df_top,
            x='decolagens',
            y='sigla_empresa',
            orientation='h',
            barmode='group',
            title=f"Top 10 Empresas com Mais Decolagens",
            color='natureza',
            color_discrete_sequence=px.colors.diverging.RdBu_r,
            height=600
        )
    fig.update_yaxes(autorange="reversed")
    st.plotly_chart(fig, use_container_width=True)

def grafico_rpk_empresa():
    df = execute_query("SELECT sigla_empresa, SUM(rpk) AS total_rpk FROM viagens GROUP BY sigla_empresa ORDER BY total_rpk DESC", return_df=True)
    df_top = df.nlargest(20, 'total_rpk')

    fig = px.bar(
            df_top,
            x='total_rpk',
            y='sigla_empresa',
            barmode='group',
            orientation='h',
            title=f"Empresas com Mais RPK(Revenue Passenger Kilometers)",
            color_discrete_sequence=px.colors.diverging.RdBu_r,
            height=600
        )
    fig.update_yaxes(autorange="reversed")
    st.plotly_chart(fig, use_container_width=True)

def grafico_donut_decolagens():
    df = execute_query("SELECT sigla_empresa, SUM(decolagens) AS total_decolagens FROM viagens GROUP BY sigla_empresa ORDER BY total_decolagens DESC", return_df=True)
    df['participacao_mercado'] = df['total_decolagens'] / df['total_decolagens'].sum()

    top_empresas = df.nlargest(4, 'participacao_mercado')
    outros = pd.DataFrame({
        'sigla_empresa': ['Outros'],
        'total_decolagens': [df['total_decolagens'].sum() - top_empresas['total_decolagens'].sum()],
        'participacao_mercado': [1 - top_empresas['participacao_mercado'].sum()]
    })

    df_final = pd.concat([top_empresas, outros], ignore_index=True)

    fig = px.pie(
        df_final, 
        names='sigla_empresa', 
        values='participacao_mercado', 
        hole=0.6,  
        color_discrete_sequence = px.colors.diverging.RdBu_r,
        width=600,
        height=600
    )

    fig.update_traces(textinfo='percent+label') 
    fig.update_layout(
        title='Participação de Mercado por Decolagens',     
        font=dict(family="Arial", size=14, color="#212121"),          
    )

    st.plotly_chart(fig, use_container_width=True)

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
        width=600,
        height=600
    )

    fig.update_traces(textinfo='percent+label') 
    fig.update_layout(
        title='Participação de Mercado por Passageiros',     
        font=dict(family="Arial", size=14, color="#212121"),          
    )

    st.plotly_chart(fig, use_container_width=True)

def tabela_resumo():
    st.subheader("Tabela de Métricas")
    df_resumo = execute_query("SELECT sigla_empresa, SUM(horas_voadas) AS total_horas_voadas, AVG(litros_combustivel / decolagens) AS combustivel_medio_por_voo, AVG(rpk / assentos) AS ocupacao_media FROM viagens WHERE decolagens > 0 AND assentos > 0 GROUP BY sigla_empresa ORDER BY total_horas_voadas DESC;", return_df=True)
    df_resumo = df_resumo[df_resumo['combustivel_medio_por_voo']> 0]
    st.dataframe(df_resumo)