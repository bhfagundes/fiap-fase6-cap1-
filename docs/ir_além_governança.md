# Ir Além 1 — Governança e monitoramento de decisões (≤2 páginas · fonte para PDF)

## 1. Como as decisões são registradas

Após cada execução com a flag `--governance`, o módulo `cardio_ia.governance` persiste um registro **JSON Lines** em `logs/decisoes_cardio_ia.jsonl`. Cada linha contém: `run_id` (UUID), `timestamp` (UTC ISO), cópia do paciente (`PatientFeatures`), decisão estruturada (`CardiacDecision`) e resultado da verificação de coerência (`ok`, lista de mensagens). O formato facilita ingestão em ferramentas de observabilidade (ELK, BigQuery) ou auditoria clínica futura.

## 2. Como a validação é realizada

A função `validate_coherence` aplica regras declarativas e explicáveis:

- **SpO2 crítico (≤88):** exige que os textos dos protocolos mencionem oxigenoterapia ou monitorização de SpO2, alinhando recomendação a variável vital crítica.  
- **Consistência probabilidade × classe:** probabilidade muito alta com classe “baixa/moderada”, ou probabilidade muito baixa com classe “crítica”, gera inconsistência explícita.

As regras são testáveis unitariamente (`tests/test_model_and_governance.py`) e podem ser estendidas com matrizes institucionais.

## 3. Importância da governança em IA na saúde

Sistemas de apoio à decisão em contexto clínico exigem **rastreabilidade** (quem/quando/o quê), **explicabilidade operacional** (inputs e outputs armazenados) e **detecção de deriva** entre recomendações e evidências. O registro estruturado e a validação simples reduzem risco de “caixa-preta” e sustentam responsabilização organizacional, sem substituir julgamento profissional nem consentimento informado.

## 4. Evidência de execução

Trecho versionado em [`docs/evidencia_governanca.jsonl`](evidencia_governanca.jsonl) (mesma estrutura que `logs/decisoes_cardio_ia.jsonl` em runtime). Para reproduzir com API: `cardio-ia-run --governance --patient-json '{...}'` após configurar `OPENAI_API_KEY`, ou offline: `python scripts/gen_governance_sample.py`.
