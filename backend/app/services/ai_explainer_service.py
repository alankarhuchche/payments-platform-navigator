"""AI explainer service that coordinates AI provider usage.

This service handles the selection and use of AI providers.
It checks configuration and selects the appropriate provider
(noop when disabled, real provider when enabled).

Design: All AI calls go through this service, so providers can be
swapped without changing application logic.
"""

from __future__ import annotations

from typing import Any

from ..config import get_settings
from .ai_provider_service import (
    AIProviderResult,
    AIProviderUnavailable,
    NoopAIProvider,
    VertexGeminiProvider,
)


class AIExplainerService:
    """Service for generating AI-assisted explanations.

    This service:
    - Checks if AI is enabled
    - Selects the appropriate provider
    - Generates explanations via the provider
    - Handles errors gracefully
    """

    def __init__(self) -> None:
        self.settings = get_settings()
        self.provider = self._select_provider()

    def _select_provider(self):
        """Select the appropriate AI provider based on configuration.

        Returns:
            An AI provider implementation (noop if disabled)
        """
        if not self.settings.enable_ai_explanations:
            return NoopAIProvider()

        if self.settings.ai_provider == "none" or not self.settings.ai_provider:
            return NoopAIProvider()

        if self.settings.ai_provider == "vertex-gemini":
            return VertexGeminiProvider(
                model_name=self.settings.ai_model or "gemini-2.5-flash"
            )

        # If AI is enabled but provider is unknown, use noop
        return NoopAIProvider()

    def is_available(self) -> bool:
        """Check if AI explanations are available and healthy.

        Returns:
            True if AI provider is available and configured, False otherwise
        """
        return (
            self.settings.enable_ai_explanations
            and self.settings.ai_provider != "none"
            and self.provider.health_check()
        )

    def explain(self, context_pack: dict[str, Any]) -> AIProviderResult:
        """Generate an AI-assisted explanation for a context pack.

        This method coordinates with the selected provider to generate
        an explanation. It gracefully handles provider failures.

        Args:
            context_pack: Structured context from context-pack builder

        Returns:
            AIProviderResult with explanation and metadata
        """
        try:
            result = self.provider.explain(context_pack)
            return result
        except Exception as e:
            # If anything goes wrong, fall back to disabled response
            return AIProviderResult(
                explanation=(
                    "AI explanations are temporarily unavailable due to a service error. "
                    "Using deterministic answer based on platform data."
                ),
                confidence=0.0,
                source_files=context_pack.get("source_files", []),
                guardrail_notes=f"AI service error: {str(e)[:100]}",
                mode="ai_disabled",
                provider_used="error_fallback",
            )

    def get_provider_status(self) -> dict[str, Any]:
        """Get the current AI provider status for health checks.

        Returns:
            Dict with provider status information
        """
        return {
            "enabled": self.settings.enable_ai_explanations,
            "provider": self.settings.ai_provider,
            "model": self.settings.ai_model if self.settings.ai_model != "none" else None,
            "available": self.is_available(),
            "health": self.provider.health_check(),
        }
