from __future__ import annotations

from src.generator import AnswerGenerator
from src.retriever import RetrievedChunk


def test_generator_abstains_without_context():
    g = AnswerGenerator()
    r = g.generate("any question", [])
    assert "No indexed evidence" in r.answer
    assert r.citations == []


def test_generator_emits_citations():
    g = AnswerGenerator()
    ctx = [
        RetrievedChunk(
            "c1",
            "d1",
            "Security audit logs must be retained for 365 days per policy section A.",
            "demo_corpus/audit.md",
            0.9,
        )
    ]
    r = g.generate("audit log retention period", ctx)
    assert r.citations
    assert "365" in r.answer
    assert "demo_corpus/audit.md" in r.citations[0]
