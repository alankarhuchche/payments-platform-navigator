# Decision Log

## 013 — Plan AI-assisted explanations as retrieval-grounded optional capability

Date: 2026-05-10

Status: Accepted

Decision: Phase 9A will create architectural and prompting design documents for an optional, AI-assisted explanation enhancement, without implementing code. The enhancement would provide contextual explanations grounded in the deterministic backend and synthetic data, disabled by default, with extensive guardrails against hallucination, confidentiality risks, and over-trust.

Rationale: The MVP successfully demonstrates deterministic, rule-based assistance for complex payments domain questions. To improve user experience for certain journeys (explaining why a checklist step matters, contextualizing glossary terms, augmenting Ask-the-Platform with deeper explanations), AI-assisted generation could be valuable. However, introducing AI to a public portfolio application requires careful planning around hallucination prevention, data safety, synthetic-data discipline, and user trust. This decision establishes the architecture, prompting strategy, risk assessment, and rollout plan before any implementation begins.

Consequences:

- The application will remain fully deterministic and functional without any AI provider configured.
- If AI is enabled in future deployments, it will augment (not replace) deterministic outputs.
- All explanations will be grounded in the structured synthetic data model; AI cannot hallucinate beyond the context-pack.
- AI features will be disabled by default (`AI_ENABLED=false`) to preserve operational simplicity and safety.
- Vertex AI (Google Cloud) is the preferred provider if AI is enabled; OpenAI is optional fallback.
- Extensive evaluation gates and abort criteria prevent low-quality AI from reaching users.
- All prompts, context-pack formats, and safety procedures are documented and open-source.
- No external AI providers are required to run or develop the application.
- Implementation (if approved) will follow a staged rollout: backend infrastructure → provider integration → frontend UI → production with feature flags.

## 011 — Use relative API paths for single-container Cloud Run deployment

Date: 2026-05-10

Status: Accepted

Decision: The React frontend will use relative API paths in production unless `VITE_API_BASE_URL` is explicitly configured.

Rationale: In local Vite development, `http://localhost:8080` correctly points to the developer's FastAPI backend. In a deployed Cloud Run browser session, `localhost` refers to the user's machine, not the Cloud Run service. Because the MVP container serves the frontend and backend from the same FastAPI origin, production builds should default to relative paths such as `/api/services`.

Consequences:

- Local development continues to default to `http://localhost:8080`.
- Single-container Cloud Run deployments call same-origin backend routes by default.
- Explicit `VITE_API_BASE_URL` values still override the default for split-origin deployments.
- No backend, database, authentication, or external AI changes are required.

## 010 — Package frontend and backend into a single Cloud Run container

Date: 2026-05-09

Status: Accepted

Decision: Package the React frontend, FastAPI backend, and synthetic data into one Docker image that runs a single FastAPI process for Cloud Run.

Rationale: The MVP should be simple to run locally and deploy to Cloud Run without introducing extra infrastructure. A multi-stage Docker build keeps frontend build tooling out of the runtime image while allowing FastAPI to serve both `/api/*` routes and the built frontend static files.

Consequences:

- The container reads `PORT`, defaults to `8080`, and binds to `0.0.0.0`.
- Frontend static files are produced during Docker build and served by FastAPI.
- Repository-level synthetic data is copied to `/app/data` in the runtime image.
- Unknown non-API routes fall back to `index.html` so frontend browser refresh works.
- External AI, database, authentication, Kubernetes, and cloud-specific service dependencies remain out of scope.

## 009 — Implement React frontend against deterministic backend contract

Date: 2026-05-08

Status: Accepted

Decision: Phase 5 will implement a Vite React TypeScript frontend that consumes the deterministic FastAPI backend contract created in Phase 4.

Rationale: The project now needs a demo-friendly user interface that proves the value of role-based onboarding, payment-flow exploration, service dependency navigation, rule-based Ask the Platform, change-safety guidance, knowledge-health metrics, and glossary lookup without introducing frontend-only business rules or external AI dependency.

Consequences:

- The frontend must call the backend APIs rather than reading data files directly.
- UI routing can remain simple for MVP.
- The interface should stay sober, practical, and payments-aware.
- Backend changes are limited to strict integration fixes only.
- Docker, authentication, database persistence, and external AI remain out of scope for this phase.

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
