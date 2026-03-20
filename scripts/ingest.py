from __future__ import annotations

import argparse

from src.chunking import chunk_documents
from src.config import load_config
from src.ingest import ingest_raw_documents, save_documents
from src.retriever import save_chunks


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest raw documents and create chunks.")
    parser.add_argument(
        "--config",
        default="configs/app.yaml",
        help="Path to YAML config file.",
    )
    args = parser.parse_args()

    cfg = load_config(args.config)
    docs = ingest_raw_documents(cfg.data_raw_dir)
    save_documents(docs, cfg.documents_path)

    chunks = chunk_documents(docs, chunk_size=cfg.chunk_size, overlap=cfg.chunk_overlap)
    save_chunks(chunks, cfg.chunks_path)

    print(f"Ingested documents: {len(docs)}")
    print(f"Created chunks: {len(chunks)}")
    print(f"Saved documents to: {cfg.documents_path}")
    print(f"Saved chunks to: {cfg.chunks_path}")


if __name__ == "__main__":
    main()

