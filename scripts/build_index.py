from __future__ import annotations

from src.config import load_config
from src.retriever import VectorRetriever, load_chunks


def main() -> None:
    cfg = load_config("configs/app.yaml")
    chunks = load_chunks(cfg.chunks_path)
    retriever = VectorRetriever(cfg.embedding_model_name)
    retriever.build(chunks)
    retriever.save(cfg.index_path, cfg.index_path + ".meta.json")

    print(f"Indexed chunks: {len(chunks)}")
    print(f"Saved index to: {cfg.index_path}")


if __name__ == "__main__":
    main()

