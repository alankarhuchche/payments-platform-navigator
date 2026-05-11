# Payments Platform Navigator Backend

FastAPI backend for the Payments Platform Navigator MVP.

The backend exposes deterministic APIs over the repository-level synthetic data files in `../data`. It supports role-based onboarding, service and flow exploration, glossary lookup, knowledge-health metrics, rule-based Ask the Platform, and deterministic change-safety checklist generation.

No database, authentication, external AI model, or real integrations are used in the MVP.

## Local Setup

From the repository root:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run Locally

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

The app also reads the `PORT` environment variable when run directly:

```bash
cd backend
PORT=8080 python -m app.main
```

## Run Tests

```bash
cd backend
pytest
```

## Full-Stack Container

From the repository root:

```bash
docker build -t payments-platform-navigator .
docker run --rm -p 8080:8080 payments-platform-navigator
```

The container runs one FastAPI app. It serves `/health`, `/api/*`, and the built React frontend from the same process.

## Endpoints

- `GET /health`
- `GET /api/services`
- `GET /api/services/{service_id}`
- `GET /api/flows`
- `GET /api/flows/{flow_id}`
- `GET /api/glossary`
- `GET /api/onboarding?role={role}&area={area}`
- `GET /api/knowledge-health`
- `POST /api/ask` - Ask the Platform deterministic or AI-assisted Q&A
- `POST /api/change-safety-checklist` - Generate change-safety checklist
- `POST /api/context-pack` - Return structured context pack for a question (Phase 9B)

### POST /api/context-pack

Returns the structured context pack for a question. Used for debugging and transparency to see what synthetic data is available behind an answer.

**Request**:
```json
{
  "question": "What should I check before changing Payment Validation Service?",
  "service_id": "optional-service-id",
  "flow_id": "optional-flow-id"
}
```

**Response**:
```json
{
  "question": "...",
  "detected_intent": "change_safety|service_explanation|payment_flow_explanation|incident_or_runbook_help|glossary_explanation|onboarding_guidance|unsupported",
  "matched_entities": {
    "services": ["service-1"],
    "flows": ["flow-1"],
    "events": ["event-name"],
    "apis": ["api-1"],
    "glossary_terms": ["term"]
  },
  "relevant_services": ["service-1", "service-2"],
  "relevant_flows": ["flow-1"],
  "relevant_events": ["event-1"],
  "relevant_apis": ["api-1"],
  "relevant_runbooks": ["runbook-1"],
  "relevant_incidents": ["INC-2024-0001"],
  "relevant_tests": ["TEST-1"],
  "relevant_risks": [{"id": "risk-1", "description": "..."}],
  "suggested_next_steps": ["..."],
  "source_files": ["services.yaml", "payment-flows.yaml"],
  "confidence": 0.92,
  "unsupported_reason": null
}
```

## Data Loading

The backend loads YAML and JSON from the repository-level `data/` folder:

- `services.yaml`
- `payment-flows.yaml`
- `event-catalogue.yaml`
- `api-catalogue.yaml`
- `runbooks.yaml`
- `incidents.json`
- `change-records.json`
- `test-coverage.json`
- `glossary.yaml`
- `onboarding-paths.yaml`
- `knowledge-health.json`

Required files are validated at startup. Data is read-only for MVP and all examples remain synthetic for public GitHub use.

## AI Configuration (Phase 9C, 9D)

AI explanations are optional and disabled by default. The backend includes an AI provider abstraction layer that supports Vertex AI Gemini (Phase 9D) and is designed for future OpenAI integration.

### Configuration

Set these environment variables to enable/configure AI:

```bash
# Enable AI explanations (default: false)
ENABLE_AI_EXPLANATIONS=false

# Select AI provider: "none" (disabled), "vertex-gemini" (Phase 9D), "openai" (future)
# Default: "none"
AI_PROVIDER=none

# AI model name (only used if provider is configured)
# For Gemini: gemini-2.5-flash, gemini-2.0-pro, etc.
# Default: gemini-2.5-flash
AI_MODEL=gemini-2.5-flash

# Google Cloud configuration (only needed for Vertex AI provider)
GOOGLE_CLOUD_PROJECT=your-gcp-project-id
GOOGLE_CLOUD_LOCATION=europe-west2

# Gemini API key (required only for vertex-gemini provider)
# DO NOT commit your real API key to git; use secret injection instead
GOOGLE_API_KEY=your-gemini-api-key-here
GEMINI_API_KEY=your-gemini-api-key-here

# OpenAI configuration (only needed for OpenAI provider)
# DO NOT commit your API key to git; use secret injection instead
OPENAI_API_KEY=sk-your-api-key-here
```

### Using AI-Assisted Explanations

To request AI-assisted explanations, set `mode: "ai_assisted"` in the `/api/ask` request:

```json
{
  "question": "What should I check before changing Payment Validation Service?",
  "mode": "ai_assisted"
}
```

Response will include:
- `answer_summary`: Deterministic rule-based answer (always included)
- `ai_explanation`: AI-assisted explanation (if AI enabled and available)
- `ai_mode`: "ai_assisted" or omitted if AI not used
- `ai_status`: Status information about AI provider

**Default mode is "deterministic"** if not specified. AI always falls back to deterministic answer if provider fails.

### Default Behaviour

- **AI is disabled by default**: `ENABLE_AI_EXPLANATIONS=false`
- **No external services are called** unless explicitly enabled
- **No secrets are required** to run the application
- **Deterministic backend remains source of truth**: All AI features are optional augmentations
- **API keys are never stored in code**: Use environment variables or secret injection

### Provider Implementations

Phase 9C-9D:
- `ai_provider_service.py`: Provider abstraction with NoopAIProvider and VertexGeminiProvider
- `ai_explainer_service.py`: Service for coordinating AI provider selection and usage
- `ai_prompt_service.py`: Strict prompting to prevent hallucination and out-of-scope answers

### Vertex AI Gemini (Phase 9D)

To enable Gemini-assisted explanations:

1. Set environment variables:
   ```bash
   ENABLE_AI_EXPLANATIONS=true
   AI_PROVIDER=vertex-gemini
   AI_MODEL=gemini-2.5-flash
   GOOGLE_API_KEY=your-api-key
   ```

2. Install google-genai (done via requirements.txt):
   ```bash
   pip install google-genai==0.4.0
   ```

3. Request AI mode in `/api/ask`:
   ```json
   {
     "question": "...",
     "mode": "ai_assisted"
   }
   ```

Gemini provider:
- Sends only context pack (structured synthetic data) to the model
- Uses strict prompting to prevent general-knowledge leakage
- Gracefully falls back to deterministic answer if provider fails
- Never sends raw repo files or unstructured data to the model
- Confidence score is capped at the context pack confidence

Future phases will add OpenAI provider without changing application logic.
