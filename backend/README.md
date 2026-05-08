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

## Endpoints

- `GET /health`
- `GET /api/services`
- `GET /api/services/{service_id}`
- `GET /api/flows`
- `GET /api/flows/{flow_id}`
- `GET /api/glossary`
- `GET /api/onboarding?role={role}&area={area}`
- `GET /api/knowledge-health`
- `POST /api/ask`
- `POST /api/change-safety-checklist`

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
