"""Treina e exporta o artefato do modelo (reproduz lógica do notebook Colab)."""
from __future__ import annotations

import sys
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / "artifacts"


def gerar_base_sintetica(n: int = 2500, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    idade = rng.integers(35, 90, size=n)
    freq_cardiaca = rng.normal(78, 18, size=n).clip(45, 180)
    spo2 = rng.normal(96, 3, size=n).clip(70, 100)
    carga_sistema = rng.uniform(0, 100, size=n)
    disponibilidade_recursos = rng.uniform(0, 100, size=n)

    score_latente = (
        0.02 * (idade - 40)
        + 0.015 * np.maximum(0, freq_cardiaca - 75)
        - 0.08 * (spo2 - 92)
        + 0.012 * carga_sistema
        - 0.01 * disponibilidade_recursos
        + rng.normal(0, 0.35, size=n)
    )
    prob = 1 / (1 + np.exp(-score_latente))
    pico_risco = (rng.random(n) < prob).astype(int)

    return pd.DataFrame(
        {
            "idade": idade.astype(float),
            "freq_cardiaca": freq_cardiaca,
            "spo2": spo2,
            "carga_sistema": carga_sistema,
            "disponibilidade_recursos": disponibilidade_recursos,
            "pico_risco": pico_risco,
        }
    )


def main() -> None:
    RANDOM_STATE = 42
    FEATURES = [
        "idade",
        "freq_cardiaca",
        "spo2",
        "carga_sistema",
        "disponibilidade_recursos",
    ]
    TARGET = "pico_risco"

    df = gerar_base_sintetica(2500, RANDOM_STATE)
    X = df[FEATURES]
    y = df[TARGET]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=RANDOM_STATE, stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=120,
        max_depth=12,
        min_samples_leaf=4,
        random_state=RANDOM_STATE,
        class_weight="balanced",
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)

    artifact = {
        "model": model,
        "features": FEATURES,
        "target": TARGET,
        "metrics": {"accuracy_test": float(acc), "confusion_matrix": cm.tolist()},
    }

    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    out_path = ARTIFACTS / "cardio_pico_risco_artifact.joblib"
    joblib.dump(artifact, out_path)
    print(f"Artefato salvo em {out_path} (acurácia teste: {acc:.4f})")


if __name__ == "__main__":
    main()
    sys.exit(0)
