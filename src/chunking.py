from __future__ import annotations

import re
from dataclasses import dataclass

from src.ingest import Document
from src.utils import stable_id


@dataclass
class Chunk:
    chunk_id: str
    doc_id: str
    text: str
    source_path: str
    start_char: int
    end_char: int


def _normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def chunk_text(text: str, chunk_size: int = 600, overlap: int = 120) -> list[tuple[int, int, str]]:
    text = _normalize_whitespace(text)
    if not text:
        return []
    if overlap >= chunk_size:
        raise ValueError("chunk_overlap must be smaller than chunk_size")

    chunks: list[tuple[int, int, str]] = []
    start = 0
    n = len(text)
    while start < n:
        end = min(start + chunk_size, n)
        chunk = text[start:end]
        chunks.append((start, end, chunk))
        if end == n:
            break
        start = end - overlap
    return chunks


def chunk_documents(
    documents: list[Document],
    chunk_size: int = 600,
    overlap: int = 120,
) -> list[Chunk]:
    all_chunks: list[Chunk] = []
    for doc in documents:
        pieces = chunk_text(doc.text, chunk_size=chunk_size, overlap=overlap)
        for start, end, text in pieces:
            chunk_id = stable_id("chunk", f"{doc.doc_id}:{start}:{end}")
            all_chunks.append(
                Chunk(
                    chunk_id=chunk_id,
                    doc_id=doc.doc_id,
                    text=text,
                    source_path=doc.source_path,
                    start_char=start,
                    end_char=end,
                )
            )
    return all_chunks

