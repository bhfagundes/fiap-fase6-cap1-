# CardioIA

## FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="docs/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=60% height=40%></a>
</p>
<br>

# Sistema Preditivo Multiagente

Projeto académico focado no desenvolvimento de um modelo de Machine Learning para predição de **pico de risco**, integrado ao **OpenAI Agents SDK**. A solução utiliza uma arquitetura de múltiplos agentes com handoffs, ferramentas (tools), histórico de conversação e saída validada via **Pydantic**.

## 👨‍🎓 Integrantes:

- <a href="https://www.linkedin.com/in/bryanjfagundes/">Bryan Fagundes</a>
- <a href="https://br.linkedin.com/in/brenner-fagundes">Brenner Fagundes</a>
- <a href="https://www.linkedin.com/in/hyankacoelho/">Hyanka Coelho</a>
- <a href="https://www.linkedin.com/in/julianahungaro/">Juliana Hungaro Fidelis</a>

## 👩‍🏫 Professores:

### Tutor(a)

- <a href="https://www.linkedin.com/in/leonardoorabona?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app">Leonardo Ruiz Orabona</a>

### Coordenador(a)

- <a href="https://www.linkedin.com/in/andregodoichiovato/">André Godoi</a>

## 📜 Descrição

Este projeto apresenta a evolução do CardioIA para um **Sistema Multiagente**, onde diferentes especialistas virtuais colaboram para o atendimento e análise de risco cardíaco.
A solução utiliza o **OpenAI Agents SDK** para orquestrar a comunicação entre agentes, garantindo que cada etapa do processo (da triagem à análise clínica) seja tratada pelo agente mais qualificado.

O pipeline do projeto inclui:

- **Modelo de ML:** Predição de risco integrado ao fluxo de agentes.
- **Orquestração de Agentes:** Uso de handoffs para transferência de contexto entre especialistas.
- **Governança de IA:** Registo estruturado em JSONL e validação de coerência de dados.
- **Processamento em Lote:** Simulação de escalabilidade para múltiplos pacientes simultâneos.
- **Saída Estruturada:** Validação rigorosa das respostas utilizando Pydantic.

## 👀 Visão Geral

O CardioIA Fase 6 simula um ecossistema que:

1. Interage com o utilizador/paciente através de uma interface de agentes.
2. Analisa dados vitais (frequência cardíaca, SpO2, idade) utilizando um modelo de ML (.joblib).
3. Orquestra o fluxo de atendimento entre agentes de triagem, analistas e governança.
4. Garante a conformidade através de um log de decisões versionado para auditoria.

## 🏗️ Arquitetura do Sistema

O sistema foi desenhado para ser modular e resiliente:

- **Agente de Triagem:** Ponto de entrada, responsável por recolher e validar os dados iniciais.
- **Agente Analista (ML):** Especialista que executa o modelo preditivo de risco.
- **Agente de Governança:** Valida se a resposta final é coerente com os protocolos médicos.

## 📁 Estrutura de Pastas
```
cardio2/
├── src/cardio_ia/ # Pacote principal: agentes, tools, modelo e governança
├── notebooks/     # Treino do modelo e exportação do artefato (.joblib)
├── scripts/       # Scripts de execução: treino, demo em lote e logs
├── data/          # Base de protocolos médicos simulada (JSON)
├── docs/          # Relatórios detalhados e evidências de governança
├── examples/      # Casos JSON de exemplo para testes
├── tests/         # Testes automatizados (Pytest)
├── artifacts/     # Modelos de ML exportados
└── README.md      # Documentação principal
```

## 📂 Organização do Código

- **Agentes:** Implementados no `src/cardio_ia/`, cada agente possui ferramentas específicas e instruções de comportamento.
- **Modelo:** O artefato de ML é carregado dinamicamente para prever o `pico_risco`.
- **Logs:** O sistema gera logs estruturados em `logs/decisoes_cardio_ia.jsonl` para fins de auditoria e governança.

## 📝 Pré-requisitos

- Python 3.10+ (Testado com 3.11).
- Conta OpenAI e chave de API (Exportar `OPENAI_API_KEY`).
- Bibliotecas: Pydantic, OpenAI Agents SDK, Joblib, Scikit-learn.

## 🤖 Funcionamento da Aplicação

#### 1. Configuração do Ambiente

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

#### 2. Artefato do modelo

O repositório inclui `artifacts/cardio_pico_risco_artifact.joblib`. Para regenerar (mesma lógica do notebook Colab):

```bash
python scripts/train_export_model.py
```

Variáveis opcionais: `CARDIO_MODEL_PATH` (artefato ML), `CARDIO_PROTOCOLS_PATH` (JSON de protocolos), `CARDIO_PROJECT_ROOT` (se o comando for executado fora da pasta do repositório).

#### 3. Execução do Pipeline Multiagente

Entrada: JSON com `idade`, `freq_cardiaca`, `spo2`, `carga_sistema`, `disponibilidade_recursos`.

```bash
cardio-ia-run --patient-file examples/caso_simples.json
```

Com **governança (Ir Além 1 — registro JSONL + validação de coerência):**

```bash
cardio-ia-run --governance --patient-file examples/caso_simples.json
```

Log estruturado em `logs/decisoes_cardio_ia.jsonl` (gitignored). Evidência versionada: `docs/evidencia_governanca.jsonl`.

#### 4. Simulação em Lote (Ir Além 2)

```bash
python scripts/batch_demo.py --input examples/pacientes_lote.json
```

## Testes

```bash
pytest tests/ -q
```

## ✍️ Documentação

- Parte 1 — relatório do modelo: [`docs/relatorio_parte1_modelo.md`](docs/relatorio_parte1_modelo.md)  
- Parte 2 — arquitetura (fonte PDF de 3 páginas): [`docs/arquitetura_parte2_multiagente.md`](docs/arquitetura_parte2_multiagente.md)  
- Ir Além 1: [`docs/ir_além_governança.md`](docs/ir_além_governança.md)  
- Ir Além 2: [`docs/ir_além_escalabilidade.md`](docs/ir_além_escalabilidade.md)

## 📋 Critérios da Atividade

| Critério | Atendimento |
| :--- | :--- |
| **Arquitetura Multiagente** | Implementada com OpenAI Agents SDK e Handoffs. |
| **Modelo de ML** | Integrado como ferramenta (Tool) para os agentes. |
| **Validação de Saída** | Implementada rigorosamente com Pydantic. |
| **Governança** | Registo estruturado de decisões para auditoria. |

## 🎥 Vídeo da Solução
https://youtu.be/xlbx4qBPc0Y?si=hbKE2LO1v72v8Dkb 

## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/agodoi/template">MODELO GIT FIAP</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">Fiap</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>

