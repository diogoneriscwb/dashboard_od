import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Gestão da Pesquisa", layout="wide")
st.title("🏆 Gestão e Produtividade da Pesquisa")

# --- 1. Verificação e Carregamento dos Dados ---
if 'dados_carregados' not in st.session_state:
    st.error("Por favor, carregue o arquivo na página principal primeiro.")
    st.stop()

# Função para "adivinhar" qual tabela é qual, baseado nas colunas
def encontrar_tabela_por_coluna(coluna_chave):
    for nome_aba, df in st.session_state.dados_carregados.items():
        if coluna_chave in df.columns:
            return df.copy() # Retorna uma cópia para segurança
    return None

df_urbanistico = encontrar_tabela_por_coluna('condicaotabulada')
df_deslocamento = encontrar_tabela_por_coluna('cidadeori')

if df_urbanistico is None:
    st.error("Não foi possível encontrar a tabela 'Urbanisticos' (com a coluna 'condicaotabulada').")
    st.stop()

# --- 2. KPIs Principais (Cartões) ---
st.header("Visão Geral do Projeto")
total_domicilios_visitados = len(df_urbanistico)
domicilios_concluidos = len(df_urbanistico[df_urbanistico['condicaotabulada'] == 'Pesquisa concluída'])
total_deslocamentos = len(df_deslocamento) if df_deslocamento is not None else 0

col1, col2, col3 = st.columns(3)
col1.metric("Total de Domicílios Visitados", f"{total_domicilios_visitados:,}")
col2.metric("Pesquisas Concluídas", f"{domicilios_concluidos:,}")
col3.metric("Total de Deslocamentos Registrados", f"{total_deslocamentos:,}")

st.markdown("---")

# --- 3. Análise de Produtividade (Gráficos) ---
st.header("Produtividade da Equipe")

# Gráfico 1: Ranking de Pesquisadores (por pesquisas CONCLUÍDAS)
df_concluidas = df_urbanistico[df_urbanistico['condicaotabulada'] == 'Pesquisa concluída']
ranking = df_concluidas['nomepesquisador'].value_counts().reset_index()
ranking.columns = ['nomepesquisador', 'Total de Pesquisas Concluídas']

fig_ranking = px.bar(
    ranking.sort_values(by='Total de Pesquisas Concluídas', ascending=True),
    x='Total de Pesquisas Concluídas',
    y='nomepesquisador',
    title="Ranking de Produtividade (Pesquisas Concluídas)",
    text='Total de Pesquisas Concluídas',
    orientation='h'
)
fig_ranking.update_layout(yaxis_title="Pesquisador")
st.plotly_chart(fig_ranking, use_container_width=True)


col1, col2 = st.columns(2)

# Gráfico 2: Status das Pesquisas (Pizza)
status_counts = df_urbanistico['condicaotabulada'].value_counts().reset_index()
status_counts.columns = ['status', 'contagem']
fig_status = px.pie(
    status_counts,
    names='status',
    values='contagem',
    title="Resultado das Visitas (Status)",
    hole=0.3
)
col1.plotly_chart(fig_status, use_container_width=True)

# Gráfico 3: Pesquisas ao Longo do Tempo (Linha)
# Limpeza da coluna de data
df_urbanistico['data_pesquisa'] = pd.to_datetime(df_urbanistico['data'], format='%d/%m/%y %H:%M', errors='coerce')
pesquisas_por_dia = df_urbanistico.dropna(subset=['data_pesquisa']) \
                                .set_index('data_pesquisa') \
                                .resample('D') \
                                .size() \
                                .reset_index(name='Contagem')

fig_tempo = px.line(
    pesquisas_por_dia,
    x='data_pesquisa',
    y='Contagem',
    title="Volume de Pesquisas por Dia"
)
col2.plotly_chart(fig_tempo, use_container_width=True)