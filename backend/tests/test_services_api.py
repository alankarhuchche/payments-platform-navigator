from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_services_endpoint_returns_eight_services():
    response = client.get("/api/services")

    assert response.status_code == 200
    payload = response.json()
    assert payload["count"] == 8
    assert len(payload["items"]) == 8
    assert any(item["id"] == "svc-payment-validation" for item in payload["items"])


def test_service_detail_returns_payment_validation_service():
    response = client.get("/api/services/svc-payment-validation")

    assert response.status_code == 200
    payload = response.json()
    assert payload["id"] == "svc-payment-validation"
    assert payload["criticality"] == "tier-0"
    assert "api-payment-validation" in payload["provides_apis"]
