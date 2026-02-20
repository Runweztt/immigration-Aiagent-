"""Immigration-specific tools for the Immigration AI Agent system.

This module provides domain-specific tools that agents use to look up
immigration data, search lawyer directories, and retrieve form guidance.
All tools are currently mocked stubs returning representative sample data.
"""

import logging
from typing import Any

from crewai.tools import BaseTool

logger = logging.getLogger(__name__)


class ImmigrationLookupTool(BaseTool):
    """Tool for looking up visa categories, requirements, and processing times.

    This tool simulates querying an immigration database for information
    about specific visa types, eligibility criteria, and current USCIS
    processing timelines.
    """

    name: str = "immigration_lookup"
    description: str = "Look up visa categories, eligibility requirements, and processing times"

    async def _run(self, query: str) -> dict[str, Any]:
        """Run the immigration lookup tool.

        Args:
            query: A search query describing the visa type or immigration topic.

        Returns:
            A dictionary containing visa information, requirements, and timelines.
        """
        logger.debug(f"ImmigrationLookupTool called with query: {query}")
        return {
            "visa_type": "H-1B",
            "category": "Employment-Based",
            "eligibility": [
                "Bachelor's degree or equivalent in a specialty occupation",
                "Job offer from a US employer",
                "Employer must file a Labor Condition Application (LCA)",
            ],
            "processing_time": "3-6 months (regular), 15 days (premium)",
            "filing_fee": "$460 base + $500 fraud prevention fee",
            "annual_cap": "65,000 regular + 20,000 advanced degree exemption",
        }


class LawyerDirectoryTool(BaseTool):
    """Tool for searching immigration lawyers by speciality and location.

    This tool simulates querying a lawyer directory to find attorneys
    who specialize in relevant immigration case types within a given region.
    """

    name: str = "lawyer_directory"
    description: str = "Search for immigration lawyers by speciality and geographic location"

    async def _run(self, speciality: str, location: str = "United States") -> list[dict[str, Any]]:
        """Run the lawyer directory search tool.

        Args:
            speciality: The immigration law speciality (e.g., asylum, work visa, family).
            location: The geographic region to search in.

        Returns:
            A list of dictionaries, each representing a recommended lawyer.
        """
        logger.debug(f"LawyerDirectoryTool called with speciality={speciality}, location={location}")
        return [
            {
                "name": "Jane Smith, Esq.",
                "firm": "Smith Immigration Law",
                "speciality": speciality,
                "location": location,
                "rating": 4.8,
                "languages": ["English", "Spanish"],
                "consultation_fee": "Free initial consultation",
            },
            {
                "name": "David Chen, Esq.",
                "firm": "Chen & Associates Immigration",
                "speciality": speciality,
                "location": location,
                "rating": 4.9,
                "languages": ["English", "Mandarin"],
                "consultation_fee": "$150/hour",
            },
        ]


class FormGuideTool(BaseTool):
    """Tool for retrieving required documents and forms for a given visa type.

    This tool simulates looking up the official forms, supporting documents,
    and filing instructions needed for a specific immigration application.
    """

    name: str = "form_guide"
    description: str = "Get required forms, documents, and filing instructions for a visa application"

    async def _run(self, visa_type: str) -> dict[str, Any]:
        """Run the form guide tool.

        Args:
            visa_type: The visa type or immigration benefit being applied for.

        Returns:
            A dictionary containing forms, documents, and step-by-step instructions.
        """
        logger.debug(f"FormGuideTool called with visa_type: {visa_type}")
        return {
            "visa_type": visa_type,
            "primary_form": "I-129 (Petition for Nonimmigrant Worker)",
            "supporting_forms": [
                "I-129 Data Collection Supplement",
                "ETA-9035 (Labor Condition Application)",
            ],
            "required_documents": [
                "Valid passport",
                "Educational credential evaluation",
                "Employer support letter",
                "Resume/CV",
                "Pay stubs or employment verification",
            ],
            "filing_instructions": [
                "Step 1: Employer files LCA with Department of Labor",
                "Step 2: Once LCA is certified, employer files I-129 with USCIS",
                "Step 3: Wait for USCIS receipt notice",
                "Step 4: Attend biometrics appointment if required",
                "Step 5: Receive approval notice or RFE",
            ],
        }
