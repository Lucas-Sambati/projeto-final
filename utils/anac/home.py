import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from db.anac.banco import execute_query
import plotly.express as px
import plotly.graph_objects as go

@st.cache_data
def empresa_com_mais_voos():
    df = execute_query("SELECT sigla_empresa, decolagens FROM viagens", return_df=True)
    
    df_empresas_com_mais_voo = df.groupby('sigla_empresa').agg({'decolagens':'sum'}).reset_index().sort_values(by='decolagens', ascending=False)
    
    return df_empresas_com_mais_voo.iloc[0, 0]

def format_number(num):
    if num >= 1_000_000:
        return f"{num / 1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num / 1_000:.0f}K"
    else:
        return str(num)

@st.cache_data
def total_voos():
    df = execute_query("SELECT decolagens FROM viagens", return_df=True)
    total = int(df['decolagens'].sum())
    return format_number(total)

@st.cache_data
def total_passageiros():
    df = execute_query("SELECT passageiros_pagos FROM viagens", return_df=True)
    total = int(df['passageiros_pagos'].sum())
    return format_number(total)

@st.cache_data
def total_distancia_voada():
    df = execute_query("SELECT SUM(distancia_voada_km) AS total FROM viagens", return_df=True)
    total = int(df.iloc[0]['total'])
    return f"{format_number(total)} km"


@st.cache_data
def load_route_data():
    df = execute_query("""
        SELECT aeroporto_origem_sigla, aeroporto_destino_sigla, sigla_empresa, aeroporto_origem_pais, aeroporto_destino_pais
        FROM viagens
    """, return_df=True)

    df['aeroporto_origem_sigla'] = df['aeroporto_origem_sigla'].str.strip().str.upper()
    df['aeroporto_destino_sigla'] = df['aeroporto_destino_sigla'].str.strip().str.upper()
    return df

@st.cache_data
def enrich_with_airport_info(df):
    df_airports = pd.read_csv('data/airports.csv')
    df_airports = df_airports[df_airports['ident'].notnull()]
    df_airports['ident'] = df_airports['ident'].str.strip().str.upper()

    airport_iso = df_airports.set_index('ident')['iso_country'].to_dict()
    df['iso_country_origem'] = df['aeroporto_origem_sigla'].map(airport_iso)
    df['iso_country_destino'] = df['aeroporto_destino_sigla'].map(airport_iso)

    airport_name = df_airports.set_index('ident')['name'].to_dict()
    df['aeroporto_origem_nome'] = df['aeroporto_origem_sigla'].map(airport_name)
    df['aeroporto_destino_nome'] = df['aeroporto_destino_sigla'].map(airport_name)

    coords_dict = df_airports.set_index('ident')[['latitude_deg', 'longitude_deg']].to_dict(orient='index')
    df['origem_lat'] = df['aeroporto_origem_sigla'].map(lambda x: coords_dict.get(x, {}).get('latitude_deg'))
    df['origem_lon'] = df['aeroporto_origem_sigla'].map(lambda x: coords_dict.get(x, {}).get('longitude_deg'))
    df['destino_lat'] = df['aeroporto_destino_sigla'].map(lambda x: coords_dict.get(x, {}).get('latitude_deg'))
    df['destino_lon'] = df['aeroporto_destino_sigla'].map(lambda x: coords_dict.get(x, {}).get('longitude_deg'))

    df['aeroporto_origem_uf_pais'] = df['iso_country_origem'] + " - " + df['aeroporto_origem_pais']
    df['aeroporto_destino_uf_pais'] = df['iso_country_destino'] + " - " + df['aeroporto_destino_pais']

    df = df.dropna(subset=['origem_lat', 'origem_lon', 'destino_lat', 'destino_lon'])
    return df

@st.cache_data
def get_origin_country_options():
    df = load_route_data()
    df = enrich_with_airport_info(df)
    return sorted(df['aeroporto_origem_uf_pais'].dropna().unique())

@st.cache_data
def get_destination_country_options():
    df = load_route_data()
    df = enrich_with_airport_info(df)
    return sorted(df['aeroporto_destino_uf_pais'].dropna().unique())


@st.cache_data
def draw_filtered_map(origin_airport=None, destination_airport=None, origin_country=None, destination_country=None):
    df = load_route_data()
    df = enrich_with_airport_info(df)

    if origin_airport:
        df = df[df['aeroporto_origem_sigla'] == origin_airport]
    if destination_airport:
        df = df[df['aeroporto_destino_sigla'] == destination_airport]
    if origin_country:
        df = df[df['aeroporto_origem_uf_pais'] == origin_country]
    if destination_country:
        df = df[df['aeroporto_destino_uf_pais'] == destination_country]

    if len(df) == 0:
        st.warning("Nenhuma rota encontrada com os filtros aplicados. Por favor, ajuste os filtros.")
        return

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
                text=f"{empresa}: {row['aeroporto_origem_nome']} → {row['aeroporto_destino_nome']}"
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

@st.cache_data
def get_origin_airport_options():
    df = load_route_data()
    df = enrich_with_airport_info(df)
    return sorted(df[['aeroporto_origem_sigla', 'aeroporto_origem_nome']].drop_duplicates().dropna().apply(lambda x: f"{x['aeroporto_origem_sigla']} - {x['aeroporto_origem_nome']}", axis=1))

@st.cache_data
def get_destination_airport_options():
    df = load_route_data()
    df = enrich_with_airport_info(df)
    return sorted(df[['aeroporto_destino_sigla', 'aeroporto_destino_nome']].drop_duplicates().dropna().apply(lambda x: f"{x['aeroporto_destino_sigla']} - {x['aeroporto_destino_nome']}", axis=1))

@st.cache_data
def voos_improdutivos():
    df = execute_query("SELECT assentos, passageiros_pagos FROM viagens WHERE assentos and passageiros_pagos IS NOT NULL", return_df=True)
    
    df['metrica'] = (df['passageiros_pagos'] / df['assentos']) * 100
    total_voos = len(df)
    df_final = df[df['metrica'] < 70]
    total_voos_improdutivos = len(df_final)
    porcentagem_voos_improdutivos = (total_voos_improdutivos / total_voos) * 100
    
    return f'{porcentagem_voos_improdutivos:.2f}%'