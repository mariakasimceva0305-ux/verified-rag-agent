from __future__ import annotations

import re
from typing import Iterable

# Детерминированные расширения по ключевым фразам (корпус demo_corpus).
_TRIGGER_EXPANSIONS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("audit log", ("retention", "365", "180", "security audit")),
    ("access log", ("retention", "180", "audit")),
    ("escalat", ("support", "ticket", "sla", "incident")),
    ("sev-1", ("severity", "incident", "outage", "response")),
    ("sev-2", ("severity", "incident", "degradation")),
    ("mfa", ("multi-factor", "authentication", "second factor")),
    ("offboard", ("checklist", "termination", "access")),
    ("onboard", ("access", "provisioning", "employee")),
    ("revok", ("access", "termination", "iam", "vpn")),
    ("suspend", ("account", "iam", "security", "review")),
    ("password", ("reset", "policy", "authentication")),
)

_STOPWORDS: frozenset[str] = frozenset(
    {
        "the",
        "a",
        "an",
        "is",
        "are",
        "was",
        "were",
        "be",
        "been",
        "being",
        "have",
        "has",
        "had",
        "do",
        "does",
        "did",
        "will",
        "would",
        "could",
        "should",
        "may",
        "might",
        "must",
        "shall",
        "can",
        "need",
        "to",
        "of",
        "in",
        "on",
        "for",
        "with",
        "at",
        "by",
        "from",
        "as",
        "into",
        "through",
        "during",
        "before",
        "after",
        "above",
        "below",
        "between",
        "under",
        "again",
        "further",
        "then",
        "once",
        "what",
        "which",
        "who",
        "whom",
        "this",
        "that",
        "these",
        "those",
        "am",
        "how",
        "when",
        "where",
        "why",
        "all",
        "each",
        "every",
        "both",
        "few",
        "more",
        "most",
        "other",
        "some",
        "such",
        "no",
        "nor",
        "not",
        "only",
        "own",
        "same",
        "so",
        "than",
        "too",
        "very",
        "just",
        "and",
        "but",
        "if",
        "or",
        "because",
        "until",
        "while",
    }
)


def _normalize_ws(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip())


def _strip_stopwords(tokens: Iterable[str]) -> list[str]:
    out: list[str] = []
    for t in tokens:
        tl = t.lower()
        if len(tl) <= 2 or tl in _STOPWORDS:
            continue
        out.append(t)
    return out


class QueryRewriter:
    """Локальная детерминированная переформулировка запроса без внешних API."""

    def rewrite(self, query: str) -> str:
        raw = query.strip()
        if not raw:
            return raw

        lower = raw.lower()
        extra: list[str] = []
        for needle, expansion in _TRIGGER_EXPANSIONS:
            if needle in lower:
                extra.extend(expansion)

        tokens = re.findall(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)?", raw)
        kept = _strip_stopwords(tokens)
        core = " ".join(kept) if kept else raw

        if not extra:
            return _normalize_ws(core)

        merged = _normalize_ws(f"{core} {' '.join(extra)}")
        return merged
