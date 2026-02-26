"""Initializes the agents package and provides a factory for creating immigration agent crews.

This module aggregates the specialized agent classes and exports them for easy access.
The `create_immigration_crew` function assembles 3 optimized agents for the
immigration assistance workflow.
"""

from crewai import Agent

from src.agents.immigration_research_agent import ImmigrationResearchAgent
from src.agents.intake_agent import IntakeAgent
from src.agents.response_agent import ResponseAgent


def create_immigration_crew(llm: any) -> list[Agent]:
    """Creates and returns a list of all immigration agents for the assistance crew.

    Uses 3 consolidated agents for optimal speed:
    1. IntakeAgent — extracts user context from the query
    2. ImmigrationResearchAgent — researches requirements and application steps
    3. ResponseAgent — produces the final concise user-facing answer

    Args:
        llm: The language model instance to be used by all agents.

    Returns:
        A list of configured Agent instances.
    """
    return [
        IntakeAgent(llm),
        ImmigrationResearchAgent(llm),
        ResponseAgent(llm),
    ]
