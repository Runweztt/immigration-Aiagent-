"""Database tools for immigration case management system."""

from typing import Any

from src.tools.database_interface import ImmigrationDatabase


# Mock immigration case database
MOCK_CASE_DB = {
    "case_001": {
        "applicant_name": "John Doe",
        "nationality": "Nigerian",
        "visa_type": "F-1",
        "status": "pending_review",
        "desired_outcome": "work_permit",
        "filed_date": "2026-01-15",
    },
    "case_002": {
        "applicant_name": "Maria Garcia",
        "nationality": "Mexican",
        "visa_type": "H-1B",
        "status": "approved",
        "desired_outcome": "permanent_residency",
        "filed_date": "2025-11-20",
    },
}


async def read_case_data(case_id: str, db: ImmigrationDatabase) -> dict[str, Any]:
    """Read immigration case data from the database.

    Args:
        case_id: ID of the immigration case
        db: Database instance

    Returns:
        Case data dictionary
    """
    return await db.read_case_data(case_id)


async def propose_case_update(case_id: str, data: dict[str, Any], db: ImmigrationDatabase) -> bool:
    """Propose an update to immigration case data.

    Args:
        case_id: ID of the immigration case
        data: Data to update
        db: Database instance

    Returns:
        True if update was successful
    """
    return await db.update_case_data(case_id, data)
