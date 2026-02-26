"""Defines the SimplifyLanguageTask for the Immigration AI Agent system.

This module creates a task that instructs the PlainLanguageAgent to
rewrite any complex legal or immigration terminology found in the
context into clear, accessible language.
"""

from crewai import Task


class SimplifyLanguageTask(Task):
    """A task for simplifying immigration legal jargon.

    This task asks the agent to identify complex terms and rewrite
    them so that a non-expert can easily understand them.
    """

    def __init__(self, agent):
        """Initializes the SimplifyLanguageTask."""
        super().__init__(
            agent=agent,
            description=(
                "Review the intake summary and any immigration terminology mentioned. "
                "Identify all complex legal terms, acronyms, and jargon. Rewrite each one "
                "in plain, simple language that someone with no legal background can understand.\n\n"
                "Examples of terms to simplify:\n"
                "- 'Study permit' → 'Official permission to study in another country'\n"
                "- 'Letter of Acceptance (LOA)' → 'A letter from the university confirming they accepted you'\n"
                "- 'Proof of funds' → 'Bank statements showing you have enough money'\n\n"
                "Keep it brief — only explain terms the user actually needs."
            ),
            expected_output=(
                "A short glossary of immigration terms found, "
                "each with a plain-language explanation. Under 150 words."
            ),
        )
