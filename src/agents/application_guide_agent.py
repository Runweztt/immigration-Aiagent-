"""Defines the ApplicationGuideAgent for the Immigration AI Agent system.

This module creates an agent that generates step-by-step guidance for
immigration applications, including required forms, documents, fees,
and deadlines.
"""

from crewai import Agent

from src.tools.immigration_tools import FormGuideTool, ImmigrationLookupTool
from src.tools.web_tools import WebSearchTool


class ApplicationGuideAgent(Agent):
    """An agent that provides step-by-step immigration application guidance.

    This agent synthesizes the user's situation and research findings to
    produce a clear, ordered checklist of steps needed to complete their
    immigration application. It covers forms, supporting documents, fees,
    and important deadlines.

    Attributes:
        agent (Agent): The crewAI agent configured for this role.
    """

    def __init__(self, llm: any):
        """Initializes the ApplicationGuideAgent.

        Args:
            llm: The language model instance to be used by the agent.
        """
        super().__init__(
            role="Immigration Application Guide",
            goal="Generate clear step-by-step guidance for immigration applications with forms, documents, and deadlines",
            backstory=(
                "You are a detail-oriented immigration paralegal with years of experience "
                "preparing visa applications. You know every form, every supporting document, "
                "and every fee. You create checklists that leave nothing to chance, always "
                "including filing deadlines and common pitfalls to avoid."
            ),
            llm=llm,
            tools=[FormGuideTool(), ImmigrationLookupTool(), WebSearchTool()],
            allow_delegation=False,
            verbose=True,
        )
