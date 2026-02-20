"""Defines the PlainLanguageAgent for the Immigration AI Agent system.

This module creates an agent responsible for rewriting complex immigration
and legal terminology into clear, accessible language that any user can
understand, regardless of their education level or native language.
"""

from crewai import Agent

from src.tools.web_tools import WebSearchTool


class PlainLanguageAgent(Agent):
    """An agent that simplifies immigration and legal jargon.

    This agent takes the technical legal language found in immigration
    policies, forms, and procedures, and rewrites it in plain, everyday
    English. It considers the user's background to tailor explanations
    appropriately.

    Attributes:
        agent (Agent): The crewAI agent configured for this role.
    """

    def __init__(self, llm: any):
        """Initializes the PlainLanguageAgent.

        Args:
            llm: The language model instance to be used by the agent.
        """
        super().__init__(
            role="Plain Language Immigration Advisor",
            goal="Rewrite complex immigration legal terms into simple, easy-to-understand language",
            backstory=(
                "You are a multilingual communication specialist with deep knowledge of "
                "immigration law. You excel at breaking down complex legal concepts like "
                "'adjustment of status', 'consular processing', or 'notice to appear' into "
                "plain language that anyone can understand. You always explain acronyms and "
                "use real-world analogies."
            ),
            llm=llm,
            tools=[WebSearchTool()],
            allow_delegation=False,
            verbose=True,
        )
