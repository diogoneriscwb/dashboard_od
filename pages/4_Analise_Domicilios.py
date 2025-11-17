import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(page_title="Análise de Domicílios", layout="wide")
st.title("🏠 Análise de Domicílios e Infraestrutura")

# --- 1. Verificação e Carregamento dos Dados ---
if 'dados_carregados' not in st.session_state:
    st.error("Por favor, carregue o arquivo na página principal primeiro.")
    st.stop()

def encontrar_tabela_por_coluna(coluna_chave):
    for nome_aba, df in st.session_state.dados_carregados.items():
        if coluna_chave in df.columns:
            return df.copy()
    return None

df_urbanistico = encontrar_tabela_por_coluna('tipodomicilio') # Coluna chave

if df_urbanistico is None:
    st.error("Não foi possível encontrar a tabela 'Urbanisticos' (com a coluna 'tipodomicilio').")
    st.stop()

# Limpeza: Analisa apenas pesquisas concluídas
df_limpo = df_urbanistico[df_urbanistico['condicaotabulada'] == 'Pesquisa concluída'].copy()
st.info(f"Analisando {len(df_limpo)} domicílios concluídos.")

# --- 2. Análise de Domicílios ---
col1, col2 = st.columns(2)

# Gráfico 1: Tipo de Domicílio (Barra)
tipo_counts = df_limpo['tipodomicilio'].value_counts().reset_index()
tipo_counts.columns = ['tipo', 'contagem']
fig_tipo = px.bar(
    tipo_counts,
    x='tipo',
    y='contagem',
    title="Tipo de Domicílio"
)
col1.plotly_chart(fig_tipo, use_container_width=True)

# Gráfico 2: Domicílios por Cidade (Pizza)
cidade_counts = df_limpo['cidaderesidencia'].value_counts().reset_index()
cidade_counts.columns = ['cidade', 'contagem']
fig_cidade = px.pie(
    cidade_counts,
    names='cidade',
    values='contagem',
    title="Distribuição de Domicílios por Cidade",
    hole=0.3
)
col2.plotly_chart(fig_cidade, use_container_width=True)

st.markdown("---")
st.header("Infraestrutura e Renda Familiar")

# --- 3. Posse de Bens e Renda ---

# Gráfico 3: Posse de Veículos e Internet (KPIs)
col1, col2, col3 = st.columns(3)
col1.metric("Possui Veículo", f"{df_limpo['possuiveiculo'].sum()} Domicílios")
col2.metric("Possui Internet", f"{df_limpo['internet'].sum()} Domicílios")
col3.metric("Nº Médio de Residentes", f"{df_limpo['numresidentes'].mean():.2f} pessoas")

# Gráfico 4: Histograma de Renda Familiar
# Limpeza: Remove valores -1, -2, etc.
df_limpo['renda_familiar_num'] = pd.to_numeric(df_limpo['rendafamiliar'], errors='coerce')
df_renda_fam = df_limpo[df_limpo['renda_familiar_num'] > 0]

fig_renda_fam = px.histogram(
    df_renda_fam,
    x='renda_familiar_num',
    title="Histograma de Renda Familiar",
    labels={'renda_familiar_num': 'Renda Familiar (R$)'}
)
st.plotly_chart(fig_renda_fam, use_container_width=True)