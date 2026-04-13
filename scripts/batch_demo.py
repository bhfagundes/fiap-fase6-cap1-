"""Simulação de múltiplos pacientes em fila (Ir Além 2 — escalabilidade modular)."""
from __future__ import annotations

import argparse
import asyncio
import json
import sys
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from cardio_ia.run import run_pipeline  # noqa: E402
from cardio_ia.schemas import PatientFeatures  # noqa: E402


async def process_queue(patients: list[PatientFeatures], governance: bool) -> list[dict]:
    """Processamento sequencial (fila em memória); fila real poderia ser SQS/Kafka."""
    results: list[dict] = []
    q: deque[PatientFeatures] = deque(patients)
    idx = 0
    while q:
        p = q.popleft()
        idx += 1
        decision = await run_pipeline(p, enable_governance=governance)
        results.append(
            {
                "index": idx,
                "paciente": p.model_dump(),
                "decisao": decision.model_dump(),
            }
        )
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="Batch de pacientes — CardioIA")
    parser.add_argument(
        "--input",
        type=str,
        required=True,
        help="JSON array de objetos paciente",
    )
    parser.add_argument("--governance", action="store_true")
    args = parser.parse_args()

    data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    patients = [PatientFeatures.model_validate(x) for x in data]
    out = asyncio.run(process_queue(patients, governance=args.governance))
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
