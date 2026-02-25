"""Unit tests for immigration agents.

This module tests that each immigration agent is instantiated correctly
with the expected role, goal, and tools configuration.
"""

from unittest.mock import MagicMock

import pytest

from src.agents import create_immigration_crew
from src.agents.application_guide_agent import ApplicationGuideAgent
from src.agents.compliance_agent import ComplianceAgent
from src.agents.immigration_research_agent import ImmigrationResearchAgent
from src.agents.intake_agent import IntakeAgent
from src.agents.lawyer_match_agent import LawyerMatchAgent
from src.agents.plain_language_agent import PlainLanguageAgent


@pytest.fixture
def mock_llm():
    """Create a mock LLM instance for testing."""
    return MagicMock()


class TestIntakeAgent:
    """Tests for the IntakeAgent class."""

    def test_intake_agent_creation(self, mock_llm):
        """Verify IntakeAgent initializes with the correct role."""
        agent = IntakeAgent(mock_llm)
        assert agent.role == "Immigration Intake Specialist"

    def test_intake_agent_has_tools(self, mock_llm):
        """Verify IntakeAgent has the expected tools assigned."""
        agent = IntakeAgent(mock_llm)
        tool_names = [tool.name for tool in agent.tools]
        assert "immigration_lookup" in tool_names
        assert "web_search" in tool_names


class TestPlainLanguageAgent:
    """Tests for the PlainLanguageAgent class."""

    def test_plain_language_agent_creation(self, mock_llm):
        """Verify PlainLanguageAgent initializes with the correct role."""
        agent = PlainLanguageAgent(mock_llm)
        assert agent.role == "Plain Language Immigration Advisor"

    def test_plain_language_agent_has_tools(self, mock_llm):
        """Verify PlainLanguageAgent has the expected tools assigned."""
        agent = PlainLanguageAgent(mock_llm)
        tool_names = [tool.name for tool in agent.tools]
        assert "web_search" in tool_names


class TestImmigrationResearchAgent:
    """Tests for the ImmigrationResearchAgent class."""

    def test_research_agent_creation(self, mock_llm):
        """Verify ImmigrationResearchAgent initializes with the correct role."""
        agent = ImmigrationResearchAgent(mock_llm)
        assert agent.role == "Immigration Research Analyst"

    def test_research_agent_has_tools(self, mock_llm):
        """Verify ImmigrationResearchAgent has the expected tools assigned."""
        agent = ImmigrationResearchAgent(mock_llm)
        tool_names = [tool.name for tool in agent.tools]
        assert "immigration_lookup" in tool_names
        assert "web_search" in tool_names


class TestApplicationGuideAgent:
    """Tests for the ApplicationGuideAgent class."""

    def test_guide_agent_creation(self, mock_llm):
        """Verify ApplicationGuideAgent initializes with the correct role."""
        agent = ApplicationGuideAgent(mock_llm)
        assert agent.role == "Immigration Application Guide"

    def test_guide_agent_has_tools(self, mock_llm):
        """Verify ApplicationGuideAgent has the expected tools assigned."""
        agent = ApplicationGuideAgent(mock_llm)
        tool_names = [tool.name for tool in agent.tools]
        assert "form_guide" in tool_names
        assert "immigration_lookup" in tool_names


class TestComplianceAgent:
    """Tests for the ComplianceAgent class."""

    def test_compliance_agent_creation(self, mock_llm):
        """Verify ComplianceAgent initializes with the correct role."""
        agent = ComplianceAgent(mock_llm)
        assert agent.role == "Immigration Compliance Verifier"

    def test_compliance_agent_has_tools(self, mock_llm):
        """Verify ComplianceAgent has the expected tools assigned."""
        agent = ComplianceAgent(mock_llm)
        tool_names = [tool.name for tool in agent.tools]
        assert "immigration_lookup" in tool_names


class TestLawyerMatchAgent:
    """Tests for the LawyerMatchAgent class."""

    def test_lawyer_match_agent_creation(self, mock_llm):
        """Verify LawyerMatchAgent initializes with the correct role."""
        agent = LawyerMatchAgent(mock_llm)
        assert agent.role == "Immigration Lawyer Matchmaker"

    def test_lawyer_match_agent_has_tools(self, mock_llm):
        """Verify LawyerMatchAgent has the expected tools assigned."""
        agent = LawyerMatchAgent(mock_llm)
        tool_names = [tool.name for tool in agent.tools]
        assert "lawyer_directory" in tool_names


class TestCreateImmigrationCrew:
    """Tests for the create_immigration_crew factory function."""

    def test_creates_correct_number_of_agents(self, mock_llm):
        """Verify the factory creates exactly 6 agents."""
        crew = create_immigration_crew(mock_llm)
        assert len(crew) == 6

    def test_creates_correct_agent_types(self, mock_llm):
        """Verify the factory creates the correct agent types in order."""
        crew = create_immigration_crew(mock_llm)
        assert isinstance(crew[0], IntakeAgent)
        assert isinstance(crew[1], PlainLanguageAgent)
        assert isinstance(crew[2], ImmigrationResearchAgent)
        assert isinstance(crew[3], ApplicationGuideAgent)
        assert isinstance(crew[4], ComplianceAgent)
        assert isinstance(crew[5], LawyerMatchAgent)
