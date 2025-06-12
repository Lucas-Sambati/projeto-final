import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from db.anac.banco import execute_query
import plotly.express as px
import plotly.graph_objects as go

@st.cache_data
def grafico_aeroportos_decolagens():
    df = execute_query("SELECT aeroporto_origem_sigla, natureza, SUM(decolagens) AS decolagens FROM viagens GROUP BY aeroporto_origem_sigla, natureza ORDER BY decolagens DESC", return_df=True)

    total_decolagens = df.groupby('aeroporto_origem_sigla')['decolagens'].sum().reset_index()
    top_empresas = total_decolagens.nlargest(10, 'decolagens')['aeroporto_origem_sigla']
    df_top = df[df['aeroporto_origem_sigla'].isin(top_empresas)]
    
    fig = px.bar(
            df_top,
            x='decolagens',
            y='aeroporto_origem_sigla',
            orientation='h',
            title=f"Top 10 Aeroportos com Mais Decolagens",
            color='natureza',
            barmode='group',
            color_discrete_sequence=px.colors.diverging.RdBu_r,
            height=600
        )
    fig.update_yaxes(autorange="reversed")
    st.plotly_chart(fig, use_container_width=True)

@st.cache_data
def grafico_aeroportos_maior_carga():
    df = execute_query("""
        SELECT aeroporto_origem_sigla, carga_paga AS carga_total
        FROM viagens
        WHERE carga_paga IS NOT NULL
        GROUP BY aeroporto_origem_sigla
        ORDER BY carga_total DESC
        LIMIT 10;
    """, return_df=True)
    
    fig = px.bar(
            df,
            x='carga_total',
            y='aeroporto_origem_sigla',
            orientation='h',
            title=f"Top 10 Aeroportos com Mais Carga Transportada",
            color_discrete_sequence=px.colors.diverging.RdBu_r,
            height=600
        )
    fig.update_yaxes(autorange="reversed")
    st.plotly_chart(fig, use_container_width=True)

@st.cache_data
def grafico_aeroportos_mais_passageiros():
    df = execute_query("""
        SELECT aeroporto_origem_sigla, passageiros_pagos AS passageiros_totais
        FROM viagens
        WHERE passageiros_pagos IS NOT NULL
        GROUP BY aeroporto_origem_sigla
        ORDER BY passageiros_totais DESC
        LIMIT 10;
    """, return_df=True)
    
    fig = px.bar(
            df,
            x='passageiros_totais',
            y='aeroporto_origem_sigla',
            orientation='h',
            title=f"Top 10 Aeroportos com Mais Passageiros Transportados",
            color_discrete_sequence=px.colors.diverging.RdBu_r,
            height=600
        )
    fig.update_yaxes(autorange="reversed")
    st.plotly_chart(fig, use_container_width=True)