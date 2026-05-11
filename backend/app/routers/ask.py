from fastapi import APIRouter

from ..models import AskRequest, ContextPackRequest, ContextPackResponse
from ..services.ask_service import AskService
from ..services.context_pack_service import ContextPackBuilder
from ..services.ai_explainer_service import AIExplainerService

router = APIRouter(prefix="/api", tags=["ask"])


@router.post("/ask")
def ask(request: AskRequest) -> dict:
    """Answer a question about the payments platform.

    Supports two modes:
    - deterministic: Rule-based answer from synthetic data (default)
    - ai_assisted: AI-assisted explanation if enabled and configured

    If AI is disabled or fails, falls back to deterministic answer.
    """
    # Get deterministic answer first
    deterministic_answer = AskService().answer(request.question, request.context)

    # Check if AI-assisted mode is requested
    if request.mode == "ai_assisted":
        return _get_ai_assisted_answer(request.question, deterministic_answer)

    return deterministic_answer


def _get_ai_assisted_answer(question: str, deterministic_answer: dict) -> dict:
    """Generate AI-assisted explanation if configured, else return deterministic."""
    try:
        ai_service = AIExplainerService()

        # Check if AI is available
        if not ai_service.is_available():
            # AI disabled or not configured - return deterministic with status
            deterministic_answer["ai_status"] = {
                "mode": "disabled",
                "reason": "AI explanations are disabled or not properly configured",
                "available": False,
            }
            return deterministic_answer

        # Build context pack for AI
        context_pack = ContextPackBuilder().build(question)

        # Get AI-assisted explanation
        ai_result = ai_service.explain(context_pack)

        # Merge AI result with deterministic answer
        return {
            **deterministic_answer,
            "ai_explanation": ai_result.explanation,
            "ai_confidence": ai_result.confidence,
            "ai_mode": "ai_assisted",
            "ai_status": {
                "mode": "ai_assisted",
                "provider": ai_result.provider_used,
                "available": True,
                "guardrail_notes": ai_result.guardrail_notes,
            },
        }
    except Exception as e:
        # AI provider failed - return deterministic with error status
        deterministic_answer["ai_status"] = {
            "mode": "error",
            "reason": f"AI provider error: {str(e)[:100]}",
            "available": False,
        }
        return deterministic_answer


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
