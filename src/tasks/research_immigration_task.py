"""Defines the ResearchImmigrationTask for the Immigration AI Agent system.

This module creates a task that instructs the ImmigrationResearchAgent
to find requirements, application steps, forms, fees, and processing
times for the user's destination country.
"""

from crewai import Task


class ResearchImmigrationTask(Task):
    """A task for researching immigration requirements and application steps.

    This task asks the agent to find eligibility requirements, required
    documents, application steps, fees, and processing times.
    """

    def __init__(self, agent):
        """Initializes the ResearchImmigrationTask."""
        super().__init__(
            agent=agent,
            description=(
                "Based on the user's extracted immigration context, research and provide:\n"
                "1. Eligibility requirements for the desired visa/permit in the destination country\n"
                "2. Required forms and documents\n"
                "3. Application steps (where to apply, how to submit)\n"
                "4. Fees\n"
                "5. Processing times\n"
                "6. Common mistakes to avoid\n\n"
                "Cite sources when possible. Keep response under 250 words. Be direct and specific."
            ),
            expected_output=(
                "A concise research summary with: eligibility requirements, required documents, "
                "step-by-step application process, fees, and processing times. Under 250 words."
            ),
        )
