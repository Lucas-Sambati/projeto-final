import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from backend import *

# Page configuration
st.set_page_config(
    page_title="Dashboard de Análise de Dados",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Database connection
@st.cache_resource
def get_connection():
    return sqlite3.connect('testeManus/analytics_data.db', check_same_thread=False)

# Load data functions
@st.cache_data
def load_sleep_data():
    conn = get_connection()
    query = "SELECT * FROM sleep_health_summary"
    df = pd.read_sql_query(query, conn)
    return df

@st.cache_data
def load_anac_data():
    conn = get_connection()
    query = "SELECT * FROM anac_flights_summary"
    df = pd.read_sql_query(query, conn)
    return df

# Main app
def main():
    st.title("📊 Dashboard de Análise de Dados")
    st.markdown("---")
    
    # Sidebar for navigation
    st.sidebar.title("Navegação")
    dataset_choice = st.sidebar.selectbox(
        "Escolha o conjunto de dados:",
        ["Saúde do Sono", "Dados de Voos ANAC"]
    )
    
    if dataset_choice == "Saúde do Sono":
        show_sleep_dashboard()
    else:
        show_anac_dashboard()

def show_sleep_dashboard():
    st.header("🛌 Análise de Saúde do Sono")
    
    # Load data
    df = load_sleep_data()
    
    # Sidebar filters
    st.sidebar.subheader("Filtros")
    
    # Gender filter
    genders = st.sidebar.multiselect(
        "Gênero:",
        options=df['Gender'].unique(),
        default=df['Gender'].unique()
    )
    
    # Age range filter
    age_range = st.sidebar.slider(
        "Faixa etária:",
        min_value=int(df['Age'].min()),
        max_value=int(df['Age'].max()),
        value=(int(df['Age'].min()), int(df['Age'].max()))
    )
    
    # Sleep duration filter
    sleep_duration_range = st.sidebar.slider(
        "Duração do sono (horas):",
        min_value=float(df['sleep_duration'].min()),
        max_value=float(df['sleep_duration'].max()),
        value=(float(df['sleep_duration'].min()), float(df['sleep_duration'].max())),
        step=0.1
    )
    
    # BMI Category filter
    bmi_categories = st.sidebar.multiselect(
        "Categoria de IMC:",
        options=df['bmi_category'].unique(),
        default=df['bmi_category'].unique()
    )
    
    # Apply filters
    filtered_df = df[
        (df['Gender'].isin(genders)) &
        (df['Age'].between(age_range[0], age_range[1])) &
        (df['sleep_duration'].between(sleep_duration_range[0], sleep_duration_range[1])) &
        (df['bmi_category'].isin(bmi_categories))
    ]
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total de Registros", len(filtered_df))
    
    with col2:
        avg_sleep = filtered_df['sleep_duration'].mean()
        st.metric("Duração Média do Sono", f"{avg_sleep:.1f}h")
    
    with col3:
        avg_quality = filtered_df['quality_of_sleep'].mean()
        st.metric("Qualidade Média do Sono", f"{avg_quality:.1f}/10")
    
    with col4:
        avg_stress = filtered_df['stress_level'].mean()
        st.metric("Nível Médio de Estresse", f"{avg_stress:.1f}/10")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Sleep duration by gender
        fig1 = px.box(
            filtered_df, 
            x='Gender', 
            y='sleep_duration',
            title="Distribuição da Duração do Sono por Gênero",
            color='Gender'
        )
        st.plotly_chart(fig1, use_container_width=True)
        
        # Sleep quality vs stress level
        fig3 = px.scatter(
            filtered_df,
            x='stress_level',
            y='quality_of_sleep',
            color='Gender',
            size='physical_activity_level',
            title="Qualidade do Sono vs Nível de Estresse",
            hover_data=['Age', 'Occupation']
        )
        st.plotly_chart(fig3, use_container_width=True)
    
    with col2:
        # Sleep disorders distribution
        disorder_counts = filtered_df['sleep_disorder'].value_counts()
        fig2 = px.pie(
            values=disorder_counts.values,
            names=disorder_counts.index,
            title="Distribuição de Distúrbios do Sono"
        )
        st.plotly_chart(fig2, use_container_width=True)
        
        # BMI Category vs Sleep Quality
        fig4 = px.violin(
            filtered_df,
            x='bmi_category',
            y='quality_of_sleep',
            title="Qualidade do Sono por Categoria de IMC",
            color='bmi_category'
        )
        st.plotly_chart(fig4, use_container_width=True)
    
    # Correlation heatmap
    st.subheader("Matriz de Correlação")
    numeric_cols = ['Age', 'sleep_duration', 'quality_of_sleep', 'physical_activity_level', 
                   'stress_level', 'systolic_pressure', 'diastolic_pressure', 'heart_rate', 'daily_steps']
    corr_matrix = filtered_df[numeric_cols].corr()
    
    fig_corr = px.imshow(
        corr_matrix,
        text_auto=True,
        aspect="auto",
        title="Correlação entre Variáveis Numéricas",
        color_continuous_scale='RdBu_r'
    )
    st.plotly_chart(fig_corr, use_container_width=True)
    
    # Data table
    st.subheader("Dados Filtrados")
    st.dataframe(filtered_df, use_container_width=True)

def show_anac_dashboard():
    st.header("✈️ Análise de Dados de Voos ANAC")
    
    # Load data
    df = load_anac_data()
    
    # Sidebar filters
    st.sidebar.subheader("Filtros")
    
    # Year filter
    years = st.sidebar.multiselect(
        "Ano:",
        options=sorted(df['ano'].unique()),
        default=sorted(df['ano'].unique())
    )
    
    # Month filter
    months = st.sidebar.multiselect(
        "Mês:",
        options=sorted(df['mes'].unique()),
        default=sorted(df['mes'].unique())
    )
    
    # Company nationality filter
    nationalities = st.sidebar.multiselect(
        "Nacionalidade da Empresa:",
        options=df['empresa_nacionalidade'].unique(),
        default=df['empresa_nacionalidade'].unique()
    )
    
    # Flight nature filter
    natures = st.sidebar.multiselect(
        "Natureza do Voo:",
        options=df['natureza'].unique(),
        default=df['natureza'].unique()
    )
    
    # Apply filters
    filtered_df = df[
        (df['ano'].isin(years)) &
        (df['mes'].isin(months)) &
        (df['empresa_nacionalidade'].isin(nationalities)) &
        (df['natureza'].isin(natures))
    ]
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total de Voos", len(filtered_df))
    
    with col2:
        total_passengers = filtered_df['passageiros_pagos'].sum() + filtered_df['passageiros_gratis'].sum()
        st.metric("Total de Passageiros", f"{total_passengers:,.0f}")
    
    with col3:
        total_cargo = filtered_df['carga_paga_kg'].sum() + filtered_df['carga_gratis_kg'].sum()
        st.metric("Total de Carga (kg)", f"{total_cargo:,.0f}")
    
    with col4:
        total_fuel = filtered_df['combustivel_litros'].sum()
        st.metric("Total de Combustível (L)", f"{total_fuel:,.0f}")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Passengers by month
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
        
        # Top companies by passengers
        company_passengers = filtered_df.groupby('empresa_nome').agg({
            'passageiros_pagos': 'sum',
            'passageiros_gratis': 'sum'
        }).reset_index()
        company_passengers['total_passengers'] = company_passengers['passageiros_pagos'] + company_passengers['passageiros_gratis']
        top_companies = company_passengers.nlargest(10, 'total_passengers')
        
        fig3 = px.bar(
            top_companies,
            x='total_passengers',
            y='empresa_nome',
            orientation='h',
            title="Top 10 Empresas por Passageiros",
            labels={'total_passengers': 'Total de Passageiros', 'empresa_nome': 'Empresa'}
        )
        st.plotly_chart(fig3, use_container_width=True)
    
    with col2:
        # Flight nature distribution
        nature_counts = filtered_df['natureza'].value_counts()
        fig2 = px.pie(
            values=nature_counts.values,
            names=nature_counts.index,
            title="Distribuição por Natureza do Voo"
        )
        st.plotly_chart(fig2, use_container_width=True)
        
        # Regional distribution (origin)
        region_counts = filtered_df['origem_regiao'].value_counts()
        fig4 = px.bar(
            x=region_counts.values,
            y=region_counts.index,
            orientation='h',
            title="Distribuição por Região de Origem",
            labels={'x': 'Número de Voos', 'y': 'Região'}
        )
        st.plotly_chart(fig4, use_container_width=True)
    
    # Fuel consumption vs distance
    st.subheader("Análise de Eficiência")
    
    # Filter out zero values for meaningful analysis
    efficiency_df = filtered_df[
        (filtered_df['combustivel_litros'] > 0) & 
        (filtered_df['distancia_voada_km'] > 0)
    ].copy()
    
    if len(efficiency_df) > 0:
        efficiency_df['fuel_efficiency'] = efficiency_df['combustivel_litros'] / efficiency_df['distancia_voada_km']
        
        fig_efficiency = px.scatter(
            efficiency_df,
            x='distancia_voada_km',
            y='combustivel_litros',
            color='empresa_nacionalidade',
            size='passageiros_pagos',
            title="Consumo de Combustível vs Distância Voada",
            hover_data=['empresa_nome', 'fuel_efficiency'],
            labels={
                'distancia_voada_km': 'Distância Voada (km)',
                'combustivel_litros': 'Combustível (L)'
            }
        )
        st.plotly_chart(fig_efficiency, use_container_width=True)
    
    # Data table
    st.subheader("Dados Filtrados")
    st.dataframe(filtered_df, use_container_width=True)
    
    st.subheader("Visualização de Rotas")
    query_params = st.query_params
    reset_triggered = "reset" in query_params

    if reset_triggered:
        st.query_params.clear()

    origin_airport = st.selectbox(
        "Aeroporto de Origem",
        [""] + get_origin_airport_options(),
        index=0 if reset_triggered else None,
        key="origin_airport"
    )

    destination_airport = st.selectbox(
        "Aeroporto de Destino",
        [""] + get_destination_airport_options(),
        index=0 if reset_triggered else None,
        key="destination_airport"
    )

    origin_country = st.selectbox(
        "País de Origem",
        [""] + get_origin_country_options(),
        index=0 if reset_triggered else None,
        key="origin_country"
    )

    destination_country = st.selectbox(
        "País de Destino",
        [""] + get_destination_country_options(),
        index=0 if reset_triggered else None,
        key="destination_country"
    )

    if st.button("Resetar Filtros"):
        st.query_params["reset"] = "true"
        st.rerun()

    def parse_code(option):
        return option.split(" - ")[0] if option else None

    with st.container(border=True):
        draw_filtered_map(
            origin_airport=parse_code(origin_airport),
            destination_airport=parse_code(destination_airport),
            origin_country=origin_country if parse_code(origin_country) else None,
            destination_country=destination_country if parse_code(destination_country) else None
        )

if __name__ == "__main__":
    main()

