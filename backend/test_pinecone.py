from app.vectorstore.pinecone_services import PineconeService
from app.embeddings.embedding_service import EmbeddingService


pinecone_service = PineconeService()
embedding_service = EmbeddingService()


query = "I forgot my password. How can I reset it?"

query_embedding = embedding_service.embed_text(query)


results = pinecone_service.search(
    query_vector=query_embedding,
    top_k=5,
)


print("\n--- SEARCH RESULTS ---\n")

for match in results["matches"]:
    print("ID:", match["id"])
    print("Score:", match["score"])
    print("Metadata:", match["metadata"])
    print()