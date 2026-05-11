"""Prompt builder for AI explanations (Phase 9D).

This module constructs strict prompts that ensure AI models answer only
from provided context packs without using general knowledge.

Design principle: Context-pack grounded, retrieval-only answers.
"""

from __future__ import annotations

from typing import Any


class AIPromptBuilder:
    """Builds strict prompts for AI models.

    Ensures:
    - AI answers only from provided context
    - No general knowledge or hallucination
    - Synthetic data boundary is clear
    - Senior, practical payments-engineering tone
    """

    SYSTEM_PROMPT = """\
You are a specialist payments-platform architect assistant.

You MUST:
1. Answer ONLY from the provided context pack
2. Refuse if context is insufficient
3. Never invent services, flows, controls, incidents, or API details
4. Never claim this represents a real bank or real payment system
5. Keep responses grounded in the synthetic payments-platform data provided
6. Use clear, senior, practical payments-engineering language
7. Structure responses as valid JSON if feasible

You MUST NOT:
- Use general knowledge about payments systems, banks, or fintech
- Answer about real banks or real payment systems
- Invent missing details
- Speculate beyond the context provided
- Reference real confidential data or real incidents

Context pack: Structured synthetic data assembled by deterministic backend retrieval.
Your role: Explain this synthetic data clearly and practically.
"""

    @staticmethod
    def build_explanation_prompt(
        context_pack: dict[str, Any],
        question: str,
    ) -> str:
        """Build a prompt for explaining a context pack.

        Args:
            context_pack: Structured context from context-pack builder
            question: The original user question

        Returns:
            A strict prompt template for the AI model
        """
        return f"""\
System: {AIPromptBuilder.SYSTEM_PROMPT}

User Question:
{question}

Context Pack (synthetic data only):
{AIPromptBuilder._format_context_pack(context_pack)}

Task:
1. Explain the context pack in response to the user's question
2. Provide structured output with:
   - answer_summary: 1-2 sentence summary
   - detailed_explanation: practical explanation grounded in context
   - key_entities: services, flows, and other relevant entities from context
   - suggested_next_steps: 2-3 actionable next steps based on context
   - confidence: float 0.0-1.0 based on context completeness
   - guardrail_notes: any limitations or disclaimers

If context is insufficient:
- Say "Insufficient context to answer this question."
- Suggest what additional data would help
- Do not invent details

IMPORTANT: All answers are about the SYNTHETIC payments-platform data model.
This is NOT real bank architecture or real payment systems.
"""

    @staticmethod
    def _format_context_pack(context_pack: dict[str, Any]) -> str:
        """Format context pack into readable prompt text.

        Args:
            context_pack: Structured context from context-pack builder

        Returns:
            Formatted context string
        """
        lines = []

        if context_pack.get("question"):
            lines.append(f"Question: {context_pack['question']}")

        if context_pack.get("detected_intent"):
            lines.append(f"Intent: {context_pack['detected_intent']}")

        if context_pack.get("confidence"):
            lines.append(f"Context Confidence: {context_pack['confidence']:.2f}")

        if context_pack.get("matched_entities"):
            entities = context_pack["matched_entities"]
            if entities.get("services"):
                lines.append(f"Services: {', '.join(entities['services'])}")
            if entities.get("flows"):
                lines.append(f"Flows: {', '.join(entities['flows'])}")
            if entities.get("apis"):
                lines.append(f"APIs: {', '.join(entities['apis'])}")
            if entities.get("glossary_terms"):
                lines.append(f"Glossary: {', '.join(entities['glossary_terms'])}")

        if context_pack.get("relevant_services"):
            lines.append(
                f"Available Services: {', '.join(context_pack['relevant_services'][:5])}"
            )

        if context_pack.get("relevant_flows"):
            lines.append(
                f"Available Flows: {', '.join(context_pack['relevant_flows'][:5])}"
            )

        if context_pack.get("relevant_runbooks"):
            lines.append(
                f"Runbooks: {', '.join(context_pack['relevant_runbooks'][:3])}"
            )

        if context_pack.get("relevant_incidents"):
            lines.append(
                f"Incidents: {', '.join(context_pack['relevant_incidents'][:3])}"
            )

        if context_pack.get("relevant_risks"):
            risks = context_pack["relevant_risks"][:3]
            risk_summaries = [
                f"{r.get('id', 'unknown')}: {r.get('title', 'unknown')}" for r in risks
            ]
            lines.append(f"Risks: {'; '.join(risk_summaries)}")

        if context_pack.get("suggested_next_steps"):
            lines.append(
                f"Next Steps: {'; '.join(context_pack['suggested_next_steps'][:3])}"
            )

        if context_pack.get("source_files"):
            lines.append(f"Source: {', '.join(context_pack['source_files'])}")

        if context_pack.get("unsupported_reason"):
            lines.append(f"Limitation: {context_pack['unsupported_reason']}")

        return "\n".join(lines)
