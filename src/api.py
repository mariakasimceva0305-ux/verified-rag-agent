from __future__ import annotations

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.config import AppConfig, load_config
from src.pipeline import RAGPipeline

app = FastAPI(title="Verified RAG Agent API", version="0.1.0")

_config: AppConfig = load_config("configs/app.yaml")
_pipeline = RAGPipeline(_config)


class AskRequest(BaseModel):
    query: str


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/ask")
def ask(request: AskRequest) -> dict:
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="query cannot be empty")

    try:
        result = _pipeline.answer(request.query)
    except FileNotFoundError:
        raise HTTPException(
            status_code=400,
            detail="Index not found. Run scripts/ingest.py and scripts/build_index.py first.",
        )

    return {
        "query": result.query,
        "rewritten_query": result.rewritten_query,
        "answer": result.answer,
        "citations": result.citations,
        "retrieved_chunks": [
            {
                "chunk_id": c.chunk_id,
                "doc_id": c.doc_id,
                "source_path": c.source_path,
                "score": c.score,
            }
            for c in result.retrieved_chunks
        ],
        "verification": (
            {
                "is_grounded": result.verification.is_grounded,
                "score": result.verification.score,
                "reason": result.verification.reason,
            }
            if result.verification
            else None
        ),
    }

