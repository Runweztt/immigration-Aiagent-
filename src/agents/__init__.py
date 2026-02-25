"""Initializes the agents package and provides a factory for creating immigration agent crews.

This module aggregates all specialized agent classes from the `agents` package and
exports them for easy access. It includes the `create_immigration_crew` function,
which assembles a list of all agent instances required for the immigration
assistance workflow.
"""

from crewai import Agent

from src.agents.application_guide_agent import ApplicationGuideAgent
from src.agents.compliance_agent import ComplianceAgent
from src.agents.immigration_research_agent import ImmigrationResearchAgent
from src.agents.intake_agent import IntakeAgent
from src.agents.lawyer_match_agent import LawyerMatchAgent
from src.agents.plain_language_agent import PlainLanguageAgent


def create_immigration_crew(llm: any) -> list[Agent]:
    """Creates and returns a list of all immigration agents for the assistance crew.

    This factory function instantiates each specialized agent with the provided
    language model and assembles them into a list, ready to be used by a CrewAI crew.

    Args:
        llm: The language model instance to be used by all agents.

    Returns:
        A list of configured Agent instances.
    """
    return [
        IntakeAgent(llm),
        PlainLanguageAgent(llm),
        ImmigrationResearchAgent(llm),
        ApplicationGuideAgent(llm),
        ComplianceAgent(llm),
        LawyerMatchAgent(llm),
    ]
