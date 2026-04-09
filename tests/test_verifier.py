from __future__ import annotations

from types import SimpleNamespace

from src.verifier import Verifier


def test_verifier_supports_grounded_answer():
    v = Verifier()
    ev = [
        SimpleNamespace(text="Retention for security audit logs is 365 days."),
    ]
    ans = "Evidence from policies:\n- Security audit logs are kept for 365 days. [demo/x#c1]"
    r = v.verify(ans, ev)
    assert r.score > 0.4
    assert r.is_grounded is True


def test_verifier_rejects_unsupported():
    v = Verifier()
    ev = [SimpleNamespace(text="Coffee machine policy in kitchen area.")]
    ans = "Evidence from policies:\n- The company revenue grew 500 percent overnight. [demo/x#c1]"
    r = v.verify(ans, ev)
    assert r.is_grounded is False
