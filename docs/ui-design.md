# UI Design

## 1. Product Design Principles

Payments Platform Navigator should feel like an internal engineering platform for a regulated payments environment, not a generic SaaS landing page and not a chatbot-first demo.

Principles:

- Start from payment flows, service ownership, operational risk, and change safety.
- Show connected evidence, not isolated pages of documentation.
- Make synthetic data explicit and safe for a public repository.
- Support role-based onboarding without hiding the underlying platform model.
- Prefer clear summaries, dependency tables, flow timelines, and checklists over decorative UI.
- Make the critical path obvious for new engineers, production support, test engineers, engineering leads, and solution architects.
- Keep MVP interactions deterministic and explainable.

## 2. Navigation Structure

Primary navigation:

- Home
- Onboarding
- Payment Flows
- Services
- Ask the Platform
- Change Safety
- Knowledge Health
- Glossary

Secondary navigation:

- Flow detail pages are reached from Payment Flows, Onboarding modules, Ask results, service detail links, and Change Safety output.
- Service detail pages are reached from Services, Payment Flow Detail, Dependency Map, Ask results, and Knowledge Health.
- Runbooks, incidents, changes, tests, APIs, and events are displayed as related evidence within flow and service screens rather than as standalone MVP routes.

## 3. Information Architecture

The UI should expose four layers of information.

Layer 1 - Orientation:

- Role selector
- Platform summary
- Knowledge-health tiles
- Key flows and services

Layer 2 - Navigation:

- Onboarding modules by role
- Flow list and flow detail
- Service list and dependency map
- Glossary search

Layer 3 - Evidence:

- APIs, events, runbooks, incidents, changes, and tests linked to flows and services
- Risks and controls from service data
- Knowledge-health scores and watch items

Layer 4 - Action:

- Rule-based Ask the Platform answer
- Change-safety checklist
- Recommended next reading or investigation path

Data source mapping:

- `data/services.yaml` drives service list, service detail, dependency map, ownership, risks, controls, and service-related evidence.
- `data/payment-flows.yaml` drives flow list, flow detail, happy-path steps, message types, synthetic examples, and flow evidence.
- `data/event-catalogue.yaml` drives event chips, producer/consumer context, payload field summaries, and Ask answers.
- `data/api-catalogue.yaml` drives API contract cards and change impact context.
- `data/runbooks.yaml` drives operational guidance cards.
- `data/incidents.json` drives incident learning summaries.
- `data/change-records.json` drives change examples and checklist source material.
- `data/test-coverage.json` drives test evidence and known gaps.
- `data/glossary.yaml` drives glossary and inline definitions.
- `data/onboarding-paths.yaml` drives role-based onboarding.
- `data/knowledge-health.json` drives executive dashboard tiles, service health, flow health, and recommended actions.

## 4. Screen-by-Screen Design

### Home / Role Selector

Purpose: Orient the user and route them into the product by role.

Primary users: New backend engineer, test engineer, production support engineer, engineering lead, solution architect.

Data used:

- `data/onboarding-paths.yaml`
- `data/knowledge-health.json`
- `data/payment-flows.yaml`
- `data/services.yaml`

UI components:

- Header with product name and synthetic-data marker.
- Role selector cards for the five onboarding roles.
- Optional area selector using domains from services, such as validation, routing, external-messaging, repair-and-investigation, and data-and-reporting.
- Knowledge-health summary strip showing overall score, trend, green/amber/red counts, and dashboard freshness.
- Key payment flows list with message type and direction.
- Tier-0 service list with owner and criticality.

User actions:

- Select a role and continue to Onboarding.
- Open a payment flow.
- Open a service.
- Open Knowledge Health.

Empty states:

- If no onboarding paths are available, show "No onboarding paths are configured in the synthetic dataset."
- If no flows are available, show "No payment flows are currently defined."

Error states:

- If data fails to load, show a concise error banner and retry action.
- If role data is malformed, disable the continue action and explain that onboarding data is unavailable.

Demo talking points:

- The first interaction is role selection because onboarding risk differs by role.
- The home page makes payment flows and tier-0 services visible immediately.
- The MVP is deterministic and grounded in structured synthetic data.

### Role-Based Onboarding Plan

Purpose: Provide a practical onboarding route based on role and optional platform area.

Primary users: New joiners, engineering leads assigning onboarding, solution architects orienting to a domain.

Data used:

- `data/onboarding-paths.yaml`
- `data/services.yaml`
- `data/payment-flows.yaml`
- `data/event-catalogue.yaml`
- `data/api-catalogue.yaml`
- `data/runbooks.yaml`
- `data/change-records.json`
- `data/test-coverage.json`

UI components:

- Role summary with goal.
- Recommended starting services.
- Primary payment flows.
- Module cards with title, resources, completion signal, and linked evidence.
- "Suggested first safe contribution" panel derived from module resources and related low or medium risk changes.
- Progress indicators for module completion in UI state only for MVP.

User actions:

- Switch role.
- Open linked service, flow, API, event, runbook, change, or test evidence.
- Mark a module as viewed in local UI state.
- Start a Change Safety Checklist from a module or service.

Empty states:

- If role is unknown, show available roles.
- If an area filter removes all modules, show all modules for the role with a note that no exact area match exists.

Error states:

- If a resource ID cannot be resolved, show the unresolved ID as "Referenced synthetic resource not found" and continue rendering the rest of the plan.

Demo talking points:

- Onboarding is treated as operational risk reduction, not a reading list.
- Completion signals describe what the person should be able to explain or do.
- Links cross-reference flows, services, APIs, events, tests, and runbooks.

### Payment Flow Explorer

Purpose: Let users scan all payment flows and understand direction, message type, involved services, and coverage.

Primary users: Backend engineers, test engineers, production support engineers, solution architects.

Data used:

- `data/payment-flows.yaml`
- `data/knowledge-health.json`
- `data/test-coverage.json`

UI components:

- Filters for direction, message type, service, and health status.
- Flow table or dense cards with name, message type, direction, entry service, service count, test count, health status, and watch item.
- Search by flow name, message type, service ID, or risk ID.

User actions:

- Filter flows.
- Open flow detail.
- Start Ask the Platform with a flow context.

Empty states:

- If no flows match filters, show a reset-filters action.

Error states:

- If flow-health data is missing, render the flow list without health badges and show a non-blocking warning.

Demo talking points:

- The explorer starts with payment journeys, which is how risk is experienced in production.
- `flow-outbound-pacs008` and `flow-outbound-pacs009` show ISO 20022 context without using real payment data.

### Payment Flow Detail

Purpose: Explain one payment flow from entry service through events, APIs, runbooks, risks, incidents, and tests.

Primary users: Backend engineers, test engineers, production support engineers, solution architects.

Data used:

- `data/payment-flows.yaml`
- `data/services.yaml`
- `data/event-catalogue.yaml`
- `data/api-catalogue.yaml`
- `data/runbooks.yaml`
- `data/incidents.json`
- `data/change-records.json`
- `data/test-coverage.json`
- `data/knowledge-health.json`

UI components:

- Flow header with name, message type, direction, business purpose, and synthetic example.
- Happy-path timeline using numbered steps and service names.
- Service involvement panel with criticality and owner.
- APIs and events panels with producer/consumer context.
- Risks and controls panel.
- Related runbooks, incidents, changes, and tests.
- Flow health card with score, status, coverage, and watch item.

User actions:

- Open service detail from any step.
- Open dependency map focused on this flow.
- Start change-safety checklist prefilled with the flow ID.
- Ask a rule-based question about the flow.

Empty states:

- If a flow has no APIs, show "This flow has no direct API calls in the synthetic dataset."
- If a flow has no incidents, show "No synthetic incident examples are linked to this flow."

Error states:

- If `flow_id` is not found, show a not-found page with link back to Payment Flows.
- If linked evidence is missing, show unresolved references in a compact warning panel.

Demo talking points:

- A single flow view connects delivery, operations, testing, and incident learning.
- The happy path is readable by a new joiner, but the linked evidence supports senior review.

### Service Dependency Map

Purpose: Show upstream and downstream service relationships and make blast radius visible.

Primary users: Solution architects, engineering leads, backend engineers, production support engineers.

Data used:

- `data/services.yaml`
- `data/payment-flows.yaml`
- `data/knowledge-health.json`

UI components:

- Dependency graph or adjacency layout.
- Service nodes coloured by criticality and knowledge-health status.
- Filters for domain, criticality, and selected flow.
- Side panel for selected service summary.
- Legend for upstream, downstream, API, and event relationships.

User actions:

- Select a service node.
- Filter map to a payment flow.
- Open service detail.
- Start change-safety checklist for selected service.

Empty states:

- If no services match filters, show reset-filters action.
- If a service has no dependencies, show it as an isolated node with explicit "No configured dependencies."

Error states:

- If map rendering fails, fall back to upstream/downstream tables.

Demo talking points:

- Dependency visibility is central to payment change safety.
- The MVP can start with tables or simple graph rendering, as long as the relationships are clear.

### Service Detail

Purpose: Provide a service-level operating and change context.

Primary users: Backend engineers, production support engineers, engineering leads, solution architects.

Data used:

- `data/services.yaml`
- `data/payment-flows.yaml`
- `data/event-catalogue.yaml`
- `data/api-catalogue.yaml`
- `data/runbooks.yaml`
- `data/incidents.json`
- `data/change-records.json`
- `data/test-coverage.json`
- `data/knowledge-health.json`

UI components:

- Service header with type, domain, owner, criticality, lifecycle, runtime, and data classification.
- Summary and supported flows.
- Upstream/downstream dependencies.
- Provides/consumes APIs.
- Publishes/consumes events.
- Risks and controls.
- Runbooks, related incidents, related changes, tests, and knowledge-health dimensions.

User actions:

- Open related flow, API, event, runbook, incident, change, or test evidence.
- Start a change-safety checklist for this service.
- Ask the Platform with this service as context.

Empty states:

- If no downstream services exist, show "No downstream services are defined."
- If no APIs are provided, show "No provided APIs are defined for this service."

Error states:

- If `service_id` is not found, show not-found page and link to Services.
- If health data is missing, show service detail without health score and include a warning.

Demo talking points:

- The detail page is built for engineers who need ownership, contracts, dependencies, runbooks, and test evidence in one place.
- Risks and controls are explicit and synthetic.

### Ask the Platform

Purpose: Provide deterministic, rule-based answers grounded in the synthetic data model.

Primary users: New joiners, production support engineers, engineering leads.

Data used:

- All data files may be searched by ID, name, role, service, flow, event, API, runbook, incident, change, test, or glossary term.

UI components:

- Search-style question input.
- Suggested prompts such as "What should I learn for the SWIFT Connector?", "What can break in outbound pacs.008?", and "Which checks apply before changing validation rules?"
- Answer panel with summary, supporting evidence links, and "Why this answer" source list.
- No conversational persona, no open-ended assistant claims.

User actions:

- Ask a question.
- Click supporting sources.
- Start change-safety checklist from an answer.

Empty states:

- Before first question, show suggested prompts grouped by onboarding, flow, service, and change safety.
- If no match is found, show suggested search terms from glossary, flows, and services.

Error states:

- If the rule engine cannot classify the question, return a structured "I can answer questions about services, flows, runbooks, incidents, changes, tests, glossary terms, and onboarding paths."

Demo talking points:

- Ask is not the product centre of gravity. It is a structured retrieval shortcut.
- MVP uses deterministic rules to avoid ungrounded AI behaviour.
- Future AI can be added after the data model is trusted.

### Change Safety Checklist

Purpose: Generate a practical pre-change checklist from affected services, flows, APIs, events, runbooks, incidents, changes, tests, and known gaps.

Primary users: Backend engineers, test engineers, solution architects, engineering leads.

Data used:

- `data/services.yaml`
- `data/payment-flows.yaml`
- `data/api-catalogue.yaml`
- `data/event-catalogue.yaml`
- `data/runbooks.yaml`
- `data/incidents.json`
- `data/change-records.json`
- `data/test-coverage.json`
- `data/knowledge-health.json`

UI components:

- Inputs for change title, services, flows, APIs, events, risk level, and change type.
- Generated checklist grouped by impact, contract checks, regression tests, runbooks, monitoring, rollback, incident learnings, and evidence gaps.
- Risk summary showing tier-0 involvement, number of affected flows, related incidents, health watch items, and test gaps.
- Exportable text block for public demo purposes.

User actions:

- Add or remove affected services/flows.
- Generate checklist.
- Open linked evidence.
- Copy checklist text.

Empty states:

- If no scope is selected, prompt the user to select at least one service, flow, API, or event.

Error states:

- If selected IDs are unknown, list invalid IDs and do not generate a checklist until they are removed.

Checklist logic:

- Include all directly selected services, flows, APIs, and events.
- Expand service scope to upstream and downstream services for blast-radius context.
- Expand flow scope to all services, APIs, events, runbooks, risks, and tests on the flow.
- Pull service risks and controls from `services.yaml`.
- Pull prior change checks from `change-records.json` where affected services, flows, APIs, or events overlap.
- Pull incidents and lessons where services or flows overlap.
- Pull required tests and known gaps from `test-coverage.json`.
- Add stronger warnings when any affected service has criticality `tier-0` or knowledge-health status `amber`.
- Always include rollback, monitoring, production-support communication, and evidence-capture sections.

Demo talking points:

- This is the clearest "engineering leader" moment: the app turns platform knowledge into safer change preparation.
- The checklist is deterministic and explainable.

### Knowledge Health Dashboard

Purpose: Give engineering leaders a concise view of knowledge quality, ownership clarity, operational readiness, and test evidence.

Primary users: Engineering leads, solution architects, platform owners.

Data used:

- `data/knowledge-health.json`
- `data/services.yaml`
- `data/payment-flows.yaml`
- `data/test-coverage.json`

UI components:

- Executive summary score, trend, green/amber/red counts.
- Dashboard tiles for tier-0 service health, runbook coverage, change readiness evidence, flow coverage, and dashboard freshness.
- Service health table with score, status, owner, last reviewed, and dimensions.
- Flow health table with coverage and watch item.
- Top risks and recommended actions.
- Known test gaps panel.

User actions:

- Filter service health by status, criticality, or domain.
- Open service detail.
- Open flow detail.
- Start Ask or Change Safety from a weak area.

Empty states:

- If dashboard tiles are missing, show service and flow health tables directly.

Error states:

- If score values are invalid, show "Score unavailable" and continue rendering non-score fields.

Demo talking points:

- Knowledge health is treated as an engineering management signal.
- The dashboard supports coaching, prioritisation, and resilience discussion without claiming production readiness.

### Glossary

Purpose: Explain payments, ISO 20022, operational, and platform terms in practical language.

Primary users: All users, especially new joiners and interview/demo viewers.

Data used:

- `data/glossary.yaml`

UI components:

- Search input.
- Alphabetical term list.
- Term detail panel.
- Related links where terms match flow names, message types, service domains, APIs, events, or runbooks.

User actions:

- Search by term or definition.
- Open related flow or service where available.

Empty states:

- If no term matches, show "No glossary term matches this search."

Error states:

- If glossary fails to load, show an error banner and retry action.

Demo talking points:

- The glossary keeps domain language accessible without diluting engineering depth.
- Terms such as pacs.008, pacs.009, replay, dead-letter queue, and four-eyes approval connect directly to platform evidence.

## 5. Visual Style Guidance

The product should look like a professional internal engineering platform.

Style:

- Dense, calm, and readable.
- Executive dashboard feel, with strong tables, status badges, compact cards, and clear hierarchy.
- Neutral background, high contrast text, restrained accent colours for status and selection.
- Green, amber, and red are reserved for health and risk states.
- Use charts and maps only when they clarify operational or dependency context.
- Avoid playful illustration, gamification, decorative gradients, marketing hero sections, oversized cards, and chatbot-style full-screen conversation layouts.

## 6. Accessibility and Usability Notes

- All core screens must be usable with keyboard navigation.
- Colour must not be the only signal for health or risk; include labels such as green, amber, red, tier-0, high, medium, and low.
- Tables need clear column headings and responsive behaviour.
- Graph views require a table fallback.
- Empty and error states should tell the user what data is missing and how to recover.
- Text should be concise and payments-aware without assuming every user already knows ISO 20022.
- Links to evidence must have descriptive labels.

## 7. MVP Scope Boundaries

In scope:

- Static synthetic data loaded through backend APIs.
- Role-based onboarding paths.
- Flow and service exploration.
- Dependency visibility.
- Rule-based Ask the Platform.
- Deterministic change-safety checklist.
- Knowledge-health dashboard.
- Glossary.

Out of scope for MVP:

- Authentication.
- Database persistence.
- External AI model.
- Real integrations.
- Real bank data.
- User-specific saved progress.
- Production operational execution.
- Incident creation or change approval workflows.
- Kubernetes or multi-container deployment.
