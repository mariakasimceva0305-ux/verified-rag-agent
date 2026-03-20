from __future__ import annotations

from src.retriever import RetrievedChunk


class Reranker:
    """Simple placeholder reranker.

    Current behavior sorts by retriever score descending.
    """

    def rerank(self, query: str, candidates: list[RetrievedChunk]) -> list[RetrievedChunk]:
        _ = query
        return sorted(candidates, key=lambda x: x.score, reverse=True)

