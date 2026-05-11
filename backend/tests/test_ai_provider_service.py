"""Tests for AI provider abstraction (Phase 9C)."""

import pytest

from app.services.ai_provider_service import (
    AIProviderError,
    AIProviderUnavailable,
    AIProviderResult,
    NoopAIProvider,
)


class TestAIProviderResult:
    """Test the AIProviderResult data class."""

    def test_result_creation(self):
        """Test creating an AIProviderResult."""
        result = AIProviderResult(
            explanation="Test explanation",
            confidence=0.85,
            source_files=["services.yaml"],
            guardrail_notes="Test notes",
            mode="ai_assisted",
            provider_used="test-provider",
        )

        assert result.explanation == "Test explanation"
        assert result.confidence == 0.85
        assert result.source_files == ["services.yaml"]
        assert result.guardrail_notes == "Test notes"
        assert result.mode == "ai_assisted"
        assert result.provider_used == "test-provider"

    def test_result_defaults(self):
        """Test AIProviderResult with default values."""
        result = AIProviderResult(
            explanation="Test",
            confidence=0.5,
            source_files=[],
        )

        assert result.explanation == "Test"
        assert result.confidence == 0.5
        assert result.source_files == []
        assert result.guardrail_notes is None
        assert result.mode == "deterministic"
        assert result.provider_used == "none"


class TestNoopAIProvider:
    """Test the no-op AI provider."""

    def test_noop_provider_creation(self):
        """Test creating a noop provider."""
        provider = NoopAIProvider()
        assert provider.provider_name == "noop"

    def test_noop_explain_returns_disabled_response(self):
        """Test that noop provider returns a disabled response."""
        provider = NoopAIProvider()
        context_pack = {
            "question": "What are the payment flows?",
            "source_files": ["payment-flows.yaml"],
        }

        result = provider.explain(context_pack)

        assert result.explanation is not None
        assert "disabled" in result.explanation.lower()
        assert result.confidence == 0.0
        assert result.mode == "ai_disabled"
        assert result.provider_used == "noop"

    def test_noop_preserves_source_files(self):
        """Test that noop provider preserves source files from context pack."""
        provider = NoopAIProvider()
        source_files = ["services.yaml", "payment-flows.yaml", "incidents.json"]
        context_pack = {"source_files": source_files}

        result = provider.explain(context_pack)

        assert result.source_files == source_files

    def test_noop_handles_empty_source_files(self):
        """Test that noop provider handles missing source files gracefully."""
        provider = NoopAIProvider()
        context_pack = {}

        result = provider.explain(context_pack)

        assert result.source_files == []

    def test_noop_health_check_always_healthy(self):
        """Test that noop provider always reports healthy."""
        provider = NoopAIProvider()
        assert provider.health_check() is True

    def test_noop_does_not_call_external_services(self):
        """Test that noop provider never calls external services.

        This is guaranteed by the implementation—noop always returns
        a hardcoded response without I/O.
        """
        provider = NoopAIProvider()
        context_pack = {"question": "Any question"}

        result = provider.explain(context_pack)

        # Should return immediately without network calls
        assert result is not None
        assert isinstance(result, AIProviderResult)

    def test_noop_includes_guardrail_notes(self):
        """Test that noop provider includes guardrail notes."""
        provider = NoopAIProvider()
        context_pack = {}

        result = provider.explain(context_pack)

        assert result.guardrail_notes is not None
        assert "deterministic" in result.guardrail_notes.lower()
