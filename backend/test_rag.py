from app.rag import RAGPipeline
 
 
rag = RAGPipeline()
 
question = "How do I reset my forgotten password?"
 
answer = rag.answer(question)
 
print("\n--- RAG ANSWER ---")
print(answer)