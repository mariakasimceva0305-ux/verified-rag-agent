from __future__ import annotations

import math
import re
from typing import Iterable

from src.retriever import RetrievedChunk


def _tokens(text: str) -> set[str]:
    return {t.lower() for t in re.findall(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)?", text) if len(t) > 1}


def _jaccard(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    inter = len(a & b)
    union = len(a | b)
    return inter / union if union else 0.0


def _phrase_bonus(query: str, doc_text: str) -> float:
    """Бонус за совпадение устойчивых биграмм из запроса в тексте документа."""
    q = query.lower()
    dt = doc_text.lower()
    bigrams: list[str] = []
    words = re.findall(r"[a-z0-9]+", q)
    for i in range(len(words) - 1):
        bigrams.append(f"{words[i]} {words[i + 1]}")
    if not bigrams:
        return 0.0
    hits = sum(1 for bg in bigrams if bg in dt)
    return min(1.0, hits / max(1, len(bigrams)))


def _title_hint_bonus(query: str, source_path: str) -> float:
    stem = source_path.replace("\\", "/").split("/")[-1]
    stem = re.sub(r"\.[^.]+$", "", stem).replace("-", " ").lower()
    if not stem:
        return 0.0
    qtok = _tokens(query)
    ttok = _tokens(stem)
    return _jaccard(qtok, ttok)


class Reranker:
    """Второй этап: комбинированный lexical score с учётом запроса."""

    def rerank(self, query: str, candidates: list[RetrievedChunk]) -> list[RetrievedChunk]:
        if not candidates:
            return []

        q_tokens = _tokens(query)
        scored: list[tuple[float, int, RetrievedChunk]] = []

        for idx, ch in enumerate(candidates):
            # Нормируем score ретривера к [0,1] внутри кандидатов.
            retriever_scores = [c.score for c in candidates]
            r_min = min(retriever_scores)
            r_max = max(retriever_scores)
            if r_max - r_min < 1e-9:
                norm_r = 1.0
            else:
                norm_r = (ch.score - r_min) / (r_max - r_min)

            doc_tokens = _tokens(ch.text)
            jac = _jaccard(q_tokens, doc_tokens)
            phr = _phrase_bonus(query, ch.text)
            tit = _title_hint_bonus(query, ch.source_path)

            combined = 0.22 * norm_r + 0.42 * jac + 0.28 * phr + 0.08 * tit
            if not math.isfinite(combined):
                combined = 0.0
            scored.append((combined, idx, ch))

        scored.sort(key=lambda x: (-x[0], x[1]))
        out: list[RetrievedChunk] = []
        for comb, _idx, ch in scored:
            out.append(
                RetrievedChunk(
                    chunk_id=ch.chunk_id,
                    doc_id=ch.doc_id,
                    text=ch.text,
                    source_path=ch.source_path,
                    score=float(comb),
                )
            )
        return out
