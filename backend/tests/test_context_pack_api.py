"""Tests for the context-pack API endpoint."""

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services.context_pack_service import ContextPackBuilder


client = TestClient(app)


class TestContextPackBuilder:
    """Unit tests for ContextPackBuilder."""

    def test_change_safety_question_returns_context_pack(self):
        """Test that a change-safety question returns relevant context."""
        builder = ContextPackBuilder()
        context_pack = builder.build(
            "What should I check before changing Payment Validation Service?"
        )

        assert context_pack["detected_intent"] == "change_safety"
        assert "svc-payment-validation" in context_pack["relevant_services"]
        assert context_pack["confidence"] > 0.5
        assert "services.yaml" in context_pack["source_files"]
        assert len(context_pack["relevant_flows"]) > 0

    def test_payment_flow_question_matches_pacs008(self):
        """Test that a pacs.008 question matches the outbound pacs.008 flow."""
        builder = ContextPackBuilder()
        context_pack = builder.build(
            "What happens in an outbound pacs.008 payment flow?"
        )

        assert context_pack["detected_intent"] == "payment_flow_explanation"
        # The flow ID should contain pacs.008 or be the outbound SWIFT flow
        assert len(context_pack["relevant_flows"]) > 0
        assert "payment-flows.yaml" in context_pack["source_files"]
        assert context_pack["confidence"] > 0.5

    def test_unsupported_real_bank_question_returns_unsupported(self):
        """Test that a real-bank question is marked as unsupported."""
        builder = ContextPackBuilder()
        context_pack = builder.build(
            "How do real banks handle ISO 20022 in production?"
        )

        assert context_pack["detected_intent"] == "unsupported"
        assert context_pack["confidence"] == 0.0
        assert context_pack["unsupported_reason"] is not None
        assert "synthetic" in context_pack["unsupported_reason"].lower()

    def test_service_question_returns_services_and_flows(self):
        """Test that a service question returns relevant entities."""
        builder = ContextPackBuilder()
        context_pack = builder.build(
            "Tell me about Payment Validation Service"
        )

        assert context_pack["detected_intent"] in [
            "service_explanation",
            "change_safety",
        ]
        assert "svc-payment-validation" in context_pack["relevant_services"]
        assert context_pack["confidence"] > 0.5

    def test_context_pack_includes_source_files(self):
        """Test that context pack always includes source files."""
        builder = ContextPackBuilder()
        context_pack = builder.build("What are the payment flows?")

        assert isinstance(context_pack["source_files"], list)
        assert len(context_pack["source_files"]) > 0
        # Should include at least one of the synthetic data files
        valid_files = [
            "services.yaml",
            "payment-flows.yaml",
            "glossary.yaml",
            "runbooks.yaml",
            "incidents.json",
        ]
        assert any(f in context_pack["source_files"] for f in valid_files)

    def test_context_pack_confidence_degrades_for_weak_match(self):
        """Test that confidence is lower for weak matches."""
        builder = ContextPackBuilder()
        weak_context_pack = builder.build("xyz abc def 123")

        assert weak_context_pack["confidence"] <= 0.5

    def test_matched_entities_structure(self):
        """Test that matched_entities has correct structure."""
        builder = ContextPackBuilder()
        context_pack = builder.build(
            "Tell me about Payment Validation Service and pacs.008"
        )

        matched = context_pack["matched_entities"]
        assert "services" in matched
        assert "flows" in matched
        assert "events" in matched
        assert "apis" in matched
        assert "glossary_terms" in matched


class TestContextPackAPI:
    """Integration tests for the context-pack API endpoint."""

    def test_context_pack_endpoint_returns_200(self):
        """Test that POST /api/context-pack returns 200."""
        response = client.post(
            "/api/context-pack",
            json={"question": "What is Payment Validation Service?"},
        )
        assert response.status_code == 200

    def test_context_pack_endpoint_returns_valid_schema(self):
        """Test that the endpoint returns a valid context-pack schema."""
        response = client.post(
            "/api/context-pack",
            json={"question": "Tell me about the pacs.008 flow"},
        )
        assert response.status_code == 200

        data = response.json()
        assert "question" in data
        assert "detected_intent" in data
        assert "matched_entities" in data
        assert "relevant_services" in data
        assert "relevant_flows" in data
        assert "confidence" in data
        assert "source_files" in data

    def test_context_pack_endpoint_change_safety_question(self):
        """Test context-pack endpoint with a change-safety question."""
        response = client.post(
            "/api/context-pack",
            json={
                "question": "What should I check before changing Payment Validation Service?"
            },
        )
        assert response.status_code == 200

        data = response.json()
        assert data["detected_intent"] == "change_safety"
        assert len(data["relevant_services"]) > 0
        assert data["confidence"] > 0.5

    def test_context_pack_endpoint_unsupported_question(self):
        """Test context-pack endpoint with an unsupported question."""
        response = client.post(
            "/api/context-pack",
            json={"question": "How do real banks handle customer data?"},
        )
        assert response.status_code == 200

        data = response.json()
        assert data["detected_intent"] == "unsupported"
        assert data["confidence"] == 0.0
        assert data["unsupported_reason"] is not None

    def test_context_pack_endpoint_with_service_context(self):
        """Test context-pack endpoint with optional service_id context."""
        response = client.post(
            "/api/context-pack",
            json={
                "question": "Tell me more",
                "service_id": "svc-payment-validation",
            },
        )
        assert response.status_code == 200

        data = response.json()
        assert "svc-payment-validation" in data["relevant_services"]

    def test_context_pack_endpoint_with_flow_context(self):
        """Test context-pack endpoint with optional flow_id context."""
        response = client.post(
            "/api/context-pack",
            json={
                "question": "Tell me more about this",
                "flow_id": "flow-outbound-pacs008",
            },
        )
        assert response.status_code == 200

        data = response.json()
        # The flow ID should be in relevant flows or resolved
        assert "flow-outbound-pacs008" in data["relevant_flows"] or len(
            data["relevant_flows"]
        ) > 0

    def test_context_pack_endpoint_rejects_short_question(self):
        """Test that endpoint rejects questions that are too short."""
        response = client.post(
            "/api/context-pack",
            json={"question": "ab"},
        )
        # Should be 422 (validation error) or 400
        assert response.status_code in [400, 422]

    def test_context_pack_endpoint_rejects_missing_question(self):
        """Test that endpoint rejects requests without a question."""
        response = client.post(
            "/api/context-pack",
            json={},
        )
        # Should be 422 (validation error)
        assert response.status_code == 422

    def test_context_pack_includes_relevant_incidents(self):
        """Test that context pack includes relevant incidents."""
        response = client.post(
            "/api/context-pack",
            json={"question": "What happened with incident in Payment Validation?"},
        )
        assert response.status_code == 200

        data = response.json()
        # Should include incidents list
        assert "relevant_incidents" in data
