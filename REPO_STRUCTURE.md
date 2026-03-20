# Структура репозитория

```text
verified-rag-agent/
  README.md
  .gitignore
  requirements.txt
  .env.example
  configs/
    app.yaml
  data/
    raw/
    processed/
  docs/
    project-notes.md
  eval/
    questions.jsonl
    results/
  examples/
    sample_queries.md
  scripts/
    ingest.py
    build_index.py
    run_eval.py
  src/
    __init__.py
    config.py
    chunking.py
    ingest.py
    retriever.py
    reranker.py
    rewriter.py
    generator.py
    verifier.py
    pipeline.py
    api.py
    utils.py
  tests/
    test_chunking.py
    test_retrieval.py
```

## Какой уровень сложности нужен
Нужен **умеренный** уровень:
- чистая структура,
- понятные модули,
- без overengineering.

## Что должно быть точно
- `src/pipeline.py` — orchestration
- `src/retriever.py` — embedding retrieval
- `src/reranker.py` — reranking
- `src/rewriter.py` — query rewriting
- `src/verifier.py` — lightweight verification
- `scripts/run_eval.py` — evaluation entrypoint
- `README.md` — очень понятный

## Что можно упростить
Если что-то усложняет v1, можно:
- verification сделать rule-based / LLM-based, но простым
- API сделать минимальным FastAPI
- тестов сделать 2–3 базовых, не больше
