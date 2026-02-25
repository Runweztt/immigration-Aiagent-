"""Defines the IntakeTask for the Immigration AI Agent system.

This module creates a task that instructs the IntakeAgent to extract
the user's nationality, current immigration status, visa type, and
desired outcome from their input query.
"""

from crewai import Task


class IntakeTask(Task):
    """A task for extracting immigration context from user input.

    This task asks the agent to parse the user's query and identify
    key personal details relevant to their immigration case.
    """

    def __init__(self):
        """Initializes the IntakeTask."""
        super().__init__(
            description=(
                "Analyze the user's immigration query and extract the following information:\n"
                "1. Nationality / country of origin\n"
                "2. Current visa type (if any)\n"
                "3. Current immigration status (e.g., valid, expired, pending)\n"
                "4. Desired outcome (e.g., work permit, green card, asylum)\n"
                "5. Any relevant personal details (family ties, employer, timeline)\n\n"
                "If any information is missing, note it as 'Not provided'."
            ),
            expected_output=(
                "A structured summary containing: nationality, current_visa_type, "
                "immigration_status, desired_outcome, and additional_details."
            ),
        )
