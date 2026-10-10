image.png

### 1. Descrição dos Sensores Utilizados

Na simulação do nó IoT (Internet of Things) para monitoramento do campo, foram utilizados os seguintes componentes virtuais através da plataforma TinkerCad:

*   **Placa Controladora (Arduino Uno R3):** Atua como o microcontrolador central do módulo de telemetria. É responsável por receber os sinais elétricos brutos dos sensores, efetuar as conversões matemáticas necessárias e empacotar a informação no formato correto para envio à nuvem.
*   **Sensor de Temperatura (TMP36):** Componente analógico utilizado para monitorar a temperatura ambiente em graus Celsius. No contexto agronômico, este dado é crucial para o motor de inteligência artificial calcular a janela ideal para a aplicação de defensivos foliares, evitando perdas por evaporação.
*   **Fotorresistor (LDR - Light Dependent Resistor):** Sensor que capta a intensidade de incidência solar na lavoura. A leitura desta luminosidade ajuda o sistema a cruzar métricas sobre o estresse hídrico e fotossintético das plantas.
*   **Potenciômetro (Simulador de Umidade do Solo):** Uma vez que a plataforma não dispõe de um sensor de umidade de solo nativo (como um higrômetro de haste), utilizou-se este componente rotativo para simular as variações hídricas da terra. Ao ser ajustado, simula porcentagens de umidade que variam de 0% (solo seco) a 100% (solo encharcado).

---

### 2. Exemplo de Dados Gerados

O código em C++ embutido no Arduino coleta as medições analógicas, converte-as para valores reais e formata a saída em um formato JSON (JavaScript Object Notation). 

Com base na sua última simulação funcional, o circuito gerou o seguinte pacote de telemetria no Monitor Serial:

```json
{
  "device_id": "TINKER-TALHAO-01",
  "temperatura_c": 24.78,
  "luminosidade_pct": 56.00,
  "umidade_solo_pct": 47.00
}