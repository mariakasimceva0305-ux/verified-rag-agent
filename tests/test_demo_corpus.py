from pathlib import Path


def test_demo_corpus_has_expected_size() -> None:
    demo_dir = Path("data/raw/demo_corpus")
    files = sorted(demo_dir.glob("*.md"))
    assert len(files) >= 8

