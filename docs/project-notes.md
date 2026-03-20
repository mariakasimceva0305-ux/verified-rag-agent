# Project Notes

This document tracks implementation assumptions and future iterations.

## Current v1 assumptions

- Local corpus only (`data/raw`).
- Supported document types: `.txt`, `.md`.
- Embeddings: sentence-transformers.
- Vector index: FAISS inner-product over normalized embeddings.
- API: minimal FastAPI service.

## Planned improvements

- Better query rewriting strategy.
- Dedicated reranker model.
- More robust groundedness verifier.
- Optional generative model path for concise final answers.

