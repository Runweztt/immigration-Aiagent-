"""Defines the LawyerMatchAgent for the Immigration AI Agent system.

This module creates an agent that recommends immigration attorneys
based on the user's specific case type, geographic location, language
preferences, and budget considerations.
"""

from crewai import Agent

from src.tools.immigration_tools import LawyerDirectoryTool
from src.tools.web_tools import WebSearchTool


class LawyerMatchAgent(Agent):
    """An agent that matches users with immigration lawyers.

    This agent analyzes the user's case details (visa type, complexity,
    location) and searches a lawyer directory to recommend attorneys
    who specialize in the relevant area of immigration law.

    Attributes:
        agent (Agent): The crewAI agent configured for this role.
    """

    def __init__(self, llm: any):
        """Initializes the LawyerMatchAgent.

        Args:
            llm: The language model instance to be used by the agent.
        """
        super().__init__(
            role="Immigration Lawyer Matchmaker",
            goal="Recommend qualified immigration attorneys or consultants based on case type, location, and user needs",
            backstory=(
                "You are a legal referral coordinator with a worldwide network of "
                "immigration attorneys and licensed consultants. You understand the nuances "
                "of different immigration specialities — study permits, work permits, asylum, "
                "family-based, employment-based, deportation defense — and you match users "
                "with professionals who have the right expertise for their destination "
                "country, speak their language, and fit their budget. You keep recommendations brief."
            ),
            llm=llm,
            tools=[LawyerDirectoryTool(), WebSearchTool()],
            allow_delegation=False,
            verbose=True,
        )
