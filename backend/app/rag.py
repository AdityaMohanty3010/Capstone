from app.retrieval.retriever import Retriever
from app.generation.llm import LLMService
 
 
class RAGPipeline:
    def __init__(self):
        self.retriever = Retriever()
        self.llm = LLMService()
 
    def answer(self, question: str, top_k: int = 3) -> str:
        """
        Generate a customer-support answer using RAG.
        """
 
        if not question.strip():
            raise ValueError("Question cannot be empty")
 
        # 1. Retrieve relevant knowledge-base chunks
        retrieved_chunks = self.retriever.retrieve(
            query=question,
            top_k=top_k
        )
 
        # 2. If nothing was retrieved
        if not retrieved_chunks:
            return (
                "I couldn't find a reliable answer in the knowledge base. "
                "Please contact support."
            )
 
        # 3. Build context
        context_parts = []
 
        for chunk in retrieved_chunks:
            context_parts.append(
                f"""
Article ID: {chunk["article_id"]}
Title: {chunk["title"]}
Source: {chunk["source"]}
 
{chunk["text"]}
"""
            )
 
        context = "\n\n---\n\n".join(context_parts)
 
        # 4. Create RAG prompt
        prompt = f"""
You are an AI customer-support assistant.
 
Answer the customer's question using ONLY the knowledge-base
information provided below.
 
Do not invent information.
 
If the answer cannot be found in the knowledge base, respond with:
 
"I couldn't find a reliable answer in the knowledge base. Please contact support."
 
Knowledge Base:
{context}
 
Customer Question:
{question}
 
Give a clear, concise and helpful answer.
"""
 
        # 5. Send prompt to Gemini
        answer = self.llm.generate(prompt)
 
        return answer
 