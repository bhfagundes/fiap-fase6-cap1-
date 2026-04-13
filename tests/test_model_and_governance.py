from __future__ import annotations

import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture()
def artifact_path() -> Path:
    p = ROOT / "artifacts" / "cardio_pico_risco_artifact.joblib"
    if not p.exists():
        pytest.skip("Artefato ML ausente — execute scripts/train_export_model.py")
    return p


def test_predict_roundtrip(artifact_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CARDIO_MODEL_PATH", str(artifact_path))
    from cardio_ia.model_service import load_artifact, predict_pico_risk
    from cardio_ia.schemas import PatientFeatures

    load_artifact.cache_clear()
    p = PatientFeatures(
        idade=60,
        freq_cardiaca=85,
        spo2=96,
        carga_sistema=40,
        disponibilidade_recursos=70,
    )
    out = predict_pico_risk(p)
    assert 0 <= out["probabilidade_pico_risco"] <= 1
    assert out["classe_por_threshold"] in ("baixo", "moderado", "alto", "critico")


def test_governance_spo2_rule() -> None:
    from cardio_ia.governance import validate_coherence
    from cardio_ia.schemas import CardiacDecision, PatientFeatures

    p = PatientFeatures(
        idade=70,
        freq_cardiaca=120,
        spo2=85,
        carga_sistema=90,
        disponibilidade_recursos=20,
    )
    bad = CardiacDecision(
        probabilidade_pico_risco=0.9,
        classificacao_risco="critico",
        protocolos_sugeridos=["Apenas observação clínica"],
    )
    ok, det = validate_coherence(p, bad)
    assert ok is False
    assert any("SpO2" in d or "oxigen" in d.lower() for d in det)


def test_protocol_tool_json() -> None:
    from cardio_ia.protocol_service import lookup_protocols_json

    payload = json.dumps({"classificacao_risco": "alto", "spo2": 87})
    raw = lookup_protocols_json(payload)
    data = json.loads(raw)
    assert "todos_protocolos" in data
    assert len(data["todos_protocolos"]) >= 1
