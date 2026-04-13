from __future__ import annotations

import json
import os
from functools import lru_cache
from pathlib import Path
from typing import Any

from cardio_ia.paths import project_root


def default_protocol_path() -> Path:
    root = project_root()
    env = os.environ.get("CARDIO_PROTOCOLS_PATH")
    if env:
        return Path(env)
    return root / "data" / "protocolos_medicos.json"


@lru_cache(maxsize=1)
def load_protocols(path: str | None = None) -> dict[str, Any]:
    p = Path(path) if path else default_protocol_path()
    if not p.exists():
        raise FileNotFoundError(f"Base de protocolos não encontrada: {p}")
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def lookup_protocols(
    classificacao_risco: str,
    spo2: float | None = None,
    path: str | None = None,
) -> dict[str, Any]:
    data = load_protocols(path)
    por = data["por_classificacao"]
    base = list(por.get(classificacao_risco, []))
    extras: list[str] = []
    g = data.get("gatilhos_spo2", {})
    if spo2 is not None:
        if spo2 <= g.get("critico", 88):
            extras.append("Reforço de oxigenoterapia / reavaliação respiratória urgente (gatilho SpO2)")
        elif spo2 < g.get("alerta", 92):
            extras.append("Monitorar SpO2 de perto e considerar oxigenoterapia conforme evolução")
    return {
        "classificacao_risco": classificacao_risco,
        "protocolos_base": base,
        "protocolos_extras_spo2": extras,
        "todos_protocolos": base + extras,
    }


def lookup_protocols_json(payload: str) -> str:
    obj = json.loads(payload)
    out = lookup_protocols(
        classificacao_risco=obj["classificacao_risco"],
        spo2=obj.get("spo2"),
    )
    return json.dumps(out, ensure_ascii=False)
