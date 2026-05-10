from fastapi import APIRouter

from ..models import AskRequest, ContextPackRequest, ContextPackResponse
from ..services.ask_service import AskService
from ..services.context_pack_service import ContextPackBuilder

router = APIRouter(prefix="/api", tags=["ask"])


@router.post("/ask")
def ask(request: AskRequest) -> dict:
    return AskService().answer(request.question, request.context)


@router.post("/context-pack", response_model=ContextPackResponse)
def context_pack(request: ContextPackRequest) -> dict:
    """Return the structured context pack for a question.

    This endpoint returns the retrieved context that would be used for
    AI-assisted explanations. It includes matched entities, relevant
    services/flows/incidents/runbooks, source files, and confidence score.

    This is primarily for debugging and transparency—to see what structured
    data is available behind an answer.
    """
    return ContextPackBuilder().build(
        request.question,
        service_id=request.service_id,
        flow_id=request.flow_id,
    )
