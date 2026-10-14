import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

st.set_page_config(page_title="Dashboard IoT - Disruptive Architectures", page_icon="🌡️", layout="wide")

# Conexão com o PostgreSQL
DB_URL = 'postgresql://postgres:sua_senha@localhost:5432/postgres'
engine = create_engine(DB_URL)

@st.cache_data
def load_data(query):
    return pd.read_sql(query, engine)

st.title("🌡️ Pipeline de Dados com IoT, Big Data e IA")
st.markdown("Painel analítico desenvolvido para monitorização de sensores de temperatura (UniFECAF).")

# --- BARRA LATERAL INTERATIVA ---
st.sidebar.header("🎛️ Filtros do Sistema")
try:
    df_devices = load_data("SELECT DISTINCT device_id FROM temperature_readings")
    dispositivos = df_devices['device_id'].tolist()
    filtro_disp = st.sidebar.multiselect("Selecione o Dispositivo:", options=dispositivos, default=dispositivos)
except Exception:
    filtro_disp = []

st.sidebar.markdown("---")
st.sidebar.info("Projeto prático integrado com PostgreSQL e Streamlit.")

# --- MÉTRICAS GLOBAIS ---
try:
    df_metricas = load_data("SELECT AVG(temperature) as med, MAX(temperature) as mx, MIN(temperature) as mn FROM temperature_readings")
    c1, c2, c3 = st.columns(3)
    c1.metric("Temperatura Média Geral", f"{df_metricas['med'].values[0]:.2f} °C")
    c2.metric("Temperatura Máxima", f"{df_metricas['mx'].values[0]:.2f} °C")
    c3.metric("Temperatura Mínima", f"{df_metricas['mn'].values[0]:.2f} °C")
    st.markdown("---")
except Exception:
    pass

# --- GRÁFICO 1 ---
st.subheader("📊 Média de Temperatura por Dispositivo")
try:
    if filtro_disp:
        placeholders = ','.join([f"'{d}'" for d in filtro_disp])
        q1 = f"SELECT device_id, AVG(temperature) as avg_temp FROM temperature_readings WHERE device_id IN ({placeholders}) GROUP BY device_id"
    else:
        q1 = "SELECT * FROM avg_temp_por_dispositivo"
        
    df_avg = load_data(q1)
    fig1 = px.bar(df_avg, x='device_id', y='avg_temp', color='device_id', template='plotly_white')
    st.plotly_chart(fig1, use_container_width=True)
except Exception as e:
    st.warning("Aguardando conexão com o banco PostgreSQL para carregar o Gráfico 1.")

# --- GRÁFICOS 2 E 3 EM COLUNAS ---
colA, colB = st.columns(2)

with colA:
    st.subheader("📈 Leituras por Hora do Dia")
    try:
        df_hora = load_data("SELECT * FROM leituras_por_hora")
        fig2 = px.line(df_hora, x='hora', y='contagem', markers=True, template='plotly_white')
        st.plotly_chart(fig2, use_container_width=True)
    except Exception:
        st.warning("Dados indisponíveis.")

with colB:
    st.subheader("📉 Máximas e Mínimas por Dia")
    try:
        df_dia = load_data("SELECT * FROM temp_max_min_por_dia")
        fig3 = px.line(df_dia, x='data', y=['temp_max', 'temp_min'], template='plotly_white')
        st.plotly_chart(fig3, use_container_width=True)
    except Exception:
        st.warning("Dados indisponíveis.")