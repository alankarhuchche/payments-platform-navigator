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


class ContextPackRequest(BaseModel):
    question: str = Field(..., min_length=3, max_length=500)
    service_id: Optional[str] = None
    flow_id: Optional[str] = None


class ContextPackResponse(BaseModel):
    question: str
    detected_intent: str
    matched_entities: Dict[str, list]
    relevant_services: list[str]
    relevant_flows: list[str]
    relevant_events: list[str]
    relevant_apis: list[str]
    relevant_runbooks: list[str]
    relevant_incidents: list[str]
    relevant_tests: list[str]
    relevant_risks: list[Dict[str, Any]]
    suggested_next_steps: list[str]
    source_files: list[str]
    confidence: float
    unsupported_reason: Optional[str] = None
