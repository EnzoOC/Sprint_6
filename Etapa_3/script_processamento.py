import json
import pandas as pd
from datetime import datetime

# 1. Simulação da extração de dados brutos (Camada Bronze / TinkerCad)
payload_bruto = {
    "device_id": "TINKER-TALHAO-01",
    "temperatura_c": 24.78,
    "luminosidade_pct": 56.00,
    "umidade_solo_pct": 47.00
}

def processar_telemetria(dado):
    """
    Função que transforma o payload bruto num dataset enriquecido.
    """
    # 2. Conversão para DataFrame (Organização Tabular)
    df = pd.DataFrame([dado])
    
    # 3. Transformação: Adição de Timestamp de Ingestão
    df['timestamp_ingestao'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 4. Transformação: Criação de Métrica Derivada (Regra de Negócio)
    # Cálculo simplificado de estresse hídrico (quanto mais quente e seco, maior o estresse)
    df['indice_estresse'] = round(
        ((df['temperatura_c'] * 1.5) - df['umidade_solo_pct'] + 50), 2
    )
    
    # 5. Classificação baseada no índice para facilitar o motor de regras futuro
    df['status_solo'] = df['indice_estresse'].apply(
        lambda x: 'CRÍTICO' if x > 60 else ('ALERTA' if x > 40 else 'IDEAL')
    )
    
    # Ordenação das colunas para exportação
    colunas_finais = [
        'timestamp_ingestao', 'device_id', 'temperatura_c', 
        'umidade_solo_pct', 'luminosidade_pct', 'indice_estresse', 'status_solo'
    ]
    
    return df[colunas_finais]

# Execução do pipeline
dataset_processado = processar_telemetria(payload_bruto)

# Exportação simulada para a Camada Silver (Parquet ou CSV)
dataset_processado.to_csv("telemetria_silver.csv", index=False)
print("✅ Dados processados e estruturados com sucesso!")
print(dataset_processado.head())