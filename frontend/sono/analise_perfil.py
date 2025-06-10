import streamlit as st
from utils.sono.analise_perfil import grafico_idade, grafico_profissao_stress, grafico_imc_por_profissao, tabela_filtragens

st.write("Análise Perfil")

selecao = st.selectbox("",['idade', 'genero', 'profissao', 'nivel_IMC'])
grafico_idade(selecao)

grafico_profissao_stress(selecao)

tabela_filtragens()

import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from db.banco import execute_query


