from __future__ import annotations

from src.rewriter import QueryRewriter


def test_rewrite_expands_audit_query():
    r = QueryRewriter()
    out = r.rewrite("How long are security audit logs retained?")
    assert "retention" in out.lower()
    assert "365" in out or "audit" in out.lower()


def test_rewrite_empty_unchanged():
    r = QueryRewriter()
    assert r.rewrite("") == ""
    assert r.rewrite("   ") == ""


def test_rewrite_short_query_stable():
    r = QueryRewriter()
    assert r.rewrite("Hi") == "Hi"
