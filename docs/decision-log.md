# Decision Log

## 008 — Implement deterministic FastAPI backend before frontend

Date: 2026-05-08

Status: Accepted

Decision: Phase 4 will implement the FastAPI backend before any React frontend work, using the existing synthetic data model and the Phase 3 API contract.

Rationale: The frontend depends on stable API shapes, deterministic Ask the Platform behaviour, and change-safety checklist logic. Implementing and testing the backend first creates a reliable contract for the later UI phase while preserving the MVP constraints of no database, no authentication, no external AI, and no real integrations.

Consequences:

- Backend endpoints must load from repository-level synthetic YAML and JSON files.
- Ask the Platform remains deterministic and rule-based.
- Change-safety output must be explainable from source data.
- The app must remain Cloud Run-ready by reading `PORT`, defaulting to `8080`, and binding to `0.0.0.0` when run directly.
- Frontend code remains out of scope for this phase.

## 007 — Create UI design and API contract before implementation

Date: 2026-05-07

Status: Accepted

Decision: Phase 3 will create UI design, API contract, demo script, and architecture documentation before backend or frontend implementation begins.

Rationale: The product needs to remain payments-aware, safe for public GitHub, and coherent across onboarding, flow exploration, service dependencies, Ask the Platform, change safety, and knowledge health. Defining the UX and API contract before coding reduces the risk of building generic screens that do not map cleanly to the connected synthetic data model.

Consequences:

- No application code should be created during this phase.
- Frontend screens must map explicitly to the synthetic data files.
- Backend endpoints must support the screens and preserve stable data IDs.
- Ask the Platform remains rule-based for MVP.
- Change-safety checklist logic must be deterministic, explainable, and source-linked.
- The single-container Cloud Run approach remains the target MVP deployment model.

## 006 — Use connected synthetic data model for MVP

Date: 2026-05-07

Status: Accepted

Decision: The MVP will use a connected synthetic data model across services, payment flows, events, APIs, runbooks, incidents, change records, tests, glossary terms, onboarding paths, and knowledge-health metrics.

Rationale: The project needs to demonstrate role-based onboarding, dependency navigation, change-safety intelligence, and payments-aware assistant responses without using real bank information. A connected synthetic dataset lets the application behave like a practical payments platform navigator while remaining safe for a public repository.

Consequences:

- All examples must remain fictional and must not include real bank names, internal systems, people, incidents, customer data, credentials, secrets, or confidential architecture.
- IDs should remain stable and cross-referenceable so frontend and backend phases can traverse the model consistently.
- Future data additions should preserve the same synthetic classification and relationship structure.
