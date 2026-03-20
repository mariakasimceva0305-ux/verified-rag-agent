from types import SimpleNamespace

from src.verifier import Verifier


def test_verifier_returns_score() -> None:
    verifier = Verifier()
    evidence = [
        SimpleNamespace(
            text="Users can reset passwords through the account security page."
        )
    ]
    result = verifier.verify(
        "Passwords can be reset using the account security page.",
        evidence,
    )

    assert 0.0 <= result.score <= 1.0
    assert isinstance(result.is_grounded, bool)

