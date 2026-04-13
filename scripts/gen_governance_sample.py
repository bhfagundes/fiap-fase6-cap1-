"""Gera um trecho de log de governança sem chamar a API OpenAI (evidência offline)."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from cardio_ia.governance import record_decision  # noqa: E402
from cardio_ia.model_service import predict_pico_risk  # noqa: E402
from cardio_ia.protocol_service import lookup_protocols  # noqa: E402
from cardio_ia.schemas import CardiacDecision, PatientFeatures  # noqa: E402


def main() -> None:
    p = PatientFeatures(
        idade=72,
        freq_cardiaca=118,
        spo2=88,
        carga_sistema=82,
        disponibilidade_recursos=35,
    )
    pr = predict_pico_risk(p)
    proto = lookup_protocols(pr["classe_por_threshold"], spo2=p.spo2)
    decision = CardiacDecision(
        probabilidade_pico_risco=pr["probabilidade_pico_risco"],
        classificacao_risco=pr["classe_por_threshold"],
        protocolos_sugeridos=proto["todos_protocolos"],
        notas="Amostra offline: ML + protocolos + governança.",
    )
    rec = record_decision(p, decision, log_dir=ROOT / "logs")
    print("Registro gravado em:", rec.log_path)
    print("Coerência:", rec.coerencia_ok, rec.coerencia_detalhes)


if __name__ == "__main__":
    main()
