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
    government sources for the relevant country to flag any inaccuracies,
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
            goal="Cross-check all immigration advice against official government sources for the relevant country",
            backstory=(
                "You are a compliance officer with a legal background in international "
                "immigration law. You verify claims against official government sources "
                "for the relevant country — IRCC (Canada), USCIS (USA), UK Home Office, "
                "etc. If something cannot be verified, you flag it clearly. "
                "You are concise and only report issues, not repeat verified information."
            ),
            llm=llm,
            tools=[ImmigrationLookupTool(), WebSearchTool()],
            allow_delegation=False,
            verbose=True,
        )
