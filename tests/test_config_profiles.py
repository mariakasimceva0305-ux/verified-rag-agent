from src.config import load_config


def test_baseline_vs_improved_flags() -> None:
    baseline = load_config("configs/baseline.yaml")
    improved = load_config("configs/improved.yaml")

    assert baseline.use_query_rewrite is False
    assert baseline.use_reranker is False
    assert baseline.use_verifier is False

    assert improved.use_query_rewrite is True
    assert improved.use_reranker is True
    assert improved.use_verifier is True

