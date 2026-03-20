from __future__ import annotations

import time

from src.config import load_config
from src.pipeline import RAGPipeline
from src.utils import read_jsonl, write_jsonl


def _mrr_from_rank(rank: int | None) -> float:
    if rank is None:
        return 0.0
    return 1.0 / rank


def main() -> None:
    cfg = load_config("configs/app.yaml")
    pipeline = RAGPipeline(cfg)
    questions = read_jsonl("eval/questions.jsonl")
    if not questions:
        print("No eval questions found in eval/questions.jsonl")
        return

    runs = []
    hit_count = 0
    mrr_sum = 0.0
    latencies_ms: list[float] = []

    for q in questions:
        query = q["question"]
        gold_doc_ids = set(q.get("gold_doc_ids", []))

        started = time.perf_counter()
        result = pipeline.answer(query)
        elapsed_ms = (time.perf_counter() - started) * 1000.0
        latencies_ms.append(elapsed_ms)

        ranked_doc_ids = [c.doc_id for c in result.retrieved_chunks]
        first_relevant_rank = None
        for i, doc_id in enumerate(ranked_doc_ids, start=1):
            if doc_id in gold_doc_ids:
                first_relevant_rank = i
                break

        is_hit = first_relevant_rank is not None
        hit_count += int(is_hit)
        mrr_sum += _mrr_from_rank(first_relevant_rank)

        runs.append(
            {
                "question": query,
                "answer": result.answer,
                "citations": result.citations,
                "latency_ms": round(elapsed_ms, 2),
                "is_hit_at_k": is_hit,
                "first_relevant_rank": first_relevant_rank,
            }
        )

    n = len(questions)
    hitrate = hit_count / n
    mrr = mrr_sum / n
    p50 = sorted(latencies_ms)[int(0.5 * (n - 1))]
    p95 = sorted(latencies_ms)[int(0.95 * (n - 1))]

    summary = [
        {
            "num_questions": n,
            "hit_rate_at_k": round(hitrate, 4),
            "mrr": round(mrr, 4),
            "latency_p50_ms": round(p50, 2),
            "latency_p95_ms": round(p95, 2),
        }
    ]

    write_jsonl("eval/results/latest_summary.jsonl", summary)
    write_jsonl("eval/results/latest_runs.jsonl", runs)

    print("Evaluation complete.")
    print(summary[0])


if __name__ == "__main__":
    main()

