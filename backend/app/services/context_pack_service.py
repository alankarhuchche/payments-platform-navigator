"""Context-pack builder for AI-assisted explanations."""

from __future__ import annotations

from typing import Any

from ..data_loader import KnowledgeData, get_knowledge_data


class ContextPackBuilder:
    """Builds structured context packs from user questions."""

    def __init__(self, data: KnowledgeData | None = None) -> None:
        self.data = data or get_knowledge_data()

    def build(
        self,
        question: str,
        service_id: str | None = None,
        flow_id: str | None = None,
    ) -> dict[str, Any]:
        """Build a context pack for a question.

        Returns a structured dict containing:
        - question
        - detected_intent
        - matched_entities
        - relevant_services
        - relevant_flows
        - relevant_events
        - relevant_apis
        - relevant_runbooks
        - relevant_incidents
        - relevant_tests
        - relevant_risks
        - suggested_next_steps
        - source_files
        - confidence
        - unsupported_reason (if applicable)
        """
        lowered = question.lower()

        # Check for unsupported questions (real bank, real data)
        unsupported_reason = self._check_unsupported(question)
        if unsupported_reason:
            return {
                "question": question,
                "detected_intent": "unsupported",
                "matched_entities": {},
                "relevant_services": [],
                "relevant_flows": [],
                "relevant_events": [],
                "relevant_apis": [],
                "relevant_runbooks": [],
                "relevant_incidents": [],
                "relevant_tests": [],
                "relevant_risks": [],
                "suggested_next_steps": ["This question is outside the scope of this synthetic platform."],
                "source_files": [],
                "confidence": 0.0,
                "unsupported_reason": unsupported_reason,
            }

        # Find matching entities
        matches = self.data.find_matching_entities(question)

        # Add context entities if provided
        context_service_id = self.data.resolve_service_id(service_id)
        context_flow_id = self.data.resolve_flow_id(flow_id)

        if context_service_id and not any(
            item["id"] == context_service_id for item in matches["services"]
        ):
            matches["services"].append(self.data.services_by_id[context_service_id])
        if context_flow_id and not any(item["id"] == context_flow_id for item in matches["flows"]):
            matches["flows"].append(self.data.flows_by_id[context_flow_id])

        # Detect intent
        intent = self._detect_intent(lowered)

        # Collect source files and linked entities
        source_files = set()
        relevant_services = [item["id"] for item in matches["services"]]
        relevant_flows = [item["id"] for item in matches["flows"]]
        relevant_events = [item["name"] for item in matches["events"]]
        relevant_apis = [item["id"] for item in matches["apis"]]
        relevant_runbooks: list[str] = []
        relevant_incidents: list[str] = []
        relevant_tests: list[str] = []
        relevant_risks: list[dict[str, Any]] = []

        # Collect from matched services
        for service in matches["services"]:
            source_files.add("services.yaml")
            relevant_flows.extend(service.get("supports_flows", []))
            relevant_runbooks.extend(service.get("runbooks", []))
            relevant_risks.extend(service.get("risks", []))
            # Find incidents related to this service
            for incident in self.data.incidents:
                if service["id"] in incident.get("related_services", []):
                    relevant_incidents.append(incident["id"])
            # Find tests related to this service
            for test in self.data.tests:
                if service["id"] in test.get("services_tested", []):
                    relevant_tests.append(test["id"])

        # Collect from matched flows
        for flow in matches["flows"]:
            source_files.add("payment-flows.yaml")
            relevant_services.extend(flow.get("services", []))
            relevant_runbooks.extend(flow.get("runbooks", []))
            relevant_events.extend(flow.get("events", []))
            relevant_apis.extend(flow.get("apis", []))
            # Find incidents related to this flow
            for incident in self.data.incidents:
                if flow["id"] in incident.get("related_flows", []):
                    relevant_incidents.append(incident["id"])
            # Find tests related to this flow
            for test in self.data.tests:
                if flow["id"] in test.get("flows_tested", []):
                    relevant_tests.append(test["id"])

        if matches["glossary_terms"]:
            source_files.add("glossary.yaml")

        if "runbook" in intent or "incident" in intent:
            relevant_runbooks.extend(self._runbooks_from_keywords(lowered))
            source_files.add("runbooks.yaml")
            source_files.add("incidents.json")

        if "change_safety" == intent:
            source_files.update(["change-records.json", "test-coverage.json"])

        # Deduplicate and sort
        relevant_services = sorted(set(relevant_services))
        relevant_flows = sorted(set(relevant_flows))
        relevant_events = sorted(set(relevant_events))
        relevant_apis = sorted(set(relevant_apis))
        relevant_runbooks = sorted(set(relevant_runbooks))
        relevant_incidents = sorted(set(relevant_incidents))
        relevant_tests = sorted(set(relevant_tests))

        # Calculate confidence
        confidence = self._confidence(
            matches, relevant_services, relevant_flows, intent
        )

        # Generate suggested next steps
        suggested_next_steps = self._next_steps(
            intent, relevant_services, relevant_flows, relevant_runbooks
        )

        return {
            "question": question,
            "detected_intent": intent,
            "matched_entities": self._matched_entities(matches),
            "relevant_services": relevant_services,
            "relevant_flows": relevant_flows,
            "relevant_events": relevant_events,
            "relevant_apis": relevant_apis,
            "relevant_runbooks": relevant_runbooks,
            "relevant_incidents": relevant_incidents,
            "relevant_tests": relevant_tests,
            "relevant_risks": relevant_risks,
            "suggested_next_steps": suggested_next_steps,
            "source_files": sorted(source_files),
            "confidence": confidence,
        }

    def _check_unsupported(self, question: str) -> str | None:
        """Check if question is unsupported (real bank, real data, etc.)."""
        lowered = question.lower()

        # Real bank questions
        if any(
            term in lowered
            for term in [
                "real bank",
                "actual bank",
                "production system",
                "live system",
                "real payment",
                "actual payment",
                "customer data",
                "real customer",
                "actual customer",
                "real incident",
                "actual incident",
                "real money",
                "real transaction",
            ]
        ):
            return "This question is about real banking systems or real data. This platform uses synthetic data only."

        return None

    def _detect_intent(self, lowered: str) -> str:
        """Detect the user's intent from the question."""
        if any(term in lowered for term in ["change", "deploy", "check before", "checklist"]):
            return "change_safety"
        if any(term in lowered for term in ["incident", "runbook", "alert", "failure", "break"]):
            return "incident_or_runbook_help"
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
        """Calculate confidence in the context pack."""
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

    def _runbooks_from_keywords(self, lowered: str) -> list[str]:
        """Find runbooks matching keywords in the question."""
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
        """Extract matched entity IDs from matches."""
        return {
            "services": [item["id"] for item in matches["services"]],
            "flows": [item["id"] for item in matches["flows"]],
            "events": [item["name"] for item in matches["events"]],
            "apis": [item["id"] for item in matches["apis"]],
            "glossary_terms": [item["term"] for item in matches["glossary_terms"]],
        }

    def _next_steps(
        self,
        intent: str,
        services: list[str],
        flows: list[str],
        runbooks: list[str],
    ) -> list[str]:
        """Generate suggested next steps based on the context pack."""
        steps = []
        if services:
            steps.append(f"Open service detail for {services[0]}.")
        if flows:
            steps.append(f"Review payment flow detail for {flows[0]}.")
        if intent == "change_safety":
            if services:
                steps.append(f"Run the change-safety checklist for {services[0]}.")
        if runbooks:
            steps.append(f"Review relevant runbooks: {', '.join(runbooks[:3])}.")
        if not steps:
            steps.append("Try searching for a different service, flow, or concept.")
        return steps
