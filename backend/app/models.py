"""Request models for generated backend responses."""

from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    question: str = Field(..., min_length=3, max_length=500)
    context: Optional[Dict[str, Any]] = None


class ChangeSafetyRequest(BaseModel):
    service_id: str
    change_type: str = Field(..., min_length=2, max_length=120)
    description: Optional[str] = Field(default=None, max_length=1000)
