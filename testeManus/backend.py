import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import sqlite3

def get_connection():
    return sqlite3.connect('testeManus/analytics_data.db', check_same_thread=False)

def execute_query(query, params=None, return_df=False):
    conn = get_connection()
    if not conn:
        return None
        
    try:
        cur = conn.cursor()
        if params == None:
            cur.execute(query)
        else:
            cur.execute(query, params)
        
        if query.strip().lower().startswith(('select', 'with')):
            if return_df:
                columns = [desc[0] for desc in cur.description]
                data = cur.fetchall()
                return pd.DataFrame(data, columns=columns)
            else:
                return cur.fetchall()
        else:
            conn.commit()
            return cur.rowcount
    except Exception as e:
        st.error(f"Erro na execução da query: {str(e)}")
        conn.rollback()
        return None
    finally:
        conn.close()

@st.cache_data
def load_route_data():
    df = execute_query("""
        SELECT origem_sigla AS aeroporto_origem_sigla, destino_sigla AS aeroporto_destino_sigla, empresa_sigla AS sigla_empresa, origem_pais AS aeroporto_origem_pais, destino_pais AS aeroporto_destino_pais
        FROM anac_flights_summary
    """, return_df=True)

    df['aeroporto_origem_sigla'] = df['aeroporto_origem_sigla'].str.strip().str.upper()
    df['aeroporto_destino_sigla'] = df['aeroporto_destino_sigla'].str.strip().str.upper()
    return df

@st.cache_data
def enrich_with_airport_info(df):
    df_airports = pd.read_csv('testeManus/airports.csv')
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
