from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any


@dataclass
class VerificationResult:
    is_grounded: bool
    score: float
    reason: str


def _split_claims(answer: str) -> list[str]:
    bullet = [ln.lstrip("- ").strip() for ln in answer.splitlines() if ln.strip().startswith("-")]
    if bullet:
        cleaned = []
        for b in bullet:
            b = re.sub(r"\s*\[[^\]]+\]\s*$", "", b).strip()
            if len(b) > 12:
                cleaned.append(b)
        if cleaned:
            return cleaned
    lines = [ln.strip() for ln in answer.splitlines() if ln.strip() and not ln.strip().startswith("-")]
    text = " ".join(lines)
    chunks = re.split(r"(?<=[.!?])\s+", text)
    return [c.strip() for c in chunks if len(c.strip()) > 10]


def _tokens(text: str) -> list[str]:
    return [t.lower() for t in re.findall(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)?", text) if len(t) > 2]


def _claim_supported(claim: str, evidence_texts: list[str]) -> bool:
    ct = _tokens(claim)
    if len(ct) < 2:
        return False
    key = set(ct[:8])
    best_ratio = 0.0
    for ev in evidence_texts:
        et = set(_tokens(ev))
        if not et:
            continue
        overlap = len(key & et) / max(1, len(key))
        if overlap > best_ratio:
            best_ratio = overlap
        # Доп. проверка: доля значимых токенов claim, встречающихся в evidence.
        hit = sum(1 for t in ct if t in et)
        ratio2 = hit / len(ct)
        best_ratio = max(best_ratio, ratio2)
    return best_ratio >= 0.35


class Verifier:
    """Проверка опоры ответа на claims по найденным фрагментам."""

    def verify(self, answer: str, evidence: list[Any]) -> VerificationResult:
        claims = _split_claims(answer)
        if not claims:
            return VerificationResult(False, 0.0, "no extractable claims")

        evidence_texts = [getattr(c, "text", str(c)) for c in evidence]
        supported = sum(1 for cl in claims if _claim_supported(cl, evidence_texts))
        total = len(claims)
        score = supported / total
        grounded = score >= 0.51
        reason = f"{supported}/{total} claims supported by retrieved evidence"
        return VerificationResult(grounded, score, reason)
