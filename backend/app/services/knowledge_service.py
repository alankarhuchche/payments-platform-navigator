"""Read-only query helpers over the synthetic knowledge model."""

from __future__ import annotations

from typing import Any

from ..data_loader import KnowledgeData, get_knowledge_data


class KnowledgeService:
    def __init__(self, data: KnowledgeData | None = None) -> None:
        self.data = data or get_knowledge_data()

    @staticmethod
    def _metadata(source: dict[str, Any] | None = None) -> dict[str, Any]:
        return {"classification": (source or {}).get("classification", "synthetic")}

    def list_services(
        self,
        domain: str | None = None,
        criticality: str | None = None,
        flow_id: str | None = None,
    ) -> dict[str, Any]:
        items = list(self.data.services)
        if domain:
            items = [item for item in items if item.get("domain") == domain]
        if criticality:
            items = [item for item in items if item.get("criticality") == criticality]
        if flow_id:
            items = [item for item in items if flow_id in item.get("supports_flows", [])]
        enriched = [self._service_summary(item) for item in items]
        return {
            "metadata": self._metadata(self.data.files["services.yaml"].get("metadata")),
            "count": len(enriched),
            "items": enriched,
        }

    def get_service(self, service_id: str) -> dict[str, Any] | None:
        resolved_id = self.data.resolve_service_id(service_id)
        if not resolved_id:
            return None
        service = dict(self.data.services_by_id[resolved_id])
        service["knowledge_health"] = self._service_health(resolved_id)
        return service

    def list_flows(
        self,
        direction: str | None = None,
        message_type: str | None = None,
        service_id: str | None = None,
        status: str | None = None,
    ) -> dict[str, Any]:
        items = list(self.data.flows)
        if direction:
            items = [item for item in items if item.get("direction") == direction]
        if message_type:
            items = [item for item in items if item.get("message_type") == message_type]
        if service_id:
            resolved_service_id = self.data.resolve_service_id(service_id)
            items = [
                item
                for item in items
                if resolved_service_id and resolved_service_id in item.get("services", [])
            ]
        if status:
            items = [
                item
                for item in items
                if self._flow_health(item["id"]).get("status") == status
            ]
        enriched = [self._flow_summary(item) for item in items]
        return {
            "metadata": self._metadata(
                self.data.files["payment-flows.yaml"].get("metadata")
            ),
            "count": len(enriched),
            "items": enriched,
        }

    def get_flow(self, flow_id: str) -> dict[str, Any] | None:
        resolved_id = self.data.resolve_flow_id(flow_id)
        if not resolved_id:
            return None
        flow = dict(self.data.flows_by_id[resolved_id])
        flow["knowledge_health"] = self._flow_health(resolved_id)
        return flow

    def glossary(self, q: str | None = None) -> dict[str, Any]:
        items = list(self.data.glossary_terms)
        if q:
            lowered = q.lower()
            items = [
                item
                for item in items
                if lowered in item["term"].lower()
                or lowered in item["definition"].lower()
            ]
        return {
            "metadata": self._metadata(self.data.files["glossary.yaml"].get("metadata")),
            "count": len(items),
            "items": items,
        }

    def onboarding(self, role: str, area: str | None = None) -> dict[str, Any] | None:
        path = self.data.onboarding_by_role.get(role.lower())
        if not path:
            return None
        response = dict(path)
        if area:
            response["area"] = area
            area_lower = area.lower()
            highlighted = [
                service["id"]
                for service in self.data.services
                if area_lower in service.get("domain", "").lower()
                or area_lower in service.get("type", "").lower()
                or area_lower in service.get("name", "").lower()
            ]
            response["area_matched_services"] = highlighted
        return response

    def knowledge_health(self) -> dict[str, Any]:
        return self.data.knowledge_health

    def _service_summary(self, service: dict[str, Any]) -> dict[str, Any]:
        return {
            "id": service["id"],
            "name": service["name"],
            "type": service.get("type"),
            "domain": service.get("domain"),
            "criticality": service.get("criticality"),
            "owned_by": service.get("owned_by"),
            "summary": service.get("summary"),
            "supports_flows": service.get("supports_flows", []),
            "upstream_services": service.get("upstream_services", []),
            "downstream_services": service.get("downstream_services", []),
            "knowledge_health": self._service_health(service["id"], summary=True),
        }

    def _flow_summary(self, flow: dict[str, Any]) -> dict[str, Any]:
        return {
            "id": flow["id"],
            "name": flow["name"],
            "message_type": flow.get("message_type"),
            "direction": flow.get("direction"),
            "business_purpose": flow.get("business_purpose"),
            "entry_service": flow.get("entry_service"),
            "services": flow.get("services", []),
            "tests": flow.get("tests", []),
            "knowledge_health": self._flow_health(flow["id"]),
        }

    def _service_health(self, service_id: str, summary: bool = False) -> dict[str, Any]:
        health = self.data.service_health_by_service_id.get(service_id, {})
        if summary:
            return {"score": health.get("score"), "status": health.get("status")}
        return health

    def _flow_health(self, flow_id: str) -> dict[str, Any]:
        return self.data.flow_health_by_flow_id.get(flow_id, {})
