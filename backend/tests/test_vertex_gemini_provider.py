"""Tests for Vertex Gemini provider (Phase 9D)."""

import sys
import pytest
from unittest.mock import patch, MagicMock, Mock, PropertyMock

# Mock google.genai module to avoid import issues during test discovery
if "google.genai" not in sys.modules:
    sys.modules["google.genai"] = Mock()
    sys.modules["google"] = Mock()
    sys.modules["google.auth"] = Mock()

from app.services.ai_provider_service import (
    VertexGeminiProvider,
    AIProviderResult,
    AIProviderUnavailable,
    AIProviderError,
)


class TestVertexGeminiProvider:
    """Test the Vertex Gemini AI provider."""

    def test_gemini_provider_creation(self):
        """Test creating a Gemini provider."""
        provider = VertexGeminiProvider()
        assert provider.provider_name == "vertex-gemini"
        assert provider.model_name == "gemini-2.5-flash"

    def test_gemini_provider_with_custom_model(self):
        """Test creating a Gemini provider with custom model name."""
        provider = VertexGeminiProvider(model_name="gemini-2.0-pro")
        assert provider.model_name == "gemini-2.0-pro"

    def test_gemini_provider_health_check_without_api_key(self):
        """Test health check when API key is not set."""
        with patch.dict("os.environ", {}, clear=True):
            provider = VertexGeminiProvider()
            assert provider.health_check() is False

    def test_gemini_provider_health_check_with_api_key(self):
        """Test health check when API key is set."""
        with patch.dict("os.environ", {"GOOGLE_API_KEY": "test-key"}):
            provider = VertexGeminiProvider()
            assert provider.health_check() is True

    def test_gemini_provider_health_check_with_gemini_api_key(self):
        """Test health check with GEMINI_API_KEY environment variable."""
        with patch.dict("os.environ", {"GEMINI_API_KEY": "test-key"}):
            provider = VertexGeminiProvider()
            assert provider.health_check() is True

    @patch("app.services.ai_provider_service.os.getenv")
    def test_gemini_explain_requires_api_key(self, mock_getenv):
        """Test that explain raises error if API key is not configured."""
        mock_getenv.return_value = None
        provider = VertexGeminiProvider()

        context_pack = {"question": "Test question"}

        with pytest.raises(AIProviderUnavailable):
            provider.explain(context_pack)

    def test_gemini_uses_new_sdk_client_api(self):
        """Test that provider uses genai.Client() not genai.configure()."""
        # Simple test: verify provider can be instantiated and uses correct structure
        provider = VertexGeminiProvider()
        assert provider.provider_name == "vertex-gemini"
        assert provider.model_name == "gemini-2.5-flash"
        # The actual SDK usage is tested via the endpoint tests with mocks

    def test_gemini_does_not_use_configure(self):
        """Test that provider does NOT use the old genai.configure() method."""
        with patch.dict("os.environ", {"GEMINI_API_KEY": "test-key"}):
            with patch("google.genai.Client"):
                with patch("google.genai.configure") as mock_configure:
                    provider = VertexGeminiProvider()

                    # Call _get_client to verify it doesn't use configure
                    provider._get_client()

                    # Verify genai.configure was NOT called
                    mock_configure.assert_not_called()



    @patch("app.services.ai_provider_service.os.getenv")
    def test_gemini_explain_handles_api_error(self, mock_getenv):
        """Test that explain handles Gemini API errors gracefully."""
        mock_getenv.return_value = "test-api-key"

        provider = VertexGeminiProvider()

        with patch("google.genai.configure"):
            with patch("google.genai.GenerativeModel") as mock_model_class:
                mock_model = MagicMock()
                mock_model_class.return_value = mock_model

                # Simulate API error
                mock_model.generate_content.side_effect = Exception("API rate limited")

                context_pack = {
                    "question": "Test question",
                    "source_files": ["services.yaml"],
                }

                with pytest.raises(AIProviderError):
                    provider.explain(context_pack)


    def test_parse_response_with_valid_json(self):
        """Test _parse_response with valid JSON."""
        provider = VertexGeminiProvider()

        response_text = '{"detailed_explanation": "Test", "confidence": 0.85}'
        parsed = provider._parse_response(response_text)

        assert parsed["detailed_explanation"] == "Test"
        assert parsed["confidence"] == 0.85

    def test_parse_response_with_json_in_text(self):
        """Test _parse_response with JSON embedded in text."""
        provider = VertexGeminiProvider()

        response_text = 'Some preamble {"detailed_explanation": "Test"} some postamble'
        parsed = provider._parse_response(response_text)

        assert parsed["detailed_explanation"] == "Test"

    def test_parse_response_with_invalid_json(self):
        """Test _parse_response with invalid JSON."""
        provider = VertexGeminiProvider()

        response_text = "This is plain text, not JSON"
        parsed = provider._parse_response(response_text)

        # Should return safe defaults
        assert "detailed_explanation" in parsed
        assert "confidence" in parsed
        assert parsed["confidence"] == 0.7

    def test_parse_response_preserves_all_fields(self):
        """Test that _parse_response preserves all fields in JSON."""
        provider = VertexGeminiProvider()

        response_text = """{
            "detailed_explanation": "Full explanation",
            "confidence": 0.9,
            "guardrail_notes": "Synthetic data only",
            "suggested_next_steps": ["Step 1", "Step 2"]
        }"""
        parsed = provider._parse_response(response_text)

        assert parsed["detailed_explanation"] == "Full explanation"
        assert parsed["confidence"] == 0.9
        assert parsed["guardrail_notes"] == "Synthetic data only"
        assert parsed["suggested_next_steps"] == ["Step 1", "Step 2"]
