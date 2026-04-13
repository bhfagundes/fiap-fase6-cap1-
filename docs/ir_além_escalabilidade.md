# Ir Além 2 — Otimização e escalabilidade (≤2 páginas · fonte para PDF)

## 1. Estrutura modular implementada

| Módulo | Responsabilidade |
|--------|------------------|
| `cardio_ia.model_service` | Carregamento do artefato `joblib` e inferência tabular. |
| `cardio_ia.protocol_service` | Leitura da base JSON e enriquecimento por gatilhos (ex.: SpO2). |
| `cardio_ia.tools` | *Tools* expostas ao LLM (`function_tool`). |
| `cardio_ia.agents` | Definição dos três agentes e cadeia de handoffs. |
| `cardio_ia.run` | Orquestração assíncrona via `Runner.run`. |
| `cardio_ia.governance` | Registro e validação (Ir Além 1). |

Separação clara entre **modelo**, **política de protocolos** e **raciocínio linguístico** facilita substituição de componentes e testes isolados.

## 2. Simulação de múltiplas requisições

O script `scripts/batch_demo.py` lê um **array JSON** de pacientes e processa uma **fila em memória** de forma **sequencial** (`asyncio`), registrando cada decisão. Isso simula filas de triagem sem acoplar infraestrutura externa; o padrão é facilmente trocado por workers consumindo uma fila real.

## 3. Evolução para arquitetura distribuída

Caminhos plausíveis: (1) API gateway stateless + fila (SQS/Rabbit) com workers Python executando o mesmo pipeline; (2) separação do modelo em serviço de inferência (container) com contrato REST/gRPC; (3) *streaming* de eventos para monitoramento (Kafka) a partir dos registros JSONL; (4) idempotência por `run_id` e limites de taxa por unidade de saúde. A modularização atual reduz o custo de migração quando a carga ultrapassar o processamento local.
