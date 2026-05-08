from fastapi import APIRouter, HTTPException

from ..models import ChangeSafetyRequest
from ..services.change_safety_service import ChangeSafetyService

router = APIRouter(prefix="/api/change-safety-checklist", tags=["change-safety"])


@router.post("")
def change_safety_checklist(request: ChangeSafetyRequest) -> dict:
    checklist = ChangeSafetyService().build_checklist(
        request.service_id, request.change_type, request.description
    )
    if not checklist:
        raise HTTPException(
            status_code=422,
            detail={
                "code": "validation_error",
                "message": "Unknown service_id.",
                "details": {"service_id": request.service_id},
            },
        )
    return checklist
