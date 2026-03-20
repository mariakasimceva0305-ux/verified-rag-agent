# Evaluation plan

## 1. Retrieval evaluation
Нужны вопросы и gold evidence / relevant documents.

### Минимум
- 30–50 вопросов
- для каждого вопроса:
  - expected relevant doc ids
  - optionally expected chunks

### Метрики
- Recall@5
- Recall@10
- HitRate@5
- MRR

## 2. Answer quality evaluation
Сделать простую ручную разметку на 20–30 вопросах.

Поля:
- `is_correct`
- `is_grounded`
- `has_useful_citations`
- `notes`

## 3. Latency
Замерить хотя бы:
- p50
- p95

## 4. С чем сравнивать
Сравнить 3–4 режима:
1. baseline
2. baseline + query rewrite
3. baseline + reranker
4. baseline + rewrite + reranker + verification

## 5. Что не делать
- не придумывать gold labels задним числом под желаемый результат
- не писать фейковые числа
- не делать overly large benchmarks в v1
