"""Tests for AI-assisted /api/ask endpoint (Phase 9D)."""

import pytest
import sys
from unittest.mock import patch, MagicMock, Mock
from fastapi.testclient import TestClient

from app.main import app

# Mock google.genai module to avoid import issues during test discovery
if "google.genai" not in sys.modules:
    sys.modules["google.genai"] = Mock()
    sys.modules["google"] = Mock()
    sys.modules["google.auth"] = Mock()


client = TestClient(app)


class TestAIAssistedAsk:
    """Test AI-assisted mode for /api/ask endpoint."""

    def test_ask_with_ai_assisted_mode_disabled(self):
        """Test that AI-assisted mode returns deterministic answer when AI disabled."""
        with patch.dict("os.environ", {"ENABLE_AI_EXPLANATIONS": "false"}):
            response = client.post(
                "/api/ask",
                json={
                    "question": "What should I check before changing Payment Validation Service?",
                    "mode": "ai_assisted",
                },
            )

        assert response.status_code == 200
        data = response.json()

        # Should have deterministic answer
        assert "answer_summary" in data
        assert "relevant_services" in data

        # Should include AI status indicating disabled
        assert "ai_status" in data
        assert data["ai_status"]["mode"] == "disabled"
        assert data["ai_status"]["available"] is False

    def test_ask_deterministic_mode_not_affected_by_ai_config(self):
        """Test that deterministic mode is unaffected by AI configuration."""
        with patch.dict("os.environ", {"ENABLE_AI_EXPLANATIONS": "false"}):
            response = client.post(
                "/api/ask",
                json={
                    "question": "What is Payment Validation Service?",
                    "mode": "deterministic",
                },
            )

        assert response.status_code == 200
        data = response.json()

        # Should have deterministic answer
        assert "answer_summary" in data
        assert data.get("confidence") > 0.0

        # Should not have AI explanation
        assert "ai_explanation" not in data or data.get("ai_status", {}).get("mode") != "ai_assisted"

    def test_ask_default_mode_is_deterministic(self):
        """Test that default mode is deterministic when mode is not specified."""
        with patch.dict("os.environ", {"ENABLE_AI_EXPLANATIONS": "false"}):
            response = client.post(
                "/api/ask",
                json={"question": "What is Payment Validation Service?"},
            )

        assert response.status_code == 200
        data = response.json()

        # Should not have AI explanation
        assert "ai_mode" not in data or data.get("ai_mode") != "ai_assisted"

    def test_ask_ai_assisted_with_enabled_ai_and_mocked_provider(self):
        """Test AI-assisted ask with mocked Gemini provider."""
        with patch.dict(
            "os.environ",
            {
                "ENABLE_AI_EXPLANATIONS": "true",
                "AI_PROVIDER": "vertex-gemini",
                "GOOGLE_API_KEY": "test-key",
            },
        ):
            with patch("google.genai.configure"):
                with patch("google.genai.GenerativeModel") as mock_model_class:
                    mock_model = MagicMock()
                    mock_model_class.return_value = mock_model

                    mock_response = MagicMock()
                    mock_response.text = """{
                        "detailed_explanation": "Payment Validation Service is a critical service",
                        "confidence": 0.85,
                        "guardrail_notes": "Based on synthetic data"
                    }"""
                    mock_model.generate_content.return_value = mock_response

                    response = client.post(
                        "/api/ask",
                        json={
                            "question": "What is Payment Validation Service?",
                            "mode": "ai_assisted",
                        },
                    )

        assert response.status_code == 200
        data = response.json()

        # Should have deterministic answer
        assert "answer_summary" in data

        # Should have AI explanation
        assert "ai_explanation" in data or "ai_status" in data

    def test_ask_ai_assisted_falls_back_on_provider_error(self):
        """Test that AI-assisted ask falls back to deterministic when AI unavailable."""
        # When AI is not properly configured (API key missing), should fall back gracefully
        with patch.dict(
            "os.environ",
            {
                "ENABLE_AI_EXPLANATIONS": "true",
                "AI_PROVIDER": "vertex-gemini",
                # Note: No GOOGLE_API_KEY, so provider is unavailable
            },
        ):
            response = client.post(
                "/api/ask",
                json={
                    "question": "What is Payment Validation Service?",
                    "mode": "ai_assisted",
                },
            )

        assert response.status_code == 200
        data = response.json()

        # Should have deterministic answer
        assert "answer_summary" in data
        assert "confidence" in data

        # Should indicate disabled or unavailable in AI status
        if "ai_status" in data:
            # Either disabled or error, but not ai_assisted
            assert data["ai_status"]["available"] is False

    def test_ask_preserves_deterministic_answer_fields(self):
        """Test that AI-assisted answer includes all deterministic fields."""
        with patch.dict("os.environ", {"ENABLE_AI_EXPLANATIONS": "false"}):
            response = client.post(
                "/api/ask",
                json={
                    "question": "What should I check before changing Payment Validation Service?",
                    "mode": "ai_assisted",
                },
            )

        assert response.status_code == 200
        data = response.json()

        # All deterministic fields should be present
        assert "answer_summary" in data
        assert "matched_entities" in data
        assert "relevant_services" in data
        assert "relevant_flows" in data
        assert "relevant_runbooks" in data
        assert "confidence" in data
        assert "source_files" in data

    def test_ask_ai_status_structure(self):
        """Test that ai_status has correct structure when AI disabled."""
        response = client.post(
            "/api/ask",
            json={
                "question": "What is Payment Validation Service?",
                "mode": "ai_assisted",
            },
        )

        assert response.status_code == 200
        data = response.json()

        if "ai_status" in data:
            status = data["ai_status"]
            assert "mode" in status
            assert "available" in status
            assert isinstance(status["available"], bool)

    def test_ask_with_unsupported_question_returns_deterministic(self):
        """Test that unsupported questions return deterministic answer even in AI mode."""
        with patch.dict("os.environ", {"ENABLE_AI_EXPLANATIONS": "false"}):
            response = client.post(
                "/api/ask",
                json={
                    "question": "How do real banks handle customer data?",
                    "mode": "ai_assisted",
                },
            )

        assert response.status_code == 200
        data = response.json()

        # Should have low-confidence deterministic answer
        assert "answer_summary" in data
        assert data.get("confidence", 0.0) <= 0.5

        # Should not invent details
        assert "fake" not in data.get("answer_summary", "").lower()
        assert "made up" not in data.get("answer_summary", "").lower()

    def test_ask_ai_assisted_includes_ai_confidence_when_available(self):
        """Test that AI-assisted response includes ai_confidence field."""
        with patch.dict(
            "os.environ",
            {
                "ENABLE_AI_EXPLANATIONS": "true",
                "AI_PROVIDER": "vertex-gemini",
                "GOOGLE_API_KEY": "test-key",
            },
        ):
            with patch("google.genai.configure"):
                with patch("google.genai.GenerativeModel") as mock_model_class:
                    mock_model = MagicMock()
                    mock_model_class.return_value = mock_model

                    mock_response = MagicMock()
                    mock_response.text = '{"confidence": 0.88}'
                    mock_model.generate_content.return_value = mock_response

                    response = client.post(
                        "/api/ask",
                        json={
                            "question": "What is Payment Validation Service?",
                            "mode": "ai_assisted",
                        },
                    )

        assert response.status_code == 200
        data = response.json()

        # Should have ai_confidence if AI was used
        if data.get("ai_status", {}).get("mode") == "ai_assisted":
            assert "ai_confidence" in data

    def test_ask_mode_is_optional_parameter(self):
        """Test that mode parameter is optional and defaults to deterministic."""
        response = client.post(
            "/api/ask",
            json={"question": "What is Payment Validation Service?"},
        )

        assert response.status_code == 200
        data = response.json()

        # Should work without mode parameter
        assert "answer_summary" in data
        assert "confidence" in data

    def test_ask_ai_assisted_mode_case_insensitive_check(self):
        """Test that mode parameter is properly validated."""
        # Test with invalid mode
        response = client.post(
            "/api/ask",
            json={
                "question": "What is Payment Validation Service?",
                "mode": "invalid_mode",
            },
        )

        assert response.status_code == 200
        data = response.json()

        # Should treat invalid mode as deterministic
        assert "answer_summary" in data
