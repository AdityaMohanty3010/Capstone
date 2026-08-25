import os

from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec


load_dotenv()


class PineconeService:
    def __init__(self):
        self.api_key = os.getenv("PINECONE_API_KEY")
        self.index_name = os.getenv("PINECONE_INDEX_NAME")

        if not self.api_key:
            raise ValueError("PINECONE_API_KEY is not set")

        if not self.index_name:
            raise ValueError("PINECONE_INDEX_NAME is not set")

        self.client = Pinecone(api_key=self.api_key)

    def list_indexes(self):
        """Return available Pinecone indexes."""
        return self.client.list_indexes().names()

    def create_index(self):
        """Create the RAG vector index if it does not already exist."""

        existing_indexes = self.list_indexes()

        if self.index_name in existing_indexes:
            print(f"Index already exists: {self.index_name}")
            return

        self.client.create_index(
            name=self.index_name,
            dimension=384,
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            )
        )
        
    def get_index(self):
        """Return the Pinecone index."""
        return self.client.Index(self.index_name)

    def upsert_vectors(self, vectors: list[dict]):
        """
        Upsert vectors into Pinecone.

        Each vector should contain:
        - id
        - values
        - metadata
        """

        if not vectors:
            return

        index = self.get_index()

        index.upsert(vectors=vectors)

        print(f"Upserted {len(vectors)} vectors.")
        
    def search(self, query_vector: list[float], top_k: int = 5):
        """
        Search Pinecone using a query embedding.
        """

        index = self.get_index()

        results = index.query(
            vector=query_vector,
            top_k=top_k,
            include_metadata=True,
        )

        return results

        print(f"Index created: {self.index_name}")