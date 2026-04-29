# 📊 Relatório Técnico — Parte 1 (Modelo Preditivo pico_risco)

**Projeto:** CardioIA — Fase 6  
**Autor:** Brenner Henrique Fagundes Araujo  

## 🎯 1. Objetivo e Dados

Treinar um classificador supervisionado para prever a variável binária `pico_risco` a partir das seguintes variáveis clínicas simuladas:

- `idade`  
- `freq_cardiaca`  
- `spo2`  
- `carga_sistema`  
- `disponibilidade_recursos`  

A base sintética foi gerada por processo estocástico (logística em score latente), preservando relações plausíveis entre sinais vitais, carga assistencial e o desfecho, sem uso de dados reais identificáveis.

## 🤖 2. Algoritmo e Justificativa

Foi adotado o algoritmo **Random Forest (`RandomForestClassifier`)**, um método ensemble baseado em árvores de decisão.

**Motivações:**
- Robustez a relações não lineares  
- Capacidade de capturar interações entre atributos  
- Bom desempenho em dados tabulares  
- Baixa necessidade de engenharia de features  

**Configurações utilizadas:**
- Hiperparâmetros moderados (`max_depth`, `min_samples_leaf`)  
- `class_weight="balanced"` para mitigar desbalanceamento  

**Alternativas consideradas:**
- Regressão logística (maior interpretabilidade linear)  
- Gradient Boosting (potencial ganho de performance)  

A Random Forest oferece um equilíbrio adequado entre desempenho, estabilidade e simplicidade para fins acadêmicos.

## 🧪 3. Protocolo Experimental

- **Divisão dos dados:**  
  `train_test_split` (75/25), com `stratify=y` e `random_state` fixo  

- **Métricas avaliadas:**
  - Acurácia no conjunto de teste  
  - Matriz de confusão  
  - `classification_report` (precision, recall, F1-score por classe)  

- **Persistência do modelo:**
  - Artefato `.joblib` contendo:
    - Modelo treinado  
    - Lista ordenada de features  
    - Métricas básicas  

Esse artefato é utilizado posteriormente pelo agente de risco no sistema multiagente.

> ℹ️ Os valores numéricos podem variar conforme a semente aleatória e o tamanho da amostra. O notebook Colab registra os resultados completos.


## 📈 4. Interpretação dos Resultados

- **Acurácia:**  
  Mede o desempenho global, mas pode mascarar erros em classes minoritárias  

- **Matriz de confusão:**  
  Permite identificar:
  - Falsos positivos  
  - Falsos negativos  
  - Tendências de erro do modelo  

- **Análise prática:**  
  - Erros em `pico_risco=1` são críticos  
  - Pode ser necessário ajustar limiar de decisão ou balanceamento  

**Limitações:**
- Dados sintéticos não refletem a realidade clínica  
- Não há modelagem de drift temporal  
- Possível ausência de vieses reais de medição  

**Melhorias futuras:**
- Validação cruzada  
- Calibração de probabilidades (Platt / Isotônica)  
- Explicabilidade (ex.: SHAP)  
- Comparação com outros algoritmos  


## 🧪 5. Caso Novo (Simulação)

O notebook inclui um paciente sintético com perfil de alto risco, por exemplo:

- Idade elevada  
- Frequência cardíaca alta  
- SpO2 reduzida  
- Alta carga do sistema  

O modelo retorna:
- Probabilidade estimada de `pico_risco`  
- Classificação binária  

Esses resultados são apresentados de forma interpretável e integrados ao fluxo de decisão do sistema multiagente.
