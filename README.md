# Verified RAG Agent for Document QA

A citation-aware RAG project for question answering over a document corpus, built as a clean engineering baseline with an extensible improved pipeline.

## What this project does

- Ingests local documents (`.txt` / `.md`) into a normalized corpus.
- Splits documents into overlapping chunks.
- Builds a FAISS vector index over sentence-transformer embeddings.
- Retrieves top-k relevant chunks for a question.
- Optionally rewrites queries, reranks candidates, and verifies groundedness.
- Returns answers with explicit source citations.

## Why this exists

The goal is to provide a realistic, interview-friendly NLP/retrieval project:

- simple enough to understand quickly,
- modular enough to extend,
- rigorous enough to evaluate baseline vs improved retrieval behavior.

## Pipeline

1. **Ingestion**: read raw docs from `data/raw/`.
2. **Chunking**: split text into overlapping windows.
3. **Indexing**: embed chunks and store FAISS index + metadata.
4. **Retrieval**: retrieve top-k chunks by vector similarity.
5. **(Optional) Rewrite**: improve query phrasing before retrieval.
6. **(Optional) Rerank**: reorder retrieved candidates.
7. **Generation**: produce answer text with citations.
8. **(Optional) Verification**: estimate whether answer is grounded in evidence.

## Baseline vs Improved

### Baseline (implemented)
- vector retrieval
- top-k chunk selection
- extractive answer synthesis
- citations

### Improved pipeline (scaffolded, lightweight placeholders in v1)
- query rewriting (`src/rewriter.py`)
- reranking (`src/reranker.py`)
- verification (`src/verifier.py`)

## Data / Corpus

The repository is initialized for a local document corpus:

- Place source docs in `data/raw/`.
- Supported formats in v1: `.txt`, `.md`.
- Processed artifacts are written to `data/processed/`.

## Evaluation plan

Evaluation entrypoint: `scripts/run_eval.py`

- **Retrieval metrics**: HitRate@k, MRR (from `gold_doc_ids` in eval set)
- **System metrics**: latency p50 / p95
- **Answer review**: manual correctness / groundedness / citation usefulness (planned in `eval/`)

No fake benchmark numbers are included; results are generated only from local runs.

## Repository layout

```text
configs/            # YAML config
data/raw/           # input corpus
data/processed/     # generated documents/chunks/index
docs/               # project notes
eval/               # eval dataset and outputs
examples/           # sample questions
scripts/            # ingest/index/eval scripts
src/                # pipeline modules
tests/              # lightweight unit tests
```

## How to run

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Add a few `.txt` or `.md` files into `data/raw/`, then:

```bash
python scripts/ingest.py
python scripts/build_index.py
uvicorn src.api:app --reload
```

API:
- `GET /health`
- `POST /ask` with JSON body: `{"query": "your question"}`

Run offline evaluation:

```bash
python scripts/run_eval.py
```

## Limitations (v1)

- Generator is extractive and simple by design.
- Query rewriting and reranking are placeholder implementations.
- Verification is lexical-overlap based, not a full fact-checker.
- Eval quality depends on manual `gold_doc_ids` in `eval/questions.jsonl`.

## Next steps

- Replace placeholder rewriter/reranker with stronger models.
- Add optional LLM generation mode with strict citation formatting.
- Expand evaluation set (30-50 questions) and manual annotation workflow.
- Add regression tests for retrieval quality and citation coverage.

