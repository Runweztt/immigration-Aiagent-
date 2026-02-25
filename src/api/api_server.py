"""Defines the FastAPI server for the Immigration AI Agent system.

This module creates a FastAPI application that exposes an endpoint for
processing immigration queries. It serves as the API gateway for the system.
"""

from fastapi import FastAPI
from pydantic import BaseModel

from src.main import process_immigration_query


app = FastAPI(
    title="Immigration AI Agent API",
    description="An API for processing immigration queries with a multi-agent system.",
    version="0.1.0",
)


class ImmigrationQueryRequest(BaseModel):
    """Request model for an immigration query."""

    text: str


@app.post("/immigration-advice/", summary="Process an immigration query")
async def immigration_advice_endpoint(request: ImmigrationQueryRequest) -> dict:
    """Processes an immigration query and returns structured guidance.

    This endpoint takes a user's immigration question as input, processes it
    through the multi-agent crew, and returns a dictionary containing
    intake analysis, research findings, application guidance, compliance
    verification, and lawyer recommendations.

    Args:
        request: A request object containing the immigration query text.

    Returns:
        A dictionary with the processed results.

    Example:
        Request Body:
        ```json
        {
            "text": "I am on an expired F-1 visa and want to apply for a work permit."
        }
        ```

        Response Body:
        ```json
        {
            "intake_summary": {
                "nationality": "Not provided",
                "current_visa_type": "F-1",
                "immigration_status": "expired",
                "desired_outcome": "work permit"
            },
            "plain_language": {
                "F-1": "A student visa for academic studies in the US",
                "OPT": "Optional Practical Training - work permission for students"
            },
            "research_findings": {
                "eligibility": "May qualify for OPT or change of status",
                "processing_time": "3-5 months"
            },
            "application_guide": {
                "steps": ["File I-765", "Gather documents", "Submit application"]
            },
            "compliance_check": {
                "accuracy_score": "high",
                "flagged_issues": []
            },
            "lawyer_recommendations": [
                {
                    "name": "Jane Smith, Esq.",
                    "speciality": "Employment-based immigration"
                }
            ]
        }
        ```
    """
    return process_immigration_query(request.text)
