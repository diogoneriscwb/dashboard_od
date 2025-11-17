import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(page_title="Análise Socioeconômica", layout="wide")
st.title("👥 Análise Socioeconômica e Demográfica")

# --- 1. Verificação e Carregamento dos Dados ---
if 'dados_carregados' not in st.session_state:
    st.error("Por favor, carregue o arquivo na página principal primeiro.")
    st.stop()

def encontrar_tabela_por_coluna(coluna_chave):
    for nome_aba, df in st.session_state.dados_carregados.items():
        if coluna_chave in df.columns:
            return df.copy()
    return None

df_socio = encontrar_tabela_por_coluna('escolaridadetabulada') # Coluna chave da tabela Sócio

if df_socio is None:
    st.error("Não foi possível encontrar a tabela 'Sócio' (com a coluna 'escolaridadetabulada').")
    st.stop()

st.info(f"Analisando {len(df_socio)} residentes.")

# --- 2. Gráficos Demográficos ---
col1, col2 = st.columns(2)

# Gráfico 1: Escolaridade (Pizza)
escolaridade_counts = df_socio['escolaridadetabulada'].value_counts().reset_index()
escolaridade_counts.columns = ['escolaridade', 'contagem']
fig_escolaridade = px.pie(
    escolaridade_counts,
    names='escolaridade',
    values='contagem',
    title="Nível de Escolaridade dos Residentes",
    hole=0.3
)
col1.plotly_chart(fig_escolaridade, use_container_width=True)

# Gráfico 2: Situação Familiar (Barra)
situacao_counts = df_socio['situacaotabulada'].value_counts().reset_index()
situacao_counts.columns = ['situacao', 'contagem']
fig_situacao = px.bar(
    situacao_counts,
    x='situacao',
    y='contagem',
    title="Composição Familiar (Situação no domicílio)"
)
col2.plotly_chart(fig_situacao, use_container_width=True)

st.markdown("---")

# --- 3. Pirâmide Etária e Renda ---
st.header("Distribuição de Idade e Renda")

# Gráfico 3: Pirâmide Etária
# Cria faixas etárias
bins = list(range(0, 90, 5)) # Faixas de 5 em 5 anos
labels = [f'{i}-{i+4}' for i in bins[:-1]]
df_socio['faixa_etaria'] = pd.cut(df_socio['idade'], bins=bins, labels=labels, right=False)

# Agrupa por faixa etária e sexo
df_piramide = df_socio.groupby(['faixa_etaria', 'sexo']).size().reset_index(name='contagem')

# Inverte a contagem de um sexo (ex: Masculino) para criar a pirâmide
df_piramide['contagem_piramide'] = df_piramide.apply(
    lambda row: row['contagem'] * -1 if row['sexo'] == 'MASCULINO' else row['contagem'],
    axis=1
)

fig_piramide = px.bar(
    df_piramide,
    x='contagem_piramide',
    y='faixa_etaria',
    color='sexo',
    title="Pirâmide Etária e por Sexo",
    orientation='h',
    labels={'contagem_piramide': 'Contagem', 'faixa_etaria': 'Faixa Etária'}
)
st.plotly_chart(fig_piramide, use_container_width=True)

# Gráfico 4: Histograma de Renda Mensal
# Limpeza: Converte para número, erros='coerce' transforma textos em NaN (inválido)
df_socio['renda_numerica'] = pd.to_numeric(df_socio['rendamensal'], errors='coerce')
# Filtra apenas quem informou renda (remove NaN e rendas 0)
df_renda = df_socio.dropna(subset=['renda_numerica'])
df_renda = df_renda[df_renda['renda_numerica'] > 0]

fig_renda = px.histogram(
    df_renda,
    x='renda_numerica',
    title="Histograma de Renda Mensal (Individual)",
    labels={'renda_numerica': 'Renda Mensal (R$)'}
)
st.plotly_chart(fig_renda, use_container_width=True)