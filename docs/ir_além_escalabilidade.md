# 🚀 Ir Além 2 — Otimização e Escalabilidade

## 🧱 1. Estrutura Modular Implementada

| Módulo | Responsabilidade |
|--------|------------------|
| `cardio_ia.model_service` | Carregamento do artefato `joblib` e inferência tabular. |
| `cardio_ia.protocol_service` | Leitura da base JSON e enriquecimento por gatilhos (ex.: SpO2). |
| `cardio_ia.tools` | *Tools* expostas ao LLM (`function_tool`). |
| `cardio_ia.agents` | Definição dos três agentes e cadeia de handoffs. |
| `cardio_ia.run` | Orquestração assíncrona via `Runner.run`. |
| `cardio_ia.governance` | Registro e validação (Ir Além 1). |

Separação clara entre **modelo**, **política de protocolos** e **raciocínio linguístico** facilita substituição de componentes e testes isolados.

## 📥 2. Simulação de Múltiplas Requisições

O script `scripts/batch_demo.py` lê um **array JSON** de pacientes e processa uma **fila em memória** de forma **sequencial** (`asyncio`), registrando cada decisão. Isso simula filas de triagem sem acoplar infraestrutura externa; o padrão é facilmente trocado por workers consumindo uma fila real.

## 🌐 3. Evolução para Arquitetura Distribuída

Caminhos plausíveis:

1. **API Gateway + Fila**  
   Gateway stateless com filas (SQS ou RabbitMQ) e workers Python executando o pipeline  

2. **Serviço de Inferência Isolado**  
   Modelo ML em container com comunicação via REST ou gRPC  

3. **Streaming de Eventos**  
   Uso de Kafka para monitoramento a partir dos registros JSONL  

4. **Controle e Governança**  
   Idempotência via `run_id` e limites de taxa por unidade de saúde  

## 📈 4. Considerações Finais

A modularização atual reduz acoplamento entre componentes, facilita a migração para ambientes distribuídos e suporta aumento de carga sem necessidade de reescrita do sistema.
