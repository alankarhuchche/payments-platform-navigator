"""AI provider abstraction layer for Phase 9C.

This module defines the interface and implementations for AI providers.
Providers handle the interface to external AI models (Gemini, OpenAI, etc).
The abstraction allows multiple providers to be implemented without
changing the rest of the application.

Design principle: Deterministic backend + context-pack is source of truth.
AI providers are optional explainers added on top.
"""

from __future__ import annotations

import json
import os
from typing import Any, Protocol
from dataclasses import dataclass


class AIProviderError(Exception):
    """Base exception for AI provider errors."""


class AIProviderUnavailable(AIProviderError):
    """Raised when the configured AI provider is not available."""


@dataclass
class AIProviderResult:
    """Result from an AI provider call."""

    explanation: str
    """The generated explanation from the AI model."""

    confidence: float
    """Confidence score for the explanation (0.0-1.0)."""

    source_files: list[str]
    """Source files that informed the explanation."""

    guardrail_notes: str | None = None
    """Optional notes about guardrails applied."""

    mode: str = "deterministic"
    """Mode used: 'deterministic', 'ai_assisted', 'ai_disabled'."""

    provider_used: str = "none"
    """Which provider generated this result."""


class BaseAIProvider(Protocol):
    """Protocol for AI provider implementations.

    All AI providers must implement this interface to be used by
    the AI explainer service.
    """

    def explain(self, context_pack: dict[str, Any]) -> AIProviderResult:
        """Generate an explanation for a context pack.

        Args:
            context_pack: Structured context from context-pack builder

        Returns:
            AIProviderResult with explanation and metadata
        """
        ...

    def health_check(self) -> bool:
        """Check if the provider is healthy and available.

        Returns:
            True if provider is available, False otherwise
        """
        ...


class NoopAIProvider:
    """No-op AI provider when AI is disabled.

    Returns a safe response indicating that AI-assisted explanations
    are not available for this deployment.
    """

    def __init__(self) -> None:
        self.provider_name = "noop"

    def explain(self, context_pack: dict[str, Any]) -> AIProviderResult:
        """Return a disabled response without calling external services."""
        return AIProviderResult(
            explanation=(
                "AI-assisted explanations are disabled for this deployment. "
                "This platform uses deterministic rule-based answers grounded in synthetic data. "
                "Enable AI explanations by setting ENABLE_AI_EXPLANATIONS=true and configuring an AI provider."
            ),
            confidence=0.0,
            source_files=context_pack.get("source_files", []),
            guardrail_notes="AI explanations are disabled. Using deterministic answer only.",
            mode="ai_disabled",
            provider_used="noop",
        )

    def health_check(self) -> bool:
        """Noop provider is always healthy."""
        return True


class VertexGeminiProvider:
    """Vertex AI Gemini provider for AI-assisted explanations (Phase 9D).

    Uses Google Generative AI SDK to send context packs to Gemini
    with strict prompting to prevent hallucination and general-knowledge leakage.
    """

    def __init__(self, model_name: str = "gemini-2.5-flash") -> None:
        """Initialize the Vertex Gemini provider.

        Args:
            model_name: Gemini model to use (default: gemini-2.5-flash)
        """
        self.provider_name = "vertex-gemini"
        self.model_name = model_name
        self._client = None
        self._model = None

    def _get_client(self):
        """Lazy-load the Gemini client using new google-genai SDK.

        The new SDK automatically picks up GEMINI_API_KEY or GOOGLE_API_KEY
        from environment variables.
        """
        if self._client is None:
            try:
                from google import genai

                # Check if API key is available before creating client
                api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
                if not api_key:
                    raise AIProviderUnavailable(
                        "GOOGLE_API_KEY or GEMINI_API_KEY environment variable not set"
                    )

                # SDK automatically uses GEMINI_API_KEY or GOOGLE_API_KEY env vars
                self._client = genai.Client()
            except AIProviderUnavailable:
                raise
            except ImportError:
                raise AIProviderUnavailable(
                    "google-genai package not installed. Install with: pip install google-genai"
                )
        return self._client

    def explain(self, context_pack: dict[str, Any]) -> AIProviderResult:
        """Generate an AI-assisted explanation using Vertex Gemini.

        Uses the new google-genai SDK with client.models.generate_content().

        Args:
            context_pack: Structured context from context-pack builder

        Returns:
            AIProviderResult with AI-assisted explanation
        """
        try:
            from .ai_prompt_service import AIPromptBuilder

            question = context_pack.get("question", "")
            prompt = AIPromptBuilder.build_explanation_prompt(context_pack, question)

            client = self._get_client()
            response = client.models.generate_content(
                model=self.model_name,
                contents=prompt,
            )

            explanation = response.text if response else ""

            # Try to extract JSON if model returns JSON
            parsed_response = self._parse_response(explanation)

            return AIProviderResult(
                explanation=parsed_response.get(
                    "detailed_explanation", explanation[:500]
                ),
                confidence=min(
                    parsed_response.get("confidence", 0.7),
                    context_pack.get("confidence", 0.7),
                ),
                source_files=context_pack.get("source_files", []),
                guardrail_notes=(
                    "AI-assisted explanation grounded in synthetic context-pack only. "
                    + parsed_response.get("guardrail_notes", "")
                ),
                mode="ai_assisted",
                provider_used="vertex-gemini",
            )
        except AIProviderUnavailable:
            raise
        except Exception as e:
            raise AIProviderError(f"Gemini provider error: {str(e)}")

    def _parse_response(self, response_text: str) -> dict[str, Any]:
        """Parse Gemini response, attempting JSON extraction.

        Args:
            response_text: Raw response text from Gemini

        Returns:
            Dict with parsed response or safe defaults
        """
        try:
            # Try to find and parse JSON in response
            start = response_text.find("{")
            end = response_text.rfind("}") + 1
            if start >= 0 and end > start:
                json_str = response_text[start:end]
                return json.loads(json_str)
        except (json.JSONDecodeError, ValueError):
            pass

        # Fallback: return safe defaults
        return {
            "detailed_explanation": response_text[:500],
            "confidence": 0.7,
            "guardrail_notes": "Response parsed as plain text (not JSON)",
        }

    def health_check(self) -> bool:
        """Check if the Gemini provider is available.

        Returns:
            True if provider can be initialized, False otherwise
        """
        try:
            api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
            return api_key is not None
        except Exception:
            return False
