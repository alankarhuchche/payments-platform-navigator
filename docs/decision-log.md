# Decision Log

## 001 — Use a dedicated repository

Decision:
Create a dedicated GitHub repository named `payments-platform-navigator`.

Reason:
This is a separate public portfolio project and should not be mixed with incident RCA, ISO address repair, or other experiments.

## 002 — Use synthetic data only

Decision:
All data in the repository will be synthetic.

Reason:
The project must be safe for public GitHub, LinkedIn, and resume use.

## 003 — Use file-based data for MVP

Decision:
Use YAML and JSON files for the first version.

Reason:
This keeps the MVP simple, transparent, and easy to run without database setup.

## 004 — Use one Cloud Run container for MVP

Decision:
Serve the frontend and backend from a single container in the first version.

Reason:
This simplifies deployment and avoids unnecessary operational complexity.

## 005 — Avoid external AI dependency in v0.1

Decision:
The first version will use deterministic, rule-based answers.

Reason:
The app should work without API keys, secrets, model cost, or hallucination risk.