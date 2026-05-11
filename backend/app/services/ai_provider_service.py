"""AI provider abstraction layer for Phase 9C.

This module defines the interface and implementations for AI providers.
Providers handle the interface to external AI models (Gemini, OpenAI, etc).
The abstraction allows multiple providers to be implemented without
changing the rest of the application.

Design principle: Deterministic backend + context-pack is source of truth.
AI providers are optional explainers added on top.
"""

from __future__ import annotations

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
