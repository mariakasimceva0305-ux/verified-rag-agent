# Стартовый пакет: первый pet-проект

Название проекта: **Verified RAG Agent for Document QA**

Этот пакет нужен, чтобы быстро и качественно собрать **первый сильный project under NLP / RAG / agents** без лишней сложности.

## Что внутри
- `PROJECT_SPEC.md` — чёткое ТЗ
- `REPO_STRUCTURE.md` — структура репозитория
- `README_SKELETON.md` — шаблон README
- `EVAL_PLAN.md` — как оценивать качество
- `NEXT_STEPS_CHECKLIST.md` — пошаговый план
- `CURSOR_PROMPT.txt` — готовый промт для Cursor
- пустые папки под будущий код и данные

## Как работать
1. Открой **эту папку** в Cursor.
2. Прочитай `PROJECT_SPEC.md` и `NEXT_STEPS_CHECKLIST.md`.
3. Вставь `CURSOR_PROMPT.txt` целиком в Cursor.
4. Попроси Cursor сначала **создать каркас проекта**, а не писать всё подряд.
5. После первого прохода проверь:
   - не переусложнил ли он проект,
   - не придумал ли фейковые метрики,
   - не добавил ли лишние framework'и.
6. Когда каркас будет готов, возвращайся ко мне — добьём evaluation, README и формулировки для резюме.

## Главная идея
Это **не paper reproduction**, а **простой сильный рабочий проект по мотивам retrieval / RAG / lightweight verification**.

## Что не делать в первой версии
- multi-agent swarm
- planner / memory
- web browsing
- UI
- cloud deployment
- сложную оркестрацию
- фейковые эксперименты

## Что должно быть в первой версии
- ingestion документов
- chunking
- embedding retrieval
- optional query rewriting
- reranking
- answer generation
- citations
- simple verification
- offline evaluation
