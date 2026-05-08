from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, HTTPException, Query

from ..services.knowledge_service import KnowledgeService

router = APIRouter(prefix="/api/flows", tags=["flows"])


@router.get("")
def list_flows(
    direction: Optional[str] = Query(default=None),
    message_type: Optional[str] = Query(default=None),
    service_id: Optional[str] = Query(default=None),
    status: Optional[str] = Query(default=None),
) -> dict:
    return KnowledgeService().list_flows(direction, message_type, service_id, status)


@router.get("/{flow_id}")
def get_flow(flow_id: str) -> dict:
    flow = KnowledgeService().get_flow(flow_id)
    if not flow:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "not_found",
                "message": "Payment flow not found.",
                "details": {"flow_id": flow_id},
            },
        )
    return flow
