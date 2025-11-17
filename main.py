import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Dashboard Pesquisa O/D", layout="wide")


# --- 1. FUNÇÃO DE CARREGAMENTO COM CACHE ---
@st.cache_data
def carregar_dados_csv():
    """
    Carrega os 3 arquivos CSV da pasta 'data' e os retorna
    em um dicionário.

    *** ATUALIZAÇÃO: sep=',' e encoding='latin1' ***
    """
    tabelas_dict = {}

    # Define os caminhos
    caminho_deslocamento = os.path.join("data", "deslocamentos.csv")
    caminho_socio = os.path.join("data", "socio.csv")
    caminho_urbanistico = os.path.join("data", "urbanisticos.csv")

    # Lista de arquivos para verificar
    arquivos_necessarios = {
        "Deslocamentos": caminho_deslocamento,
        "Socio": caminho_socio,
        "Urbanisticos": caminho_urbanistico
    }

    try:
        # Tenta carregar cada arquivo
        for nome_aba, caminho in arquivos_necessarios.items():
            if not os.path.exists(caminho):
                st.error(f"ERRO: Arquivo não encontrado: {caminho}")
                st.warning("Verifique se o nome do arquivo CSV está correto na pasta 'data'.")
                return None

            # --- ESTA É A CONFIGURAÇÃO MAIS PROVÁVEL ---
            tabelas_dict[nome_aba] = pd.read_csv(
                caminho,
                sep=',',  # <-- CORRETO: O separador é vírgula
                encoding='latin1',  # <-- CORRIGIDO: Para lidar com 'Guará', 'Almeida'
                on_bad_lines='skip',  # Ignora linhas problemáticas se houver
                low_memory=False  # Ajuda a ler arquivos grandes sem adivinhar tipos
            )

        return tabelas_dict

    except Exception as e:
        st.error(f"Erro crítico ao ler os arquivos CSV: {e}")
        return None


# --- 2. CARREGAMENTO AUTOMÁTICO ---
if 'dados_carregados' not in st.session_state:
    with st.spinner("Carregando dados..."):
        st.session_state.dados_carregados = carregar_dados_csv()

# --- 3. PÁGINA "HOME" ---
st.title("📊 Dashboard de Análise da Pesquisa O/D")
st.write("Este dashboard analisa os dados da Pesquisa Origem-Destino.")

if st.session_state.get('dados_carregados') is not None:
    st.success("Dados carregados com sucesso!")
    st.write("As seguintes tabelas estão prontas para análise:")

    for nome_aba, df in st.session_state.dados_carregados.items():
        st.write(f"- **{nome_aba}**: {len(df)} linhas")

    st.info("Navegue pelas páginas na barra lateral à esquerda para iniciar as análises.")
else:
    st.error("Falha ao carregar os dados. Verifique o terminal do PyCharm para erros.")