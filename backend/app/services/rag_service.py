from app.services.embedding_service import embedding_service
from app.services.llm_service import llm_service
from app.services.vector_service import vector_service


class RAGService:

    def answer_question(self, question: str, limit: int = 5) -> str:
        query_embedding = embedding_service.embed_text(question)

        results = vector_service.search(
            query_embedding=query_embedding,
            limit=limit,
        )

        context_parts = []

        for result in results:
            text = result.payload.get("text")

            if text:
                context_parts.append(text)

        context = "\n\n---\n\n".join(context_parts)

        return llm_service.generate_answer(
            question=question,
            context=context,
        )


rag_service = RAGService()