"""Defines the ImmigrationResearchAgent for the Immigration AI Agent system.

This module creates an agent that specializes in researching current
immigration rules, policy changes, processing times, and news updates
relevant to the user's specific situation.
"""

from crewai import Agent

from src.tools.immigration_tools import ImmigrationLookupTool
from src.tools.web_tools import WebSearchTool


class ImmigrationResearchAgent(Agent):
    """An agent that researches current immigration laws, news, and policy updates.

    This agent uses search tools and immigration databases to find the
    most current and relevant information about visa rules, processing
    times, policy changes, and immigration news that applies to the
    user's case.

    Attributes:
        agent (Agent): The crewAI agent configured for this role.
    """

    def __init__(self, llm: any):
        """Initializes the ImmigrationResearchAgent.

        Args:
            llm: The language model instance to be used by the agent.
        """
        super().__init__(
            role="Immigration Research Analyst",
            goal="Find the latest immigration rules, policy updates, processing times, and relevant news",
            backstory=(
                "You are a meticulous immigration research analyst who monitors USCIS "
                "bulletins, visa bulletin updates, executive orders, and immigration news "
                "daily. You know where to find the most authoritative and up-to-date "
                "information and you always cite your sources."
            ),
            llm=llm,
            tools=[ImmigrationLookupTool(), WebSearchTool()],
            allow_delegation=False,
            verbose=True,
        )
