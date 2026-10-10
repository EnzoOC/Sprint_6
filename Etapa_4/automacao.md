## 4. Automação Inteligente Baseada em Dados

A solução AgroSmart implementa um **Motor Inferencial Baseado em Regras** para a sua automação. Em vez de depender que o agrônomo analise o painel, o sistema lê continuamente os dados processados da camada Silver e, com base nos limites agronômicos definidos, gera recomendações autônomas e aciona o sistema de alertas.

### 4.1 Lógica de Automação (Script Python)

O código abaixo simula o serviço de automação (*worker*) rodando na nuvem. Ele consome o dataset estruturado, interpreta a métrica de `indice_estresse` e classifica a situação, recomendando a ação adequada.

```python
import pandas as pd

def motor_de_decisao_autonoma(caminho_arquivo):
    """
    Motor de regras que avalia os dados e dispara ações automatizadas.
    """
    print("Iniciando Motor de Automação AgroSmart...\n")
    
    # 1. Consumo dos dados da camada Trusted (Silver)
    try:
        df = pd.read_csv(caminho_arquivo)
    except FileNotFoundError:
        print("Arquivo de dados não encontrado.")
        return

    # 2. Avaliação e Lógica de Decisão
    for index, linha in df.iterrows():
        talhao = linha['device_id']
        status = linha['status_solo']
        indice = linha['indice_estresse']
        data_hora = linha['timestamp_ingestao']
        
        print(f"[{data_hora}] Processando telemetria de: {talhao}")
        
        # Árvore de decisão baseada no status do campo
        if status == 'CRÍTICO':
            gerar_alerta_urgente(talhao, indice)
        elif status == 'ALERTA':
            gerar_recomendacao_preventiva(talhao, indice)
        else:
            print(f"✅ STATUS NORMAL (Índice: {indice}). Nenhuma intervenção necessária no momento.")
        
        print("-" * 60)

def gerar_alerta_urgente(talhao, indice):
    print(f"🚨 AÇÃO AUTOMATIZADA - ALERTA CRÍTICO!")
    print(f"   Motivo: Índice de estresse hídrico extremamente alto ({indice}).")
    print(f"   Ação Acionada: Disparo de SMS/WhatsApp para o Gerente Agrícola.")
    print(f"   Recomendação da IA: Iniciar irrigação imediatamente e suspender aplicação foliar devido à alta evaporação.")

def gerar_recomendacao_preventiva(talhao, indice):
    print(f"⚠️ AÇÃO AUTOMATIZADA - AVISO PREVENTIVO!")
    print(f"   Motivo: Índice de estresse em elevação ({indice}). Condição climática favorável à proliferação de fungos (ex: Ferrugem Asiática).")
    print(f"   Ação Acionada: Notificação enviada ao App Mobile do Agrônomo.")
    print(f"   Recomendação da IA: Priorizar inspeção visual neste talhão nas próximas 24 horas.")

```

# Simulação da execução do motor lendo o arquivo gerado na Etapa 3
### motor_de_decisao_autonoma('telemetria_silver.csv')

### 4.2 Descrição da Decisão Automatizada

A decisão foi modelada utilizando lógica determinística (Se/Então) cruzada com regras de negócio da agronomia:
*   **Condição Normal (Índice < 40):** O sistema apenas registra em log. Não há perturbação ao operador.
*   **Condição de Alerta (Índice entre 40 e 60):** O motor identifica um clima úmido e quente, propício para doenças foliares. A decisão automática é modificar a rota do agrônomo, enviando uma notificação preventiva para inspecionar aquele talhão específico, evitando que ele perca tempo vasculhando áreas saudáveis.
*   **Condição Crítica (Índice > 60):** O estresse hídrico está no limite, podendo causar murcha permanente. O sistema "pula" a necessidade de aprovação humana e emite ordens de serviço diretas de contingência (irrigação imediata) via WhatsApp/SMS, maximizando o tempo de resposta.

### 4.3 Exemplo de Saída Gerada pelo Sistema

Ao processar o dataset da Etapa 3 (onde o índice calculado foi de `40.17` e o status foi `ALERTA`), o terminal do servidor gera a seguinte saída automatizada:

```text
Iniciando Motor de Automação AgroSmart...

[2026-10-10 15:30:45] Processando telemetria de: TINKER-TALHAO-01
⚠️ AÇÃO AUTOMATIZADA - AVISO PREVENTIVO!
   Motivo: Índice de estresse em elevação (40.17). Condição climática favorável à proliferação de fungos (ex: Ferrugem Asiática).
   Ação Acionada: Notificação enviada ao App Mobile do Agrônomo.
   Recomendação da IA: Priorizar inspeção visual neste talhão nas próximas 24 horas.
------------------------------------------------------------
```