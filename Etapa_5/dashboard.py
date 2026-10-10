import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Configuração da página
st.set_page_config(page_title="AgroSmart Dashboard", page_icon="🌱", layout="wide")

st.title("🌱 AgroSmart - Painel de Gestão Agrícola")
st.markdown("Monitoramento de Telemetria e Alertas (Camada Silver)")

# 1. Tentar ler o arquivo real da Etapa 3
try:
    df_real = pd.read_csv('../Etapa_3/telemetria_silver.csv')
    leitura_atual = df_real.iloc[-1] # Pega a última linha
except FileNotFoundError:
    st.error("Arquivo telemetria_silver.csv não encontrado. Verifique o caminho.")
    st.stop()

# 2. Criar dados históricos simulados (para o gráfico ficar bonito para a apresentação)
# Como só temos 1 leitura no CSV, vamos gerar 10 horas de passado falso para o gráfico
horarios = [datetime.strptime(leitura_atual['timestamp_ingestao'], "%Y-%m-%d %H:%M:%S") - timedelta(hours=i) for i in range(10, 0, -1)]
horarios.append(datetime.strptime(leitura_atual['timestamp_ingestao'], "%Y-%m-%d %H:%M:%S"))

dados_historicos = pd.DataFrame({
    'Horário': horarios,
    'Temperatura (°C)': [22.0, 22.5, 23.1, 23.8, 24.0, 24.5, 24.7, 24.9, 25.1, 24.8, leitura_atual['temperatura_c']],
    'Umidade do Solo (%)': [60.0, 58.0, 55.0, 52.0, 50.0, 49.0, 48.0, 47.5, 47.0, 47.0, leitura_atual['umidade_solo_pct']]
})

# 3. Exibir KPIs Principais
st.subheader(f"📍 Última Leitura: {leitura_atual['device_id']} ({leitura_atual['timestamp_ingestao']})")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Temperatura", f"{leitura_atual['temperatura_c']} °C")
col2.metric("Umidade Solo", f"{leitura_atual['umidade_solo_pct']} %")
col3.metric("Luminosidade", f"{leitura_atual['luminosidade_pct']} %")

# Cor do status baseado na regra de negócio
cor_status = "red" if leitura_atual['status_solo'] == 'CRÍTICO' else ("orange" if leitura_atual['status_solo'] == 'ALERTA' else "green")
col4.markdown(f"### Status: <span style='color:{cor_status}'>{leitura_atual['status_solo']}</span>", unsafe_allow_html=True)
col4.markdown(f"**Índice de Estresse:** {leitura_atual['indice_estresse']}")

st.divider()

# 4. Gráfico Histórico
st.subheader("📈 Evolução Climática (Últimas 10 horas)")
st.line_chart(dados_historicos.set_index('Horário'))

# 5. Tabela de Dados Brutos
st.subheader("🗄️ Dados Processados (Camada Silver)")
st.dataframe(df_real)