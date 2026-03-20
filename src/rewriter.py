from __future__ import annotations


class QueryRewriter:
    """Lightweight placeholder for query rewriting.

    Current behavior returns input unchanged.
    """

    def rewrite(self, query: str) -> str:
        return query.strip()

