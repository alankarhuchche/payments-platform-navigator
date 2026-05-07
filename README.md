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

## Planned MVP

The MVP will include:

- role-based onboarding journey
- payment flow explorer
- service dependency map
- service detail view
- ask-the-platform assistant
- change-safety checklist
- knowledge-health dashboard
- payments glossary

## Target Architecture

Initial MVP:

- React TypeScript frontend
- FastAPI Python backend
- YAML/JSON synthetic data
- Docker container
- Google Cloud Run deployment
- GitHub to Cloud Run continuous deployment

## Project Status

Current phase: Product and repository foundation.

See:

- `docs/product-brief.md`
- `docs/architecture.md`
- `docs/decision-log.md`
- `AGENTS.md`