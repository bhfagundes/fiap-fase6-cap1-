from __future__ import annotations

from agents import function_tool

from cardio_ia.model_service import predict_from_json
from cardio_ia.protocol_service import lookup_protocols_json


@function_tool
def prever_pico_risco_cardiaco(paciente_json: str) -> str:
    """Calcula probabilidade de pico de risco cardíaco e classificação por limiares.

    paciente_json: objeto JSON com chaves idade, freq_cardiaca, spo2,
    carga_sistema, disponibilidade_recursos (números).
    Retorna JSON com probabilidade, classe por threshold e predição binária do modelo.
    """
    return predict_from_json(paciente_json)


@function_tool
def consultar_protocolos_medicos(parametros_json: str) -> str:
    """Consulta protocolos simulados conforme classificação de risco e opcionalmente SpO2.

    parametros_json: {"classificacao_risco": "baixo"|"moderado"|"alto"|"critico", "spo2": opcional float}
    """
    return lookup_protocols_json(parametros_json)
