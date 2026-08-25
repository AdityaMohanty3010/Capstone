from app.embeddings.embedding_service import EmbeddingService
from app.vectorstore.pinecone_services import PineconeService


class Retriever:
    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.pinecone_service = PineconeService()

    def retrieve(self, query: str, top_k: int = 5) -> list[dict]:
        """
        Retrieve the most relevant chunks for a user query.
        """

        if not query.strip():
            raise ValueError("Query cannot be empty")

        query_embedding = self.embedding_service.embed_text(query)

        results = self.pinecone_service.search(
            query_vector=query_embedding,
            top_k=top_k,
        )

        retrieved_chunks = []

        for match in results["matches"]:
            retrieved_chunks.append(
                {
                    "chunk_id": match["id"],
                    "score": match["score"],
                    "text": match["metadata"].get("text", ""),
                    "source": match["metadata"].get("source", ""),
                    "article_id": match["metadata"].get("article_id", ""),
                    "title": match["metadata"].get("title", ""),
                }
            )

        return retrieved_chunks