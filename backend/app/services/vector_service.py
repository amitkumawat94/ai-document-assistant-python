from uuid import uuid4

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

from app.config import settings


class VectorService:
    def __init__(self):
        self.client = QdrantClient(url=settings.qdrant_url)
        self.collection_name = settings.qdrant_collection

    def create_collection(self):
        collections = self.client.get_collections().collections

        exists = any(
            collection.name == self.collection_name
            for collection in collections
        )

        if not exists:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=384,
                    distance=Distance.COSINE,
                ),
            )

    def collection_exists(self) -> bool:
        collections = self.client.get_collections().collections

        return any(
            collection.name == self.collection_name
            for collection in collections
        )

    def add_chunks(
        self,
        chunks: list[str],
        embeddings: list[list[float]],
        document_name: str,
    ):
        points = []

        for index, (chunk, embedding) in enumerate(
            zip(chunks, embeddings)
        ):
            points.append(
                PointStruct(
                    id=str(uuid4()),
                    vector=embedding,
                    payload={
                        "document_name": document_name,
                        "chunk_index": index,
                        "text": chunk,
                    },
                )
            )

        self.client.upsert(
            collection_name=self.collection_name,
            points=points,
        )

        return len(points)

    def search(
        self,
        query_embedding: list[float],
        limit: int = 5,
    ):
        results = self.client.query_points(
            collection_name=self.collection_name,
            query=query_embedding,
            limit=limit,
        )

        return results.points


vector_service = VectorService()