## 3. Processamento e Preparação dos Dados

A arquitetura do AgroSmart pressupõe que os dados brutos recolhidos em campo (IoT) não podem ser consumidos diretamente para a tomada de decisão. Nesta etapa, simulamos o pipeline de processamento de dados (*Data Preparation*) utilizando Python, responsável por transformar o JSON bruto da camada Raw (Bronze) num formato tabular, limpo e enriquecido com novas métricas de negócio para a camada Trusted (Silver).

### 3.1 Script de Processamento (Python)

O script abaixo utiliza a biblioteca `pandas` para estruturar os dados. Ele aplica regras de transformação, como a inserção de um carimbo de data/hora (*timestamp*) de processamento, e calcula um novo indicador derivado: o **Índice de Estresse Hídrico**, cruzando a temperatura e a umidade do solo.

```python
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

```

### 3.2 Exemplo do Dataset Processado

Após a execução do script de engenharia de dados, o arquivo original JSON com 4 chaves brutas é transformado no seguinte conjunto de dados estruturado (formato CSV/Tabular):

| timestamp_ingestao | device_id | temperatura_c | umidade_solo_pct | luminosidade_pct | indice_estresse | status_solo |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 2026-10-10 15:30:45 | TINKER-TALHAO-01 | 24.78 | 47.0 | 56.0 | 40.17 | ALERTA |

### 3.3 Explicação do Fluxo de Dados

O fluxo de processamento funciona de forma linear e automatizada:

1. **Extração (Read):** O script consome o arquivo JSON gerado pelos sensores (neste cenário simulado pelo TinkerCad) que repousa no OCI Object Storage.
2. **Organização:** Os dados hierárquicos (JSON) são planificados utilizando *DataFrames* do Pandas, transformando chaves em colunas e organizando o *schema*.
3. **Enriquecimento e Transformação:** O dado é contextualizado através da adição do horário exato de processamento (*timestamp*). De seguida, aplicamos uma transformação matemática para gerar a coluna `indice_estresse`, que é uma métrica derivada de negócio (cruzamento de umidade e temperatura).
4. **Carga (Write):** O dado estruturado, agora classificado como "ALERTA" ou "CRÍTICO", é salvo num formato tabular otimizado (simulado como `.csv`) e disponibilizado para as próximas etapas de Automação Inteligente e visualização em Dashboard.