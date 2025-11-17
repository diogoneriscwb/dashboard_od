import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(page_title="Análise de Deslocamento", layout="wide")
st.title("🚗 Análise de Deslocamentos (O/D)")

# --- 1. Verificação e Carregamento dos Dados ---
if 'dados_carregados' not in st.session_state:
    st.error("Por favor, carregue o arquivo na página principal primeiro.")
    st.stop()


def encontrar_tabela_por_coluna(coluna_chave):
    for nome_aba, df in st.session_state.dados_carregados.items():
        if coluna_chave in df.columns:
            return df.copy()
    return None


df_deslocamento = encontrar_tabela_por_coluna('cidadeori')  # Acha a tabela

if df_deslocamento is None:
    st.error("Não foi possível encontrar a tabela 'Deslocamentos' (com a coluna 'cidadeori').")
    st.stop()

# Limpeza: Remove registros inválidos (onde idpesquisador é 0)
df_limpo = df_deslocamento[df_deslocamento['idpesquisador'] != 0].copy()
st.info(f"Analisando {len(df_limpo)} deslocamentos válidos.")

# --- 2. CRIAÇÃO DAS "LEGENDAS" (Mapas) ---
st.markdown("---")

# Mapa de Cidades (criado dinamicamente)
# 1. Pega todas as linhas onde 'cidadeoritabulada' NÃO está vazia
df_nomes_cidades = df_limpo.dropna(subset=['cidadeoritabulada']).copy()
df_nomes_cidades['cidadeoritabulada'] = df_nomes_cidades['cidadeoritabulada'].astype(str)
df_nomes_cidades = df_nomes_cidades[df_nomes_cidades['cidadeoritabulada'].str.strip() != '']
# 2. Cria o dicionário: {6: 'Guará/SIA/...', 14: 'Plano Piloto', ...}
mapa_cidades = pd.Series(
    df_nomes_cidades['cidadeoritabulada'].values,
    index=df_nomes_cidades['cidadeori']
).to_dict()

# Mapas de Modo e Motivo (fixos, pois as colunas tabuladas estão vazias)
# (Você pode adicionar mais IDs a estas listas se os vir nos gráficos)
mapa_modo = {
    1: 'A Pé',
    10: 'Ônibus Coletivo',
    13: 'Carro (Motorista)',
    0: 'Não Informado / Outros',
    # Adicione outros IDs que você vê
}

mapa_motivo = {
    0: 'Casa (Retorno)',
    1: 'Trabalho',
    2: 'Escola / Educação',
    5: 'Compras',
    6: 'Saúde',
    8: 'Lazer',
    # Adicione outros IDs que você vê
}
# --- FIM DAS LEGENDAS ---


# --- 3. Matriz Origem-Destino (Heatmap) ---
st.header("Matriz Origem-Destino (O/D)")
st.write("A matriz usa os IDs numéricos, mas os filtros e eixos mostram os nomes.")

# Pega todos os IDs de cidades que TEMOS um nome no mapa
ids_cidades_validas = sorted(list(mapa_cidades.keys()))

# Cria uma lista de Nomes para o filtro (ex: "6 - Guará/SIA/...")
opcoes_filtro_cidade = [f"{id_} - {mapa_cidades[id_]}" for id_ in ids_cidades_validas]

# Filtro Único:
cidades_selecionadas_filtro = st.multiselect(
    "Selecione as Cidades para a Matriz (Eixos X e Y):",
    options=opcoes_filtro_cidade,
    default=opcoes_filtro_cidade[:10]  # Pega os 10 primeiros
)

# Extrai os IDs numéricos do filtro (ex: "6 - Guará/SIA/..." -> 6)
ids_selecionados = [int(s.split(' - ')[0]) for s in cidades_selecionadas_filtro]

if not ids_selecionados:
    st.warning("Selecione pelo menos uma cidade no filtro acima.")
else:
    # 1. Filtra o DataFrame SÓ com os IDs numéricos
    df_filtrado = df_limpo[
        df_limpo['cidadeori'].isin(ids_selecionados) &
        df_limpo['cidadedes'].isin(ids_selecionados)
        ]

    # 2. Cria a matriz de contagem (usando IDs numéricos)
    matriz_od = df_filtrado.groupby(
        ['cidadeori', 'cidadedes']
    ).size().reset_index(name='contagem')

    matriz_pivot = matriz_od.pivot(
        index='cidadeori',
        columns='cidadedes',
        values='contagem'
    ).fillna(0)

    # 3. Força a Matriz a ser "Quadrada" (usando IDs)
    matriz_pivot = matriz_pivot.reindex(
        index=ids_selecionados,
        columns=ids_selecionados,
        fill_value=0
    )

    # --- A MÁGICA DA "LEGENDA" ---
    # Renomeia os índices (linhas) e colunas (cabeçalhos)
    # de números (6) para nomes ('Guará/SIA/...') usando o mapa
    matriz_pivot = matriz_pivot.rename(index=mapa_cidades, columns=mapa_cidades)
    # --- FIM DA MÁGICA ---

    # 4. Cria o gráfico (agora com nomes)
    fig_heatmap = px.imshow(
        matriz_pivot,
        text_auto=True,
        aspect="auto",
        title="Matriz de Deslocamentos (Origem vs. Destino)",
        labels=dict(x="Cidade de Destino", y="Cidade de Origem", color="Nº de Viagens")
    )
    fig_heatmap.update_layout(height=800)
    st.plotly_chart(fig_heatmap, use_container_width=True)

# --- 4. Outras Análises de Mobilidade ---
st.markdown("---")
col1, col2 = st.columns(2)

# Gráfico 1: Divisão Modal (Pizza)
st.subheader("Divisão Modal (Modo de Transporte)")
df_modo = df_limpo.dropna(subset=['modo']).copy()
# Cria a coluna de Nomes usando a "legenda" (mapa)
df_modo['modo_nome'] = df_modo['modo'].map(mapa_modo).fillna('Outro (ID ' + df_modo['modo'].astype(str) + ')')

modos_counts = df_modo['modo_nome'].value_counts().reset_index()
modos_counts.columns = ['modo_nome', 'contagem']
fig_modo = px.pie(
    modos_counts,
    names='modo_nome',  # <-- Usando Nomes
    values='contagem',
    title="Divisão Modal",
    hole=0.3
)
col1.plotly_chart(fig_modo, use_container_width=True)

# Gráfico 2: Motivo da Viagem (Barra)
st.subheader("Motivo da Viagem")
df_motivo = df_limpo.dropna(subset=['motivoori']).copy()
# Cria a coluna de Nomes usando a "legenda" (mapa)
df_motivo['motivo_nome'] = df_motivo['motivoori'].map(mapa_motivo).fillna(
    'Outro (ID ' + df_motivo['motivoori'].astype(str) + ')')

motivo_counts = df_motivo['motivo_nome'].value_counts().reset_index()
motivo_counts.columns = ['motivo_nome', 'contagem']
fig_motivo = px.bar(
    motivo_counts,
    x='motivo_nome',  # <-- Usando Nomes
    y='contagem',
    title="Principal Motivo na Origem"
)
col2.plotly_chart(fig_motivo, use_container_width=True)

# --- 5. Análise Temporal (Horários) ---
st.markdown("---")
st.header("Análise de Horários de Pico")

df_limpo['hora_saida'] = pd.to_datetime(df_limpo['horasaida'], format='%H:%M:%S', errors='coerce').dt.hour
contagem_por_hora = df_limpo.dropna(subset=['hora_saida']) \
    ['hora_saida'].value_counts() \
    .sort_index().reset_index()
contagem_por_hora.columns = ['Hora do Dia', 'Nº de Viagens']

fig_pico = px.bar(
    contagem_por_hora,
    x='Hora do Dia',
    y='Nº de Viagens',
    title="Viagens por Hora de Saída (Horários de Pico)"
)
st.plotly_chart(fig_pico, use_container_width=True)