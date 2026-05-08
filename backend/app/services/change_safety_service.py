"""Deterministic change-safety checklist generation."""

from __future__ import annotations

from typing import Any

from ..data_loader import KnowledgeData, get_knowledge_data


class ChangeSafetyService:
    def __init__(self, data: KnowledgeData | None = None) -> None:
        self.data = data or get_knowledge_data()

    def build_checklist(
        self, service_id: str, change_type: str, description: str | None = None
    ) -> dict[str, Any] | None:
        resolved_service_id = self.data.resolve_service_id(service_id)
        if not resolved_service_id:
            return None

        service = self.data.services_by_id[resolved_service_id]
        impacted_flows = sorted(set(service.get("supports_flows", [])))
        impacted_events = sorted(
            set(service.get("publishes_events", []) + service.get("consumes_events", []))
        )
        impacted_apis = sorted(
            set(service.get("provides_apis", []) + service.get("consumes_apis", []))
        )
        impacted_services = sorted(
            set(
                [resolved_service_id]
                + service.get("upstream_services", [])
                + service.get("downstream_services", [])
            )
        )

        for flow_id in impacted_flows:
            flow = self.data.flows_by_id.get(flow_id, {})
            impacted_services.extend(flow.get("services", []))
            impacted_events.extend(flow.get("events", []))
            impacted_apis.extend(flow.get("apis", []))

        impacted_services = sorted(set(impacted_services))
        impacted_events = sorted(set(impacted_events))
        impacted_apis = sorted(set(impacted_apis))

        runbooks = sorted(
            set(service.get("runbooks", []) + self._flow_linked_values(impacted_flows, "runbooks"))
        )
        tests = sorted(
            set(service.get("tests", []) + self._flow_linked_values(impacted_flows, "tests"))
        )
        incidents = sorted(
            set(
                service.get("related_incidents", [])
                + [
                    incident["id"]
                    for incident in self.data.incidents
                    if resolved_service_id in incident.get("services", [])
                    or set(impacted_flows).intersection(incident.get("flows", []))
                ]
            )
        )
        known_risks = list(service.get("risks", []))
        related_gaps = [
            gap
            for gap in self.data.test_gaps
            if set(impacted_services).intersection(gap.get("related_services", []))
        ]

        risk_level = self._risk_level(service, impacted_flows, impacted_events, impacted_services)
        summary = (
            f"{service['name']} is a {service.get('criticality')} service. A {change_type} change "
            f"may affect {len(impacted_flows)} flows, {len(impacted_services)} services, "
            f"{len(impacted_events)} events, and {len(impacted_apis)} APIs."
        )
        if description:
            summary = f"{summary} Description reviewed: {description}"

        return {
            "service": {
                "id": service["id"],
                "name": service["name"],
                "criticality": service.get("criticality"),
                "owned_by": service.get("owned_by"),
            },
            "change_type": change_type,
            "impacted_flows": impacted_flows,
            "impacted_services": impacted_services,
            "impacted_events": impacted_events,
            "impacted_apis": impacted_apis,
            "runbooks_to_review": runbooks,
            "tests_to_run": tests,
            "related_incidents": incidents,
            "known_risks": known_risks,
            "known_test_gaps": related_gaps,
            "documentation_updates": self._documentation_updates(service, impacted_flows),
            "operational_checks": self._operational_checks(service, runbooks),
            "rollback_considerations": self._rollback_considerations(change_type),
            "risk_level": risk_level,
            "summary": summary,
        }

    def _flow_linked_values(self, flow_ids: list[str], key: str) -> list[str]:
        values: list[str] = []
        for flow_id in flow_ids:
            values.extend(self.data.flows_by_id.get(flow_id, {}).get(key, []))
        return values

    def _risk_level(
        self,
        service: dict[str, Any],
        impacted_flows: list[str],
        impacted_events: list[str],
        impacted_services: list[str],
    ) -> str:
        criticality = str(service.get("criticality", "")).lower()
        if criticality in {"tier-0", "tier-1"}:
            return "high"
        if len(impacted_flows) >= 3 or len(impacted_events) >= 6 or len(impacted_services) >= 5:
            return "high"
        if len(impacted_flows) >= 1 or len(impacted_services) >= 3:
            return "medium"
        return "low"

    def _documentation_updates(self, service: dict[str, Any], flow_ids: list[str]) -> list[str]:
        return [
            f"Update service detail evidence for {service['name']} if APIs, events, risks, or ownership change.",
            "Update affected payment flow documentation: " + ", ".join(flow_ids),
            "Update onboarding resources if the change alters first-week learning or safe-contribution guidance.",
        ]

    def _operational_checks(self, service: dict[str, Any], runbooks: list[str]) -> list[str]:
        checks = [
            "Confirm production support can identify expected alerts, status changes, and recovery signals.",
            "Confirm monitoring covers impacted events and APIs before release.",
            "Confirm test evidence and approval notes are attached to the synthetic change record.",
        ]
        if runbooks:
            checks.insert(0, "Review runbooks: " + ", ".join(runbooks))
        if service.get("criticality") in {"tier-0", "tier-1"}:
            checks.append("Confirm tier-critical service communication plan and rollback owner.")
        return checks

    def _rollback_considerations(self, change_type: str) -> list[str]:
        return [
            f"Define rollback criteria for {change_type}.",
            "Keep the previous approved configuration or code path available until post-release checks pass.",
            "Validate rollback does not duplicate payment submission, replay, or status publication side effects.",
        ]
