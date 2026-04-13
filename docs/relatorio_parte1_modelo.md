# Relatório técnico — Parte 1 (modelo preditivo `pico_risco`)

**Projeto:** CardioIA — Fase 6 · **Grupo 34** · **Autor:** Brenner Henrique Fagundes Araujo

## 1. Objetivo e dados

Treinar um classificador supervisionado para prever a variável binária `pico_risco` a partir de variáveis clínicas simuladas: `idade`, `freq_cardiaca`, `spo2`, `carga_sistema`, `disponibilidade_recursos`. A base sintética foi gerada por processo estocástico (logística em score latente) para preservar relações plausíveis entre sinais vitais, carga assistencial e o desfecho, sem uso de dados reais identificáveis.

## 2. Algoritmo e justificativa

Foi adotada **Random Forest** (`RandomForestClassifier`), algoritmo ensemble baseado em árvores, robusto a não linearidades e interações entre atributos, com bom desempenho preditivo em dados tabulares sem necessidade de engenharia extensiva de features. Hiperparâmetros moderados (`max_depth`, `min_samples_leaf`) e `class_weight="balanced"` mitigam sobreajuste parcial e viés de classe. Alternativas razoáveis seriam regressão logística com interpretação linear explícita ou gradient boosting; a floresta aleatória equilibra performance e estabilidade para prototipagem acadêmica.

## 3. Protocolo experimental

- **Separação:** `train_test_split` 75/25, `stratify=y`, `random_state` fixo para reprodutibilidade.  
- **Métricas:** acurácia no conjunto de teste; **matriz de confusão**; `classification_report` (precision/recall/F1 por classe).  
- **Persistência:** artefato `joblib` contendo modelo, lista ordenada de features e métricas básicas, para consumo pelo agente de risco.

Os valores numéricos exatos dependem da semente e do tamanho amostral; o notebook Colab registra as saídas da execução.

## 4. Interpretação (exemplo de leitura)

- **Acurácia:** mede acertos globais; em bases com desbalanceamento de classe, pode mascarar desempenho na classe minoritária.  
- **Matriz de confusão:** evidencia se o modelo confunde principalmente falsos positivos ou falsos negativos para `pico_risco=1`, guiando ajustes (limiar de decisão, custos, rebalanceamento).  
- **Limitações:** dados sintéticos não refletem epidemiologia real; drift temporal e viés de medição não são modelados. Melhorias: validação cruzada, calibração de probabilidades (Platt/Isotônica), explicabilidade (SHAP) e comparação sistemática com outros classificadores.

## 5. Caso novo (simulação)

O notebook inclui um paciente sintético com perfil de alto risco (ex.: idade elevada, FC alta, SpO2 reduzida, alta carga do sistema). A probabilidade estimada e a classe binária são exibidas de forma interpretável, conectando o modelo ao fluxo decisório do sistema multiagente.
