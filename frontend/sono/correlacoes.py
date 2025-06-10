import streamlit as st
from utils.sono.correlacoes import heatmap_exercicio_sono, heatmap_stress_sono, heatmap_obesidade_batimentos_sono

st.title("Correlações de sono com diversos fatores")
heatmap_exercicio_sono()
st.subheader("""Dados analisados: Duração do sono, qualidade do sono, atividade física e passos diários.

***Principais observações***:

Provavelmente mostra uma correlação positiva entre atividade física/passos diários e qualidade do sono, indicando que pessoas mais ativas tendem a ter melhor qualidade de sono.

A duração do sono pode mostrar uma correlação moderada com a qualidade do sono, já que quantidade e qualidade nem sempre andam juntas.

Possivelmente há uma correlação negativa entre atividade física intensa (muitos passos) e duração do sono, sugerindo que exercício excessivo pode reduzir horas de sono.

***Implicações práticas***:

Recomendar atividade física moderada para melhorar a qualidade do sono

Alertar sobre possíveis efeitos negativos de exercícios excessivos na duração do sono""")

heatmap_stress_sono()
st.subheader("""Dados analisados: Duração do sono, qualidade do sono e nível de estresse.

***Principais observações***:

Forte correlação negativa entre nível de estresse e qualidade do sono (quanto mais estresse, pior o sono)

Possível correlação negativa moderada entre estresse e duração do sono

A qualidade do sono parece ser mais afetada pelo estresse do que a duração

***Implicações práticas***:

Estratégias de redução de estresse são cruciais para melhorar a qualidade do sono

Intervenções como mindfulness e técnicas de relaxamento podem ser particularmente eficazes""")

heatmap_obesidade_batimentos_sono()
st.subheader("""Dados analisados: Nível de IMC (convertido para escala numérica), taxa de batimentos cardíacos e qualidade do sono.

***Principais observações***:

Correlação positiva entre IMC elevado e taxa de batimentos (pessoas com sobrepeso tendem a ter frequência cardíaca mais alta)

Correlação negativa entre IMC elevado e qualidade do sono

Possível correlação negativa entre taxa de batimentos e qualidade do sono

***Implicações práticas***:

Controle de peso é importante não só para saúde cardiovascular mas também para qualidade do sono

Pessoas com IMC elevado podem se beneficiar de monitoramento cardíaco e intervenções para melhorar o sono""")

st.title("Conclusões gerais")
st.subheader("""Fatores de estilo de vida (exercício, estresse, peso) têm impacto significativo na qualidade do sono

Qualidade do sono parece ser mais sensível a esses fatores do que a duração do sono

Abordagem holística é necessária para melhorar a saúde do sono, considerando atividade física, gestão de estresse e controle de peso

Intervenções personalizadas podem ser desenvolvidas com base nessas correlações para diferentes perfis de pacientes""")