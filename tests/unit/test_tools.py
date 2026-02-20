"""Unit tests for immigration tools.

This module tests that each immigration tool returns the expected mock
data structure when called.
"""

import asyncio

import pytest

from src.tools.immigration_tools import FormGuideTool, ImmigrationLookupTool, LawyerDirectoryTool
from src.tools.web_tools import WebSearchTool


class TestImmigrationLookupTool:
    """Tests for the ImmigrationLookupTool class."""

    def test_tool_has_correct_name(self):
        """Verify the tool has the expected name."""
        tool = ImmigrationLookupTool()
        assert tool.name == "immigration_lookup"

    def test_tool_returns_visa_info(self):
        """Verify the tool returns a dictionary with visa information."""
        tool = ImmigrationLookupTool()
        result = asyncio.get_event_loop().run_until_complete(tool._run("H-1B visa requirements"))
        assert "visa_type" in result
        assert "eligibility" in result
        assert "processing_time" in result
        assert isinstance(result["eligibility"], list)


class TestLawyerDirectoryTool:
    """Tests for the LawyerDirectoryTool class."""

    def test_tool_has_correct_name(self):
        """Verify the tool has the expected name."""
        tool = LawyerDirectoryTool()
        assert tool.name == "lawyer_directory"

    def test_tool_returns_lawyer_list(self):
        """Verify the tool returns a list of lawyer dictionaries."""
        tool = LawyerDirectoryTool()
        result = asyncio.get_event_loop().run_until_complete(tool._run("asylum", "New York"))
        assert isinstance(result, list)
        assert len(result) >= 2
        assert "name" in result[0]
        assert "speciality" in result[0]
        assert "rating" in result[0]


class TestFormGuideTool:
    """Tests for the FormGuideTool class."""

    def test_tool_has_correct_name(self):
        """Verify the tool has the expected name."""
        tool = FormGuideTool()
        assert tool.name == "form_guide"

    def test_tool_returns_form_information(self):
        """Verify the tool returns form and document guidance."""
        tool = FormGuideTool()
        result = asyncio.get_event_loop().run_until_complete(tool._run("H-1B"))
        assert "primary_form" in result
        assert "required_documents" in result
        assert "filing_instructions" in result
        assert isinstance(result["required_documents"], list)
        assert isinstance(result["filing_instructions"], list)


class TestWebSearchTool:
    """Tests for the WebSearchTool class."""

    def test_tool_has_correct_name(self):
        """Verify the tool has the expected name."""
        tool = WebSearchTool()
        assert tool.name == "web_search"

    def test_tool_returns_string_result(self):
        """Verify the tool returns a mock search result string."""
        tool = WebSearchTool()
        result = asyncio.get_event_loop().run_until_complete(tool._run("immigration policy update"))
        assert isinstance(result, str)
        assert "immigration policy update" in result
