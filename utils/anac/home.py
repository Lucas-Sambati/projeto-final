import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from db.anac.banco import execute_query
from rotas_aeroportos import maiores_transportes_passageiros, maiores_transportes_carga
import plotly.express as px
import plotly.graph_objects as go

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

def total_passageiros():
    df = execute_query("SELECT passageiros_pagos FROM viagens", return_df=True)
    
    return int(df['passageiros_pagos'].sum())

def total_distancia_voada():
    df = execute_query("SELECT SUM(distancia_voada_km) AS total FROM viagens", return_df=True)
    total = df.iloc[0]['total']
    return f'{int(total)}km'

@st.cache_data
def aeroportos_unicos():
    df = execute_query("""
        SELECT aeroporto_origem_sigla, aeroporto_destino_sigla, sigla_empresa
        FROM viagens
    """, return_df=True)

    df['aeroporto_origem_sigla'] = df['aeroporto_origem_sigla'].str.strip().str.upper()
    df['aeroporto_destino_sigla'] = df['aeroporto_destino_sigla'].str.strip().str.upper()

    df_airports = pd.read_csv('data/airports.csv')
    df_airports = df_airports[df_airports['ident'].notnull()]
    df_airports['ident'] = df_airports['ident'].str.strip().str.upper()

    coords_dict = df_airports.set_index('ident')[['latitude_deg', 'longitude_deg']].to_dict(orient='index')

    df['origem_lat'] = df['aeroporto_origem_sigla'].map(lambda x: coords_dict.get(x, {}).get('latitude_deg'))
    df['origem_lon'] = df['aeroporto_origem_sigla'].map(lambda x: coords_dict.get(x, {}).get('longitude_deg'))
    df['destino_lat'] = df['aeroporto_destino_sigla'].map(lambda x: coords_dict.get(x, {}).get('latitude_deg'))
    df['destino_lon'] = df['aeroporto_destino_sigla'].map(lambda x: coords_dict.get(x, {}).get('longitude_deg'))

    df = df.dropna(subset=['origem_lat', 'origem_lon', 'destino_lat', 'destino_lon'])

    df = df.sample(n=min(len(df), 300), random_state=42)

    fig = go.Figure()

    empresas = df['sigla_empresa'].unique()
    colors = px.colors.qualitative.Dark24
    color_map = {empresa: colors[i % len(colors)] for i, empresa in enumerate(empresas)}

    for empresa in empresas:
        df_empresa = df[df['sigla_empresa'] == empresa]
        for _, row in df_empresa.iterrows():
            fig.add_trace(go.Scattermapbox(
                mode="lines",
                lon=[row['origem_lon'], row['destino_lon']],
                lat=[row['origem_lat'], row['destino_lat']],
                line=dict(width=1, color=color_map[empresa]),
                hoverinfo="text",
                text=f"{empresa}: {row['aeroporto_origem_sigla']} → {row['aeroporto_destino_sigla']}"
            ))

    fig.update_layout(
        mapbox_style="open-street-map",
        mapbox_zoom=2.1,
        mapbox_center={"lat": 10, "lon": -19},
        height=600,
        margin={"r":0,"t":0,"l":0,"b":0},
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)

maiores_transportes_passageiros()
maiores_transportes_carga()