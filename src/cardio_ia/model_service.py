from __future__ import annotations

import json
import os
from functools import lru_cache
from pathlib import Path
from typing import Any

import joblib
import pandas as pd

from cardio_ia.paths import project_root
from cardio_ia.schemas import PatientFeatures, classificar_risco


def default_model_path() -> Path:
    root = project_root()
    env = os.environ.get("CARDIO_MODEL_PATH")
    if env:
        return Path(env)
    return root / "artifacts" / "cardio_pico_risco_artifact.joblib"


@lru_cache(maxsize=1)
def load_artifact(path: str | None = None) -> dict[str, Any]:
    p = Path(path) if path else default_model_path()
    if not p.exists():
        raise FileNotFoundError(
            f"Artefato do modelo não encontrado: {p}. "
            "Execute scripts/train_export_model.py ou exporte o .joblib do Colab."
        )
    return joblib.load(p)


def predict_pico_risk(patient: PatientFeatures, artifact_path: str | None = None) -> dict[str, Any]:
    art = load_artifact(artifact_path)
    model = art["model"]
    features: list[str] = art["features"]
    row = pd.DataFrame([[getattr(patient, f) for f in features]], columns=features)
    proba = float(model.predict_proba(row)[0][1])
    pred_class = int(model.predict(row)[0])
    classe = classificar_risco(proba)
    return {
        "probabilidade_pico_risco": proba,
        "classe_por_threshold": classe,
        "pred_class_binaria": pred_class,
        "features_ordem": features,
    }


def predict_from_json(patient_json: str) -> str:
    data = json.loads(patient_json)
    patient = PatientFeatures.model_validate(data)
    result = predict_pico_risk(patient)
    return json.dumps(result, ensure_ascii=False)
