from __future__ import annotations

import json
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from cardio_ia.paths import project_root
from cardio_ia.schemas import CardiacDecision, PatientFeatures


@dataclass
class GovernanceRecord:
    run_id: str
    timestamp_iso: str
    entrada_paciente: dict[str, Any]
    decisao: dict[str, Any]
    coerencia_ok: bool
    coerencia_detalhes: list[str]
    log_path: str | None = None


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def validate_coherence(patient: PatientFeatures, decision: CardiacDecision) -> tuple[bool, list[str]]:
    """Verificação simples de alinhamento entre variáveis críticas e protocolos sugeridos."""
    detalhes: list[str] = []
    ok = True
    texto = " ".join(decision.protocolos_sugeridos).lower()

    if patient.spo2 <= 88:
        if "oxigen" not in texto and "spo2" not in texto:
            ok = False
            detalhes.append(
                "SpO2 crítico (<=88): esperava menção a oxigenoterapia/monitorização de SpO2 nos protocolos."
            )

    if decision.probabilidade_pico_risco >= 0.75 and decision.classificacao_risco in ("baixo", "moderado"):
        ok = False
        detalhes.append("Alta probabilidade (>=0.75) incompatível com classificação baixa/moderada.")

    if decision.probabilidade_pico_risco < 0.35 and decision.classificacao_risco == "critico":
        ok = False
        detalhes.append("Probabilidade baixa (<0.35) incompatível com classificação crítica.")

    if not detalhes:
        detalhes.append("Nenhuma inconsistência simples detectada pelas regras configuradas.")

    return ok, detalhes


def append_jsonl(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False) + "\n")


def record_decision(
    patient: PatientFeatures,
    decision: CardiacDecision,
    log_dir: Path | None = None,
    run_id: str | None = None,
) -> GovernanceRecord:
    rid = run_id or str(uuid.uuid4())
    coerencia_ok, coerencia_detalhes = validate_coherence(patient, decision)
    base = log_dir or project_root() / "logs"
    log_file = base / "decisoes_cardio_ia.jsonl"

    payload = {
        "run_id": rid,
        "timestamp": _utc_now(),
        "paciente": patient.model_dump(),
        "decisao": decision.model_dump(),
        "coerencia": {"ok": coerencia_ok, "detalhes": coerencia_detalhes},
    }
    append_jsonl(log_file, payload)

    return GovernanceRecord(
        run_id=rid,
        timestamp_iso=payload["timestamp"],
        entrada_paciente=patient.model_dump(),
        decisao=decision.model_dump(),
        coerencia_ok=coerencia_ok,
        coerencia_detalhes=coerencia_detalhes,
        log_path=str(log_file),
    )
