import os
from typing import Protocol
from uuid import UUID

from fastapi import HTTPException, status

from ..core.models import GuestPreferences, GuestProfileResponse
from .db import MOCK_GUEST_DATABASE


class SnowflakeClientProtocol(Protocol):
    """Protocol defining the interface for Snowflake Cortex AI queries."""
    
    def get_guest_profile(self, guest_id: UUID) -> GuestProfileResponse:
        ...


class LiveSnowflakeClient(SnowflakeClientProtocol):
    """Live implementation that connects to Snowflake."""
    
    def __init__(self) -> None:
        # Placeholder for actual snowflake-connector-python initialization
        self.account = os.environ.get("SNOWFLAKE_ACCOUNT")
        self.user = os.environ.get("SNOWFLAKE_USER")
        self.password = os.environ.get("SNOWFLAKE_PASSWORD")
        self.database = os.environ.get("SNOWFLAKE_DATABASE")
        self.warehouse = os.environ.get("SNOWFLAKE_WAREHOUSE")
        
        if not all([self.account, self.user, self.password, self.database, self.warehouse]):
            raise ValueError("Missing required Snowflake environment variables.")

    def get_guest_profile(self, guest_id: UUID) -> GuestProfileResponse:
        # Placeholder for actual Cortex AI queries mapping to GuestProfileResponse
        raise NotImplementedError("Live Snowflake connection is not yet implemented.")


class MockSnowflakeClient(SnowflakeClientProtocol):
    """Mock implementation returning deterministic local data for tests."""

    def get_guest_profile(self, guest_id: UUID) -> GuestProfileResponse:
        if guest_id not in MOCK_GUEST_DATABASE:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Guest profile with ID {guest_id} not found"
            )

        data = MOCK_GUEST_DATABASE[guest_id]
        return GuestProfileResponse(
            guest_id=guest_id,
            full_name=data["full_name"],
            medallion_status=data["medallion_status"],
            preferences=GuestPreferences(**data["preferences"])
        )


def get_snowflake_client() -> SnowflakeClientProtocol:
    """Factory to return the appropriate Snowflake client based on env vars."""
    use_mock = os.environ.get("USE_MOCK_SNOWFLAKE", "true").lower() == "true"
    if use_mock:
        return MockSnowflakeClient()
    
    try:
        return LiveSnowflakeClient()
    except ValueError:
        # Fallback to mock if environment variables are missing
        return MockSnowflakeClient()
