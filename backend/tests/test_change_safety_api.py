from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_change_safety_returns_impacted_flows_and_tests_for_payment_validation():
    response = client.post(
        "/api/change-safety-checklist",
        json={
            "service_id": "payment-validation-service",
            "change_type": "validation-rule-change",
            "description": "Synthetic update to validation rule pack.",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["service"]["id"] == "svc-payment-validation"
    assert payload["risk_level"] == "high"
    assert "flow-outbound-pacs009" in payload["impacted_flows"]
    assert "tc-validation-rules" in payload["tests_to_run"]
    assert "tc-payment-repair-e2e" in payload["tests_to_run"]
    assert "payment.validated" in payload["impacted_events"]
    assert "api-payment-validation" in payload["impacted_apis"]
