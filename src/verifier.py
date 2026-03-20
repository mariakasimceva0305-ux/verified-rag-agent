from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class VerificationResult:
    is_grounded: bool
    score: float
    reason: str


class Verifier:
    """Lightweight lexical-overlap groundedness checker."""

    def verify(self, answer: str, evidence: list[Any]) -> VerificationResult:
        answer_tokens = {t.lower() for t in answer.split() if len(t) > 3}
        evidence_tokens = {
            t.lower()
            for c in evidence
            for t in c.text.split()
            if len(t) > 3
        }

        if not answer_tokens:
            return VerificationResult(False, 0.0, "empty answer")

        overlap = answer_tokens.intersection(evidence_tokens)
        score = len(overlap) / len(answer_tokens)
        grounded = score >= 0.3
        reason = "sufficient lexical overlap" if grounded else "low lexical overlap"
        return VerificationResult(grounded, score, reason)

