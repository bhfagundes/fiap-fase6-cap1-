from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from agents import Runner

from cardio_ia.agents import build_entry_agent
from cardio_ia.governance import record_decision
from cardio_ia.schemas import CardiacDecision, PatientFeatures


async def run_pipeline(patient: PatientFeatures, enable_governance: bool) -> CardiacDecision:
    agent = build_entry_agent()
    user_msg = (
        "Analise o seguinte paciente (JSON). Siga o fluxo de handoffs até a decisão final.\n"
        f"{patient.model_dump_json()}"
    )
    result = await Runner.run(agent, user_msg)
    final = result.final_output
    if not isinstance(final, CardiacDecision):
        raise TypeError(f"Saída final inesperada: {type(final)}")
    if enable_governance:
        record_decision(patient, final)
    return final


def main() -> None:
    parser = argparse.ArgumentParser(description="CardioIA — pipeline multiagente")
    parser.add_argument(
        "--patient-json",
        type=str,
        default="",
        help='JSON do paciente, ex.: \'{"idade":72,"freq_cardiaca":118,...}\'',
    )
    parser.add_argument(
        "--patient-file",
        type=str,
        default="",
        help="Arquivo JSON com um objeto PatientFeatures",
    )
    parser.add_argument(
        "--governance",
        action="store_true",
        help="Persistir decisão em logs/decisoes_cardio_ia.jsonl e validar coerência",
    )
    args = parser.parse_args()

    if not os.environ.get("OPENAI_API_KEY"):
        print("Defina OPENAI_API_KEY no ambiente.", file=sys.stderr)
        sys.exit(1)

    if args.patient_file:
        raw = Path(args.patient_file).read_text(encoding="utf-8")
        data = json.loads(raw)
    elif args.patient_json:
        data = json.loads(args.patient_json)
    else:
        data = {
            "idade": 72,
            "freq_cardiaca": 118,
            "spo2": 88,
            "carga_sistema": 82,
            "disponibilidade_recursos": 35,
        }

    patient = PatientFeatures.model_validate(data)
    decision = asyncio.run(run_pipeline(patient, enable_governance=args.governance))
    print(decision.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
