from src.chunking import chunk_text


def test_chunk_text_overlap_behavior() -> None:
    text = "A" * 1000
    chunks = chunk_text(text, chunk_size=300, overlap=100)

    assert len(chunks) >= 4
    assert chunks[0][0] == 0
    assert chunks[1][0] == 200
    assert chunks[-1][1] == len(text)

