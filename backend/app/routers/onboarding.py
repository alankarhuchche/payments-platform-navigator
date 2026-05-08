from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, HTTPException, Query

from ..services.knowledge_service import KnowledgeService

router = APIRouter(prefix="/api/onboarding", tags=["onboarding"])


@router.get("")
def onboarding(
    role: str = Query(..., min_length=2),
    area: Optional[str] = Query(default=None),
) -> dict:
    path = KnowledgeService().onboarding(role, area)
    if not path:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "not_found",
                "message": "Onboarding role not found.",
                "details": {"role": role},
            },
        )
    return path
