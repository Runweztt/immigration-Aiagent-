"""Defines the ResponseTask for the Immigration AI Agent system.

This module creates a task that instructs the ResponseAgent to produce
the final user-facing answer — concise, plain language, with compliance
notes and professional recommendations.
"""

from crewai import Task


class ResponseTask(Task):
    """A task for producing the final immigration response.

    This task asks the agent to combine all research and intake information
    into one clear, actionable answer for the user.
    """

    def __init__(self, agent):
        """Initializes the ResponseTask."""
        super().__init__(
            agent=agent,
            description=(
                "Using the intake summary and research findings, produce the FINAL response "
                "for the user. This is what the user will read, so it must be:\n\n"
                "1. Written in plain, simple language — no legal jargon without explanation\n"
                "2. Directly answering what the user asked\n"
                "3. Accurate — verify key facts against official sources\n"
                "4. Actionable — tell the user exactly what steps to take\n"
                "5. Include a brief disclaimer that this is informational advice\n"
                "6. If relevant, suggest consulting an immigration professional\n\n"
                "IMPORTANT: Keep the ENTIRE response under 250 words. "
                "Use plain text. No markdown. Be direct."
            ),
            expected_output=(
                "A concise, plain-language immigration answer that directly addresses "
                "the user's question with actionable steps. Under 250 words total."
            ),
        )
