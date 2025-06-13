import streamlit as st
from utils.sono.correlacoes import heatmap_exercicio_sono, heatmap_stress_sono, heatmap_obesidade_batimentos_sono

st.title("Correlações de sono com diversos fatores")
st.divider()
with st.container(border=True):
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Dados analisados: Duração e Qualidade do Sono, Atividade Física e Passos Diários")
        
        st.markdown("""
        **Principais observações:**

        - **Correlação positiva:** Atividade física e passos diários mostram uma correlação positiva com a *qualidade* do sono. Pessoas mais ativas tendem a ter um sono de melhor qualidade.
        - **Correlação moderada:** A *duração* do sono tem uma correlação moderada com a qualidade, indicando que mais tempo dormindo não significa, necessariamente, um sono melhor.
        - **Correlação negativa:** Há uma possível correlação negativa entre atividade física intensa (passos diários) e a *duração* do sono, sugerindo que exercício em excesso pode impactar o tempo de sono.
        """)
        
        st.subheader("💡 Implicações Práticas")

        st.success("**Recomendação:** Praticar atividade física moderada para melhorar a qualidade do sono.")
        
        st.warning("**Alerta:** Exercícios excessivos podem ter efeitos negativos na duração total do sono.")

    with col2:
        heatmap_exercicio_sono()

with st.container(border=True):
    col1, col2 = st.columns(2)
    with col1:
        heatmap_stress_sono()
    with col2:
        st.subheader("Dados analisados: Nível de Estresse e Qualidade do Sono")
        
        st.markdown("""
        **Principais observações:**
        - **Forte correlação negativa:** Quanto maior o nível de estresse, pior a qualidade do sono.
        - **Correlação moderada:** O estresse também pode impactar negativamente a duração do sono, mas com menor intensidade.
        - **Impacto principal:** A qualidade do sono parece ser a variável mais afetada pelo estresse.
        """)

        st.subheader("💡 Implicações Práticas")
        
        st.success("**Foco na Causa:** Estratégias de redução de estresse são cruciais para melhorar a qualidade do sono.")
        st.info("**Sugestão de Intervenção:** Técnicas de relaxamento, como *mindfulness* e meditação, podem ser particularmente eficazes.")


with st.container(border=True):
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Dados analisados: IMC, Batimentos Cardíacos e Qualidade do Sono")

        st.markdown("""
        **Principais observações:**
        - **Correlação positiva:** IMC elevado tende a se correlacionar com uma frequência cardíaca mais alta.
        - **Correlação negativa:** Um IMC mais alto está associado a uma pior qualidade do sono.
        - **Possível efeito cascata:** A frequência cardíaca elevada também pode se correlacionar negativamente com a qualidade do sono.
        """)

        st.subheader("💡 Implicações Práticas")

        st.success("**Saúde Integral:** O controle de peso é importante não apenas para a saúde cardiovascular, mas também para a qualidade do sono.")
        st.warning("**Atenção Específica:** Pessoas com IMC elevado podem se beneficiar de monitoramento cardíaco e intervenções focadas na melhoria do sono.")

    with col2:
        heatmap_obesidade_batimentos_sono()

