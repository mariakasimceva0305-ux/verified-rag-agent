from __future__ import annotations

import argparse

from src.config import load_config
from src.retriever import VectorRetriever, load_chunks


def main() -> None:
    parser = argparse.ArgumentParser(description="Build FAISS index from chunks.")
    parser.add_argument(
        "--config",
        default="configs/app.yaml",
        help="Path to YAML config file.",
    )
    args = parser.parse_args()

    cfg = load_config(args.config)
    chunks = load_chunks(cfg.chunks_path)
    retriever = VectorRetriever(cfg.embedding_model_name)
    retriever.build(chunks)
    retriever.save(cfg.index_path, cfg.index_path + ".meta.json")

    print(f"Indexed chunks: {len(chunks)}")
    print(f"Saved index to: {cfg.index_path}")


if __name__ == "__main__":
    main()

