from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_endpoint_returns_loaded_data_files():
    response = client.get("/health")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["service"] == "payments-platform-navigator"
    assert payload["data_classification"] == "synthetic"
    assert "services.yaml" in payload["data_files_loaded"]
