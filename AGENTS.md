# AGENTS.md — Payments Platform Navigator

## Project Context

Payments Platform Navigator is a public, portfolio-grade reference implementation for an engineering leader in a UK bank payments platform.

The product demonstrates how fragmented payments engineering knowledge can be converted into role-based onboarding, dependency navigation, and change-safety intelligence for complex regulated payment platforms.

This is not a generic chatbot or generic onboarding app. It must feel like it was created by someone who understands payments engineering, ISO 20022, SWIFT connectivity, production operations, incident management, dependency risk, control evidence, and regulated banking delivery.

## Data Safety Rules

Use synthetic data only.

Do not include:
- real bank names
- real service names
- real people
- real internal architecture
- real incidents
- real operational procedures
- confidential details
- proprietary implementation patterns
- customer data
- payment data
- credentials
- secrets

All examples must be clearly synthetic and safe for a public GitHub repository.

## Technical Direction

MVP stack:
- Frontend: React with TypeScript
- Backend: FastAPI with Python
- Data: YAML and JSON files
- Runtime: Docker container
- Deployment: Google Cloud Run
- CI/CD: GitHub to Cloud Run using Cloud Build

The MVP should not require:
- database
- authentication
- external AI model
- private network
- Kubernetes
- real integrations

## Cloud Run Requirements

The application must:
- listen on the `PORT` environment variable
- default to port `8080`
- bind to `0.0.0.0`
- run in a single container for MVP
- avoid hardcoded local-only ports

## Product Principles

Prioritise:
- payment flows
- service dependencies
- role-based onboarding
- change-safety guidance
- operational runbooks
- incident learning
- knowledge-health metrics

Avoid:
- generic chatbot behaviour
- over-engineering
- vague AI buzzwords
- fake claims of production readiness
- unnecessary frameworks
- complex infrastructure before MVP

## Delivery Approach

Build in phases:

1. Product brief
2. Synthetic data model
3. UI design
4. Backend API
5. Frontend app
6. Docker/local run
7. Cloud Run deployment
8. README, blog, LinkedIn, resume assets

Do not jump to feature implementation before the relevant design and data files exist.

## Writing Style

Use clear, practical, senior engineering language.

The tone should be:
- commercially grounded
- payments-aware
- implementation-oriented
- suitable for public GitHub
- suitable for LinkedIn and resume use

Avoid generic consultant language and exaggerated claims.