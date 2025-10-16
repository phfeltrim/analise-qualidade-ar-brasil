import streamlit as st
import pandas as pd
import os
import joblib

# --- CONFIGURAÇÕES E CARREGAMENTO INICIAL ---

st.set_page_config(layout="wide", page_title="Dashboard Qualidade do Ar")

@st.cache_resource
def carregar_modelo():
    caminho_modelo = os.path.join('05_modelos', 'modelo_xgboost_mp25.pkl')
    if os.path.exists(caminho_modelo):
        modelo = joblib.load(caminho_modelo)
        return modelo
    return None

@st.cache_data
def carregar_dados():
    # Usamos o arquivo que foi salvo pelo notebook na Célula 3.1
    caminho_dados = os.path.join('02_dados_processados', 'dados_para_dashboard.csv')
    if os.path.exists(caminho_dados):
        df = pd.read_csv(caminho_dados, parse_dates=['datetime'])
        return df
    return pd.DataFrame() # Retorna um DataFrame vazio se o arquivo não existir

modelo = carregar_modelo()
df_wide = carregar_dados()

# --- SIDEBAR DE FILTROS ---

st.sidebar.header("Filtros da Análise")

if not df_wide.empty:
    # Filtro de Estação
    estacoes_disponiveis = df_wide['Estacao'].unique()
    estacao_selecionada = st.sidebar.selectbox("Selecione a Estação", estacoes_disponiveis)

    # Filtro de Poluente
    poluentes_disponiveis = [col for col in df_wide.columns if col not in ['datetime', 'Estacao']]
    poluente_selecionado = st.sidebar.selectbox("Selecione o Poluente", poluentes_disponiveis, index=poluentes_disponiveis.index('MP2.5') if 'MP2.5' in poluentes_disponiveis else 0)
    
    # Filtra o DataFrame com base nas seleções
    df_filtrado = df_wide[df_wide['Estacao'] == estacao_selecionada].set_index('datetime')
else:
    st.sidebar.error("Arquivo 'dados_para_dashboard.csv' não encontrado na pasta '02_dados_processados/'. Por favor, execute o notebook de análise primeiro.")
    st.stop()

# --- TÍTULO PRINCIPAL ---
st.title("Análise de Dados da Qualidade do Ar")
st.markdown(f"Analisando dados da estação: **{estacao_selecionada}**")


# --- SEÇÃO 1: VISÃO GERAL E SÉRIE TEMPORAL ---

st.header(f"Série Temporal de {poluente_selecionado}")

if not df_filtrado.empty and poluente_selecionado in df_filtrado.columns:
    # Gráfico de linha interativo
    st.line_chart(df_filtrado[poluente_selecionado])

    # KPIs
    col1, col2, col3 = st.columns(3)
    col1.metric("Média Geral", f"{df_filtrado[poluente_selecionado].mean():.2f} µg/m³")
    col2.metric("Valor Máximo", f"{df_filtrado[poluente_selecionado].max():.2f} µg/m³")
    col3.metric("Valor Mínimo", f"{df_filtrado[poluente_selecionado].min():.2f} µg/m³")

else:
    st.warning("Não há dados para exibir com os filtros selecionados.")
