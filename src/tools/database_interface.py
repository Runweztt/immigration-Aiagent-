"""Database interface for immigration case management."""

from abc import ABC, abstractmethod


class ImmigrationDatabase(ABC):
    """Abstract base class for immigration database operations."""

    @abstractmethod
    async def read_case_data(self, case_id: str) -> dict[str, object]:
        """Read immigration case data from the database.

        Args:
            case_id: The ID of the immigration case

        Returns:
            Dictionary containing case data
        """
        pass

    @abstractmethod
    async def update_case_data(self, case_id: str, update_data: dict[str, object]) -> bool:
        """Update immigration case data in the database.

        Args:
            case_id: The ID of the immigration case
            update_data: Dictionary containing data to update

        Returns:
            True if update was successful, False otherwise
        """
        pass

    @abstractmethod
    async def log_audit_event(
        self,
        event_type: str,
        case_id: str,
        user_id: str,
        details: dict[str, object] | None = None,
    ) -> bool:
        """Log an audit event for immigration operations.

        Args:
            event_type: Type of event being logged
            case_id: ID of the immigration case involved
            user_id: ID of the user performing the action
            details: Optional additional details about the event

        Returns:
            True if logging was successful, False otherwise
        """
        pass
