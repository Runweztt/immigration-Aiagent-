"""Defines the ComplianceCheckTask for the Immigration AI Agent system.

This module creates a task that instructs the ComplianceAgent to
cross-check all advice and information against official government
sources to ensure accuracy.
"""

from crewai import Task


class ComplianceCheckTask(Task):
    """A task for verifying immigration advice against official sources.

    This task asks the agent to review all outputs from previous agents
    and verify their accuracy and currency against authoritative sources.
    """

    def __init__(self):
        """Initializes the ComplianceCheckTask."""
        super().__init__(
            description=(
                "Review all information provided by the previous agents and verify:\n"
                "1. Are the visa requirements accurate and current?\n"
                "2. Are the processing times up to date?\n"
                "3. Are the forms and fees correct?\n"
                "4. Do the steps align with official USCIS/DOS procedures?\n"
                "5. Are there any disclaimers or caveats that should be added?\n\n"
                "Flag any information that cannot be verified or may be outdated. "
                "Add a confidence score (high/medium/low) for each section."
            ),
            expected_output=(
                "A compliance report with: verification_status for each section, "
                "confidence_scores, flagged_issues, and recommended_disclaimers."
            ),
        )
