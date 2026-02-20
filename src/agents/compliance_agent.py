"""Defines the ComplianceAgent for the Immigration AI Agent system.

This module creates an agent responsible for cross-checking all advice
and information against official government sources to ensure that the
guidance provided to the user is accurate and legally sound.
"""

from crewai import Agent

from src.tools.immigration_tools import ImmigrationLookupTool
from src.tools.web_tools import WebSearchTool


class ComplianceAgent(Agent):
    """An agent that verifies immigration advice against official sources.

    This agent acts as the quality-control gate. It reviews all outputs
    from the other agents and cross-references them with authoritative
    government sources (USCIS, DOS, etc.) to flag any inaccuracies,
    outdated information, or potentially misleading advice.

    Attributes:
        agent (Agent): The crewAI agent configured for this role.
    """

    def __init__(self, llm: any):
        """Initializes the ComplianceAgent.

        Args:
            llm: The language model instance to be used by the agent.
        """
        super().__init__(
            role="Immigration Compliance Verifier",
            goal="Cross-check all immigration advice against official government sources for accuracy",
            backstory=(
                "You are a compliance officer with a legal background in immigration law. "
                "Your job is to ensure that no incorrect or outdated information reaches the "
                "user. You verify every claim against official USCIS, Department of State, "
                "and DOL sources. If something cannot be verified, you flag it clearly."
            ),
            llm=llm,
            tools=[ImmigrationLookupTool(), WebSearchTool()],
            allow_delegation=False,
            verbose=True,
        )
