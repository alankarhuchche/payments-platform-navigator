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
- `POST /api/ask` - Ask the Platform deterministic Q&A
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

## AI Configuration (Phase 9C)

AI explanations are optional and disabled by default. The backend includes an AI provider abstraction layer that can be extended with real providers (Gemini, OpenAI) in future phases.

### Configuration

Set these environment variables to enable/configure AI:

```bash
# Enable AI explanations (default: false)
ENABLE_AI_EXPLANATIONS=false

# Select AI provider: "none" (disabled), "vertex-ai" (future), "openai" (future)
# Default: "none"
AI_PROVIDER=none

# AI model name (only used if provider is configured)
# Default: "none"
AI_MODEL=none

# Google Cloud configuration (only needed for Vertex AI provider)
GOOGLE_CLOUD_PROJECT=your-gcp-project-id
GOOGLE_CLOUD_LOCATION=europe-west2

# OpenAI configuration (only needed for OpenAI provider)
# DO NOT commit your API key to git; use secret injection instead
OPENAI_API_KEY=sk-your-api-key-here
```

### Default Behaviour

- **AI is disabled by default**: `ENABLE_AI_EXPLANATIONS=false`
- **No external services are called** unless explicitly enabled
- **No secrets are required** to run the application
- **Deterministic backend remains source of truth**: All AI features are optional augmentations

### Provider Abstraction (Phase 9C)

The backend includes:
- `ai_provider_service.py`: Provider abstraction and NoopAIProvider implementation
- `ai_explainer_service.py`: Service for coordinating AI provider usage

Future phases will add real provider implementations (Vertex AI, OpenAI) that plug into this abstraction.
