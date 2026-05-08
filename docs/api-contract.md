# API Contract

## 1. Backend API Principles

The backend API exposes the synthetic payments platform knowledge model to the React frontend. It should be small, deterministic, and easy to run on Cloud Run.

Principles:

- Use only local YAML and JSON files under `data/`.
- Return stable IDs that match the source files.
- Resolve linked evidence where it materially helps the frontend, but avoid hiding the original IDs.
- Keep responses deterministic and cacheable for MVP.
- Validate user input for `POST` endpoints.
- Keep Ask the Platform rule-based for MVP.
- Make synthetic classification visible in metadata where useful.

## 2. Base URL

Local development:

```text
http://localhost:8080
```

Cloud Run:

```text
https://<cloud-run-service-url>
```

The application must listen on the `PORT` environment variable, default to `8080`, and bind to `0.0.0.0`.

## 3. Request and Response Conventions

- Request and response bodies use JSON.
- IDs are lower-case stable strings from the data files, for example `svc-payment-validation` and `flow-outbound-pacs008`.
- Date and timestamp values remain strings as supplied by the synthetic data.
- Unknown query parameters should be ignored unless they conflict with validation.
- List endpoints return an envelope with `metadata`, `items`, and `count`.
- Detail endpoints return a single object with linked evidence IDs and selected resolved evidence for UI convenience.
- The backend should not mutate source data during MVP.

List response shape:

```json
{
  "metadata": {
    "classification": "synthetic"
  },
  "count": 1,
  "items": []
}
```

## 4. Error Response Format

```json
{
  "error": {
    "code": "not_found",
    "message": "Service not found.",
    "details": {
      "service_id": "svc-unknown"
    }
  }
}
```

Common status codes:

- `200` for successful reads and deterministic generated responses.
- `400` for invalid parameters or request bodies.
- `404` for unknown service or flow IDs.
- `422` for structurally valid JSON that fails domain validation.
- `500` for unexpected backend errors.

## 5. Endpoint Specifications

### GET /health

Purpose: Confirm the API is running and data files can be loaded.

Response `200`:

```json
{
  "status": "ok",
  "service": "payments-platform-navigator",
  "data_classification": "synthetic",
  "data_files_loaded": [
    "services.yaml",
    "payment-flows.yaml",
    "event-catalogue.yaml",
    "api-catalogue.yaml",
    "runbooks.yaml",
    "incidents.json",
    "change-records.json",
    "test-coverage.json",
    "glossary.yaml",
    "onboarding-paths.yaml",
    "knowledge-health.json"
  ]
}
```

### GET /api/services

Purpose: Return services for service list and dependency map.

Optional filters:

- `domain`
- `criticality`
- `flow_id`

Response `200` example:

```json
{
  "metadata": {
    "classification": "synthetic"
  },
  "count": 2,
  "items": [
    {
      "id": "svc-payment-gateway",
      "name": "Payment Gateway",
      "type": "api-edge",
      "domain": "payment-initiation",
      "criticality": "tier-0",
      "owned_by": "Synthetic Payments API Team",
      "summary": "Receives outbound payment instructions, normalises request envelopes, and starts platform orchestration.",
      "supports_flows": ["flow-outbound-pacs008", "flow-outbound-pacs009", "flow-payment-repair-investigation"],
      "upstream_services": [],
      "downstream_services": ["svc-payment-validation", "svc-status-publisher"],
      "knowledge_health": {
        "score": 88,
        "status": "green"
      }
    },
    {
      "id": "svc-payment-validation",
      "name": "Payment Validation Service",
      "type": "domain-service",
      "domain": "validation",
      "criticality": "tier-0",
      "owned_by": "Synthetic Payments Validation Team",
      "summary": "Applies syntactic, reference-data, cut-off, currency, and message-rule checks before screening and routing.",
      "supports_flows": ["flow-outbound-pacs008", "flow-outbound-pacs009", "flow-payment-repair-investigation"],
      "upstream_services": ["svc-payment-gateway", "svc-investigation-workbench"],
      "downstream_services": ["svc-sanctions-screening", "svc-routing-decision", "svc-status-publisher"],
      "knowledge_health": {
        "score": 83,
        "status": "green"
      }
    }
  ]
}
```

### GET /api/services/{service_id}

Purpose: Return service detail with linked evidence for the Service Detail screen.

Response `200` example:

```json
{
  "id": "svc-payment-validation",
  "name": "Payment Validation Service",
  "type": "domain-service",
  "domain": "validation",
  "lifecycle": "production-reference",
  "summary": "Applies syntactic, reference-data, cut-off, currency, and message-rule checks before screening and routing.",
  "owned_by": "Synthetic Payments Validation Team",
  "criticality": "tier-0",
  "runtime": "Cloud Run",
  "data_classification": "synthetic-payment-instruction",
  "upstream_services": ["svc-payment-gateway", "svc-investigation-workbench"],
  "downstream_services": ["svc-sanctions-screening", "svc-routing-decision", "svc-status-publisher"],
  "supports_flows": ["flow-outbound-pacs008", "flow-outbound-pacs009", "flow-payment-repair-investigation"],
  "publishes_events": ["payment.validated", "payment.validation_failed"],
  "consumes_events": ["payment.initiated", "payment.repaired"],
  "provides_apis": ["api-payment-validation"],
  "consumes_apis": ["api-sanctions-screening", "api-routing-decision"],
  "runbooks": ["rb-validation-failure-spike"],
  "risks": [
    {
      "id": "risk-validation-rule-drift",
      "title": "Validation rules can drift from scheme rulebooks and create avoidable repair volume.",
      "controls": ["Versioned rule packs.", "Regression tests for high-volume payment corridors."]
    }
  ],
  "related_incidents": ["inc-2026-002"],
  "related_changes": ["chg-2026-002", "chg-2026-006"],
  "tests": ["tc-validation-rules", "tc-payment-repair-e2e"],
  "knowledge_health": {
    "score": 83,
    "status": "green",
    "last_reviewed": "2026-04-26",
    "dimensions": {
      "documentation_freshness": 82,
      "ownership_clarity": 90,
      "dependency_coverage": 80,
      "operational_readiness": 84,
      "test_evidence": 82
    }
  }
}
```

### GET /api/flows

Purpose: Return payment flows for the Payment Flow Explorer.

Optional filters:

- `direction`
- `message_type`
- `service_id`
- `status`

Response `200` example:

```json
{
  "metadata": {
    "classification": "synthetic"
  },
  "count": 1,
  "items": [
    {
      "id": "flow-outbound-pacs008",
      "name": "Outbound SWIFT pacs.008 customer credit transfer",
      "message_type": "pacs.008",
      "direction": "outbound",
      "business_purpose": "Customer credit transfer from a synthetic digital channel to an overseas beneficiary.",
      "entry_service": "svc-payment-gateway",
      "services": ["svc-payment-gateway", "svc-payment-validation", "svc-sanctions-screening", "svc-routing-decision", "svc-swift-connector", "svc-status-publisher", "svc-data-lake-publisher"],
      "tests": ["tc-outbound-pacs008-e2e", "tc-payment-gateway-contract", "tc-swift-message-contract"],
      "knowledge_health": {
        "score": 86,
        "status": "green",
        "coverage": "strong",
        "watch_item": "Ack uncertainty examples need one more support scenario."
      }
    }
  ]
}
```

### GET /api/flows/{flow_id}

Purpose: Return full flow detail with happy path and evidence.

Response `200` example:

```json
{
  "id": "flow-outbound-pacs008",
  "name": "Outbound SWIFT pacs.008 customer credit transfer",
  "message_type": "pacs.008",
  "direction": "outbound",
  "business_purpose": "Customer credit transfer from a synthetic digital channel to an overseas beneficiary.",
  "entry_service": "svc-payment-gateway",
  "services": ["svc-payment-gateway", "svc-payment-validation", "svc-sanctions-screening", "svc-routing-decision", "svc-swift-connector", "svc-status-publisher", "svc-data-lake-publisher"],
  "events": ["payment.initiated", "payment.validated", "sanctions.screening_requested", "routing.decision_completed", "swift.message_submitted", "swift.ack_received", "payment.status_updated"],
  "apis": ["api-payment-submission", "api-payment-validation", "api-sanctions-screening", "api-routing-decision", "api-swift-submission"],
  "runbooks": ["rb-payment-submission-latency", "rb-swift-ack-delay", "rb-status-publication-lag"],
  "tests": ["tc-outbound-pacs008-e2e", "tc-payment-gateway-contract", "tc-swift-message-contract"],
  "risks": ["risk-duplicate-submission", "risk-screening-timeout", "risk-acknowledgement-gap"],
  "happy_path": [
    {
      "step": 1,
      "service": "svc-payment-gateway",
      "action": "Accept synthetic payment request and publish payment.initiated."
    },
    {
      "step": 2,
      "service": "svc-payment-validation",
      "action": "Validate pacs.008 mandatory fields, currency, cut-off, and party structure."
    }
  ],
  "synthetic_example": {
    "payment_id": "pay-syn-008-0001",
    "instructed_amount": "12500.00",
    "currency": "GBP",
    "debtor_country": "GB",
    "creditor_country": "NL"
  },
  "knowledge_health": {
    "score": 86,
    "status": "green",
    "coverage": "strong",
    "watch_item": "Ack uncertainty examples need one more support scenario."
  }
}
```

### GET /api/glossary

Purpose: Return glossary terms.

Optional filters:

- `q`

Response `200` example:

```json
{
  "metadata": {
    "classification": "synthetic"
  },
  "count": 2,
  "items": [
    {
      "term": "pacs.008",
      "definition": "ISO 20022 customer credit transfer message used here for synthetic outbound customer payments."
    },
    {
      "term": "Idempotency key",
      "definition": "Client-provided key used to safely detect duplicate payment submissions."
    }
  ]
}
```

### GET /api/onboarding?role={role}&area={area}

Purpose: Return role-based onboarding path. `area` is optional and should filter or highlight relevant services/domains when possible.

Supported roles should match `data/onboarding-paths.yaml`, normalised case-insensitively:

- `Backend engineer`
- `Test engineer`
- `Production support engineer`
- `Engineering lead`
- `Solution architect`

Response `200` example:

```json
{
  "id": "onboard-backend-engineer",
  "role": "Backend engineer",
  "goal": "Become productive changing payment APIs, events, validation rules, and service integrations.",
  "area": "validation",
  "recommended_starting_services": ["svc-payment-gateway", "svc-payment-validation", "svc-routing-decision"],
  "primary_flows": ["flow-outbound-pacs008", "flow-outbound-pacs009"],
  "modules": [
    {
      "id": "be-001",
      "title": "Platform shape and payment lifecycle",
      "resources": ["flow-outbound-pacs008", "flow-outbound-pacs009", "payment.initiated", "payment.status_updated"],
      "completion_signal": "Can explain how a submitted payment becomes a SWIFT message and status update."
    },
    {
      "id": "be-003",
      "title": "Change-safety checklist",
      "resources": ["chg-2026-001", "chg-2026-002", "chg-2026-004", "rb-validation-failure-spike"],
      "completion_signal": "Can prepare a low-risk change plan with rollback and monitoring."
    }
  ]
}
```

### GET /api/knowledge-health

Purpose: Return dashboard data for engineering leads and health badges across the UI.

Response `200` example:

```json
{
  "metadata": {
    "classification": "synthetic",
    "as_of": "2026-05-07"
  },
  "executive_summary": {
    "overall_score": 82,
    "trend": "improving",
    "services_green": 4,
    "services_amber": 4,
    "services_red": 0,
    "top_risks": [
      "Sanctions negative-path knowledge is thinner than tier-0 criticality requires.",
      "SWIFT acknowledgement runbook needs stronger replay examples.",
      "Data lake freshness metrics are improving but still amber."
    ],
    "recommended_actions": [
      "Prioritise sanctions hold-and-release examples for production support onboarding.",
      "Add correlation diagrams for SWIFT acknowledgement handling.",
      "Review knowledge-health dashboard thresholds monthly with engineering leads."
    ]
  },
  "dashboard_tiles": [
    {
      "id": "tile-runbook-coverage",
      "title": "Runbook coverage",
      "value": 90,
      "unit": "percent",
      "status": "green"
    }
  ],
  "service_health": [
    {
      "service_id": "svc-sanctions-screening",
      "score": 76,
      "status": "amber",
      "last_reviewed": "2026-04-20",
      "owner": "Synthetic Financial Crime Integration Team"
    }
  ],
  "flow_health": [
    {
      "flow_id": "flow-sanctions-hold-release",
      "score": 75,
      "status": "amber",
      "coverage": "moderate",
      "watch_item": "Negative-path sanctions scenarios need more detail."
    }
  ]
}
```

### POST /api/ask

Purpose: Return a rule-based answer grounded in the synthetic data model.

Request body:

```json
{
  "question": "What can break in outbound pacs.008?",
  "context": {
    "role": "Backend engineer",
    "service_id": "svc-payment-validation",
    "flow_id": "flow-outbound-pacs008"
  }
}
```

Response `200` example:

```json
{
  "answer_type": "flow_risk_summary",
  "summary": "Outbound pacs.008 depends on submission, validation, sanctions screening, routing, SWIFT submission, acknowledgement handling, and status publication. The main synthetic risks are duplicate submission, screening timeout, and acknowledgement gaps.",
  "supporting_evidence": [
    {
      "type": "flow",
      "id": "flow-outbound-pacs008",
      "label": "Outbound SWIFT pacs.008 customer credit transfer"
    },
    {
      "type": "runbook",
      "id": "rb-swift-ack-delay",
      "label": "SWIFT acknowledgement delay"
    },
    {
      "type": "incident",
      "id": "inc-2026-005",
      "label": "Delayed synthetic SWIFT acknowledgement reconciliation"
    }
  ],
  "recommended_next_actions": [
    "Review the flow happy path.",
    "Open the SWIFT Connector service detail.",
    "Run a change-safety checklist before changing validation, routing, or acknowledgement behaviour."
  ],
  "limitations": "This answer is rule-based and uses only synthetic repository data."
}
```

Rule-based answer classes for MVP:

- Service summary by service ID or service name.
- Flow summary by flow ID, flow name, or message type.
- Runbook lookup by symptom keyword.
- Change-safety prompt by terms such as change, deploy, modify, rule pack, route table, API, event, or status.
- Glossary definition by term.
- Onboarding guidance by role.
- Fallback response when no supported pattern matches.

### POST /api/change-safety-checklist

Purpose: Generate deterministic checklist guidance for a proposed synthetic platform change.

Request body:

```json
{
  "title": "Update validation rule pack for pacs.009 settlement fields",
  "risk_level": "high",
  "change_type": "validation-rule-change",
  "services": ["svc-payment-validation"],
  "flows": ["flow-outbound-pacs009"],
  "apis": ["api-payment-validation"],
  "events": ["payment.validated", "payment.validation_failed"]
}
```

Response `200` example:

```json
{
  "title": "Update validation rule pack for pacs.009 settlement fields",
  "risk_summary": {
    "risk_level": "high",
    "tier_0_services": ["svc-payment-validation"],
    "affected_services": ["svc-payment-validation", "svc-payment-gateway", "svc-investigation-workbench", "svc-sanctions-screening", "svc-routing-decision", "svc-status-publisher"],
    "affected_flows": ["flow-outbound-pacs009", "flow-payment-repair-investigation"],
    "related_incidents": ["inc-2026-002"],
    "known_gaps": ["gap-002"]
  },
  "checklist": [
    {
      "section": "Impact",
      "items": [
        "Confirm pacs.009 flow impact across validation, routing, SWIFT submission, and repair handling.",
        "Review upstream and downstream dependencies for Payment Validation Service."
      ]
    },
    {
      "section": "Contract and regression evidence",
      "items": [
        "Run tc-validation-rules.",
        "Run tc-outbound-pacs009-e2e.",
        "Confirm api-payment-validation response fields remain backwards-compatible."
      ]
    },
    {
      "section": "Operational readiness",
      "items": [
        "Review rb-validation-failure-spike.",
        "Confirm repair queue rollback route.",
        "Prepare monitoring for payment.validation_failed rate and rule_pack_version."
      ]
    },
    {
      "section": "Incident learning",
      "items": [
        "Review inc-2026-002 lesson: add pacs.009 regression fixtures and require flow-level sign-off."
      ]
    },
    {
      "section": "Rollback and communications",
      "items": [
        "Prepare rollback to previous approved rule pack.",
        "Notify production support of expected validation-failure signals.",
        "Capture synthetic change evidence for review."
      ]
    }
  ],
  "source_ids": {
    "services": ["svc-payment-validation"],
    "flows": ["flow-outbound-pacs009"],
    "changes": ["chg-2026-002"],
    "tests": ["tc-validation-rules", "tc-outbound-pacs009-e2e"],
    "runbooks": ["rb-validation-failure-spike"],
    "incidents": ["inc-2026-002"]
  },
  "limitations": "Checklist is deterministic guidance for synthetic demo data and is not a production approval workflow."
}
```

Checklist generation rules:

- Validate all submitted IDs before generating the checklist.
- Expand selected services to include direct upstream and downstream services.
- Expand selected flows to include linked services, APIs, events, runbooks, tests, and risks.
- Match prior changes where any service, flow, API, or event overlaps.
- Match prior incidents where any service or flow overlaps.
- Include known test gaps where related services overlap.
- Escalate language when `risk_level` is `high`, any affected service is `tier-0`, or any affected service/flow is amber in knowledge health.
- Always include impact, contracts, tests, runbooks, monitoring, rollback, communications, and evidence capture.

## 6. Validation Rules

General:

- IDs must match source data exactly after trimming whitespace.
- `role` is case-insensitive but must resolve to a configured onboarding role.
- `area` is optional and may match service domain, type, or service name.
- `risk_level` must be one of `low`, `medium`, or `high`.
- Request bodies larger than 16 KB should be rejected for MVP.

`POST /api/ask`:

- `question` is required.
- `question` must be between 3 and 500 characters.
- `context` is optional.
- Unknown context IDs should return `422`.

`POST /api/change-safety-checklist`:

- At least one of `services`, `flows`, `apis`, or `events` is required.
- Each submitted ID must exist in the corresponding data catalogue.
- Unknown IDs should return `422` with all invalid IDs listed.
- Duplicate IDs should be de-duplicated.

## 7. Notes for Future AI Integration

MVP has no external AI dependency. `POST /api/ask` should be implemented as deterministic retrieval and template generation over the synthetic dataset.

Future AI integration may be considered after the structured knowledge model is stable. Any future model-backed answer should:

- Use retrieval from the same data files or a governed equivalent.
- Cite source IDs and avoid unsupported claims.
- Keep synthetic/public data boundaries explicit.
- Refuse questions seeking real bank data, real internal systems, credentials, or confidential procedures.
- Keep deterministic fallback paths for demos and reliability.
