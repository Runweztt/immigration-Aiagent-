"""Initializes the tasks package for the Immigration AI Agent system.

This module aggregates all specialized task classes from the `tasks` package,
making them easily accessible for use in defining agent workflows (crews).
Each task class represents a specific, self-contained unit of work that an
agent can execute.
"""

from src.tasks.compliance_check_task import ComplianceCheckTask
from src.tasks.guide_application_task import GuideApplicationTask
from src.tasks.intake_task import IntakeTask
from src.tasks.lawyer_match_task import LawyerMatchTask
from src.tasks.research_immigration_task import ResearchImmigrationTask
from src.tasks.simplify_language_task import SimplifyLanguageTask


__all__ = [
    "IntakeTask",
    "SimplifyLanguageTask",
    "ResearchImmigrationTask",
    "GuideApplicationTask",
    "ComplianceCheckTask",
    "LawyerMatchTask",
]
