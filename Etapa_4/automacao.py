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

# --- AQUI É ONDE CHAMAMOS A FUNÇÃO PARA ELA EXECUTAR ---
motor_de_decisao_autonoma('../Etapa_3/telemetria_silver.csv')