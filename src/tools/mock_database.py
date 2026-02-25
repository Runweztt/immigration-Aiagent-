"""Mock database implementation for immigration case testing."""

from datetime import datetime

from src.tools.database_interface import ImmigrationDatabase


class MockImmigrationDatabase(ImmigrationDatabase):
    """Mock implementation of immigration database for testing."""

    def __init__(self):
        """Initialize the mock database."""
        self._case_data = {}
        self._audit_log = []

    async def read_case_data(self, case_id: str) -> dict[str, object]:
        """Read immigration case data from mock database.

        Args:
            case_id: The ID of the immigration case

        Returns:
            Dictionary containing case data
        """
        if case_id in self._case_data:
            return self._case_data[case_id]
        return {}

    async def update_case_data(self, case_id: str, update_data: dict[str, object]) -> bool:
        """Update immigration case data in mock database.

        Args:
            case_id: The ID of the immigration case
            update_data: Dictionary containing data to update

        Returns:
            True if update was successful, False otherwise
        """
        if case_id in self._case_data:
            self._case_data[case_id].update(update_data)
        else:
            self._case_data[case_id] = update_data
        return True

    async def log_audit_event(
        self,
        event_type: str,
        case_id: str,
        user_id: str,
        details: dict[str, object] | None = None,
    ) -> bool:
        """Log audit event in mock database.

        Args:
            event_type: Type of event being logged
            case_id: ID of the immigration case involved
            user_id: ID of the user performing the action
            details: Optional additional details about the event

        Returns:
            True if logging was successful, False otherwise
        """
        event = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "case_id": case_id,
            "user_id": user_id,
        }
        if details:
            event["details"] = details
        self._audit_log.append(event)
        return True

    def get_audit_log(self) -> list:
        """Get the audit log for testing."""
        return self._audit_log
