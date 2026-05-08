from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_ask_endpoint_returns_structured_change_safety_answer():
    response = client.post(
        "/api/ask",
        json={
            "question": "What should I check before changing Payment Validation Service?"
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert "Payment Validation Service" in payload["answer_summary"]
    assert "svc-payment-validation" in payload["relevant_services"]
    assert "flow-outbound-pacs009" in payload["relevant_flows"]
    assert "rb-validation-failure-spike" in payload["relevant_runbooks"]
    assert payload["confidence"] >= 0.5
    assert "services.yaml" in payload["source_files"]
