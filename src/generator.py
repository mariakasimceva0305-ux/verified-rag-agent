from __future__ import annotations

import re
from dataclasses import dataclass

from src.retriever import RetrievedChunk


@dataclass
class GeneratedAnswer:
    answer: str
    citations: list[str]


def _tokens(text: str) -> set[str]:
    return {t.lower() for t in re.findall(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)?", text) if len(t) > 2}


def _overlap_score(query: str, chunk_text: str) -> float:
    q = _tokens(query)
    d = _tokens(chunk_text)
    if not q:
        return 0.0
    return len(q & d) / len(q)


def _pick_evidence(query: str, contexts: list[RetrievedChunk], max_chunks: int = 3) -> list[RetrievedChunk]:
    scored = [( _overlap_score(query, c.text), i, c) for i, c in enumerate(contexts)]
    scored.sort(key=lambda x: (-x[0], x[1]))
    picked: list[RetrievedChunk] = []
    for ov, _i, ch in scored[:max_chunks]:
        if ov <= 0 and picked:
            break
        picked.append(ch)
    return picked


def _compress_sentence(text: str, limit: int = 220) -> str:
    t = re.sub(r"\s+", " ", text.strip())
    if len(t) <= limit:
        return t
    return t[: limit - 1].rsplit(" ", 1)[0] + "…"


class AnswerGenerator:
    """Краткий ответ по выбранным фрагментам с явными ссылками на источники."""

    def generate(self, query: str, contexts: list[RetrievedChunk]) -> GeneratedAnswer:
        if not contexts:
            return GeneratedAnswer(
                answer="No indexed evidence was available to answer the question.",
                citations=[],
            )

        evidence = _pick_evidence(query, contexts, max_chunks=3)
        best_ov = max((_overlap_score(query, c.text) for c in evidence), default=0.0)
        if best_ov < 0.06:
            return GeneratedAnswer(
                answer="Retrieved passages are too weakly related to the query; abstaining from a factual answer.",
                citations=[],
            )

        sentences: list[str] = []
        citations: list[str] = []
        for ch in evidence:
            cite = f"{ch.source_path}#{ch.chunk_id}"
            citations.append(cite)
            snippet = _compress_sentence(ch.text)
            sentences.append(f"- {snippet} [{cite}]")

        answer = "Evidence from policies:\n" + "\n".join(sentences)
        return GeneratedAnswer(answer=answer, citations=citations)
