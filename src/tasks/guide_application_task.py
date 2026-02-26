"""Defines the GuideApplicationTask for the Immigration AI Agent system.

This module creates a task that instructs the ApplicationGuideAgent to
generate step-by-step guidance for the user's immigration application,
including forms, documents, fees, and deadlines.
"""

from crewai import Task


class GuideApplicationTask(Task):
    """A task for generating immigration application guidance.

    This task asks the agent to produce a comprehensive, ordered checklist
    of steps the user needs to follow for their immigration application.
    """

    def __init__(self, agent):
        """Initializes the GuideApplicationTask."""
        super().__init__(
            agent=agent,
            description=(
                "Using the research findings and the user's context, create a concise "
                "step-by-step application guide that includes:\n"
                "1. Which forms or applications to submit\n"
                "2. Required supporting documents\n"
                "3. Filing fees and payment methods\n"
                "4. Where to apply (online portal, embassy, immigration office)\n"
                "5. Key deadlines\n"
                "6. Common mistakes to avoid\n\n"
                "Keep it brief and actionable. Under 200 words."
            ),
            expected_output=(
                "A numbered step-by-step application guide with forms, documents, "
                "fees, and tips. Under 200 words."
            ),
        )
