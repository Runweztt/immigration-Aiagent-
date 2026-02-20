"""Unit tests for immigration tasks.

This module tests that each immigration task is instantiated correctly
with the expected description and expected output.
"""

import pytest

from src.tasks import (
    ComplianceCheckTask,
    GuideApplicationTask,
    IntakeTask,
    LawyerMatchTask,
    ResearchImmigrationTask,
    SimplifyLanguageTask,
)


class TestIntakeTask:
    """Tests for the IntakeTask class."""

    def test_task_has_description(self):
        """Verify the task has a non-empty description."""
        task = IntakeTask()
        assert task.description
        assert "nationality" in task.description.lower()

    def test_task_has_expected_output(self):
        """Verify the task defines an expected output."""
        task = IntakeTask()
        assert task.expected_output
        assert "nationality" in task.expected_output.lower()


class TestSimplifyLanguageTask:
    """Tests for the SimplifyLanguageTask class."""

    def test_task_has_description(self):
        """Verify the task has a non-empty description."""
        task = SimplifyLanguageTask()
        assert task.description
        assert "jargon" in task.description.lower() or "plain" in task.description.lower()

    def test_task_has_expected_output(self):
        """Verify the task defines an expected output."""
        task = SimplifyLanguageTask()
        assert task.expected_output


class TestResearchImmigrationTask:
    """Tests for the ResearchImmigrationTask class."""

    def test_task_has_description(self):
        """Verify the task has a non-empty description."""
        task = ResearchImmigrationTask()
        assert task.description
        assert "processing" in task.description.lower() or "eligibility" in task.description.lower()

    def test_task_has_expected_output(self):
        """Verify the task defines an expected output."""
        task = ResearchImmigrationTask()
        assert task.expected_output


class TestGuideApplicationTask:
    """Tests for the GuideApplicationTask class."""

    def test_task_has_description(self):
        """Verify the task has a non-empty description."""
        task = GuideApplicationTask()
        assert task.description
        assert "forms" in task.description.lower() or "step" in task.description.lower()

    def test_task_has_expected_output(self):
        """Verify the task defines an expected output."""
        task = GuideApplicationTask()
        assert task.expected_output


class TestComplianceCheckTask:
    """Tests for the ComplianceCheckTask class."""

    def test_task_has_description(self):
        """Verify the task has a non-empty description."""
        task = ComplianceCheckTask()
        assert task.description
        assert "verify" in task.description.lower() or "accurate" in task.description.lower()

    def test_task_has_expected_output(self):
        """Verify the task defines an expected output."""
        task = ComplianceCheckTask()
        assert task.expected_output


class TestLawyerMatchTask:
    """Tests for the LawyerMatchTask class."""

    def test_task_has_description(self):
        """Verify the task has a non-empty description."""
        task = LawyerMatchTask()
        assert task.description
        assert "lawyer" in task.description.lower()

    def test_task_has_expected_output(self):
        """Verify the task defines an expected output."""
        task = LawyerMatchTask()
        assert task.expected_output
