from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv


@dataclass
class AppConfig:
    data_raw_dir: str = "data/raw"
    data_processed_dir: str = "data/processed"
    index_path: str = "data/processed/index.faiss"
    chunks_path: str = "data/processed/chunks.jsonl"
    documents_path: str = "data/processed/documents.jsonl"
    embedding_model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
    top_k: int = 5
    chunk_size: int = 600
    chunk_overlap: int = 120
    use_query_rewrite: bool = False
    use_reranker: bool = False
    use_verifier: bool = True
    generator_mode: str = "extractive"
    openai_model: str = "gpt-4o-mini"
    openai_api_key: str = ""


def _apply_dict_overrides(config: AppConfig, values: dict[str, Any]) -> AppConfig:
    for key, value in values.items():
        if hasattr(config, key):
            setattr(config, key, value)
    return config


def load_config(config_path: str | None = None) -> AppConfig:
    load_dotenv()
    cfg = AppConfig()

    if config_path and Path(config_path).exists():
        with open(config_path, "r", encoding="utf-8") as f:
            file_values = yaml.safe_load(f) or {}
        cfg = _apply_dict_overrides(cfg, file_values)

    env_map = {
        "data_raw_dir": os.getenv("DATA_RAW_DIR"),
        "data_processed_dir": os.getenv("DATA_PROCESSED_DIR"),
        "index_path": os.getenv("INDEX_PATH"),
        "chunks_path": os.getenv("CHUNKS_PATH"),
        "documents_path": os.getenv("DOCUMENTS_PATH"),
        "embedding_model_name": os.getenv("EMBEDDING_MODEL_NAME"),
        "openai_model": os.getenv("OPENAI_MODEL"),
        "openai_api_key": os.getenv("OPENAI_API_KEY"),
        "generator_mode": os.getenv("GENERATOR_MODE"),
    }

    numeric_map = {
        "top_k": os.getenv("TOP_K"),
        "chunk_size": os.getenv("CHUNK_SIZE"),
        "chunk_overlap": os.getenv("CHUNK_OVERLAP"),
    }

    bool_map = {
        "use_query_rewrite": os.getenv("USE_QUERY_REWRITE"),
        "use_reranker": os.getenv("USE_RERANKER"),
        "use_verifier": os.getenv("USE_VERIFIER"),
    }

    for key, value in env_map.items():
        if value not in (None, ""):
            setattr(cfg, key, value)

    for key, value in numeric_map.items():
        if value not in (None, ""):
            setattr(cfg, key, int(value))

    for key, value in bool_map.items():
        if value not in (None, ""):
            setattr(cfg, key, value.lower() in {"1", "true", "yes", "on"})

    return cfg

