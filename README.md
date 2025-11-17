# 📊 Dashboard de Análise de Mobilidade (O/D)

Este projeto é um dashboard web interativo construído para analisar dados de uma Pesquisa de Mobilidade Urbana (Origem-Destino). Ele permite a visualização de padrões de deslocamento, perfis socioeconômicos e características dos domicílios.

## 🚀 Demo Online

**Você pode acessar o dashboard ao vivo neste link:**

[**https://seu-link-aqui.streamlit.app**](https://seu-link-aqui.streamlit.app)

*(Substitua o link acima pelo seu link do Streamlit Community Cloud após o deploy)*

---

## 📋 Funcionalidades (Páginas)

O dashboard é dividido em quatro seções principais de análise:

1.  **Gestão da Pesquisa:**
    * KPIs de progresso do projeto (visitas, pesquisas concluídas).
    * Ranking de produtividade dos pesquisadores.
    * Análise do status das visitas (concluídas, ausentes, etc.).

2.  **Análise de Deslocamentos:**
    * Heatmap (Matriz O/D) interativo com os fluxos de viagem entre regiões.
    * Gráficos de divisão modal (como as pessoas se movem).
    * Análise dos principais motivos de viagem.
    * Gráfico de horários de pico.

3.  **Análise Socioeconômica:**
    * Perfil demográfico dos residentes (escolaridade, situação familiar).
    * Pirâmide etária e divisão por sexo.
    * Histograma de renda individual.

4.  **Análise de Domicílios:**
    * Distribuição dos tipos de domicílio (casa, apartamento).
    * Infraestrutura residencial (posse de internet, veículos).
    * Histograma de renda familiar.

---

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python
* **Dashboard:** Streamlit
* **Manipulação de Dados:** Pandas
* **Gráficos:** Plotly Express
* **Hospedagem:** Streamlit Community Cloud

---

## 🏃 Como Executar Localmente

1.  Clone este repositório:
    ```bash
    git clone [https://github.com/diogoneriscwb/dashboard_od.git](https://github.com/diogoneriscwb/dashboard_od.git)
    cd dashboard_od
    ```
2.  Crie e ative um ambiente virtual:
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows: .\venv\Scripts\activate
    ```
3.  Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```
4.  Execute o aplicativo Streamlit:
    ```bash
    streamlit run main.py
    ```