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

    def __init__(self):
        """Initializes the ResearchImmigrationTask."""
        super().__init__(
            description=(
                "Based on the user's extracted immigration context, research the following:\n"
                "1. Current eligibility requirements for the desired visa or status\n"
                "2. Latest processing times from USCIS\n"
                "3. Any recent policy changes or executive orders that may affect the case\n"
                "4. Relevant news or updates from the Visa Bulletin\n"
                "5. Known backlogs or country-specific wait times\n\n"
                "Always cite the source of information when possible."
            ),
            expected_output=(
                "A research report containing: eligibility_requirements, processing_times, "
                "recent_policy_changes, visa_bulletin_updates, and source_citations."
            ),
        )
