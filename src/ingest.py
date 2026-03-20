from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from src.utils import stable_id, write_jsonl

SUPPORTED_SUFFIXES = {".txt", ".md"}


@dataclass
class Document:
    doc_id: str
    title: str
    text: str
    source_path: str


def _read_text_file(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore").strip()


def ingest_raw_documents(raw_dir: str) -> list[Document]:
    root = Path(raw_dir)
    if not root.exists():
        raise FileNotFoundError(f"Raw data directory not found: {raw_dir}")

    docs: list[Document] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in SUPPORTED_SUFFIXES:
            continue
        text = _read_text_file(path)
        if not text:
            continue
        rel_path = str(path.relative_to(root))
        doc_id = stable_id("doc", rel_path)
        docs.append(
            Document(
                doc_id=doc_id,
                title=path.stem,
                text=text,
                source_path=rel_path,
            )
        )
    return docs


def save_documents(documents: list[Document], output_path: str) -> None:
    rows = [
        {
            "doc_id": d.doc_id,
            "title": d.title,
            "text": d.text,
            "source_path": d.source_path,
        }
        for d in documents
    ]
    write_jsonl(output_path, rows)

