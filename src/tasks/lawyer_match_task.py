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

    def __init__(self, agent):
        """Initializes the LawyerMatchTask."""
        super().__init__(
            agent=agent,
            description=(
                "Based on the user's immigration case details, find and recommend professionals:\n"
                "1. Identify the speciality needed (study permits, work permits, asylum, family, etc.)\n"
                "2. Consider the user's destination country and current location\n"
                "3. Factor in language preferences if mentioned\n"
                "4. Provide 2-3 recommendations with name, speciality, and contact method\n\n"
                "Keep it brief. Under 150 words."
            ),
            expected_output=(
                "A list of 2-3 recommended immigration professionals with their details "
                "and a brief reason for the recommendation. Under 150 words."
            ),
        )
