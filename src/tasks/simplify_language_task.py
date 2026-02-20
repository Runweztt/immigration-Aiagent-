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

    def __init__(self):
        """Initializes the SimplifyLanguageTask."""
        super().__init__(
            description=(
                "Review the intake summary and any immigration terminology mentioned. "
                "Identify all complex legal terms, acronyms, and jargon. Rewrite each one "
                "in plain, simple language that someone with no legal background can understand.\n\n"
                "Examples of terms to simplify:\n"
                "- 'Adjustment of Status' → 'Changing your visa to a green card while in the US'\n"
                "- 'RFE' → 'Request for Evidence — USCIS asking you for more documents'\n"
                "- 'NTA' → 'Notice to Appear — a document that starts removal proceedings'"
            ),
            expected_output=(
                "A glossary-style breakdown of all immigration terms found, "
                "each with a plain-language explanation."
            ),
        )
