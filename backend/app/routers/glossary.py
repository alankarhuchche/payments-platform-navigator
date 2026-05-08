from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Query

from ..services.knowledge_service import KnowledgeService

router = APIRouter(prefix="/api/glossary", tags=["glossary"])


@router.get("")
def glossary(q: Optional[str] = Query(default=None)) -> dict:
    return KnowledgeService().glossary(q)
