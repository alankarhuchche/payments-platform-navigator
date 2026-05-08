from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_flows_endpoint_returns_five_flows():
    response = client.get("/api/flows")

    assert response.status_code == 200
    payload = response.json()
    assert payload["count"] == 5
    assert len(payload["items"]) == 5
    assert any(item["id"] == "flow-outbound-pacs008" for item in payload["items"])


def test_glossary_returns_at_least_thirty_terms():
    response = client.get("/api/glossary")

    assert response.status_code == 200
    payload = response.json()
    assert payload["count"] >= 30
