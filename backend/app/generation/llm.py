import os
 
from dotenv import load_dotenv
from google import genai
 
load_dotenv()
 
 
class LLMService:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
 
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is not set")
 
        self.client = genai.Client(api_key=self.api_key)
 
        self.model = "gemini-3.5-flash"
 
        self.chat = self.client.chats.create(
            model=self.model
        )
 
    def generate(self, prompt: str) -> str:
        """
        Generate an answer using Gemini.
        """
 
        if not prompt.strip():
            raise ValueError("Prompt cannot be empty")
 
        response = self.chat.send_message(prompt)
 
        return response.text
 