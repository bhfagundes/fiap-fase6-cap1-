# CardioIA — Fase 6 · Sistema preditivo multiagente

Projeto acadêmico (FIAP): modelo de ML para `pico_risco` integrado ao **OpenAI Agents SDK** com **handoffs**, **tools**, **histórico de conversa** e **saída validada** (Pydantic).

## Requisitos

- **Python 3.10+** (testado com 3.11; o pacote `openai-agents` não suporta 3.8).
- Conta OpenAI e chave de API para executar o pipeline completo.

## Configuração rápida

```bash
cd cardio2
python3.11 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -U pip
pip install -e ".[dev]"
cp env.example .env          # opcional; exporte OPENAI_API_KEY no shell
```

Defina a variável de ambiente:

```bash
export OPENAI_API_KEY="sk-..."
# opcional: export CARDIO_AGENT_MODEL="gpt-4o-mini"
```

### Artefato do modelo

O repositório inclui `artifacts/cardio_pico_risco_artifact.joblib`. Para regenerar (mesma lógica do notebook Colab):

```bash
python scripts/train_export_model.py
```

Variáveis opcionais: `CARDIO_MODEL_PATH` (artefato ML), `CARDIO_PROTOCOLS_PATH` (JSON de protocolos), `CARDIO_PROJECT_ROOT` (se o comando for executado fora da pasta do repositório).

## Execução — pipeline multiagente

Entrada: JSON com `idade`, `freq_cardiaca`, `spo2`, `carga_sistema`, `disponibilidade_recursos`.

```bash
cardio-ia-run --patient-file examples/caso_simples.json
```

Com **governança** (Ir Além 1 — registro JSONL + validação de coerência):

```bash
cardio-ia-run --governance --patient-file examples/caso_simples.json
```

Log estruturado em `logs/decisoes_cardio_ia.jsonl` (gitignored). Evidência versionada: `docs/evidencia_governanca.jsonl`.

### Ir Além 2 — lote simulado

```bash
python scripts/batch_demo.py --input examples/pacientes_lote.json
```

## Testes

```bash
pytest tests/ -q
```

## Estrutura do repositório

| Caminho | Descrição |
|---------|-----------|
| `notebooks/cardio_pico_risco_colab.ipynb` | Parte 1 — base sintética, treino, métricas, exportação |
| `scripts/train_export_model.py` | Treino local e geração do `.joblib` |
| `scripts/batch_demo.py` | Fila sequencial de pacientes (simulação de carga) |
| `scripts/gen_governance_sample.py` | Amostra de log de governança sem API |
| `src/cardio_ia/` | Pacote: agentes, tools, modelo, protocolos, governança |
| `data/protocolos_medicos.json` | Base simulada de protocolos |
| `docs/` | Relatórios em Markdown (exportar para PDF conforme entrega) |
| `examples/` | Casos JSON de exemplo |

## Vídeo de demonstração (≤ 3 min)

**Link YouTube (não listado):** _[inserir aqui após publicação — mostrar: entrada do paciente → handoffs/tools → resposta final estruturada]_

## Documentação de entrega

- Parte 1 — relatório do modelo: [`docs/relatorio_parte1_modelo.md`](docs/relatorio_parte1_modelo.md)  
- Parte 2 — arquitetura (fonte PDF de 3 páginas): [`docs/arquitetura_parte2_multiagente.md`](docs/arquitetura_parte2_multiagente.md)  
- Ir Além 1: [`docs/ir_além_governança.md`](docs/ir_além_governança.md)  
- Ir Além 2: [`docs/ir_além_escalabilidade.md`](docs/ir_além_escalabilidade.md)  

## Aviso

Este software é **educacional** e utiliza **dados simulados**. Não substitui avaliação clínica profissional nem constitui dispositivo médico.
