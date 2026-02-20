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

    def __init__(self):
        """Initializes the GuideApplicationTask."""
        super().__init__(
            description=(
                "Using the research findings and the user's context, create a detailed "
                "step-by-step application guide that includes:\n"
                "1. Which forms to file (with form numbers and names)\n"
                "2. Required supporting documents\n"
                "3. Filing fees and payment methods\n"
                "4. Where to file (online, by mail, specific USCIS office)\n"
                "5. Important deadlines and processing milestones\n"
                "6. Common mistakes to avoid\n"
                "7. What to expect after filing (receipt notices, biometrics, interviews)"
            ),
            expected_output=(
                "A numbered step-by-step application guide with forms, documents, "
                "fees, deadlines, and tips for avoiding common mistakes."
            ),
        )
