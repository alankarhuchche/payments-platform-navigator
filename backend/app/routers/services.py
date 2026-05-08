from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, HTTPException, Query

from ..services.knowledge_service import KnowledgeService

router = APIRouter(prefix="/api/services", tags=["services"])


@router.get("")
def list_services(
    domain: Optional[str] = Query(default=None),
    criticality: Optional[str] = Query(default=None),
    flow_id: Optional[str] = Query(default=None),
) -> dict:
    return KnowledgeService().list_services(domain, criticality, flow_id)


@router.get("/{service_id}")
def get_service(service_id: str) -> dict:
    service = KnowledgeService().get_service(service_id)
    if not service:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "not_found",
                "message": "Service not found.",
                "details": {"service_id": service_id},
            },
        )
    return service
