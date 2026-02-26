"""Defines the ResponseAgent for the Immigration AI Agent system.

This module creates an agent that produces the final user-facing response.
It combines plain-language explanation, compliance verification, and
professional recommendations into one concise answer.
"""

from crewai import Agent

from src.tools.immigration_tools import ImmigrationLookupTool, LawyerDirectoryTool
from src.tools.web_tools import WebSearchTool


class ResponseAgent(Agent):
    """An agent that produces the final concise, user-facing immigration response.

    This agent takes the intake summary and research findings, then produces
    a single clear answer in plain language. It verifies accuracy against
    official sources and includes professional recommendations when relevant.
    """

    def __init__(self, llm: any):
        """Initializes the ResponseAgent.

        Args:
            llm: The language model instance to be used by the agent.
        """
        super().__init__(
            role="Immigration Response Advisor",
            goal="Produce a single concise, accurate, plain-language immigration answer for the user",
            backstory=(
                "You are a senior immigration advisor who communicates complex immigration "
                "processes in simple, clear language anyone can understand. You verify all "
                "information against official sources before responding. You provide "
                "actionable advice and recommend qualified professionals when appropriate. "
                "You NEVER use jargon without explaining it. You keep your responses "
                "concise and directly address what the user asked — no filler, no fluff."
            ),
            llm=llm,
            tools=[ImmigrationLookupTool(), LawyerDirectoryTool(), WebSearchTool()],
            allow_delegation=False,
            verbose=True,
        )
