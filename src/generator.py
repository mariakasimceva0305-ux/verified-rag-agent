from __future__ import annotations

from dataclasses import dataclass

from src.retriever import RetrievedChunk


@dataclass
class GeneratedAnswer:
    answer: str
    citations: list[str]


class AnswerGenerator:
    """Minimal extractive generator with citation list."""

    def generate(self, query: str, contexts: list[RetrievedChunk]) -> GeneratedAnswer:
        if not contexts:
            return GeneratedAnswer(
                answer="I could not find relevant evidence in the indexed corpus.",
                citations=[],
            )

        top = contexts[:2]
        snippets = []
        citations: list[str] = []
        for chunk in top:
            snippets.append(chunk.text[:300].strip())
            citations.append(f"{chunk.source_path}#{chunk.chunk_id}")

        answer = (
            f"Question: {query}\n\n"
            "Based on retrieved documents, the most relevant evidence is:\n"
            + "\n\n".join(f"- {s}" for s in snippets)
        )
        return GeneratedAnswer(answer=answer, citations=citations)

