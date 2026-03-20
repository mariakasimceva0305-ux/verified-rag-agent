# Checklist

## Шаг 1. Зафиксировать тему и корпус
- [ ] выбрать corpus type
- [ ] определить 50–100 документов
- [ ] решить, как их хранить

## Шаг 2. Поднять каркас проекта
- [ ] создать базовую структуру
- [ ] создать requirements.txt
- [ ] создать .env.example
- [ ] создать FastAPI skeleton (минимальный)

## Шаг 3. Собрать baseline
- [ ] ingestion
- [ ] chunking
- [ ] embeddings retrieval
- [ ] answer generation
- [ ] citations

## Шаг 4. Собрать eval set
- [ ] 30–50 вопросов
- [ ] gold relevant docs
- [ ] simple evaluation script

## Шаг 5. Добавить improvement
- [ ] query rewriting
- [ ] reranking
- [ ] simple verification

## Шаг 6. Посчитать метрики
- [ ] Recall@5
- [ ] Recall@10
- [ ] MRR
- [ ] groundedness
- [ ] citation coverage
- [ ] p50 / p95 latency

## Шаг 7. Дожать README
- [ ] pipeline diagram / description
- [ ] baseline vs improved
- [ ] setup
- [ ] examples
- [ ] limitations

## Когда идти в Cursor
Иди в Cursor **сразу после чтения этого пакета**, но проси его сначала:
1. создать каркас проекта,
2. предложить минимальную реализацию baseline,
3. не переусложнять,
4. не выдумывать метрики.

## Когда возвращаться ко мне
Возвращайся ко мне после:
- первого каркаса,
- baseline,
- первых результатов eval.
