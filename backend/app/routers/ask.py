from fastapi import APIRouter

from ..models import AskRequest
from ..services.ask_service import AskService

router = APIRouter(prefix="/api/ask", tags=["ask"])


@router.post("")
def ask(request: AskRequest) -> dict:
    return AskService().answer(request.question, request.context)
