"""Integration tests for the FastAPI application.

This module contains tests that verify the functionality of the API endpoints,
ensuring they process immigration queries correctly and return expected responses.
"""

from fastapi.testclient import TestClient

from src.api.api_server import app


client = TestClient(app)


def test_immigration_advice_endpoint():
    """Tests the /immigration-advice/ endpoint.

    Verifies that:
    1. The endpoint returns a successful response (status code 200).
    2. The response is a valid JSON object.
    3. The response contains the expected keys for the processed results.
    """
    payload = {
        "text": "I am on an expired F-1 visa and want to apply for a work permit."
    }

    response = client.post("/immigration-advice/", json=payload)

    assert response.status_code == 200

    response_data = response.json()
    assert isinstance(response_data, dict)

    expected_keys = [
        "intake_summary",
        "plain_language",
        "research_findings",
        "application_guide",
        "compliance_check",
        "lawyer_recommendations",
    ]
    for key in expected_keys:
        assert key in response_data
