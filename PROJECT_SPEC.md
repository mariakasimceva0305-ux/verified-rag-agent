# PROJECT SPEC

## Project title
**Verified RAG Agent for Document QA**

Возможные короткие repo names:
- `verified-rag-agent`
- `docu-agent-rag`
- `citation-aware-rag-agent`

## Цель
Сделать систему, которая отвечает на вопросы по корпусу документов, показывает **цитаты** и сравнивает:

1. **Baseline RAG**
2. **Improved RAG** = query rewriting + reranking + lightweight verification

## Почему этот проект хороший
- понятный сценарий,
- не слишком сложный,
- выглядит современно,
- легко объяснить на собесе,
- хорошо ложится в резюме под NLP / LLM / retrieval / agents.

## Пользовательский сценарий
Пользователь задаёт вопрос по набору документов.  
Система:
1. при необходимости переписывает запрос,
2. ищет релевантные фрагменты,
3. при необходимости переранжирует их,
4. строит ответ,
5. показывает источники,
6. делает простую проверку: ответ действительно опирается на retrieved chunks или нет.

## Scope первой версии
### Обязательно
- document ingestion
- chunking
- embeddings retrieval
- top-k retrieval
- answer generation
- citations
- evaluation pipeline
- baseline vs improved comparison

### Желательно
- query rewriting
- reranker
- verification flag / groundedness check

### Не включать в v1
- complex multi-agent systems
- memory
- web search
- frontend
- cloud infra
- advanced observability

## Корпус документов
Лучший вариант для v1:
**knowledge base / help center / documentation corpus**

Пример:
- 50–100 документов
- docs / help articles / FAQ / policy pages
- корпус должен быть однородным и понятным

## Eval set
Собрать вручную:
- 30–50 вопросов
- разной сложности
- часть вопросов должна требовать нескольких документов / фрагментов
- часть вопросов должна быть "hard negatives"

## Baseline
- chunking
- embedding retrieval
- answer generation from top-k chunks
- citations

## Improvement
- query rewriting
- reranking
- simple verification / groundedness check

## Минимальные метрики
### Retrieval
- Recall@k
- HitRate@k
- MRR

### Answer quality
- grounded / not grounded
- citation coverage
- manual correctness on small eval set

### System
- latency p50 / p95

## Что писать в README
README должен отвечать на 4 вопроса:
1. Что это?
2. Как работает?
3. Что ты улучшила по сравнению с baseline?
4. Как это запустить и проверить?
