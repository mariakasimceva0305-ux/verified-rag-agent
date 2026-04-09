from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

from src.config import load_config
from src.pipeline import RAGPipeline
from src.utils import read_jsonl, stable_id, write_jsonl


def _mrr_from_rank(rank: int | None) -> float:
    if rank is None:
        return 0.0
    return 1.0 / rank


def _build_gold_alias_map(documents_path: str) -> dict[str, str]:
    """Сопоставляет gold doc_id из eval (часто POSIX-путь) с фактическим doc_id в текущем индексе."""
    rows = read_jsonl(documents_path)
    alias: dict[str, str] = {}
    for r in rows:
        actual = r["doc_id"]
        sp = r.get("source_path") or ""
        variants = {sp, sp.replace("\\", "/"), sp.replace("/", "\\")}
        from pathlib import PurePath

        variants.add(PurePath(sp).as_posix())
        for v in variants:
            if not v:
                continue
            gid = stable_id("doc", v)
            alias[gid] = actual
    return alias


def _resolve_gold_set(raw_ids: list[str], alias: dict[str, str]) -> set[str]:
    out: set[str] = set()
    for g in raw_ids:
        out.add(alias.get(g, g))
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="Run offline retrieval evaluation.")
    parser.add_argument(
        "--config",
        default="configs/app.yaml",
        help="Path to YAML config file.",
    )
    args = parser.parse_args()

    cfg = load_config(args.config)
    alias_map = _build_gold_alias_map(cfg.documents_path)

    pipeline = RAGPipeline(cfg)
    pipeline.load_index()
    questions = read_jsonl("eval/questions.jsonl")
    if not questions:
        print("No eval questions found in eval/questions.jsonl")
        return

    runs = []
    hit_count = 0
    mrr_sum = 0.0
    latencies_ms: list[float] = []
    grounded_hits = 0
    grounded_total = 0

    for q in questions:
        query = q["question"]
        gold_doc_ids = _resolve_gold_set(q.get("gold_doc_ids", []), alias_map)

        rw = query.strip()
        if cfg.use_query_rewrite:
            rw = pipeline.rewriter.rewrite(query)
        raw_chunks = pipeline.retriever.search(rw, top_k=cfg.top_k)
        pre_rerank_ids = [c.doc_id for c in raw_chunks]

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

        v = result.verification
        if v is not None:
            grounded_total += 1
            grounded_hits += int(v.is_grounded)

        runs.append(
            {
                "question": query,
                "rewritten_query": result.rewritten_query,
                "pre_rerank_top_doc_ids": pre_rerank_ids,
                "ranked_top_doc_ids": ranked_doc_ids,
                "answer": result.answer,
                "citations": result.citations,
                "latency_ms": round(elapsed_ms, 2),
                "is_hit_at_k": is_hit,
                "first_relevant_rank": first_relevant_rank,
                "verification": None
                if v is None
                else {
                    "is_grounded": v.is_grounded,
                    "score": v.score,
                    "reason": v.reason,
                },
            }
        )

    n = len(questions)
    hitrate = hit_count / n
    mrr = mrr_sum / n
    p50 = sorted(latencies_ms)[int(0.5 * (n - 1))]
    p95 = sorted(latencies_ms)[int(0.95 * (n - 1))]
    grounded_rate = (grounded_hits / grounded_total) if grounded_total else None

    summary = {
        "config_path": args.config,
        "num_questions": n,
        "hit_rate_at_k": round(hitrate, 4),
        "mrr": round(mrr, 4),
        "latency_p50_ms": round(p50, 2),
        "latency_p95_ms": round(p95, 2),
        "grounded_rate": None if grounded_rate is None else round(grounded_rate, 4),
        "documents_path": cfg.documents_path,
    }

    out_dir = Path("eval/results")
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = Path(args.config).stem
    summary_path = out_dir / f"summary_{stem}.json"
    runs_path = out_dir / f"runs_{stem}.jsonl"

    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    write_jsonl(str(runs_path), runs)
    write_jsonl(str(out_dir / "latest_summary.jsonl"), [summary])
    write_jsonl(str(out_dir / "latest_runs.jsonl"), runs)

    print("Evaluation complete.")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print(f"Wrote {summary_path} and {runs_path}")


if __name__ == "__main__":
    main()
