import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from db.sono.banco import execute_query
from io import BytesIO
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import MinMaxScaler

query = """
SELECT profissao, condicao_sono, taxa_batimentos, nivel_estresse, genero
FROM pessoas
"""  
df = execute_query(query, return_df=True)

@st.cache_data
def show_occupation_count_chart():
# CONTAGEM DE PROFISSIONAIS
    contagem = df['profissao'].value_counts().reset_index()
    contagem.columns = ['profissao', 'Frequência']

    fig = px.bar(
        contagem,
        x='Frequência',
        y='profissao',
        orientation='h',
        color='profissao',
        color_discrete_sequence=px.colors.diverging.RdBu_r,
        title='Contagem de Profissões',
        labels={
            'Frequência': 'Número de Pessoas',
            'profissao': 'Profissão'
        },
        height=600
    )

    st.plotly_chart(fig, use_container_width=True)
    
@st.cache_data
def show_sleep_disorder_frequency_chart():
# HEATMAP
    sleep_crosstab = pd.crosstab(
        df['profissao'], 
        df['condicao_sono'],
        normalize='index'
    )
    
    fig_corr = px.imshow(
        sleep_crosstab,
        text_auto=True,
        aspect="auto",
        title="Correlação entre Variáveis Sono e Profissão",
        color_continuous_scale='Blues'
    )
    st.plotly_chart(fig_corr, use_container_width=True)

@st.cache_data
def show_stress_level_heart_rate_chart():
    agg_df = df.groupby('profissao').agg(
        avg_heart_rate=('taxa_batimentos', 'mean'),
        avg_stress=('nivel_estresse', 'mean')
    ).reset_index().sort_values(by='avg_heart_rate', ascending=False)

    scaler = MinMaxScaler()
    agg_df['stress_normalized'] = scaler.fit_transform(agg_df[['avg_stress']])
    colors = px.colors.diverging.RdBu_r
    color_scale = [colors[int(val * (len(colors)-1))] for val in agg_df['stress_normalized']]

    bar = go.Bar(
        x=agg_df['avg_heart_rate'],
        y=agg_df['profissao'],
        orientation='h',
        name='Média de Batimentos Cardíacos',
        marker=dict(color=color_scale),
    )

    line = go.Scatter(
        x=agg_df['avg_stress'],
        y=agg_df['profissao'],
        mode='lines+markers',
        name='Nível Médio de Estresse',
        marker=dict(color='crimson'),
        line=dict(width=3),
        xaxis='x2'
    )

    max_hr = agg_df['avg_heart_rate'].max()
    range_max = ((max_hr // 10) + 1) * 10

    layout = go.Layout(
        title='Batimentos Cardíacos e Estresse por Profissão',
        xaxis=dict(
            title=dict(text='Média de Batimentos Cardíacos', font=dict(color='royalblue')),
            tickfont=dict(color='royalblue'),
            tickmode='linear',
            tick0=0,
            dtick=10,
            range=[0, range_max]
        ),
        xaxis2=dict(
            tickfont=dict(color='crimson'),
            overlaying='x',
            side='top'
        ),
        yaxis=dict(
            title=dict(text='Profissão'),
            automargin=True
        ),
        template='simple_white'
    )

    fig = go.Figure(data=[bar, line], layout=layout)
    fig.update_yaxes(autorange='reversed')

    st.plotly_chart(fig, use_container_width=True)



def show_health_risk_per_occupation():
    risk_df = df.groupby('profissao').agg(
        sleep_apnea_prevalence=('condicao_sono', lambda x: (x == 'Sleep Apnea').mean()),
        avg_heart_rate=('taxa_batimentos', 'mean'),
        avg_stress=('nivel_estresse', 'mean')
    ).reset_index()

    # Cria o scatter plot
    fig = px.scatter(
        risk_df,
        x='sleep_apnea_prevalence',
        y='avg_heart_rate',
        size='avg_stress',
        color='profissao',
        color_discrete_sequence=px.colors.diverging.RdBu_r,
        size_max=50,
        opacity=0.8,
        labels={
            'sleep_apnea_prevalence': 'Prevalência de Apneia do Sono',
            'avg_heart_rate': 'Média de Batimentos Cardíacos',
            'avg_stress': 'Nível Médio de Estresse',
            'profissao': 'Profissão'
        },
        title='Risco de Saúde por Ocupação'
    )

    # Adiciona anotações para pontos com prevalência > 0.3
    for i, row in risk_df[risk_df['sleep_apnea_prevalence'] > 0.3].iterrows():
        fig.add_annotation(
            x=row['sleep_apnea_prevalence'],
            y=row['avg_heart_rate'],
            text=row['profissao'],
            showarrow=True,
            arrowhead=2,
            ax=20,
            ay=-20,
            font=dict(color='red', size=12)
        )

    st.plotly_chart(fig, use_container_width=True)
