# Payments Platform Navigator

Payments Platform Navigator is a public reference implementation that demonstrates how fragmented payments engineering knowledge can be converted into role-based onboarding, dependency navigation, and change-safety intelligence for complex regulated payment platforms.

The project is designed as a portfolio-grade Cloud Run application for payments engineering, platform engineering, operational resilience, and ISO 20022-aware delivery.

## What This Demonstrates

The project shows how a complex payments platform could organise knowledge around:

- payment flows
- service ownership
- service dependencies
- ISO 20022 message concepts
- operational runbooks
- incident learnings
- change-safety checks
- test coverage
- knowledge-health metrics
- role-based onboarding journeys

## Important Data Notice

This project uses synthetic data only.

It does not contain real bank data, real payment data, real service names, real incidents, real people, customer data, credentials, or confidential architecture.

## MVP

The MVP includes:

- role-based onboarding journey
- payment flow explorer
- service dependency map
- service detail view
- ask-the-platform assistant
- change-safety checklist
- knowledge-health dashboard
- payments glossary

## Run Locally With Docker

Build the single-container full-stack image:

```bash
docker build -t payments-platform-navigator .
```

Run the container:

```bash
docker run --rm -p 8080:8080 payments-platform-navigator
```

Open:

- `http://localhost:8080/`
- `http://localhost:8080/health`
- `http://localhost:8080/api/services`
- `http://localhost:8080/api/flows`

The container runs one FastAPI app. It serves the React frontend static files, keeps API routes under `/api/*`, exposes `/health`, reads `PORT`, defaults to `8080`, and binds to `0.0.0.0`.

## Run Locally Without Docker

Backend:

```bash
cd backend
python -m pytest
uvicorn app.main:app --host 0.0.0.0 --port 8080
```

Frontend:

```bash
cd frontend
npm install
npm run build
npm run dev
```

## Target Architecture

Initial MVP:

- React TypeScript frontend
- FastAPI Python backend
- YAML/JSON synthetic data
- Docker container
- Google Cloud Run deployment
- GitHub to Cloud Run continuous deployment

## Project Status

Current phase: Docker and local full-stack run.

See:

- `docs/product-brief.md`
- `docs/architecture.md`
- `docs/decision-log.md`
- `AGENTS.md`
