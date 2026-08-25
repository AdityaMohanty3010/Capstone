from app.generation.llm import LLMService
 
 
llm = LLMService()
 
prompt = """
You are a helpful customer support assistant.
 
Answer the following question clearly:
 
How do I reset my forgotten password?
"""
 
answer = llm.generate(prompt)
 
print("\n--- GEMINI RESPONSE ---")
print(answer)
 