# AI-Assisted Explanation Design

## 1. Executive Summary

Payments Platform Navigator is a deterministic, retrieval-based assistant for complex payments platform knowledge. This document proposes an optional AI-assisted explanation layer that enhances the user experience by generating contextual explanations grounded in retrieved synthetic data.

The core principle is simple: **retrieval first, AI for explanation only**. The deterministic backend remains the source of truth. The AI layer is optional, disabled by default, and designed to help engineers understand *why* platform guidance matters—not to replace structured knowledge with unsupported opinions.

This is not a chatbot enhancement. It is a targeted explanation tool for engineers navigating complex payment architecture using a synthetic knowledge base.

---

## 2. Design Principles

The AI-assisted explanation layer is built on these non-negotiable principles:

### Retrieval First
The deterministic backend retrieves entities (services, flows, incidents, runbooks, tests) from the synthetic knowledge base before any AI is involved. AI never discovers or searches independently. AI only explains what has already been retrieved.

### Deterministic Context as Source of Truth
The change-safety checklist, onboarding paths, and Ask-the-Platform answers are deterministically generated from the data model. AI explanations augment these answers but never override them. Users making critical decisions rely on deterministic outputs, not AI opinion.

### AI Disabled by Default
The application runs fully without any AI provider. Environment variable `ENABLE_AI_EXPLANATIONS=false` is the default. Cloud Run deployments work without Secret Manager AI credentials. Developers can build, test, and understand the system without AI complexity.

### Source-Aware Answers
Every explanation cites the synthetic data it references (service ID, flow ID, incident ID, runbook ID). No explanation is shown without traceable sources. If the context-pack doesn't cover a question, AI declines to answer.

### No Unsupported Claims
AI does not invent facts, extend beyond the context-pack, or claim knowledge about real banks. If a question asks about real payment systems, real regulations, or real bank architecture, AI refuses clearly.

### No Real-Bank Inference
AI never uses internet knowledge, Wikipedia, banking textbooks, or external sources as evidence. The only source of truth is the synthetic data provided in the context-pack.

### Public Portfolio Safety
All data is synthetic and fictional. All guardrails are designed so that a public GitHub repository remains safe. No confidential architecture, customer data, or real incident details are at risk.

### Cloud Run Compatibility
The design works within Google Cloud Run's constraints: stateless execution, environment-variable configuration, Secret Manager integration, no persistent state, no external service dependencies beyond optional AI providers.

---

## 3. What AI Is Allowed to Do

- Rewrite retrieved context into clearer, more detailed explanations
- Explain how payment flows work using retrieved synthetic data
- Explain service dependencies using retrieved service metadata
- Explain why change-safety checklist items matter using incident/test data
- Explain onboarding paths using role definitions and learning progressions
- Summarise relevant incidents and runbooks from the retrieved context
- Help new engineers understand payment platform concepts using synthetic knowledge base
- Decline to answer out-of-scope questions clearly and helpfully

---

## 4. What AI Is Not Allowed to Do

- Invent services, flows, incidents, events, APIs, controls, owners, or data that don't exist
- Answer questions about real bank architecture or real payment operations
- Claim the synthetic system reflects any real bank or production environment
- Use external internet knowledge as source of truth
- Make operational decisions or override deterministic guidance
- Provide regulatory, legal, or compliance advice
- Process, reference, or reason about customer data, payment details, or real incident information
- Hide uncertainty or claim confidence beyond what the data supports
- Operate statelessly across conversation turns (each request is independent)
- Suggest changes to the source YAML/JSON data model (that's a human decision)

---

## 5. Target User Journeys

### Journey 1: AI-Assisted Change-Safety Explanation

Engineer runs the deterministic change-safety checklist for Payment Validation Service. The UI shows the checklist items. Engineer clicks "Explain why this step matters" on a specific checklist item.

System flow:
1. Deterministic backend already retrieved: affected flows, services, tests, incidents, runbooks
2. Context-pack assembled with relevant entities
3. AI generates explanation connecting the step to real platform risks
4. Explanation cites incidents, tests, and runbooks that inform the requirement
5. Engineer understands not just *what* to do, but *why* it matters

Result: Engineer confidence increases. Change safety improves because the engineer understands the reasoning.

### Journey 2: AI-Assisted Payment-Flow Explanation

Engineer is learning the platform and opens the "Outbound SWIFT pacs.008 Customer Credit Transfer" flow. The UI shows the deterministic flow steps. Engineer clicks "Explain what happens here" on a specific step.

System flow:
1. Deterministic backend retrieved: flow definition, services involved, events, APIs, risks
2. Context-pack assembled with retrieved entities
3. AI generates narrative explanation of that step
4. Explanation explains which services are involved, what message changes happen, what events are published
5. Engineer reads explanation to understand the flow

Result: New engineer learns faster. Flow understanding is grounded in synthetic platform data.

### Journey 3: AI-Assisted Service Explanation

Engineer investigates "Payment Validation Service" in the dependency map. The UI shows deterministic service metadata. Engineer clicks "Explain the full picture" to get deeper context.

System flow:
1. Deterministic backend retrieved: service definition, dependencies, flows using it, incidents, risks, runbooks
2. Context-pack assembled with all relevant entities
3. AI generates comprehensive explanation of service purpose, importance, and failure modes
4. Explanation cites specific incidents that show why this service matters
5. Engineer understands the service in platform context, not just as code

Result: Service understanding is grounded in platform risks and incident history.

### Journey 4: AI-Assisted Onboarding Guidance

New test engineer receives an onboarding path generated deterministically by role and experience level. The UI shows the learning path phases. Engineer clicks "Why is this phase important?" on a specific phase.

System flow:
1. Deterministic backend retrieved: onboarding path definition, recommended flows, services, learning objectives
2. Context-pack assembled with learning phase context
3. AI generates explanation of why this phase matters before the next phase
4. Explanation connects to specific flows and risks the engineer will encounter
5. Engineer understands the learning architecture, not just reading order

Result: Onboarding engagement increases. Engineer understands *why* the path is structured this way.

### Journey 5: AI-Assisted Glossary Explanation

Engineer looks up "sanctions screening" in the glossary. The UI shows the deterministic glossary definition. Engineer clicks "Show platform examples" to see how this term applies.

System flow:
1. Deterministic backend retrieved: glossary term, relevant services, flows, incidents, glossary links
2. Context-pack assembled with term-specific context
3. AI generates explanation of how this term applies in the specific platform
4. Explanation shows which services implement this, which flows involve it, which incidents demonstrate it
5. Engineer learns the term in platform context, not as isolated definition

Result: Glossary becomes learning tool, not just reference.

### Journey 6: Unsupported/Out-of-Scope Question Handling

Engineer asks: "What's the difference between SWIFT and ACH payment types?"

System flow:
1. Deterministic backend detects: question is about real banking (outside platform scope)
2. Context-pack is empty or insufficient
3. AI is instructed to refuse: "I only know about this synthetic platform. Your platform uses SWIFT. If you want to understand real banking differences, consult external resources."
4. AI offers: "I can explain how your platform handles SWIFT or what ACH would look like here, but I can't compare against real-world systems."
5. User is directed to appropriate learning path or external source

Result: User is not hallucinated an answer. Trust increases because AI admits boundaries.

---

## 6. Proposed Architecture

The AI-assisted explanation flow fits into the existing system like this:

```
User opens React App
    ↓
User sees deterministic output
(change-safety checklist, flow details, service definition, etc.)
    ↓
User sees "Explain" button (if AI is enabled)
    ↓
User clicks button
    ↓
React sends request to FastAPI /api/ask?mode=explain
    ↓
FastAPI Intent Detection
(What is the user asking about?)
    ↓
FastAPI Entity Matching
(Which services, flows, incidents, runbooks match?)
    ↓
Context-Pack Builder
(Assemble all relevant data into structured format)
    ↓
Deterministic Answer Generated
(Change-safety checklist, flow step, service detail, etc.)
    ↓
Decision: Is AI enabled?
    ├─ NO → Return deterministic answer only
    └─ YES → Call AI Explainer Service with context-pack
        ↓
    AI Explainer
    (Vertex AI Gemini or OpenAI)
        ↓
    Response with explanation, citations, confidence, guardrail notes
        ↓
React displays answer
(Deterministic output + AI explanation + sources + confidence)
```

The deterministic path works at every step. AI is optional and never blocks the user from seeing the deterministic answer.

---

## 7. Context-Pack Architecture

A context-pack is the structured data container that holds everything the AI explainer needs—and nothing it doesn't need. It prevents hallucination by providing strict boundaries: the AI can only reference entities in the context-pack.

### Context-Pack Structure

```json
{
  "question": {
    "text": "User's original question or request",
    "intent": "explain_checklist_step | explain_flow_step | explain_service | explain_onboarding_phase | explain_glossary_term",
    "user_journey": "change_safety | flow_exploration | service_investigation | onboarding_guidance | glossary_lookup"
  },
  "detected_context": {
    "primary_entity_type": "service | flow | checklist_step | onboarding_phase | glossary_term",
    "primary_entity_id": "entity-id",
    "primary_entity_name": "Human readable name"
  },
  "matched_entities": {
    "services": [
      {
        "id": "service-id",
        "name": "Service Name",
        "criticality": "critical | high | medium | low",
        "description": "Brief description",
        "owner": "Team name",
        "published_events": ["event-1", "event-2"],
        "consumed_events": ["event-3"],
        "exposed_apis": ["api-1"]
      }
    ],
    "flows": [
      {
        "id": "flow-id",
        "name": "Flow Name",
        "description": "What this flow does",
        "services_involved": ["service-1", "service-2"],
        "events_involved": ["event-1"],
        "apis_involved": ["api-1"],
        "risks": ["risk-category-1"],
        "relevant_runbooks": ["RB-id"],
        "test_coverage": ["TEST-id"]
      }
    ],
    "events": [
      {
        "id": "event-id",
        "name": "event.name",
        "publisher": "service-id",
        "subscribers": ["service-id"],
        "description": "What this event represents"
      }
    ],
    "apis": [
      {
        "id": "api-id",
        "name": "GET /api/services",
        "service": "service-id",
        "description": "What this API does",
        "contract_documented": true
      }
    ],
    "runbooks": [
      {
        "id": "runbook-id",
        "title": "Runbook Title",
        "topic": "incident_response | operational_procedure | troubleshooting",
        "description": "What this runbook covers",
        "relevant_to": ["service-id", "incident-id"],
        "excerpt": "Key steps or context"
      }
    ],
    "incidents": [
      {
        "id": "INC-2024-0042",
        "title": "Incident title",
        "date": "2024-04-15",
        "services_involved": ["service-id"],
        "flows_affected": ["flow-id"],
        "description": "What happened",
        "lessons_learned": "Key takeaway",
        "contributing_factors": ["root-cause"]
      }
    ],
    "tests": [
      {
        "id": "TEST-id",
        "title": "Test name",
        "description": "What this test validates",
        "coverage": "critical | recommended | optional",
        "services_tested": ["service-id"],
        "flows_tested": ["flow-id"]
      }
    ],
    "risks": [
      {
        "id": "risk-id",
        "category": "timeout | data-loss | cascading-failure | dependency-failure",
        "description": "What could go wrong",
        "mitigation": "How to prevent or handle it",
        "related_incidents": ["INC-id"]
      }
    ]
  },
  "metadata": {
    "generated_at": "2026-05-10T14:30:00Z",
    "generated_by": "intent_matching | flow_reference | service_reference | checklist_step | glossary_lookup",
    "source_version": "main-2026-05-10-abc123",
    "source_files": [
      "data/services.yaml",
      "data/payment-flows.yaml",
      "data/incidents.json",
      "data/runbooks.yaml"
    ],
    "confidence": 0.92,
    "completeness": "high | medium | low"
  },
  "constraints": {
    "synthetic_data_only": true,
    "no_external_sources": true,
    "must_cite_all_claims": true,
    "refuse_if_context_insufficient": true,
    "max_hallucination_risk": "low"
  },
  "exclusions": {
    "out_of_scope_topics": ["real_bank_architecture", "regulatory_requirements", "competitor_systems"],
    "unsupported_questions": "If user asks about real banking, state boundaries clearly",
    "missing_entities": ["entity-id-that-was-referenced-but-not-found"]
  }
}
```

### Context-Pack Assembly Rules

- Retrieve only entities directly relevant to the user's question and detected intent
- Include enough detail (descriptions, relationships) that AI can explain without guessing
- Include source file references so users can verify claims
- Include confidence score—if context is weak, AI confidence degrades
- Mark completeness: is this a complete picture or partial context?
- List any missing entities that were referenced but not found (data integrity check)
- Set exclusions and boundaries upfront: out-of-scope topics, unsupported questions
- Context-pack has an implicit expiration: if data changes, old context is stale

---

## 8. Backend Changes for Later Phases

These components will be implemented in future phases (not in Phase 9A):

### context_pack_service.py

Responsibility: Assemble context-packs from retrieved entities.

```python
class ContextPackBuilder:
    def build_for_change_safety(self, service_id: str, change_type: str) -> ContextPack
    def build_for_flow_explanation(self, flow_id: str, step_number: int) -> ContextPack
    def build_for_service_explanation(self, service_id: str) -> ContextPack
    def build_for_glossary_term(self, term: str) -> ContextPack
    def validate_completeness(self, context_pack: ContextPack) -> CompletionScore
```

### ai_provider_service.py

Responsibility: Manage AI provider configuration and selection.

```python
class AIProviderService:
    def is_enabled(self) -> bool
    def get_provider(self) -> AIProvider
    def health_check(self) -> bool
    def list_supported_providers(self) -> List[str]
```

### ai_explainer_service.py

Responsibility: Call the AI provider with context-pack and prompt.

```python
class AIExplainerService:
    def explain_change_safety_step(self, context_pack: ContextPack, step_id: str) -> ExplanationResult
    def explain_flow_step(self, context_pack: ContextPack, step_number: int) -> ExplanationResult
    def explain_service(self, context_pack: ContextPack) -> ExplanationResult
    def explain_glossary_term(self, context_pack: ContextPack) -> ExplanationResult
    def validate_citations(self, response: str, context_pack: ContextPack) -> ValidationResult
```

### Provider Interface

All providers must implement:

```python
class AIProvider:
    def call(self, system_prompt: str, user_message: str, context_pack: ContextPack) -> AIResponse
    def health_check(self) -> bool
    def supports_feature(self, feature: str) -> bool
```

### Gemini Provider (Vertex AI)

```python
class GeminiProvider(AIProvider):
    def __init__(self, project_id: str, location: str, model: str)
    def call(self, system_prompt: str, user_message: str, context_pack: ContextPack) -> AIResponse
```

### OpenAI Provider (Optional)

```python
class OpenAIProvider(AIProvider):
    def __init__(self, api_key: str, model: str)
    def call(self, system_prompt: str, user_message: str, context_pack: ContextPack) -> AIResponse
```

### Updated /api/ask Endpoint

```python
@app.post("/api/ask")
async def ask_platform(
    question: str,
    mode: str = "deterministic",  # "deterministic" or "explain"
    service_id: Optional[str] = None,
    flow_id: Optional[str] = None
) -> AskResponse:
    # mode="deterministic" → current behavior, no AI
    # mode="explain" → deterministic answer + AI explanation
```

---

## 9. Frontend Changes for Later Phases

These UI changes will be implemented in future phases (not in Phase 9A):

### Answer Mode Toggle

Add a toggle in the Ask-the-Platform result screen:
- Option: "Show deterministic answer only"
- Option: "Show with AI-assisted explanation"
- Default: "Deterministic only" (matches `ENABLE_AI_EXPLANATIONS=false`)

### Clear Synthetic-Data Notice

When AI explanation is shown, include:
> This explanation is generated from the synthetic Payments Platform knowledge base. This is a fictional reference implementation, not a real bank system.

### Source Files Shown

Display which data files the explanation is grounded in:
```
Sources: data/services.yaml, data/incidents.json, data/runbooks.yaml
```

### Confidence Shown

Display confidence score:
```
Confidence: 92%
(Based on matched entities and data completeness)
```

### Guardrail Notes Shown

If explanation contains uncertainty or limitations:
```
Note: This explanation covers the primary flow. Edge cases in 
exceptional scenarios are not modeled here. See RB-ROUTING-TIMEOUT 
for operational details.
```

### Disabled State (When AI Not Configured)

If `ENABLE_AI_EXPLANATIONS=false`:
- No "Explain" buttons appear
- Ask-the-Platform works deterministically only
- No user-facing indication that AI capability exists

---

## 10. Provider Strategy

### Default Provider: None

The application ships with no AI provider required or configured.

- `ENABLE_AI_EXPLANATIONS=false` (default)
- `AI_PROVIDER=none` (default)
- App runs fully on deterministic mode only

### First Cloud Provider: Vertex AI Gemini

If and when AI is enabled, Vertex AI (Google Cloud) is the preferred first provider because:

- The application is deployed on Google Cloud Run
- Vertex AI is native to the same cloud environment
- Data stays within Google Cloud infrastructure
- Billing integrates with existing GCP project
- No separate API key management needed (uses Cloud authentication)

Configuration:
```
ENABLE_AI_EXPLANATIONS=true
AI_PROVIDER=vertex-ai
GOOGLE_CLOUD_PROJECT=<project-id>
GOOGLE_CLOUD_LOCATION=europe-west2
VERTEX_AI_MODEL=gemini-1.5-pro
```

### Optional Later Provider: OpenAI

OpenAI is an optional fallback provider for teams that:
- Already use OpenAI for other projects
- Have existing OpenAI infrastructure
- Prefer a non-Google provider

Configuration:
```
ENABLE_AI_EXPLANATIONS=true
AI_PROVIDER=openai
OPENAI_API_KEY=<from-secret-manager>
OPENAI_MODEL=gpt-4-turbo
```

### Provider Swappability

The AI provider interface is designed to be swappable:
- Core logic doesn't depend on specific provider
- Adding a new provider requires implementing `AIProvider` interface
- Provider selection happens at startup based on environment variables
- If selected provider is unavailable, app falls back to deterministic-only

### App Works Without Any AI Provider

This is non-negotiable. The entire application—backend, frontend, tests, deployment—works without `ENABLE_AI_EXPLANATIONS=true`. No developer is forced to use or understand AI infrastructure to contribute.

---

## 11. Environment Variables

### Feature Enablement

```
# Default: false
# Set to true only if AI provider is configured
ENABLE_AI_EXPLANATIONS=false

# Default: none
# Options: none, vertex-ai, openai
AI_PROVIDER=none

# Default: unset
# Only required if AI is enabled
AI_MODEL=gemini-1.5-pro
```

### Vertex AI Configuration

```
# Required if AI_PROVIDER=vertex-ai
GOOGLE_CLOUD_PROJECT=<gcp-project-id>

# Default: europe-west2
# Set to nearest GCP region for your deployment
GOOGLE_CLOUD_LOCATION=europe-west2

# Optional: override model
VERTEX_AI_MODEL=gemini-1.5-pro
```

### OpenAI Configuration (Optional)

```
# Required if AI_PROVIDER=openai
# Must be injected via Secret Manager, not committed to code
OPENAI_API_KEY=<key-from-secret-manager>

# Optional: override model
OPENAI_MODEL=gpt-4-turbo
```

### Advanced Configuration

```
# Default: 5 seconds
# Maximum time to wait for AI response before timeout
AI_RESPONSE_TIMEOUT_SECONDS=5

# Default: 0.8
# Minimum confidence threshold to show explanation
AI_MIN_CONFIDENCE_THRESHOLD=0.8

# Default: false
# Enable detailed logging of AI requests/responses (for debugging)
AI_VERBOSE_LOGGING=false
```

---

## 12. Secret Handling

### Principle: No Secrets in GitHub

API keys, credentials, and secrets must never be committed to the repository.

### Local Development

For local testing with Vertex AI:
```bash
export GOOGLE_CLOUD_PROJECT=<your-project>
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account-key.json
```

The `GOOGLE_APPLICATION_CREDENTIALS` file must be:
- Generated from a GCP service account
- Added to `.gitignore`
- Never committed to GitHub

For local testing with OpenAI:
```bash
export OPENAI_API_KEY=sk-...
```

This must be:
- Set in local `.env` (which is `.gitignore`'d)
- Never committed to GitHub

### Cloud Run Deployment

Secrets are injected into Cloud Run environment at deployment time.

Google Cloud Secret Manager:
```bash
# Create secret
gcloud secrets create openai-api-key --data-file=- <<< "sk-..."

# Grant Cloud Run service account access
gcloud secrets add-iam-policy-binding openai-api-key \
  --member=serviceAccount:payments-navigator@<project>.iam.gserviceaccount.com \
  --role=roles/secretmanager.secretAccessor

# Update Cloud Run to inject secret
gcloud run deploy payments-platform-navigator \
  --set-env-vars OPENAI_API_KEY=projects/<project>/secrets/openai-api-key/latest
```

Vertex AI uses Cloud authentication directly (no explicit API key).

### Audit Trail

Every AI API call is logged with:
- Timestamp
- User context (if available)
- Query intent
- Response generation time
- Provider used
- Result status (success, timeout, failure)

Logs must be retained for 90 days for compliance review.

### Principles

- **Never commit secrets**: Zero tolerance policy
- **Use Secret Manager**: Not environment files
- **Principle of least privilege**: Service account can only access secrets it needs
- **Rotation**: API keys rotated quarterly
- **Audit**: All secret access is logged

---

## 13. Evaluation Strategy

Before any AI explanation is shown to users, it must pass evaluation gates:

### Supported Questions

For each supported question type (change safety, flow explanation, service explanation, glossary explanation, onboarding guidance):

1. **Source Citations**: Every claim must reference source files
   - Service claims cite `data/services.yaml`
   - Flow claims cite `data/payment-flows.yaml`
   - Incident claims cite `data/incidents.json`
   - Runbook claims cite `data/runbooks.yaml`

2. **No Invented Entities**: AI cannot claim something exists if it's not in the data
   - No service inventions
   - No flow inventions
   - No incident inventions
   - Validation: check against real data files

3. **Accuracy Against Source**: Claims must match the source data
   - Service description accuracy >95%
   - Risk description accuracy >95%
   - Incident detail accuracy >95%

### Unsupported Questions

When the user asks an out-of-scope question:

1. **Safe Refusal**: AI declines clearly
   - "I only know about this synthetic platform"
   - "I can't answer questions about real banking"
   - "See external resources for regulatory details"

2. **Boundary Clarity**: AI explains what it *can* help with
   - "I can explain how this platform models payment validation"
   - "I can't compare our synthetic system to real banks"

3. **Graceful Redirection**: AI suggests alternatives
   - "Try asking about specific services or flows"
   - "Check the glossary for payment terms"

### Regression Tests

Test suite must cover:

```python
def test_ai_refuses_real_bank_questions():
    # Verify AI refuses to answer about real banks
    
def test_ai_refuses_regulatory_questions():
    # Verify AI refuses to give legal/regulatory advice
    
def test_ai_refuses_real_data_questions():
    # Verify AI refuses to answer about customer data
    
def test_ai_cites_all_claims():
    # Verify every explanation cites source files
    
def test_ai_does_not_invent_services():
    # Verify AI doesn't claim non-existent services
    
def test_ai_preserves_synthetic_disclaimer():
    # Verify explanations include synthetic data notice
    
def test_ai_confidence_degrades_with_weak_context():
    # Verify confidence score reflects context quality
```

### Human Review

Before deploying to production:

1. **Sample Review**: 50+ sample explanations reviewed by human
2. **Quality Checks**: Accuracy, citations, tone, boundaries
3. **Edge Case Testing**: Unusual questions, ambiguous requests, unusual data
4. **Failure Mode Testing**: What happens when AI service is down?

---

## 14. Rollout Plan

### Phase 9A: AI Design Documents (Current)

**Deliverables**:
- docs/ai-design.md ✓
- docs/ai-prompting-strategy.md ✓
- docs/ai-risk-and-guardrails.md ✓
- docs/decision-log.md Decision 013 ✓

**Duration**: Week 1

**Success Criteria**: Design documents reviewed and approved

---

### Phase 9B: Context-Pack Builder (Future)

**Deliverables**:
- `backend/app/context_pack_service.py`
- Unit tests for context-pack assembly
- Integration tests with existing data loader

**Duration**: Week 2

**Success Criteria**: Context-packs generated correctly for all question types

---

### Phase 9C: Provider Abstraction (Future)

**Deliverables**:
- `backend/app/ai_provider_service.py`
- `backend/app/providers/base.py` (AIProvider interface)
- `backend/app/providers/mock.py` (mock provider for testing)

**Duration**: Week 3

**Success Criteria**: Providers are swappable, mock provider works

---

### Phase 9D: Vertex AI Integration (Future)

**Deliverables**:
- `backend/app/providers/vertex_ai.py`
- Integration with Google Cloud Vertex AI SDK
- Configuration for europe-west2 location
- Health checks and fallback logic

**Duration**: Week 4

**Success Criteria**: Real Vertex AI calls succeed, timeouts handled gracefully

---

### Phase 9E: Frontend UI Toggle (Future)

**Deliverables**:
- "Show AI explanation" toggle in Ask-the-Platform
- Conditional rendering if AI is enabled
- Source files and confidence display
- Guardrail notes display
- Synthetic data disclaimer

**Duration**: Week 5

**Success Criteria**: UI works with and without AI enabled

---

### Phase 9F: Evaluation and Testing (Future)

**Deliverables**:
- Regression test suite (no-answer, hallucination, citations)
- Evaluation of 50+ sample explanations
- Documentation of quality standards
- Failure mode testing

**Duration**: Week 6

**Success Criteria**: All evaluation gates passed, <1% hallucination rate

---

### Phase 9G: Cloud Run Secret Configuration (Future)

**Deliverables**:
- Cloud Run service account configuration
- Secret Manager bindings
- Deployment documentation
- Audit log setup

**Duration**: Week 7

**Success Criteria**: Cloud Run deployment with AI enabled, secrets properly secured

---

### Go/No-Go Decision Gates

After Phase 9F (evaluation):

**Go Criteria**:
- Hallucination rate <1%
- Citation accuracy 100%
- Explanation relevance >95%
- User confusion/misunderstanding <5%
- Response time <2 seconds (p95)

**No-Go Criteria** (If met, return to design or disable AI):
- Hallucination rate >2%
- Citation accuracy <99%
- Explanation relevance <90%
- User confusion >10%
- Response time >5 seconds

### Abort Decision

At any phase, if:
- A security vulnerability is discovered
- Hallucinations become frequent (>5% of responses)
- Quality metrics drop below targets
- Prompt injection vulnerabilities emerge

Then: Disable AI immediately, revert to deterministic-only mode, investigate root cause.

---

## Summary

This document defines the architecture for an optional, retrieval-grounded AI-assisted explanation layer for Payments Platform Navigator.

The core principles are:
1. **Retrieval first** — AI only explains what has been retrieved
2. **Deterministic is source of truth** — AI never overrides structured decisions
3. **Disabled by default** — App works fully without any AI provider
4. **Source-aware** — All claims cite synthetic data
5. **Safe for public portfolio** — Synthetic data only, no confidential information
6. **Cloud Run compatible** — Works within GCP constraints

No code is implemented in Phase 9A. All implementation is deferred to future phases with clear go/no-go decision gates.
