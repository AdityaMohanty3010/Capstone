from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.rag import RAGPipeline


router = APIRouter(prefix="/api", tags=["Chat"])

rag_pipeline = RAGPipeline()


class ChatRequest(BaseModel):
    question: str
    top_k: int = 3


class ChatResponse(BaseModel):
    answer: str


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty"
        )

    try:
        answer = rag_pipeline.answer(
            question=request.question,
            top_k=request.top_k
        )

        return ChatResponse(
            answer=answer
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )