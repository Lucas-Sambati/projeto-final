import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from db.anac.banco import execute_query
import plotly.express as px

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

def total_passageiros_pagos():
    df = execute_query("SELECT passageiros_pagos FROM viagens", return_df=True)
    
    return int(df['passageiros_pagos'].sum())

@st.cache_data
def grafico_barras():
    df = execute_query("SELECT atk, rtk FROM viagens WHERE atk and rtk IS NOT NULL", return_df=True)
    
    fig, ax = plt.subplots()
    sns.barplot(x='atk', y='rtk', data=df, ax=ax)
    st.pyplot(fig)

def aeroportos_unicos():
    df = execute_query("SELECT aeroporto_origem_sigla, aeroporto_destino_sigla FROM viagens", return_df=True)    

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

    df_plot = df.rename(columns={
        'origem_lat': 'lat',
        'origem_lon': 'lon',
        'aeroporto_origem_sigla': 'sigla'
    })

    # Remove linhas sem coordenadas
    df_plot = df_plot.dropna(subset=['lat', 'lon'])

    # Cria o mapa
    fig = px.scatter_mapbox(
        df_plot,
        lat="lat",
        lon="lon",
        hover_name="sigla",
        zoom=3,
        height=500
    )

    # Configura estilo e layout
    fig.update_layout(
        mapbox_style="open-street-map",
        mapbox_zoom=4,
        mapbox_center={"lat": -15, "lon": -50},  # Centraliza no Brasil
        margin={"r":0,"t":0,"l":0,"b":0}
    )

    st.plotly_chart(fig, use_container_width=True)
    
    return df[['aeroporto_destino_sigla', 'origem_lat', 'origem_lon']].drop_duplicates().reset_index(drop=True)

