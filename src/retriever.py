from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

from src.chunking import Chunk
from src.utils import ensure_parent_dir, read_jsonl


@dataclass
class RetrievedChunk:
    chunk_id: str
    doc_id: str
    text: str
    source_path: str
    score: float


class VectorRetriever:
    def __init__(self, model_name: str) -> None:
        self.model = SentenceTransformer(model_name)
        self.index: faiss.Index | None = None
        self.metadata: list[dict] = []

    def build(self, chunks: list[Chunk]) -> None:
        texts = [c.text for c in chunks]
        if not texts:
            raise ValueError("No chunks provided for indexing")

        vectors = self.model.encode(texts, normalize_embeddings=True)
        matrix = np.asarray(vectors, dtype=np.float32)
        dim = matrix.shape[1]

        self.index = faiss.IndexFlatIP(dim)
        self.index.add(matrix)

        self.metadata = [
            {
                "chunk_id": c.chunk_id,
                "doc_id": c.doc_id,
                "text": c.text,
                "source_path": c.source_path,
            }
            for c in chunks
        ]

    def search(self, query: str, top_k: int = 5) -> list[RetrievedChunk]:
        if self.index is None:
            raise RuntimeError("Retriever index is not built or loaded")

        query_vec = self.model.encode([query], normalize_embeddings=True)
        q = np.asarray(query_vec, dtype=np.float32)
        scores, indices = self.index.search(q, top_k)

        results: list[RetrievedChunk] = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < 0:
                continue
            meta = self.metadata[idx]
            results.append(
                RetrievedChunk(
                    chunk_id=meta["chunk_id"],
                    doc_id=meta["doc_id"],
                    text=meta["text"],
                    source_path=meta["source_path"],
                    score=float(score),
                )
            )
        return results

    def save(self, index_path: str, metadata_path: str) -> None:
        if self.index is None:
            raise RuntimeError("No index to save")
        ensure_parent_dir(index_path)
        ensure_parent_dir(metadata_path)
        faiss.write_index(self.index, index_path)
        with open(metadata_path, "w", encoding="utf-8") as f:
            json.dump(self.metadata, f, ensure_ascii=False, indent=2)

    def load(self, index_path: str, metadata_path: str) -> None:
        self.index = faiss.read_index(index_path)
        with open(metadata_path, "r", encoding="utf-8") as f:
            self.metadata = json.load(f)


def load_chunks(chunks_path: str) -> list[Chunk]:
    rows = read_jsonl(chunks_path)
    return [
        Chunk(
            chunk_id=r["chunk_id"],
            doc_id=r["doc_id"],
            text=r["text"],
            source_path=r["source_path"],
            start_char=r["start_char"],
            end_char=r["end_char"],
        )
        for r in rows
    ]


def save_chunks(chunks: list[Chunk], chunks_path: str) -> None:
    rows = [
        {
            "chunk_id": c.chunk_id,
            "doc_id": c.doc_id,
            "text": c.text,
            "source_path": c.source_path,
            "start_char": c.start_char,
            "end_char": c.end_char,
        }
        for c in chunks
    ]
    from src.utils import write_jsonl

    write_jsonl(chunks_path, rows)

