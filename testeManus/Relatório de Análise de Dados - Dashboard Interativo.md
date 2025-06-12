# Relatório de Análise de Dados - Dashboard Interativo

## Resumo Executivo

Este projeto implementou um fluxo completo de análise de dados em dois conjuntos de dados distintos:
1. **Sleep Health and Lifestyle Dataset** - Dados sobre saúde do sono e estilo de vida
2. **Dados de Voos ANAC 2025** - Dados estatísticos de voos da Agência Nacional de Aviação Civil

## Exploração dos Dados

### Dataset 1: Sleep Health and Lifestyle
- **Registros**: 374 entradas
- **Colunas**: 13 variáveis incluindo dados demográficos, métricas de sono, atividade física e saúde
- **Problemas identificados**: 
  - 219 valores nulos na coluna 'Sleep Disorder' (58.6% dos dados)
  - Campo 'Blood Pressure' necessitava separação em pressão sistólica e diastólica
- **Sem duplicatas**

### Dataset 2: Dados de Voos ANAC
- **Registros**: 13.329 entradas
- **Colunas**: 38 variáveis sobre operações de voo, empresas, aeroportos e métricas operacionais
- **Problemas identificados**:
  - Múltiplas colunas com valores nulos (UF e Região dos aeroportos)
  - Dados de métricas operacionais com valores ausentes
  - Campo 'HORAS VOADAS' em formato texto
- **Sem duplicatas**

## Limpeza e Padronização

### Tratamento de Dados Ausentes
- **Sleep Dataset**: Valores nulos em 'Sleep Disorder' preenchidos com 'None'
- **ANAC Dataset**: 
  - UF/Região ausentes preenchidos com 'Desconhecido'
  - Métricas numéricas ausentes preenchidas com 0
  - 'HORAS VOADAS' convertido para numérico

### Transformações Aplicadas
- Separação da pressão arterial em componentes sistólica e diastólica
- Conversão de tipos de dados para formatos apropriados
- Padronização de encoding (latin1 para dados ANAC)

## Banco de Dados SQLite

### Estrutura
- **Tabela**: `sleep_health` - dados limpos de saúde do sono
- **Tabela**: `anac_flights` - dados limpos de voos ANAC
- **Views SQL**:
  - `sleep_health_summary` - view simplificada dos dados de sono
  - `anac_flights_summary` - view com nomes de colunas padronizados

## Dashboard Interativo Streamlit

### Funcionalidades Implementadas

#### Análise de Saúde do Sono
- **Filtros interativos**:
  - Seleção de gênero (múltipla escolha)
  - Faixa etária (slider)
  - Duração do sono (slider)
  - Categoria de IMC (múltipla escolha)

- **Métricas principais**:
  - Total de registros
  - Duração média do sono
  - Qualidade média do sono
  - Nível médio de estresse

- **Visualizações**:
  - Box plot: Distribuição da duração do sono por gênero
  - Gráfico de pizza: Distribuição de distúrbios do sono
  - Scatter plot: Qualidade do sono vs nível de estresse
  - Violin plot: Qualidade do sono por categoria de IMC
  - Heatmap: Matriz de correlação entre variáveis numéricas

#### Análise de Dados de Voos ANAC
- **Filtros interativos**:
  - Ano (múltipla escolha)
  - Mês (múltipla escolha)
  - Nacionalidade da empresa (múltipla escolha)
  - Natureza do voo (múltipla escolha)

- **Métricas principais**:
  - Total de voos
  - Total de passageiros
  - Total de carga (kg)
  - Total de combustível (L)

- **Visualizações**:
  - Gráfico de linha: Evolução mensal de passageiros
  - Gráfico de pizza: Distribuição por natureza do voo
  - Gráfico de barras: Top 10 empresas por passageiros
  - Gráfico de barras: Distribuição por região de origem
  - Scatter plot: Análise de eficiência (combustível vs distância)

### Recursos Técnicos
- Interface responsiva com sidebar para navegação
- Filtros dinâmicos que atualizam visualizações em tempo real
- Tabelas de dados filtrados para exploração detalhada
- Gráficos interativos usando Plotly
- Cache de dados para performance otimizada

## Insights Principais

### Saúde do Sono
- Mulheres tendem a ter duração de sono ligeiramente maior que homens
- 58.6% dos participantes não apresentam distúrbios do sono
- Correlação negativa entre nível de estresse e qualidade do sono
- Categoria de IMC mostra variação na qualidade do sono

### Dados de Voos ANAC
- Dados cobrem os primeiros 4 meses de 2025
- Predominância de voos domésticos sobre internacionais
- Empresas brasileiras e estrangeiras bem representadas
- Análise de eficiência mostra relação entre consumo de combustível e distância

## Tecnologias Utilizadas
- **Python 3.11** - Linguagem principal
- **Pandas** - Manipulação e análise de dados
- **SQLite** - Banco de dados relacional
- **Streamlit** - Framework para dashboard web
- **Plotly** - Visualizações interativas
- **NumPy** - Computação numérica

## Acesso ao Dashboard
O dashboard está disponível publicamente em:
https://8501-i70bxw1ykz8t6bxapk5k7-80205deb.manusvm.computer

## Conclusão
O projeto demonstra um fluxo completo de análise de dados, desde a exploração inicial até a entrega de um dashboard interativo funcional. Os dados foram adequadamente limpos, organizados em banco de dados relacional e apresentados através de uma interface intuitiva que permite exploração dinâmica pelos usuários.

