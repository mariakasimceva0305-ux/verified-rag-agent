# README skeleton

# Verified RAG Agent for Document QA

A citation-aware RAG system for answering questions over a document corpus, with baseline vs improved retrieval comparison.

## What this project does
- answers questions over a document collection
- retrieves relevant chunks
- optionally rewrites the query
- reranks retrieved chunks
- generates an answer with citations
- performs a lightweight groundedness / verification step

## Why this project
The goal is to build a simple but strong retrieval + agent-style project that is easy to explain, evaluate, and extend.

## Pipeline
1. Ingest documents
2. Split into chunks
3. Build vector index
4. Retrieve top-k chunks
5. Optionally rewrite query
6. Rerank candidates
7. Generate answer with citations
8. Verify whether the answer is grounded in the cited evidence

## Baseline
- vector retrieval
- top-k chunks
- answer generation
- citations

## Improved version
- query rewriting
- reranking
- lightweight verification

## Data
- corpus type
- number of documents
- source
- preprocessing notes

## Evaluation
### Retrieval
- Recall@k
- HitRate@k
- MRR

### Answer quality
- groundedness
- citation coverage
- manual correctness

### System
- p50 / p95 latency

## Results
| setup | Recall@5 | MRR | grounded answers | citation coverage | notes |
|---|---:|---:|---:|---:|---|
| baseline | TODO | TODO | TODO | TODO | TODO |
| + query rewrite | TODO | TODO | TODO | TODO | TODO |
| + reranker | TODO | TODO | TODO | TODO | TODO |
| + verification | TODO | TODO | TODO | TODO | TODO |

## How to run
```bash
# install
pip install -r requirements.txt

# ingest docs
python scripts/ingest.py

# build index
python scripts/build_index.py

# run evaluation
python scripts/run_eval.py
```

## Example queries
- What is the refund policy for delayed orders?
- Which documents mention access revocation?
- Under what conditions is a request escalated?

## Limitations
- limited corpus size
- offline-only evaluation in v1
- lightweight verification, not a full fact-checker

## Next steps
- better evaluation
- stronger reranking
- richer verifier
- simple web UI or demo API
