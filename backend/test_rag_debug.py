from app.rag import RAGPipeline


def main():
    question = "How do I reset my forgotten password?"

    rag = RAGPipeline()

    print("\n" + "=" * 70)
    print("STEP 1 — USER QUESTION")
    print("=" * 70)
    print(question)

    # ---------------------------------------------------------
    # STEP 2 — RETRIEVAL
    # ---------------------------------------------------------

    print("\n" + "=" * 70)
    print("STEP 2 — RETRIEVING RELEVANT CHUNKS")
    print("=" * 70)

    retrieved_chunks = rag.retriever.retrieve(
        query=question,
        top_k=3
    )

    if not retrieved_chunks:
        print("No chunks retrieved.")
        return

    print(f"Retrieved {len(retrieved_chunks)} chunks:\n")

    for i, chunk in enumerate(retrieved_chunks, start=1):

        print(f"--- CHUNK {i} ---")

        print(f"Chunk ID   : {chunk.get('chunk_id')}")
        print(f"Article ID : {chunk.get('article_id')}")
        print(f"Title      : {chunk.get('title')}")
        print(f"Source     : {chunk.get('source')}")

        if "score" in chunk:
            print(f"Score      : {chunk.get('score')}")

        print("\nText:")
        print(chunk.get("text"))

        print("-" * 70)

    # ---------------------------------------------------------
    # STEP 3 — CONTEXT
    # ---------------------------------------------------------

    print("\n" + "=" * 70)
    print("STEP 3 — CONTEXT SENT TO LLM")
    print("=" * 70)

    context_parts = []

    for chunk in retrieved_chunks:
        context_parts.append(
            f"""
Article ID: {chunk.get('article_id')}
Title: {chunk.get('title')}
Source: {chunk.get('source')}

{chunk.get('text')}
"""
        )

    context = "\n---\n".join(context_parts)

    print(context)

    # ---------------------------------------------------------
    # STEP 4 — FINAL RAG ANSWER
    # ---------------------------------------------------------

    print("\n" + "=" * 70)
    print("STEP 4 — FINAL RAG ANSWER")
    print("=" * 70)

    answer = rag.answer(
        question=question,
        top_k=3
    )

    print(answer)

    print("\n" + "=" * 70)
    print("RAG PIPELINE TEST COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    main()