"""Defines the LawyerMatchTask for the Immigration AI Agent system.

This module creates a task that instructs the LawyerMatchAgent to
recommend immigration attorneys based on the user's specific case
type, location, and preferences.
"""

from crewai import Task


class LawyerMatchTask(Task):
    """A task for recommending immigration lawyers.

    This task asks the agent to search the lawyer directory and match
    the user with qualified attorneys for their case type.
    """

    def __init__(self):
        """Initializes the LawyerMatchTask."""
        super().__init__(
            description=(
                "Based on the user's immigration case details, find and recommend lawyers:\n"
                "1. Identify the speciality needed (asylum, employment, family, deportation defense, etc.)\n"
                "2. Consider the user's geographic location\n"
                "3. Factor in language preferences if mentioned\n"
                "4. Provide at least 2-3 lawyer recommendations\n"
                "5. Include each lawyer's name, firm, speciality, rating, and consultation fee\n"
                "6. Add a brief note on why each lawyer is a good match for this specific case"
            ),
            expected_output=(
                "A list of 2-3 recommended immigration lawyers with their details, "
                "speciality match, and a personalized reason for the recommendation."
            ),
        )
