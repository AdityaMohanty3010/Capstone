from sentence_transformers import SentenceTransformer


class EmbeddingService:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def embed_text(self, text: str) -> list[float]:
        """
        Convert a single text into an embedding vector.
        """
        if not text.strip():
            raise ValueError("Text cannot be empty")

        embedding = self.model.encode(
            text,
            convert_to_numpy=True
        )

        return embedding.tolist()

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        """
        Convert multiple texts into embedding vectors.
        """
        if not texts:
            return []

        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True
        )

        return embeddings.tolist()

    def get_dimension(self) -> int:
        """
        Return the dimensionality of the embedding model.
        """
        return self.model.get_sentence_embedding_dimension()