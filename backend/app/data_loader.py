"""Load and index the synthetic payments platform data files."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
import json
import re
from typing import Any

import yaml

from .config import get_settings


REQUIRED_DATA_FILES = [
    "services.yaml",
    "payment-flows.yaml",
    "event-catalogue.yaml",
    "api-catalogue.yaml",
    "runbooks.yaml",
    "incidents.json",
    "change-records.json",
    "test-coverage.json",
    "glossary.yaml",
    "onboarding-paths.yaml",
    "knowledge-health.json",
]


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


class DataLoadError(RuntimeError):
    """Raised when required synthetic data cannot be loaded."""


class KnowledgeData:
    def __init__(self, data_dir: Path | None = None) -> None:
        self.data_dir = data_dir or get_settings().data_dir
        self.files = self._load_required_files()
        self.services = self.files["services.yaml"].get("services", [])
        self.flows = self.files["payment-flows.yaml"].get("flows", [])
        self.events = self.files["event-catalogue.yaml"].get("events", [])
        self.apis = self.files["api-catalogue.yaml"].get("apis", [])
        self.runbooks = self.files["runbooks.yaml"].get("runbooks", [])
        self.incidents = self.files["incidents.json"].get("incidents", [])
        self.changes = self.files["change-records.json"].get("changes", [])
        self.tests = self.files["test-coverage.json"].get("tests", [])
        self.test_gaps = self.files["test-coverage.json"].get("gaps", [])
        self.glossary_terms = self.files["glossary.yaml"].get("terms", [])
        self.onboarding_paths = self.files["onboarding-paths.yaml"].get("paths", [])
        self.knowledge_health = self.files["knowledge-health.json"]

        self.services_by_id = {item["id"]: item for item in self.services}
        self.flows_by_id = {item["id"]: item for item in self.flows}
        self.events_by_name = {item["name"]: item for item in self.events}
        self.apis_by_id = {item["id"]: item for item in self.apis}
        self.runbooks_by_id = {item["id"]: item for item in self.runbooks}
        self.incidents_by_id = {item["id"]: item for item in self.incidents}
        self.changes_by_id = {item["id"]: item for item in self.changes}
        self.tests_by_id = {item["id"]: item for item in self.tests}
        self.glossary_by_term = {item["term"].lower(): item for item in self.glossary_terms}
        self.onboarding_by_role = {
            item["role"].lower(): item for item in self.onboarding_paths
        }
        self.service_health_by_service_id = {
            item["service_id"]: item
            for item in self.knowledge_health.get("service_health", [])
        }
        self.flow_health_by_flow_id = {
            item["flow_id"]: item for item in self.knowledge_health.get("flow_health", [])
        }

    def _load_required_files(self) -> dict[str, Any]:
        if not self.data_dir.exists():
            raise DataLoadError(f"Data directory does not exist: {self.data_dir}")

        loaded: dict[str, Any] = {}
        missing = [
            filename
            for filename in REQUIRED_DATA_FILES
            if not (self.data_dir / filename).is_file()
        ]
        if missing:
            raise DataLoadError(f"Missing required data files: {', '.join(missing)}")

        for filename in REQUIRED_DATA_FILES:
            path = self.data_dir / filename
            with path.open("r", encoding="utf-8") as handle:
                if filename.endswith(".yaml"):
                    loaded[filename] = yaml.safe_load(handle) or {}
                else:
                    loaded[filename] = json.load(handle)
        return loaded

    @property
    def data_files_loaded(self) -> list[str]:
        return list(REQUIRED_DATA_FILES)

    def resolve_service_id(self, value: str | None) -> str | None:
        if not value:
            return None
        candidate = value.strip()
        if candidate in self.services_by_id:
            return candidate
        candidate_slug = slugify(candidate)
        for service in self.services:
            if candidate_slug in {slugify(service["name"]), slugify(service["id"])}:
                return service["id"]
        return None

    def resolve_flow_id(self, value: str | None) -> str | None:
        if not value:
            return None
        candidate = value.strip()
        if candidate in self.flows_by_id:
            return candidate
        candidate_slug = slugify(candidate)
        for flow in self.flows:
            if candidate_slug in {slugify(flow["name"]), slugify(flow["id"])}:
                return flow["id"]
        return None

    def find_matching_entities(self, text: str) -> dict[str, list[dict[str, Any]]]:
        lowered = text.lower()
        service_matches = [
            service
            for service in self.services
            if service["id"].lower() in lowered or service["name"].lower() in lowered
        ]
        flow_matches = [
            flow
            for flow in self.flows
            if flow["id"].lower() in lowered
            or flow["name"].lower() in lowered
            or flow.get("message_type", "").lower() in lowered
        ]
        event_matches = [
            event for event in self.events if event["name"].lower() in lowered
        ]
        api_matches = [
            api
            for api in self.apis
            if api["id"].lower() in lowered or api["name"].lower() in lowered
        ]
        glossary_matches = [
            term for term in self.glossary_terms if term["term"].lower() in lowered
        ]
        return {
            "services": service_matches,
            "flows": flow_matches,
            "events": event_matches,
            "apis": api_matches,
            "glossary_terms": glossary_matches,
        }


@lru_cache
def get_knowledge_data() -> KnowledgeData:
    return KnowledgeData()
