"""Defines the ImmigrationResearchAgent for the Immigration AI Agent system.

This module creates an agent that researches current immigration rules,
eligibility requirements, application steps, and processing times
relevant to the user's specific situation and destination country.
"""

from crewai import Agent

from src.tools.immigration_tools import FormGuideTool, ImmigrationLookupTool
from src.tools.web_tools import WebSearchTool


class ImmigrationResearchAgent(Agent):
    """An agent that researches immigration rules and provides application guidance.

    This agent uses search tools and immigration databases to find the
    most current information about visa requirements, application steps,
    forms, fees, and processing times for the user's destination country.
    """

    def __init__(self, llm: any):
        """Initializes the ImmigrationResearchAgent.

        Args:
            llm: The language model instance to be used by the agent.
        """
        super().__init__(
            role="Immigration Research Analyst",
            goal=(
                "Research immigration requirements, application steps, forms, fees, "
                "and processing times for the user's destination country"
            ),
            backstory=(
                "You are a meticulous immigration research analyst with knowledge of "
                "immigration authorities worldwide — IRCC (Canada), USCIS (USA), "
                "UK Home Office, Schengen authorities, and others. You find the most "
                "authoritative information for the user's destination country, including "
                "eligibility requirements, required forms, fees, and step-by-step "
                "application procedures. You are concise, cite sources, and focus on "
                "what the user actually needs."
            ),
            llm=llm,
            tools=[ImmigrationLookupTool(), FormGuideTool(), WebSearchTool()],
            allow_delegation=False,
            verbose=True,
        )
