# 🌱 AgroSmart 

Este projeto simula um pipeline completo de dados e automação, demonstrando como as informações físicas se transformam em decisões estratégicas de negócio.

## 🚀 Fluxo de Dados e Arquitetura

O ecossistema foi construído sob uma perspetiva de microsserviços integrados, fluindo através de 4 etapas principais:

1. **O Sensor (IoT - TinkerCad):** O módulo de campo simula a captação de dados físicos (temperatura, luminosidade e humidade do solo) através de um Arduino, gerando os dados brutos num *payload* em formato JSON.
2. **A Engenharia de Dados (`script_processamento.py`):** Consome o JSON gerado pelos sensores, atua na limpeza das informações e enriquece o dado (calculando o Índice de Estresse Hídrico e adicionando carimbos de tempo). O resultado é exportado de forma estruturada (CSV) para a camada *Silver*.
3. **A Automação (`automacao.py`):** Funciona como um motor inferencial. Consome o dado limpo e toma uma decisão de negócio automática, classificando o cenário e disparando alertas preditivos ou urgentes para o gestor.
4. **O Dashboard (`dashboard.py`):** Interface de visualização que consome os dados limpos e exibe, de forma gráfica e visual, os indicadores de desempenho (KPIs), o histórico de leituras e os alertas operacionais.

💡 **Escalabilidade (Cloud-Ready):** 
Esta é uma plataforma integrada e altamente escalável. Se este ecossistema estivesse num ambiente de produção real na Oracle Cloud Infrastructure (OCI), estes scripts Python estariam a correr dentro de *Functions* ou *Containers* separados (Docker), conversando entre si via serviços de *Streaming*.

## 🛠️ Tecnologias Utilizadas

Todo o desenvolvimento lógico foi construído e isolado num ambiente virtual Python (`.venv`), garantindo a integridade das dependências do projeto.

* **Python 3:** Linguagem base de todo o motor de regras e *data prep*.
* **Pandas:** Biblioteca de engenharia de dados utilizada para a conversão de ficheiros JSON, manipulação de *DataFrames* e cálculos de negócio.
* **Streamlit:** Framework web empregue na construção rápida e responsiva do Dashboard Analítico.
* **TinkerCad (C++):** Utilizado para a montagem virtual e programação do circuito IoT embarcado.

---
