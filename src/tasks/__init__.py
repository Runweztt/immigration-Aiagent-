"""Initializes the tasks package for the Immigration AI Agent system.

This module aggregates the task classes for the 3-agent immigration workflow.
Each task represents a specific unit of work that an agent executes.
"""

from src.tasks.intake_task import IntakeTask
from src.tasks.research_immigration_task import ResearchImmigrationTask
from src.tasks.response_task import ResponseTask


__all__ = [
    "IntakeTask",
    "ResearchImmigrationTask",
    "ResponseTask",
]
