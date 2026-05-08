from fastapi import APIRouter

from ..services.knowledge_service import KnowledgeService

router = APIRouter(prefix="/api/knowledge-health", tags=["knowledge-health"])


@router.get("")
def knowledge_health() -> dict:
    return KnowledgeService().knowledge_health()
