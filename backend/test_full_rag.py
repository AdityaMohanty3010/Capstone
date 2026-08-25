from app.retrieval.retriever import Retriever
from app.generation.llm import LLMService
 
 
def main():
    query = "How do I reset a forgotten password?"
 
    print("\n" + "=" * 70)
    print("              FULL RAG PIPELINE TEST")
    print("=" * 70)
 
    # ---------------------------------------------------------
    # STEP 1: USER QUERY
    # ---------------------------------------------------------
    print("\n[1] USER QUERY")
    print("-" * 70)
    print(query)
 
    # ---------------------------------------------------------
    # STEP 2: RETRIEVAL
    # ---------------------------------------------------------
    print("\n[2] RETRIEVAL")
    print("-" * 70)
 
    retriever = Retriever()
 
    retrieved_chunks = retriever.retrieve(
        query=query,
        top_k=3
    )
 
    if not retrieved_chunks:
        print("No relevant chunks found.")
        return
 
    print(f"Retrieved {len(retrieved_chunks)} chunks:\n")
 
    for i, chunk in enumerate(retrieved_chunks, start=1):
        print(f"--- Retrieved Chunk {i} ---")
        print(f"Chunk ID : {chunk.get('chunk_id', '')}")
        print(f"Article  : {chunk.get('article_id', '')}")
        print(f"Title    : {chunk.get('title', '')}")
        print(f"Source   : {chunk.get('source', '')}")
        print(f"Score    : {chunk.get('score', 0):.6f}")
        print(f"Text     : {chunk.get('text', '')}")
        print()
 
    # ---------------------------------------------------------
    # STEP 3: BUILD CONTEXT
    # ---------------------------------------------------------
    print("\n[3] CONTEXT SENT TO LLM")
    print("-" * 70)
 
    context_parts = []
 
    for chunk in retrieved_chunks:
        context_parts.append(
            f"""
Article ID: {chunk.get('article_id', '')}
Title: {chunk.get('title', '')}
Source: {chunk.get('source', '')}
 
Content:
{chunk.get('text', '')}
"""
        )
 
    context = "\n".join(context_parts)
 
    print(context)
 
    # ---------------------------------------------------------
    # STEP 4: BUILD PROMPT
    # ---------------------------------------------------------
    prompt = f"""
You are an AI customer-support assistant.
 
Answer the customer's question using ONLY the
knowledge-base information provided below.
 
Do not invent information.
 
If the answer cannot be found in the knowledge base,
respond with:
 
"I couldn't find a reliable answer in the knowledge base.
Please contact support."
 
Knowledge Base:
{context}
 
Customer Question:
{query}
 
Give a clear, concise and helpful answer.
"""
 
    print("\n[4] PROMPT SENT TO GEMINI")
    print("-" * 70)
    print(prompt)
 
    # ---------------------------------------------------------
    # STEP 5: GEMINI
    # ---------------------------------------------------------
    print("\n[5] GEMINI RESPONSE")
    print("-" * 70)
 
    llm = LLMService()
 
    answer = llm.generate(prompt)
 
    print(answer)
 
    # ---------------------------------------------------------
    # COMPLETE
    # ---------------------------------------------------------
    print("\n" + "=" * 70)
    print("              RAG PIPELINE COMPLETED")
    print("=" * 70)
 
    print("""
Flow verified:
 
User Query
    ↓
Embedding
    ↓
Pinecone Retrieval
    ↓
Top-K Relevant Chunks
    ↓
Context Construction
    ↓
Gemini Prompt
    ↓
Gemini Response
    ↓
Final Answer
""")
 
 
if __name__ == "__main__":
    main()
 