from app.retrieval.retriever import Retriever


retriever = Retriever()

query = "I forgot my password and cannot log in. What should I do?"

results = retriever.retrieve(query, top_k=3)

print("\n--- RETRIEVAL RESULTS ---\n")

for result in results:
    print("Chunk ID:", result["chunk_id"])
    print("Score:", result["score"])
    print("Article ID:", result["article_id"])
    print("Title:", result["title"])
    print("Source:", result["source"])
    print("Text:", result["text"])
    print("-" * 50)