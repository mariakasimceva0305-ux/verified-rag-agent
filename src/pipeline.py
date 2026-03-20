from __future__ import annotations

from dataclasses import dataclass

from src.config import AppConfig
from src.generator import AnswerGenerator, GeneratedAnswer
from src.reranker import Reranker
from src.retriever import RetrievedChunk, VectorRetriever
from src.rewriter import QueryRewriter
from src.verifier import VerificationResult, Verifier


@dataclass
class PipelineResult:
    query: str
    rewritten_query: str
    answer: str
    citations: list[str]
    retrieved_chunks: list[RetrievedChunk]
    verification: VerificationResult | None


class RAGPipeline:
    def __init__(self, config: AppConfig) -> None:
        self.config = config
        self.rewriter = QueryRewriter()
        self.reranker = Reranker()
        self.generator = AnswerGenerator()
        self.verifier = Verifier()
        self.retriever = VectorRetriever(model_name=config.embedding_model_name)
        self._is_loaded = False

    @property
    def metadata_path(self) -> str:
        return self.config.index_path + ".meta.json"

    def load_index(self) -> None:
        if not self._is_loaded:
            self.retriever.load(self.config.index_path, self.metadata_path)
            self._is_loaded = True

    def answer(self, query: str) -> PipelineResult:
        self.load_index()

        rewritten_query = query
        if self.config.use_query_rewrite:
            rewritten_query = self.rewriter.rewrite(query)

        retrieved = self.retriever.search(rewritten_query, top_k=self.config.top_k)
        if self.config.use_reranker:
            retrieved = self.reranker.rerank(rewritten_query, retrieved)

        generated: GeneratedAnswer = self.generator.generate(rewritten_query, retrieved)

        verification = None
        if self.config.use_verifier:
            verification = self.verifier.verify(generated.answer, retrieved)

        return PipelineResult(
            query=query,
            rewritten_query=rewritten_query,
            answer=generated.answer,
            citations=generated.citations,
            retrieved_chunks=retrieved,
            verification=verification,
        )

