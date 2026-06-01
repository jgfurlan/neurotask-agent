"""
OceanVortex Snowflake Cortex AI Provider
Handles cloud-side AI inference: LLM completions, embeddings, and RAG queries.

Guest profile lookups are NOT handled here — they live on the ship's Couchbase
Edge layer for offline-first sub-millisecond access.
"""

import os
from typing import Protocol
from uuid import UUID

from ..core.models import GuestProfileResponse
from .couchbase import ocean_vortex_get_couchbase_edge_client


class SnowflakeClientProtocol(Protocol):
    """Protocol defining the interface for Snowflake Cortex AI queries."""

    def get_guest_profile(self, guest_id: UUID) -> GuestProfileResponse:
        ...


class LiveSnowflakeClient(SnowflakeClientProtocol):
    """Live implementation that connects to Snowflake."""

    def __init__(self) -> None:
        self.account = os.environ.get("SNOWFLAKE_ACCOUNT")
        self.user = os.environ.get("SNOWFLAKE_USER")
        self.password = os.environ.get("SNOWFLAKE_PASSWORD")
        self.database = os.environ.get("SNOWFLAKE_DATABASE")
        self.warehouse = os.environ.get("SNOWFLAKE_WAREHOUSE")

        if not all([self.account, self.user, self.password, self.database, self.warehouse]):
            raise ValueError("Missing required Snowflake environment variables.")

    def get_guest_profile(self, guest_id: UUID) -> GuestProfileResponse:
        """
        Example Cortex SQL Pattern:
        SELECT
            guest_id,
            full_name,
            medallion_status,
            SNOWFLAKE.CORTEX.COMPLETE('claude-3-5-sonnet',
                'Summarize preferences for guest: ' || preferences_json) as preference_summary
        FROM GUEST_GENOMICS_TABLE
        WHERE guest_id = '{guest_id}'
        """
        raise NotImplementedError("Live Snowflake connection is not yet implemented.")

    def generate_recommendation(self, prompt: str) -> str:
        """
        Production Pattern for Cortex LLM Inference:
        sql = f"SELECT SNOWFLAKE.CORTEX.COMPLETE('claude-3-5-sonnet', '{prompt}')"
        """
        return "Cortex AI recommendation placeholder"

    def get_embeddings(self, text: str) -> list[float]:
        """
        Production Pattern for Cortex Embeddings:
        sql = f"SELECT SNOWFLAKE.CORTEX.EMBED_TEXT_768('snowflake-arctic-embed-m', '{text}')"
        """
        return [0.0] * 768


class MockSnowflakeClient(SnowflakeClientProtocol):
    """Mock implementation delegating guest profiles to Couchbase Edge."""

    def get_guest_profile(self, guest_id: UUID) -> GuestProfileResponse:
        """Delegate to Couchbase Edge — single source of truth for guest data."""
        edge = ocean_vortex_get_couchbase_edge_client()
        return edge.ocean_vortex_couchbase_get_guest_profile(guest_id)


def get_snowflake_client() -> SnowflakeClientProtocol:
    """Factory to return the appropriate Snowflake client based on env vars."""
    use_mock = os.environ.get("USE_MOCK_SNOWFLAKE", "true").lower() == "true"
    if use_mock:
        return MockSnowflakeClient()

    try:
        return LiveSnowflakeClient()
    except ValueError:
        return MockSnowflakeClient()
