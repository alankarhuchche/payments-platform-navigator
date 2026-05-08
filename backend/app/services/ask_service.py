"""Deterministic rule-based Ask the Platform implementation."""

from __future__ import annotations

from typing import Any

from ..data_loader import KnowledgeData, get_knowledge_data


class AskService:
    def __init__(self, data: KnowledgeData | None = None) -> None:
        self.data = data or get_knowledge_data()

    def answer(self, question: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        context = context or {}
        lowered = question.lower()
        matches = self.data.find_matching_entities(question)

        context_service_id = self.data.resolve_service_id(context.get("service_id"))
        context_flow_id = self.data.resolve_flow_id(context.get("flow_id"))
        if context_service_id and not any(
            item["id"] == context_service_id for item in matches["services"]
        ):
            matches["services"].append(self.data.services_by_id[context_service_id])
        if context_flow_id and not any(item["id"] == context_flow_id for item in matches["flows"]):
            matches["flows"].append(self.data.flows_by_id[context_flow_id])

        intent = self._detect_intent(lowered)
        source_files = set()
        relevant_services = [item["id"] for item in matches["services"]]
        relevant_flows = [item["id"] for item in matches["flows"]]
        relevant_runbooks: list[str] = []
        relevant_risks: list[dict[str, Any]] = []
        suggested_next_steps: list[str] = []

        for service in matches["services"]:
            source_files.add("services.yaml")
            relevant_flows.extend(service.get("supports_flows", []))
            relevant_runbooks.extend(service.get("runbooks", []))
            relevant_risks.extend(service.get("risks", []))
        for flow in matches["flows"]:
            source_files.add("payment-flows.yaml")
            relevant_services.extend(flow.get("services", []))
            relevant_runbooks.extend(flow.get("runbooks", []))

        if matches["glossary_terms"]:
            source_files.add("glossary.yaml")
        if "runbook" in intent or "incident" in intent:
            relevant_runbooks.extend(self._runbooks_from_keywords(lowered))
            source_files.add("runbooks.yaml")
            source_files.add("incidents.json")
        if "change_safety" == intent:
            source_files.update(["change-records.json", "test-coverage.json"])
            suggested_next_steps.append("Generate a change-safety checklist for the affected service.")

        relevant_services = sorted(set(relevant_services))
        relevant_flows = sorted(set(relevant_flows))
        relevant_runbooks = sorted(set(relevant_runbooks))

        confidence = self._confidence(matches, relevant_services, relevant_flows, intent)
        if confidence < 0.35:
            return {
                "answer_summary": "I do not have enough structured synthetic data to answer that confidently. I can help with services, payment flows, change safety, incidents, runbooks, glossary terms, and onboarding paths.",
                "matched_entities": self._matched_entities(matches),
                "relevant_services": [],
                "relevant_flows": [],
                "relevant_runbooks": [],
                "relevant_risks": [],
                "suggested_next_steps": [
                    "Try naming a service, flow, API, event, runbook, or glossary term from the synthetic dataset."
                ],
                "confidence": confidence,
                "source_files": [],
            }

        summary = self._summary(intent, matches, relevant_services, relevant_flows)
        if not suggested_next_steps:
            suggested_next_steps = self._next_steps(intent, relevant_services, relevant_flows)

        return {
            "answer_summary": summary,
            "matched_entities": self._matched_entities(matches),
            "relevant_services": relevant_services,
            "relevant_flows": relevant_flows,
            "relevant_runbooks": relevant_runbooks,
            "relevant_risks": relevant_risks,
            "suggested_next_steps": suggested_next_steps,
            "confidence": confidence,
            "source_files": sorted(source_files),
        }

    def _detect_intent(self, lowered: str) -> str:
        if any(term in lowered for term in ["change", "deploy", "check before", "checklist"]):
            return "change_safety"
        if any(term in lowered for term in ["incident", "runbook", "alert", "failure", "break"]):
            return "incident_runbook_help"
        if any(term in lowered for term in ["onboard", "learn", "role"]):
            return "onboarding_guidance"
        if any(term in lowered for term in ["what is", "define", "meaning"]):
            return "glossary_explanation"
        if "flow" in lowered or "pacs" in lowered:
            return "payment_flow_explanation"
        return "service_explanation"

    def _confidence(
        self,
        matches: dict[str, list[dict[str, Any]]],
        relevant_services: list[str],
        relevant_flows: list[str],
        intent: str,
    ) -> float:
        score = 0.15
        if matches["services"]:
            score += 0.35
        if matches["flows"]:
            score += 0.25
        if matches["apis"] or matches["events"] or matches["glossary_terms"]:
            score += 0.2
        if relevant_services or relevant_flows:
            score += 0.15
        if intent == "change_safety" and relevant_services:
            score += 0.1
        return min(round(score, 2), 0.95)

    def _summary(
        self,
        intent: str,
        matches: dict[str, list[dict[str, Any]]],
        relevant_services: list[str],
        relevant_flows: list[str],
    ) -> str:
        if intent == "change_safety" and matches["services"]:
            service = matches["services"][0]
            return (
                f"Before changing {service['name']}, review supported payment flows, "
                "upstream and downstream dependencies, API and event contracts, runbooks, "
                "related incidents, regression tests, rollback, monitoring, and production support communication."
            )
        if matches["flows"]:
            flow = matches["flows"][0]
            return (
                f"{flow['name']} is a {flow.get('direction')} {flow.get('message_type')} flow. "
                f"It involves {len(flow.get('services', []))} services and should be reviewed through its linked events, APIs, runbooks, tests, and risks."
            )
        if matches["services"]:
            service = matches["services"][0]
            return (
                f"{service['name']} is a {service.get('criticality')} {service.get('type')} in the {service.get('domain')} domain. "
                f"It supports {len(service.get('supports_flows', []))} payment flows and has {len(service.get('downstream_services', []))} downstream dependencies."
            )
        if matches["glossary_terms"]:
            term = matches["glossary_terms"][0]
            return f"{term['term']}: {term['definition']}"
        return (
            f"The structured data links {len(relevant_services)} services and {len(relevant_flows)} flows for this question."
        )

    def _next_steps(self, intent: str, services: list[str], flows: list[str]) -> list[str]:
        steps = []
        if services:
            steps.append(f"Open service detail for {services[0]}.")
        if flows:
            steps.append(f"Review payment flow detail for {flows[0]}.")
        if intent == "change_safety":
            steps.append("Run the change-safety checklist for the affected service.")
        steps.append("Review linked runbooks, incidents, and tests before making changes.")
        return steps

    def _runbooks_from_keywords(self, lowered: str) -> list[str]:
        matches = []
        for runbook in self.data.runbooks:
            searchable = " ".join(
                [
                    runbook.get("title", ""),
                    runbook.get("severity_guidance", ""),
                    " ".join(runbook.get("signals", [])),
                ]
            ).lower()
            if any(word in searchable for word in lowered.split()):
                matches.append(runbook["id"])
        return matches

    def _matched_entities(self, matches: dict[str, list[dict[str, Any]]]) -> dict[str, list[str]]:
        return {
            "services": [item["id"] for item in matches["services"]],
            "flows": [item["id"] for item in matches["flows"]],
            "events": [item["name"] for item in matches["events"]],
            "apis": [item["id"] for item in matches["apis"]],
            "glossary_terms": [item["term"] for item in matches["glossary_terms"]],
        }
