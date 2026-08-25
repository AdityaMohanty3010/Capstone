from app.embeddings.embedding_service import EmbeddingService


embedding_service = EmbeddingService()

text = "How do I reset my forgotten password?"

embedding = embedding_service.embed_text(text)

print("Embedding dimension:", len(embedding))
print("First 10 values:", embedding[:10])
print("Model dimension:", embedding_service.get_dimension())