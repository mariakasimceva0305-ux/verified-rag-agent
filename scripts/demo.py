from __future__ import annotations

import argparse
from pathlib import Path

from src.chunking import chunk_documents
from src.config import load_config
from src.ingest import ingest_raw_documents, save_documents
from src.pipeline import RAGPipeline
from src.retriever import VectorRetriever, save_chunks


def _ensure_index(config_path: str) -> None:
    cfg = load_config(config_path)
    index_file = Path(cfg.index_path)
    meta_file = Path(cfg.index_path + ".meta.json")
    chunks_file = Path(cfg.chunks_path)
    docs_file = Path(cfg.documents_path)

    if index_file.exists() and meta_file.exists():
        return

    docs = ingest_raw_documents(cfg.data_raw_dir)
    save_documents(docs, cfg.documents_path)
    chunks = chunk_documents(docs, chunk_size=cfg.chunk_size, overlap=cfg.chunk_overlap)
    save_chunks(chunks, cfg.chunks_path)

    retriever = VectorRetriever(cfg.embedding_model_name)
    retriever.build(chunks)
    retriever.save(cfg.index_path, cfg.index_path + ".meta.json")

    print(f"[setup] documents: {len(docs)} -> {docs_file}")
    print(f"[setup] chunks: {len(chunks)} -> {chunks_file}")
    print(f"[setup] index: {index_file}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run end-to-end demo questions.")
    parser.add_argument(
        "--config",
        default="configs/improved.yaml",
        help="Config profile to use (baseline or improved).",
    )
    args = parser.parse_args()

    _ensure_index(args.config)
    cfg = load_config(args.config)
    pipeline = RAGPipeline(cfg)

    sample_questions = [
        "When should a support ticket be escalated?",
        "How long are security audit logs retained?",
        "Who handles SEV-1 incidents outside business hours?",
        "When can a suspended account be restored?",
    ]

    print(f"\n[demo] profile: {args.config}")
    for idx, question in enumerate(sample_questions, start=1):
        result = pipeline.answer(question)
        print(f"\nQ{idx}: {question}")
        print("Answer:")
        print(result.answer)
        print("Citations:")
        if result.citations:
            for c in result.citations:
                print(f"- {c}")
        else:
            print("- none")

        if result.verification is not None:
            print(
                "Verification: "
                f"is_grounded={result.verification.is_grounded}, "
                f"score={result.verification.score:.2f}, "
                f"reason={result.verification.reason}"
            )


if __name__ == "__main__":
    main()

