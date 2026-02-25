"""Integration tests for immigration agent system."""

from unittest.mock import AsyncMock

import pytest

from src.tasks import (
    ComplianceCheckTask,
    GuideApplicationTask,
    IntakeTask,
    LawyerMatchTask,
    ResearchImmigrationTask,
    SimplifyLanguageTask,
)


@pytest.fixture
def mock_llm():
    """Create a mock LLM for testing."""
    return AsyncMock()


@pytest.fixture
def mock_db():
    """Create a mock database for testing."""
    return AsyncMock()


@pytest.fixture
def mock_logger():
    """Create a mock logger for testing."""
    return AsyncMock()


@pytest.mark.asyncio
async def test_immigration_agent_system(mock_llm, mock_db, mock_logger):
    """Test the integration of all immigration agents and tasks."""
    tasks = [
        IntakeTask(),
        SimplifyLanguageTask(),
        ResearchImmigrationTask(),
        GuideApplicationTask(),
        ComplianceCheckTask(),
        LawyerMatchTask(),
    ]

    # Verify all tasks instantiate correctly
    for task in tasks:
        assert task is not None
