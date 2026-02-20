"""Defines the IntakeAgent for the Immigration AI Agent system.

This module creates an agent that specializes in extracting personal
identity information from user queries, including nationality, current
visa type, immigration status, and desired outcome.
"""

from crewai import Agent

from src.tools.immigration_tools import ImmigrationLookupTool
from src.tools.web_tools import WebSearchTool


class IntakeAgent(Agent):
    """An agent that extracts user context from an immigration query.

    The IntakeAgent is the first step in the crew. It parses the user's
    input to identify key details such as their nationality, current
    immigration status, visa type, and what they are trying to achieve.

    Attributes:
        agent (Agent): The crewAI agent configured for this role.
    """

    def __init__(self, llm: any):
        """Initializes the IntakeAgent.

        Args:
            llm: The language model instance to be used by the agent.
        """
        super().__init__(
            role="Immigration Intake Specialist",
            goal="Extract nationality, current visa status, and desired immigration outcome from user queries",
            backstory=(
                "You are an experienced immigration intake officer. You carefully read "
                "each query to identify the person's country of origin, current immigration "
                "status, visa type if any, and what outcome they are hoping for. You are "
                "thorough and never make assumptions about missing information."
            ),
            llm=llm,
            tools=[ImmigrationLookupTool(), WebSearchTool()],
            allow_delegation=False,
            verbose=True,
        )
