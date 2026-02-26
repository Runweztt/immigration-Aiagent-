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

    def __init__(self, agent):
        """Initializes the IntakeTask."""
        super().__init__(
            agent=agent,
            description=(
                "Analyze the following immigration query and extract the information listed below.\n\n"
                "USER CONTEXT:\n"
                "Name: {user_name}\n"
                "Country of origin: {user_country}\n"
                "Currently living in: {user_location}\n\n"
                "USER QUERY:\n{query}\n\n"
                "Extract:\n"
                "1. Nationality / country of origin\n"
                "2. Current location (where the user lives now)\n"
                "3. Destination country\n"
                "4. Current visa type (if any)\n"
                "5. Current immigration status (e.g., valid, expired, pending)\n"
                "6. Desired outcome (e.g., study permit, work permit, permanent residence)\n"
                "7. Any relevant personal details (family ties, employer, timeline)\n\n"
                "If any information is missing, note it as 'Not provided'.\n"
                "Be concise. Use plain text, no markdown headers."
            ),
            expected_output=(
                "A brief structured summary containing: name, nationality, current_location, "
                "destination_country, current_visa_type, immigration_status, desired_outcome, "
                "and additional_details. Keep it under 150 words."
            ),
        )
