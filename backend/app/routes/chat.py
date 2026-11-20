from fastapi import APIRouter

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.rag_service import rag_service


router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest):
    answer = rag_service.answer_question(request.question)

    return ChatResponse(answer=answer)