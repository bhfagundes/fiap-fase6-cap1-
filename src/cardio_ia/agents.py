from __future__ import annotations

import os

from agents import Agent
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX

from cardio_ia.schemas import CardiacDecision
from cardio_ia.tools import consultar_protocolos_medicos, prever_pico_risco_cardiaco


def default_model_name() -> str:
    return os.environ.get("CARDIO_AGENT_MODEL", "gpt-4o-mini")


def build_entry_agent() -> Agent:
    """Cadeia: Orquestrador → Analista de Risco → Especialista em Protocolos (saída estruturada)."""
    model = default_model_name()

    protocol_specialist = Agent(
        name="Especialista em Protocolos",
        model=model,
        handoff_description=(
            "Especialista que cruza a classificação de risco com a base de protocolos simulada."
        ),
        instructions=f"""{RECOMMENDED_PROMPT_PREFIX}
Você é o Especialista em Protocolos (CardioIA).

Passos obrigatórios:
1) Localize no histórico o resultado JSON da ferramenta `prever_pico_risco_cardiaco` (probabilidade e classe_por_threshold).
2) Chame a ferramenta `consultar_protocolos_medicos` com um JSON contendo:
   - "classificacao_risco": o valor de classe_por_threshold retornado pelo analista
   - "spo2": valor SpO2 do paciente (extraia do JSON do usuário ou do contexto)
3) Monte a resposta final no schema estruturado CardiacDecision:
   - probabilidade_pico_risco: copie exatamente a probabilidade retornada pelo modelo
   - classificacao_risco: use classe_por_threshold
   - protocolos_sugeridos: use o campo "todos_protocolos" retornado pela consulta, sem duplicar
   - notas: uma frase objetiva sobre coerência risco × protocolos (simulado)

Não invente probabilidades; use apenas os números das ferramentas.
""",
        tools=[consultar_protocolos_medicos],
        output_type=CardiacDecision,
    )

    risk_analyst = Agent(
        name="Analista de Risco",
        model=model,
        handoff_description=(
            "Calcula score de risco com o modelo ML treinado (pico_risco) via ferramenta dedicada."
        ),
        instructions=f"""{RECOMMENDED_PROMPT_PREFIX}
Você é o Analista de Risco Cardíaco.

1) Extraia o JSON do paciente da mensagem do usuário (campos: idade, freq_cardiaca, spo2, carga_sistema, disponibilidade_recursos).
2) Chame EXATAMENTE uma vez a ferramenta `prever_pico_risco_cardiaco` passando esse JSON como string.
3) Em seguida, faça handoff para o Especialista em Protocolos usando a ferramenta de transferência,
   resumindo em uma linha o resultado (probabilidade e classe) para facilitar a próxima etapa.

Não finalize o atendimento você mesmo: o especialista em protocolos emitirá a decisão estruturada final.
""",
        tools=[prever_pico_risco_cardiaco],
        handoffs=[protocol_specialist],
    )

    orchestrator = Agent(
        name="Orquestrador CardioIA",
        model=model,
        handoff_description=(
            "Coordena o fluxo entre analista de risco e especialista em protocolos via handoffs."
        ),
        instructions=f"""{RECOMMENDED_PROMPT_PREFIX}
Você é o Orquestrador do sistema CardioIA.

O usuário enviará um JSON com dados do paciente.
Sua única ação inicial é delegar ao Analista de Risco usando o handoff apropriado,
garantindo que o JSON completo do paciente permaneça visível no histórico.

Não tente prever risco você mesmo: use o especialista e as ferramentas dele.
Após o especialista em protocolos concluir, a execução termina com a saída estruturada dele.
""",
        handoffs=[risk_analyst],
    )

    return orchestrator
