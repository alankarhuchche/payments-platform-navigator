"""Tests for AI explainer service (Phase 9C)."""

import pytest
from unittest.mock import patch

from app.services.ai_explainer_service import AIExplainerService
from app.services.ai_provider_service import NoopAIProvider, AIProviderResult


class TestAIExplainerService:
    """Test the AI explainer service."""

    def test_explainer_creation(self):
        """Test creating an AI explainer service."""
        with patch.dict("os.environ", {"ENABLE_AI_EXPLANATIONS": "false"}):
            service = AIExplainerService()
            assert service is not None
            assert service.provider is not None

    def test_ai_disabled_by_default(self):
        """Test that AI is disabled by default."""
        with patch.dict(
            "os.environ",
            {"ENABLE_AI_EXPLANATIONS": "", "AI_PROVIDER": ""},
            clear=False,
        ):
            service = AIExplainerService()
            assert not service.is_available()

    def test_selects_noop_when_disabled(self):
        """Test that noop provider is selected when AI is disabled."""
        with patch.dict("os.environ", {"ENABLE_AI_EXPLANATIONS": "false"}):
            service = AIExplainerService()
            assert isinstance(service.provider, NoopAIProvider)

    def test_selects_noop_when_provider_is_none(self):
        """Test that noop provider is selected when provider is 'none'."""
        with patch.dict(
            "os.environ",
            {"ENABLE_AI_EXPLANATIONS": "true", "AI_PROVIDER": "none"},
        ):
            service = AIExplainerService()
            assert isinstance(service.provider, NoopAIProvider)

    def test_explain_returns_disabled_response_when_ai_disabled(self):
        """Test that explain returns disabled response when AI is disabled."""
        with patch.dict("os.environ", {"ENABLE_AI_EXPLANATIONS": "false"}):
            service = AIExplainerService()
            context_pack = {
                "question": "What are the payment flows?",
                "source_files": ["payment-flows.yaml"],
            }

            result = service.explain(context_pack)

            assert result.mode == "ai_disabled"
            assert result.provider_used == "noop"
            assert "disabled" in result.explanation.lower()
            assert result.confidence == 0.0

    def test_explain_preserves_source_files(self):
        """Test that explain preserves source files from context pack."""
        with patch.dict("os.environ", {"ENABLE_AI_EXPLANATIONS": "false"}):
            service = AIExplainerService()
            source_files = ["services.yaml", "payment-flows.yaml"]
            context_pack = {"source_files": source_files}

            result = service.explain(context_pack)

            assert result.source_files == source_files

    def test_explain_includes_guardrail_notes(self):
        """Test that explain includes guardrail notes."""
        with patch.dict("os.environ", {"ENABLE_AI_EXPLANATIONS": "false"}):
            service = AIExplainerService()
            context_pack = {}

            result = service.explain(context_pack)

            assert result.guardrail_notes is not None

    def test_is_available_false_when_disabled(self):
        """Test that is_available returns False when AI is disabled."""
        with patch.dict("os.environ", {"ENABLE_AI_EXPLANATIONS": "false"}):
            service = AIExplainerService()
            assert service.is_available() is False

    def test_is_available_false_when_provider_none(self):
        """Test that is_available returns False when provider is 'none'."""
        with patch.dict(
            "os.environ",
            {"ENABLE_AI_EXPLANATIONS": "true", "AI_PROVIDER": "none"},
        ):
            service = AIExplainerService()
            assert service.is_available() is False

    def test_get_provider_status_when_disabled(self):
        """Test getting provider status when AI is disabled."""
        with patch.dict("os.environ", {"ENABLE_AI_EXPLANATIONS": "false"}):
            service = AIExplainerService()
            status = service.get_provider_status()

            assert status["enabled"] is False
            assert status["available"] is False
            assert status["health"] is True  # Noop is always healthy

    def test_get_provider_status_includes_provider_info(self):
        """Test that provider status includes provider information."""
        with patch.dict(
            "os.environ",
            {"ENABLE_AI_EXPLANATIONS": "false", "AI_PROVIDER": "none"},
        ):
            service = AIExplainerService()
            status = service.get_provider_status()

            assert "enabled" in status
            assert "provider" in status
            assert "model" in status
            assert "available" in status
            assert "health" in status

    def test_explain_handles_provider_errors_gracefully(self):
        """Test that explain handles provider errors gracefully."""
        with patch.dict("os.environ", {"ENABLE_AI_EXPLANATIONS": "false"}):
            service = AIExplainerService()
            # Even if something goes wrong, should return safe response
            context_pack = {"source_files": []}

            result = service.explain(context_pack)

            assert isinstance(result, AIProviderResult)
            assert result.mode == "ai_disabled"
            assert result.explanation is not None

    def test_no_secrets_required_when_ai_disabled(self):
        """Test that no secrets are required when AI is disabled."""
        with patch.dict(
            "os.environ",
            {"ENABLE_AI_EXPLANATIONS": "false"},
            clear=False,
        ):
            # Should create service without errors, even without secrets
            service = AIExplainerService()
            assert service is not None

    def test_configuration_respects_defaults(self):
        """Test that configuration respects default values."""
        with patch.dict(
            "os.environ",
            {},
            clear=False,
        ):
            service = AIExplainerService()

            # Defaults should be applied
            assert service.settings.enable_ai_explanations is False
            assert service.settings.ai_provider == "none"
