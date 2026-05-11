# Demo Script

## 1. 90-Second Demo Script

"Payments Platform Navigator is a public reference implementation for a common problem in payments engineering: critical knowledge is scattered across services, runbooks, incidents, test evidence, and change records.

This demo uses synthetic data only. It is not based on any real bank, real platform, real incident, or real operational procedure.

I start by choosing a role, for example Backend engineer. The onboarding plan does not just give reading links. It shows the payment flows, services, APIs, events, runbooks, and completion signals that help a new engineer become safe and productive.

Next I open the outbound SWIFT pacs.008 flow. The view shows the happy path from payment submission through validation, sanctions screening, routing, SWIFT submission, acknowledgements, and status publication. It also links to runbooks, incidents, risks, controls, and regression tests.

Then I open the Payment Validation Service. In one place I can see ownership, criticality, upstream and downstream dependencies, APIs, events, related incidents, tests, and knowledge-health evidence.

The most important capability is Change Safety. If I propose a validation rule change, the Navigator generates a deterministic checklist from the synthetic data model: impact, contracts, regression tests, runbooks, incident learnings, monitoring, rollback, and evidence capture.

The point is not to claim production readiness. The point is to show how payments engineering knowledge can be connected into onboarding, dependency navigation, and safer change preparation."

## 2. 3-Minute Demo Script

"Payments Platform Navigator is a Cloud Run-ready reference implementation for complex payments platforms. It demonstrates how engineering knowledge can be structured so new joiners, support engineers, test engineers, architects, and leads can reason about flows, dependencies, incidents, runbooks, and change risk.

Everything here is synthetic and safe for a public GitHub repository.

I start on the Home screen. The product begins with roles because a backend engineer, production support engineer, test engineer, solution architect, and engineering lead need different entry points into the same platform knowledge.

I select Backend engineer. The onboarding plan gives a practical route: platform shape, APIs and events, and change safety. Each module has resources and a completion signal. That matters because onboarding in payments is not just familiarity with code. It is understanding message flow, validation behaviour, operational states, controls, and testing obligations.

Now I open Payment Flows and choose outbound SWIFT pacs.008. This is a synthetic ISO 20022 customer credit transfer. The flow detail shows the happy path: payment gateway, validation, sanctions screening, routing decision, SWIFT connector, status publisher, and analytics publication. It also shows linked APIs, events, runbooks, risks, incidents, and tests. A new engineer can understand the journey; a lead or architect can inspect operational and dependency evidence.

Next I open the Service Dependency Map and select Payment Validation Service. This shows upstream and downstream services, including the gateway, investigation workbench, sanctions screening, routing, and status publisher. The service detail adds ownership, tier-0 criticality, provided and consumed APIs, published and consumed events, risks, controls, related changes, and test evidence.

Ask the Platform is deliberately rule-based for the MVP. If I ask what can break in outbound pacs.008, it returns a grounded answer with source links. It is a retrieval shortcut, not a free-form chatbot.

Finally, I open Change Safety. I enter a high-risk validation rule change against pacs.009 and the validation API. The checklist is generated from the same data model. It highlights affected services, related incidents, regression tests, runbooks, rollback, monitoring, and production support communication.

This demonstrates the product thesis: in payments platforms, connected engineering knowledge reduces onboarding friction and improves change safety."

## 3. 5-Minute Walkthrough

1. Start with the Home screen.

   Explain that this is a public, synthetic reference implementation for payments engineering knowledge navigation. Point out the role selector, knowledge-health summary, core flows, and tier-0 services.

2. Select `Backend engineer`.

   Show the role-based onboarding plan. Explain the difference between a document index and an onboarding path with completion signals. Open `flow-outbound-pacs008` from the module resources.

3. Walk through Payment Flow Detail.

   Use outbound SWIFT pacs.008 as the main story. Explain the happy path and why the services matter:

   - `svc-payment-gateway` accepts the synthetic instruction.
   - `svc-payment-validation` checks ISO 20022 and platform rules.
   - `svc-sanctions-screening` handles screening and possible hold behaviour.
   - `svc-routing-decision` selects the synthetic route and settlement profile.
   - `svc-swift-connector` submits the synthetic SWIFT message and handles acknowledgements.
   - `svc-status-publisher` publishes platform status.

   Show linked runbooks, incidents, and tests to demonstrate connected evidence.

4. Open Service Dependency Map.

   Filter or focus on `svc-payment-validation`. Explain upstream and downstream dependencies. Note that dependency visibility is a practical change-safety concern, especially for tier-0 services.

5. Open Service Detail.

   Show owner, criticality, APIs, events, risks, controls, runbooks, incidents, changes, tests, and knowledge-health dimensions. Explain that this is the kind of context engineers usually have to reconstruct manually.

6. Open Ask the Platform.

   Ask: "What can break in outbound pacs.008?" Explain that MVP answers are deterministic and source-backed. Show the supporting evidence links and limitations.

   **Optional AI-assisted Mode**: If the deployment has AI enabled (requires `ENABLE_AI_EXPLANATIONS=true` and a configured provider such as Vertex AI Gemini), demonstrate the AI-assisted mode toggle:
   - Show the "Answer mode" selector with "Deterministic" (default) and "AI-assisted" options.
   - Select "AI-assisted" and re-ask the same question.
   - Show the AI explanation section (grounded in synthetic data) with confidence score.
   - Explain that the AI explanation augments the deterministic answer and is grounded only in the synthetic knowledge base.
   - Point out the safety disclaimer: "AI-assisted answers are generated only from the synthetic Payments Platform Navigator knowledge base."
   - If desired, show a scenario where AI is disabled: the mode selector shows only "Deterministic" and a warning explains why.

7. Open Change Safety Checklist.

   Use a change such as "Update validation rule pack for pacs.009 settlement fields" with `svc-payment-validation`, `flow-outbound-pacs009`, `api-payment-validation`, `payment.validated`, and `payment.validation_failed`. Show the generated impact, contract, regression, runbook, incident learning, monitoring, rollback, and evidence sections.

8. Finish on Knowledge Health.

   Show overall score, amber services, top risks, and recommended actions. Explain that engineering leaders need knowledge-health signals because documentation quality is part of operational resilience.

## 4. Suggested Screen Recording Flow

Recording sequence:

1. Home / role selector - 10 seconds.
2. Backend engineer onboarding plan - 20 seconds.
3. Outbound pacs.008 flow detail - 35 seconds.
4. Service dependency map focused on Payment Validation Service - 25 seconds.
5. Service detail for Payment Validation Service - 30 seconds.
6. Ask the Platform with a flow risk question - 25 seconds.
7. Change Safety Checklist for a validation rule change - 40 seconds.
8. Knowledge Health Dashboard - 25 seconds.

Recording notes:

- Keep the cursor steady and avoid rapid scrolling.
- Use `flow-outbound-pacs008` for the main journey and `flow-outbound-pacs009` for change-safety contrast.
- Keep the synthetic-data statement visible early.
- Do not describe the app as production-ready.

## 5. LinkedIn Demo Narrative

"I built Payments Platform Navigator as a public reference implementation for a problem I have seen across complex engineering organisations: platform knowledge is usually fragmented, and that fragmentation becomes onboarding risk, delivery risk, and operational risk.

The project uses synthetic payments data only. It models services, ISO 20022 payment flows, APIs, events, runbooks, incidents, changes, test evidence, onboarding paths, and knowledge-health metrics.

The demo shows a role-based onboarding path, a payment-flow explorer, service dependency navigation, a deterministic Ask the Platform feature, a change-safety checklist, and an engineering-lead knowledge-health dashboard.

The design choice I care about most: the assistant is not the centre of the product. The centre is structured payments engineering context. The assistant is just one way to retrieve it.

The goal is to show how engineering leaders can turn scattered knowledge into safer onboarding, clearer dependency understanding, and better change preparation."

## 6. Interview Explanation Narrative

"The project is intentionally scoped as a reference implementation rather than a production platform. I wanted to demonstrate senior engineering judgement: start with the domain model and product brief, build a connected synthetic dataset, define UX and API contracts, then implement the application.

The domain is payments engineering. A change to a validation rule, route table, SWIFT acknowledgement handler, or status publisher can affect operational visibility, customer outcomes, repair queues, testing obligations, and production support readiness. So the product is organised around flows, services, dependencies, runbooks, incidents, changes, and tests.

For the MVP, I avoided a database, authentication, real integrations, and external AI. That keeps it suitable for Cloud Run and safe for public GitHub. Ask the Platform is rule-based because the data model needs to be trustworthy before adding model-generated answers.

The Change Safety Checklist is the strongest example of the product thinking. It takes a proposed change, expands impacted services and flows, pulls related APIs and events, includes previous incident lessons, identifies tests and known gaps, and produces a practical checklist. That is the kind of workflow that connects engineering knowledge to delivery risk.

If I extended it, I would add governed AI retrieval, richer dependency visualisation, documentation freshness automation, and integration with delivery tooling. But the MVP deliberately proves the core value without requiring private data or complex infrastructure."
