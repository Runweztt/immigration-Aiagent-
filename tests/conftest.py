"""Common test fixtures for immigration AI multi-agent system."""

import os
from unittest.mock import patch

import pytest
import requests

from src.llm.circuit_breaker import is_ollama_available, is_openai_available


# Constants
HTTP_OK = 200


def is_service_available(url: str, timeout: int = 5) -> bool:
    """Check if a service is available."""
    try:
        response = requests.get(url, timeout=timeout)
        return response.status_code == HTTP_OK
    except (requests.RequestException, TimeoutError):
        return False


@pytest.fixture
def mock_env_vars():
    """Mock environment variables for testing."""
    with patch.dict(
        os.environ,
        {
            "LLM_PROVIDER": "ANTHROPIC",
            "ANTHROPIC_API_KEY": "test-key",
            "ANTHROPIC_MODEL_NAME": "claude-sonnet-4-20250514",
            "OPENAI_API_KEY": "test-key",
            "OPENAI_MODEL_NAME": "gpt-3.5-turbo",
            "OLLAMA_BASE_URL": "http://localhost:11434",
            "OLLAMA_MODEL_NAME": "llama3",
        },
    ):
        yield


@pytest.fixture
def mock_immigration_query():
    """Mock immigration query for testing."""
    return (
        "I am a Nigerian citizen currently in the United States on an F-1 student visa. "
        "My visa expires in 3 months and I just graduated with a Master's degree in "
        "Computer Science. I want to stay and work in the US. What are my options?"
    )


@pytest.fixture
def mock_case_data():
    """Mock immigration case database."""
    return {
        "case_001": {
            "applicant_name": "John Doe",
            "nationality": "Nigerian",
            "visa_type": "F-1",
            "status": "pending_review",
            "desired_outcome": "work_permit",
            "filed_date": "2026-01-15",
        }
    }


@pytest.fixture
def ollama_available():
    """Check if Ollama service is available."""
    return is_ollama_available()


@pytest.fixture
def openai_available():
    """Check if OpenAI API is available."""
    return is_openai_available()


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers",
        "integration: mark test as integration test requiring external services",
    )
    config.addinivalue_line(
        "markers",
        "llm: mark test as requiring LLM access",
    )
    config.addinivalue_line(
        "markers",
        "slow: mark test as slow running",
    )


def pytest_runtest_setup(item):
    """Skip tests based on service availability."""
    if "integration" in item.keywords:
        if not (is_ollama_available() or is_openai_available()):
            pytest.skip("No LLM service available for integration tests")

    if "llm" in item.keywords:
        if not is_openai_available():
            pytest.skip("OpenAI API not available")
