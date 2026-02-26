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
    about specific visa types, eligibility criteria, and current
    processing timelines for any country worldwide.
    """

    name: str = "immigration_lookup"
    description: str = "Look up visa categories, eligibility requirements, and processing times for any country"

    async def _run(self, query: str) -> dict[str, Any]:
        """Run the immigration lookup tool.

        Args:
            query: A search query describing the visa type or immigration topic.

        Returns:
            A dictionary containing visa information, requirements, and timelines.
        """
        logger.debug(f"ImmigrationLookupTool called with query: {query}")
        return {
            "visa_type": "Study Permit / Student Visa",
            "category": "Temporary Residence",
            "eligibility": [
                "Letter of Acceptance from a recognized educational institution",
                "Proof of sufficient funds to cover tuition and living expenses",
                "Valid passport",
                "Clean criminal record / police clearance certificate",
                "Medical examination (if required by destination country)",
            ],
            "processing_time": "Varies by country — typically 4-12 weeks",
            "filing_fee": "Varies by country and visa type",
            "notes": "Requirements differ by destination country. Check official immigration authority.",
        }


class LawyerDirectoryTool(BaseTool):
    """Tool for searching immigration lawyers by speciality and location.

    This tool simulates querying a lawyer directory to find attorneys
    or licensed immigration consultants who specialize in relevant
    case types within a given region worldwide.
    """

    name: str = "lawyer_directory"
    description: str = "Search for immigration lawyers or consultants by speciality and location worldwide"

    async def _run(self, speciality: str, location: str = "Global") -> list[dict[str, Any]]:
        """Run the lawyer directory search tool.

        Args:
            speciality: The immigration law speciality (e.g., study permits, work visas, asylum).
            location: The geographic region to search in.

        Returns:
            A list of dictionaries, each representing a recommended professional.
        """
        logger.debug(f"LawyerDirectoryTool called with speciality={speciality}, location={location}")
        return [
            {
                "name": "Immigration Consultant A",
                "firm": "Global Immigration Services",
                "speciality": speciality,
                "location": location,
                "rating": 4.8,
                "languages": ["English", "French"],
                "consultation_fee": "Varies — contact for details",
            },
            {
                "name": "Immigration Consultant B",
                "firm": "International Visa Advisors",
                "speciality": speciality,
                "location": location,
                "rating": 4.9,
                "languages": ["English", "Spanish", "Portuguese"],
                "consultation_fee": "Initial consultation available",
            },
        ]


class FormGuideTool(BaseTool):
    """Tool for retrieving required documents and forms for a given visa type.

    This tool simulates looking up the official forms, supporting documents,
    and filing instructions needed for a specific immigration application
    in any country.
    """

    name: str = "form_guide"
    description: str = "Get required forms, documents, and filing instructions for a visa application in any country"

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
            "primary_form": "Application form (varies by destination country)",
            "supporting_forms": [
                "Identity documents (passport, birth certificate)",
                "Financial proof documents",
            ],
            "required_documents": [
                "Valid passport",
                "Passport-sized photographs",
                "Proof of funds (bank statements, sponsorship letter)",
                "Letter of Acceptance or employment offer",
                "Police clearance certificate",
                "Medical examination results (if required)",
            ],
            "filing_instructions": [
                "Step 1: Gather all required documents",
                "Step 2: Complete the application form for the destination country",
                "Step 3: Pay the application fee",
                "Step 4: Submit application (online or at embassy/consulate)",
                "Step 5: Attend biometrics appointment if required",
                "Step 6: Wait for decision",
            ],
        }
