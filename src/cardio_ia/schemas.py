from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, field_validator


class PatientFeatures(BaseModel):
    """Características clínicas simuladas de entrada (alinhadas ao notebook)."""

    idade: float = Field(ge=0, le=120)
    freq_cardiaca: float = Field(ge=30, le=220)
    spo2: float = Field(ge=70, le=100)
    carga_sistema: float = Field(ge=0, le=100)
    disponibilidade_recursos: float = Field(ge=0, le=100)


class CardiacDecision(BaseModel):
    """Saída final validada do pipeline multiagente."""

    probabilidade_pico_risco: float = Field(ge=0.0, le=1.0)
    classificacao_risco: Literal["baixo", "moderado", "alto", "critico"]
    protocolos_sugeridos: list[str] = Field(min_length=1)
    notas: str | None = None

    @field_validator("probabilidade_pico_risco")
    @classmethod
    def round_prob(cls, v: float) -> float:
        return float(round(v, 4))


def classificar_risco(prob: float) -> Literal["baixo", "moderado", "alto", "critico"]:
    if prob < 0.30:
        return "baixo"
    if prob < 0.55:
        return "moderado"
    if prob < 0.75:
        return "alto"
    return "critico"
