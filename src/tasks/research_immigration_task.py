"""Defines the ResearchImmigrationTask for the Immigration AI Agent system.

This module creates a task that instructs the ImmigrationResearchAgent
to find the latest rules, policy updates, processing times, and news
relevant to the user's immigration case.
"""

from crewai import Task


class ResearchImmigrationTask(Task):
    """A task for researching current immigration rules and news.

    This task asks the agent to search for the most up-to-date
    immigration information relevant to the user's specific situation.
    """

    def __init__(self, agent):
        """Initializes the ResearchImmigrationTask."""
        super().__init__(
            agent=agent,
            description=(
                "Based on the user's extracted immigration context, research the following:\n"
                "1. Current eligibility requirements for the desired visa or status in the destination country\n"
                "2. Latest processing times from the relevant immigration authority\n"
                "3. Any recent policy changes that may affect the case\n"
                "4. Known backlogs or country-specific wait times\n\n"
                "Cite sources when possible. Keep response under 200 words. Be direct and specific."
            ),
            expected_output=(
                "A concise research summary containing: eligibility_requirements, "
                "processing_times, recent_policy_changes, and source_citations. Under 200 words."
            ),
        )
