from app.data_loader import REQUIRED_DATA_FILES, get_knowledge_data


def test_data_loader_loads_required_synthetic_files():
    data = get_knowledge_data()

    assert data.data_files_loaded == REQUIRED_DATA_FILES
    assert len(data.services) == 8
    assert len(data.flows) == 5
    assert len(data.glossary_terms) >= 30
    assert data.services_by_id["svc-payment-validation"]["name"] == "Payment Validation Service"
