from fastapi import FastAPI
from dotenv import load_dotenv

from app.api.chat import router as chat_router
from app.api.ingest import router as ingest_router

load_dotenv()

app = FastAPI(
    title="AI Customer Support RAG",
    description="AI-powered customer support system using Retrieval-Augmented Generation",
    version="1.0.0",
)

app.include_router(chat_router)
app.include_router(ingest_router)


@app.get("/")
def root():
    return {
        "message": "AI Customer Support RAG API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }