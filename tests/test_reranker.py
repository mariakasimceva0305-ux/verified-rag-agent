from __future__ import annotations

from src.reranker import Reranker
from src.retriever import RetrievedChunk


def test_rerank_prefers_lexical_match():
    rr = Reranker()
    q = "password reset workflow"
    cands = [
        RetrievedChunk("c1", "d1", "unrelated marketing text", "x.md", 0.99),
        RetrievedChunk("c2", "d2", "Password reset workflow requires MFA verification step", "y.md", 0.5),
    ]
    out = rr.rerank(q, cands)
    assert out[0].doc_id == "d2"
    assert out[0].score >= out[1].score
