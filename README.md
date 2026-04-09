# Verified RAG Agent

[Русская версия](#ru) | [English version](#en)

## RU

### TL;DR
Локальный RAG-пайплайн с фокусом на проверяемость: retrieval, ответы с цитированием, baseline/improved режимы.

### Гипотезы
1. Query rewrite + rerank улучшают релевантность top-k.
2. Явное цитирование повышает проверяемость ответа.
3. Verification-step помогает отсекать слабозаземлённые ответы.

### Метрики
`HitRate@k`, `MRR`, latency p50/p95, groundedness checks.

## EN

### Overview
A verification-oriented local RAG pipeline with citation-aware answering, baseline/improved profiles, and reproducible offline evaluation.
