from fastembed import TextEmbedding


class EmbeddingService:
    def __init__(self):
        self.model = TextEmbedding(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

    def embed_text(self, text: str) -> list[float]:
        embedding = next(self.model.embed([text]))
        return embedding.tolist()


embedding_service = EmbeddingService()