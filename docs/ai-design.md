# AI-Assisted Explanation Design

## 1. AI Enhancement Objective

The Payments Platform Navigator currently answers user questions through deterministic, rule-based logic applied to synthetic structured data. This design document outlines an optional AI-assisted enhancement that would allow the system to generate contextual explanations and answer open-ended platform questions using a grounded AI explainer, while preserving the existing deterministic architecture as the source of truth.

The goal is not to turn the product into a chatbot. The goal is to provide an optional, explainer-augmented experience that helps engineers understand *why* certain guidance applies to their platform questions, sourced entirely from the structured knowledge already in the system.

---

## 2. What AI Is and Is Not Allowed to Do

### Allowed

- Generate explanations and prose descriptions grounded in structured data.
- Rephrase technical concepts in multiple styles (detailed, executive, practical).
- Answer "why" and "how" questions if the context data contains the answer.
- Generate examples from the synthetic glossary, runbooks, and incident records.
- Suggest related services, flows, or runbooks based on platform context.
- Surface unresolved questions or edge cases back to the user for clarification.
- Refusal: explicitly decline to answer questions outside the synthetic platform scope.

### Not Allowed

- Make up services, flows, APIs, events, or incidents not in the data model.
- Answer questions about real banks, payment systems, or financial infrastructure.
- Claim to understand real operational behaviour that is not explicitly in the structured data.
- Bypass the deterministic backend or suggest guidance not grounded in source data.
- Handle real customer data, real incidents, or real payment information.
- Operate in stateful conversation mode where prior responses become implicit context.
- Generate documentation claims that should instead update the source YAML/JSON files.
- Override the change-safety checklist or other deterministic outputs with AI opinion.

---

## 3. Why Deterministic Retrieval Remains the Source of Truth

The deterministic backend will continue to be the authoritative source for all platform intelligence:

- **Change-safety checklist**: Generated deterministically from service links, flow dependencies, test records, and incident patterns. No AI rewriting.
- **Onboarding paths**: Rule-based on role and experience level. No AI substitution.
- **Service dependencies**: Explicitly defined in `services.yaml`. AI only contextualizes.
- **Payment flows**: Authoritative in `payment-flows.yaml`. AI only narrates.
- **Operational risks**: Sourced from `incidents.json`, `knowledge-health.json`, and linked runbooks. AI only explains.

The AI layer is an *explanation and exploration helper*, not a replacement for the deterministic architecture. Users making critical decisions (change approval, incident diagnosis, production operations) rely on structured data, not AI opinion.

---

## 4. Target User Journeys for AI-Assisted Explanation

### Journey A: "Why" Questions on Deterministic Output

User runs the change-safety checklist for Payment Validation Service.

The UI shows:
- Deterministic checklist (as today)
- Optional "Explain why this step matters" button

User clicks the button. The AI generates a 2-3 paragraph explanation grounding the step in:
- Which services are actually impacted
- Which payment flows could be affected
- Which prior incidents inform this requirement
- Practical actions the user should take

Result: User understands not just *what* to check, but *why* it matters to their platform.

---

### Journey B: Open-Ended Platform Questions

User asks: "What happens when a SWIFT connector timeout occurs in an outbound pacs.008 transfer?"

The system:
1. Searches the glossary, flows, services, incidents for relevant context.
2. Retrieves the outbound SWIFT flow definition, the SWIFT Connector service, related incidents, and applicable runbooks.
3. Passes this context to the AI explainer with a grounded prompt.
4. AI generates a structured answer explaining: the flow step where timeout occurs, which services are affected, what state change happens, which runbook applies, what a support engineer should do.
5. All claims are cited back to source data.

Result: User gets a platform-specific answer, not generic internet knowledge.

---

### Journey C: Glossary Context and Examples

User looks up "sanctions screening" in the glossary.

The UI shows:
- Glossary definition (as today)
- Optional "Show platform examples" button

User clicks the button. The AI generates:
- Which services perform sanctions screening in this platform
- Which flows include sanctions screening
- Which payment types trigger screening
- Which incidents involved screening decisions
- What a new engineer should understand about screening risk

Result: User understands the glossary term in the context of their specific platform.

---

### Journey D: Onboarding Path Exploration

A new test engineer receives an onboarding path generated by the rule-based system.

The UI shows:
- Role-based learning path (as today)
- Optional "Explain this phase" button for each section

User clicks the button. The AI generates:
- Why this particular flow is important to understand before others
- Which services will become clear after learning this flow
- Which test scenarios they should expect to write
- Common misconceptions to avoid

Result: User understands the *learning architecture*, not just a reading list.

---

## 5. AI-Assisted Ask-the-Platform Flow

Today's Ask the Platform is deterministic (pattern matching on the question, retrieving structured answers).

Optional enhancement:

1. **User enters question** (e.g., "What should I check before changing the routing logic?")

2. **Deterministic phase**: Backend identifies question intent, retrieves structured context (related services, flows, incidents, tests, runbooks).

3. **Context-pack assembly**: System builds a structured context package with:
   - Query intent classification
   - Retrieved service/flow/incident IDs
   - Relevant YAML snippets
   - Linked runbook excerpts
   - Test coverage records
   - Architecture metadata

4. **AI explanation phase** (if enabled and answer not directly available):
   - AI receives context-pack + grounded prompt
   - AI generates structured explanation
   - AI cites every claim back to source data ID

5. **User receives answer**:
   - Answer text with inline citations
   - Links to source data items
   - "View this in deterministic checklist" option
   - "Refined by: Production-ready AI" badge

The deterministic system is the *decision authority*. The AI is the *explainer*.

---

## 6. Context-Pack Architecture

A context-pack is a structured data container that holds all the information an AI explainer needs to answer a question *without hallucinating*.

### Context-Pack Structure

```json
{
  "query": {
    "text": "What should I check before changing the routing logic?",
    "intent": "change_impact_assessment",
    "classification": "routing_service_change"
  },
  "metadata": {
    "generated_at": "2026-05-10T14:30:00Z",
    "expires_at": "2026-05-10T15:00:00Z",
    "source_version": "main-2026-05-10",
    "source_hashes": {
      "services.yaml": "abc123...",
      "payment-flows.yaml": "def456...",
      "incidents.json": "ghi789..."
    }
  },
  "retrieved_entities": {
    "services": [
      {
        "id": "routing-decision-service",
        "name": "Routing Decision Service",
        "excerpt": "...",
        "risk_level": "critical",
        "related_incidents_count": 3
      }
    ],
    "flows": [
      {
        "id": "outbound_pacs008_customer",
        "name": "Outbound SWIFT pacs.008 Customer Credit Transfer",
        "uses_routing": true,
        "excerpt": "..."
      }
    ],
    "incidents": [
      {
        "id": "INC-2024-0042",
        "title": "Routing timeout during surge",
        "excerpt": "...",
        "service": "routing-decision-service"
      }
    ],
    "runbooks": [
      {
        "id": "RB-ROUTING-TIMEOUT",
        "title": "Routing Timeout - Incident Response",
        "excerpt": "...",
        "relevance": "high"
      }
    ],
    "tests": [
      {
        "id": "TEST-ROUTING-FAILOVER",
        "title": "Routing failover under load",
        "coverage": "critical",
        "excerpt": "..."
      }
    ]
  },
  "constraints": {
    "no_external_sources": true,
    "synthetic_data_only": true,
    "must_cite": true,
    "max_hallucination_risk": "low"
  }
}
```

### Context-Pack Assembly Rules

- Include only entities directly relevant to the query intent.
- Include enough detail that the AI can answer without making assumptions.
- Include source IDs and versions so all claims can be verified.
- Include retrieval confidence scores where applicable.
- Expire context-packs if underlying data changes.
- Mark unresolved references (e.g., missing linked incident).

---

## 7. Proposed Backend Components

### 7.1 AI Configuration Service

**Responsibility**: Manage AI provider credentials, feature flags, and capability settings.

**Files/Modules**:
- `backend/app/ai_config.py`

**Interface**:
- Load AI provider settings from environment variables (disabled by default).
- Feature flags for: enable AI explanations, enable Ask-the-Platform AI augmentation, max AI response length, citation requirements.
- Provider selection: Vertex AI (Google Cloud) by default if enabled, OpenAI as optional fallback.
- Circuit breaker: if AI service fails, fall back to deterministic-only mode.

---

### 7.2 Context-Pack Builder

**Responsibility**: Assemble context-packs from structured data.

**Files/Modules**:
- `backend/app/context_builder.py`

**Interface**:
- `build_context_pack(query_intent: str, entity_ids: list, scope: str) -> dict`
- Retrieves entities from the data loader.
- Includes relevant excerpts, related records, and metadata.
- Adds source hashes and version info.
- Sets expiration and constraint markers.

---

### 7.3 AI Explainer Service

**Responsibility**: Call the AI provider with a grounded prompt and context-pack.

**Files/Modules**:
- `backend/app/ai_explainer.py`

**Interface**:
- `explain(context_pack: dict, prompt_template: str, style: str) -> ExplanationResult`
- Takes a context-pack and a prompt template.
- Calls the configured AI provider.
- Returns structured explanation with citations and confidence.
- Times out and falls back if AI service is slow or unavailable.

**Internal Methods**:
- `extract_citations(ai_response: str, context_pack: dict) -> list[Citation]`
- `validate_hallucination_risk(response: str, context_pack: dict) -> bool`

---

### 7.4 Explanation Endpoints

**Responsibility**: Expose AI explanation capabilities through the API.

**Files/Modules**:
- `backend/app/routers/explanations.py`

**Proposed Endpoints**:

```
POST /api/explanations/change-safety-detail
  Input: service_id, change_type
  Output: explanation of why each checklist item matters, grounded in incidents and flows

GET /api/explanations/glossary/{term}
  Input: term
  Output: glossary definition + platform examples from flows, services, incidents

POST /api/ask-the-platform/augmented
  Input: question, intent
  Output: deterministic answer + AI-generated explanation and context

POST /api/explanations/onboarding-phase
  Input: role, phase_number
  Output: explanation of why this phase is important
```

All endpoints:
- Return AI capability status (enabled/disabled).
- Include citation IDs.
- Include response generation time and provider.
- Gracefully degrade to deterministic-only if AI is disabled or fails.

---

## 8. Proposed Frontend Changes

### 8.1 Explanation UI Pattern

Add an optional "Explain" or "Why?" button next to deterministic outputs:

- Change-safety checklist: "Explain why this step matters" → generates AI explanation for that step
- Glossary entries: "Show platform examples" → retrieves AI-augmented examples
- Onboarding paths: "Why this phase?" → explains learning architecture
- Ask results: "Elaborate" → generates deeper AI explanation

Design approach:
- Explanations appear in a side panel or collapsible section (non-intrusive).
- Always show the deterministic result first.
- Make AI explanations clearly labeled and differentiated from core guidance.
- Include "Powered by Vertex AI" or equivalent provider attribution.

### 8.2 Citation Display

When AI explanation is shown, include inline citations:

```
The routing change will impact 3 critical flows:
  - Outbound SWIFT pacs.008 transfers [flow-001]
  - Inbound status updates [flow-002]
  - Exception investigations [flow-004]

All three flows were involved in incident INC-2024-0042 [incident link].
```

Users can click cited entities to navigate to deterministic details.

### 8.3 Disabled/Degraded Behavior

If AI is disabled:
- No "Explain" buttons appear.
- Ask the Platform works deterministically only.
- No user-facing AI attribution.

If AI is available but slow:
- Show "Loading explanation..." state.
- Allow user to skip waiting.
- Gracefully show deterministic answer while fetching explanation.

---

## 9. Provider Strategy

### Default: No AI Provider Required

The application works fully without any AI provider. This is the MVP production default.

### When AI is Enabled

Priority order:

1. **Vertex AI (Google Cloud)**: Preferred for public Google Cloud deployments.
   - Uses `google.cloud.aiplatform`
   - Minimal additional infrastructure.
   - Data privacy aligned with Cloud Run hosting.

2. **OpenAI API**: Optional fallback.
   - For teams already using OpenAI.
   - Requires separate API key management.
   - Consider data residency implications.

### No Other Providers

- No local LLM models (complexity and maintenance burden).
- No proprietary in-house models (out of scope for a public reference implementation).
- No embedding services for now (future enhancement if RAG complexity increases).

### Provider Selection Logic

```python
if AI_ENABLED:
  if VERTEX_AI_PROJECT_ID:
    use Vertex AI
  elif OPENAI_API_KEY:
    use OpenAI
  else:
    disable AI, warn in logs
```

---

## 10. Environment Variables

### Feature Flags

```
# AI feature enablement (default: false)
AI_ENABLED=false

# AI explanation max length in tokens (default: 500)
AI_EXPLANATION_MAX_TOKENS=500

# Require citations for all AI claims (default: true)
AI_REQUIRE_CITATIONS=true

# AI response timeout in seconds (default: 5)
AI_RESPONSE_TIMEOUT_SECONDS=5
```

### Vertex AI Configuration

```
# Google Cloud project ID (if using Vertex AI)
VERTEX_AI_PROJECT_ID=<gcp-project>

# Vertex AI location (default: us-central1)
VERTEX_AI_LOCATION=us-central1

# Vertex AI model (default: gemini-1.5-pro)
VERTEX_AI_MODEL=gemini-1.5-pro
```

### OpenAI Configuration (Optional)

```
# OpenAI API key (if using OpenAI as fallback)
OPENAI_API_KEY=<key>

# OpenAI model (default: gpt-4-turbo)
OPENAI_MODEL=gpt-4-turbo
```

### Logging and Observability

```
# Log all AI requests and responses (default: false)
AI_VERBOSE_LOGGING=false

# Require minimum confidence score for AI responses (default: 0.8)
AI_MIN_CONFIDENCE=0.8
```

---

## 11. Secret Handling Principles

### Credential Storage

- **Development**: Environment variables in `.env` (Git-ignored).
- **Cloud Run**: Use Google Cloud Secret Manager. Cloud Run injects via environment binding.
- **Secrets** must never be hardcoded or logged.

### Audit Trail

- Every AI API call should be logged with:
  - Timestamp
  - User context (if available)
  - Query intent
  - Response generation time
  - Provider used
  - Confidence score

- Audit logs must be retained for at least 90 days.
- Do not log the full AI response if it contains sensitive inference (unlikely given synthetic data).

### Data Residency

- If using Vertex AI on Google Cloud, data stays within Google Cloud.
- If using OpenAI, data is sent to OpenAI's infrastructure (different data residency).
- Clearly document this difference in deployment guides.

---

## 12. Local Development Behavior

### Default (AI Disabled)

```bash
cd payments-platform-navigator
python backend/app/main.py
```

Application runs with full deterministic functionality, no AI dependencies.

### With Vertex AI Emulator (Future)

```bash
export AI_ENABLED=true
export VERTEX_AI_PROJECT_ID=local-testing
python backend/app/main.py
```

Backend attempts to use Vertex AI. If unavailable, logs warning and falls back to deterministic-only.

### Testing

```bash
# Unit tests must not require AI
pytest backend/tests/test_backend.py

# Integration tests can mock AI responses
pytest backend/tests/test_explanations.py --mock-ai
```

---

## 13. Cloud Run Deployment Behavior

### Startup

1. Cloud Run injects `PORT` (default 8080).
2. Backend loads synthetic data files.
3. Backend reads `AI_ENABLED` flag.
4. If AI enabled, reads `VERTEX_AI_PROJECT_ID` from Secret Manager binding.
5. Initializes Vertex AI client (or logs warning if credentials unavailable).
6. FastAPI starts on `0.0.0.0:${PORT}`.

### Health Check

`GET /health` returns:

```json
{
  "status": "ok",
  "timestamp": "2026-05-10T14:30:00Z",
  "ai": {
    "enabled": true,
    "provider": "vertex-ai",
    "available": true
  }
}
```

Users and monitoring systems can detect whether AI is available at deployment time.

### Rollback

If an AI provider becomes unavailable:
- Explanation endpoints return 503 Service Unavailable (AI not available).
- Deterministic endpoints continue to work.
- Monitoring alert triggers.
- No user-facing impact to core functionality.

---

## 14. Evaluation Strategy

### Before Publishing Explanations

Each AI-generated explanation must be evaluated for:

1. **Hallucination Risk**: Does every claim come from the context-pack?
2. **Relevance**: Does the explanation actually answer the user's question?
3. **Completeness**: Are critical related concepts missing?
4. **Citation Accuracy**: Do all inline citations link to real source data?
5. **Tone**: Does the explanation match payments-engineering professionalism?

### Evaluation Process

```
User requests explanation
  ↓
Backend generates explanation with citations
  ↓
Frontend displays explanation
  ↓
User provides feedback: "Was this helpful? Accurate? Complete?"
  ↓
Feedback collected (if telemetry enabled)
  ↓
Weekly review of low-confidence or questioned explanations
  ↓
If pattern emerges: refine prompt or update source data
```

### Feedback Mechanisms

- "Helpful / Not helpful" button on each explanation.
- "Report hallucination" link for incorrect claims.
- Backend logs which explanations receive negative feedback.
- Weekly report on explanation quality metrics.

### Data Quality Checks

If AI suggests a missing or unclear concept:
- Instead of hallucinating, AI says: "The data I have doesn't cover this. You might want to consult [relevant runbook]."
- Log suggestion as potential data model gap.
- Evaluate whether source YAML/JSON should be updated to cover the gap.

---

## 15. Rollout Plan

### Phase 1: Documentation and Design Review

- Publish this document.
- Gather feedback from stakeholders.
- Review for security and data-safety implications.
- No code changes.

### Phase 2: Backend Infrastructure (If Approved)

- Implement context-pack builder.
- Implement AI config service.
- Implement AI explainer service with mock provider.
- Add explanation endpoints (returning mock AI responses).
- Full test coverage of context-pack assembly.
- No real AI calls yet. No frontend changes.

### Phase 3: Provider Integration (If Approved)

- Integrate Vertex AI client.
- Add OpenAI client as optional fallback.
- Update health checks.
- Test with real AI provider in development/staging.
- Real AI responses appear in logs, not UI.
- Documentation updated.

### Phase 4: Frontend Integration (If Approved)

- Add "Explain" buttons to UI.
- Add explanation side panels.
- Test citation display.
- User testing with small cohort.
- Collect feedback on explanation quality.

### Phase 5: Production Rollout (If Approved)

- Deploy to Cloud Run with AI disabled by default.
- Monitor health checks and error logs.
- Gradually enable AI for subset of users.
- Collect feedback over 2 weeks.
- If quality is good: enable for all users.
- If quality is poor: disable, refine prompts, re-evaluate.

### Abort Criteria

At any phase:
- Explanation quality drops below 80% accuracy.
- AI hallucinations are frequent (>5% of explanations).
- Response latency exceeds 3 seconds (poor user experience).
- AI costs exceed forecast.
- Security concerns arise.

If abort triggered:
- Disable AI immediately.
- Users revert to deterministic-only (no user impact).
- Investigate root cause.
- Return to deterministic architecture.

---

## 16. Success Metrics

### Quality Metrics

- Explanation accuracy: >95% (evaluated on sample set).
- Citation accuracy: 100% (all claims traceable to source data).
- Hallucination rate: <1% (AI making false claims about platform).
- User satisfaction: >4/5 on "Was this helpful?" rating.

### Performance Metrics

- Explanation generation time: <2 seconds p95.
- Explanation API availability: >99.5%.
- Fallback to deterministic-only: <1% of requests.

### Adoption Metrics

- % of users who view explanations: >30%.
- Repeat users who use explanations: >50%.
- Negative feedback rate: <5%.

### Business Metrics

- User satisfaction with Ask the Platform (with explanation): >4/5.
- Time-to-answer for complex questions: reduced by >30%.
- Engagement with onboarding paths: increased.
- Churn rate for new engineers: stable or improved.

---

## 17. Future Enhancements (Out of Scope)

These are intentionally not part of the initial AI design:

- **Stateful conversation**: Multi-turn dialogue where context persists across questions.
- **RAG at scale**: Retrieval-augmented generation against external documentation corpus.
- **Custom fine-tuning**: Training AI on historical Q&A from this specific platform.
- **Interactive debugging**: AI helping engineer diagnose a live incident.
- **Autonomous change approval**: AI suggesting or approving changes (human stays in control).
- **Real-time operational dashboards**: AI analyzing live logs and metrics (requires live data connection).

These require significant additional architecture and safety measures.

---

## Summary

This design preserves the deterministic, structured, payment-engineering-focused core of Payments Platform Navigator while adding an optional, grounded AI-explanation layer. The AI is a *helper and explainer*, not a decision-maker. All core guidance remains sourced from deterministic logic applied to synthetic structured data.

The design is cautious: AI is disabled by default, providers are optional, fallback to deterministic-only is automatic, and evaluation gates any expansion beyond explanations.
