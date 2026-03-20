# Verified RAG Agent

Небольшой инженерный проект по RAG: система отвечает на вопросы по внутреннему набору документов, показывает цитаты и позволяет сравнить базовый и улучшенный режимы пайплайна.

## Краткий обзор

- Проект ориентирован на понятный `v1` без лишней сложности.
- Основной фокус: retrieval, цитирование источников, простая проверка groundedness.
- В репозитории есть встроенный demo-корпус и готовые профили `baseline` / `improved`.

## Что делает проект

Система:

- читает документы из локального корпуса,
- разбивает их на чанки,
- строит векторный индекс (FAISS + sentence-transformers),
- находит релевантные чанки по вопросу,
- формирует ответ с цитатами,
- опционально применяет rewrite, rerank и verification.

## Зачем проект сделан

Цель — показать практичную реализацию retrieval/RAG-задачи, которую легко объяснить на интервью:

- есть четкий pipeline,
- есть сравнение режимов,
- есть воспроизводимый запуск и локальная оценка.

Это не research-репликация и не production-платформа.

## Pipeline (шаг за шагом)

1. **Ingest**: загрузка `.md`/`.txt` документов из `data/raw/`.
2. **Chunking**: разбиение текста на перекрывающиеся чанки.
3. **Indexing**: эмбеддинги чанков + сохранение FAISS индекса.
4. **Retrieval**: поиск top-k релевантных чанков.
5. **Query rewrite (опционально)**: простая нормализация запроса.
6. **Rerank (опционально)**: легкая переупорядочивающая логика.
7. **Generation**: сбор ответа на основе найденных фрагментов.
8. **Verification (опционально)**: простая оценка groundedness по пересечению лексики.

## Baseline vs Improved

### Baseline (`configs/baseline.yaml`)

- `use_query_rewrite: false`
- `use_reranker: false`
- `use_verifier: false`

Назначение: минимальный рабочий RAG-режим с retrieval + answer + citations.

### Improved (`configs/improved.yaml`)

- `use_query_rewrite: true`
- `use_reranker: true`
- `use_verifier: true`

Назначение: сравнимый с baseline режим с дополнительными легкими шагами.

Важно: в `v1` rewriter/reranker/verifier остаются намеренно простыми.

## Demo-корпус

В репозитории уже включен набор документов:

- путь: `data/raw/demo_corpus/`
- тема: support / security / access policies
- объем: 10 кратких и согласованных документов

Примеры:

- `password-reset-policy.md`
- `escalation-policy.md`
- `audit-log-retention.md`
- `access-revocation.md`

## Структура репозитория

```text
configs/            # профили запуска и настройки
data/raw/           # исходные документы (включая demo_corpus)
data/processed/     # артефакты ingest/chunk/index
docs/               # рабочие заметки
eval/               # eval-набор и результаты
examples/           # примеры вопросов
scripts/            # CLI-скрипты
src/                # модули пайплайна
tests/              # минимальные тесты
```

## Как запустить

### 1) Установка

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### 2) Быстрый демо-прогон (рекомендуется)

```bash
python scripts/demo.py --config configs/improved.yaml
```

Скрипт сам проверит наличие индекса, при необходимости выполнит ingest/index и запустит несколько вопросов.

### 3) Пошаговый запуск

```bash
python scripts/ingest.py --config configs/baseline.yaml
python scripts/build_index.py --config configs/baseline.yaml
python scripts/run_eval.py --config configs/baseline.yaml
```

Для improved-режима просто замените конфиг на `configs/improved.yaml`.

### 4) API

```bash
uvicorn src.api:app --reload
```

- `GET /health`
- `POST /ask` с телом `{"query": "..."}`  
  (API по умолчанию использует `configs/app.yaml`).

## Примеры вопросов

- When must a support ticket be escalated?
- How long are security audit logs retained?
- Who handles SEV-1 incidents outside business hours?
- Under what conditions can an account be suspended?

Больше примеров: `examples/sample_queries.md` и `eval/questions.jsonl`.

## Evaluation

Скрипт: `scripts/run_eval.py`

Используется локальный eval-набор (`eval/questions.jsonl`) с вопросами и `gold_doc_ids`.

Текущие метрики:

- HitRate@k
- MRR
- latency p50/p95

Результаты сохраняются в:

- `eval/results/latest_summary.jsonl`
- `eval/results/latest_runs.jsonl`

В репозитории нет заранее «нарисованных» результатов: метрики считаются только после локального запуска.

## Ограничения v1

- Генерация ответа сделана в extractive-стиле, без полноценной LLM-генерации.
- Rewrite/rerank/verifier реализованы легковесно (placeholder-уровень).
- Корпус и eval-набор маленькие и предназначены для демонстрации.
- Проект не позиционируется как production-ready.

## Следующие шаги

- Усилить rewriter/reranker без усложнения архитектуры.
- Добавить более строгую проверку корректности цитат.
- Расширить eval-набор (больше сложных вопросов и multi-doc кейсов).
- Добавить несколько регрессионных тестов на retrieval-качество.

