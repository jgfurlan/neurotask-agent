"""
OceanVortex Couchbase Edge Client
Simulates Carnival's offline-first Couchbase Lite/Server Edge layer.

In production, this connects to a Couchbase Server cluster running on the ship's
local network. Guest profiles, POS orders, and IoT context are stored here for
sub-millisecond access even when satellite uplink is unavailable.

This mock uses an in-memory dict to replicate the Couchbase KV (Key-Value) API
pattern: get_document(key), upsert_document(key, value).
"""

from typing import Any
from uuid import UUID

from fastapi import HTTPException, status

from ..core.models import GuestPreferences, GuestProfileResponse

# ---------------------------------------------------------------------------
# Seed data — canonical guest profiles for deterministic tests & demos
# ---------------------------------------------------------------------------

_OCEAN_VORTEX_COUCHBASE_EDGE_SEED: dict[str, dict[str, Any]] = {
    "guest::4a7114b0-681b-4b20-9430-863a15234de1": {
        "guest_id": "4a7114b0-681b-4b20-9430-863a15234de1",
        "full_name": "Alexander Mercer",
        "medallion_status": "Ruby",
        "preferences": {
            "dietary_restrictions": ["gluten-free"],
            "beverage_preferences": ["Mojito", "Sparkling Water"],
            "activity_interests": ["Snorkeling", "Live Music", "Wine Tasting"],
        },
    },
    "guest::5b8225c1-792c-4c31-8541-974a26355ef2": {
        "guest_id": "5b8225c1-792c-4c31-8541-974a26355ef2",
        "full_name": "Junior Mercer",
        "medallion_status": "Gold",
        "preferences": {
            "dietary_restrictions": ["alcohol-free"],
            "beverage_preferences": ["Cola", "Juice"],
            "activity_interests": ["Arcade", "Water Slide"],
        },
    },
}


class CouchbaseEdgeClient:
    """
    Mock Couchbase KV client for the ship's Edge database.

    Replicates the Couchbase SDK pattern:
        bucket.default_collection().get(key)
        bucket.default_collection().upsert(key, value)
    """

    def __init__(self) -> None:
        self._store: dict[str, dict[str, Any]] = dict(_OCEAN_VORTEX_COUCHBASE_EDGE_SEED)

    # -- KV operations -------------------------------------------------------

    def ocean_vortex_couchbase_get_document(self, key: str) -> dict[str, Any]:
        """Retrieve a document by key. Raises HTTPException 404 if missing."""
        doc = self._store.get(key)
        if doc is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Document '{key}' not found in Couchbase Edge bucket",
            )
        return doc

    def ocean_vortex_couchbase_upsert_document(
        self, key: str, value: dict[str, Any]
    ) -> None:
        """Insert or update a document by key."""
        self._store[key] = value

    # -- Domain helpers ------------------------------------------------------

    def ocean_vortex_couchbase_get_guest_profile(
        self, guest_id: UUID
    ) -> GuestProfileResponse:
        """Fetch a guest profile from Edge KV and return typed Pydantic model."""
        key = f"guest::{guest_id}"
        data = self.ocean_vortex_couchbase_get_document(key)
        return GuestProfileResponse(
            guest_id=guest_id,
            full_name=data["full_name"],
            medallion_status=data["medallion_status"],
            preferences=GuestPreferences(**data["preferences"]),
        )


# ---------------------------------------------------------------------------
# Singleton factory
# ---------------------------------------------------------------------------

_edge_client: CouchbaseEdgeClient | None = None


def ocean_vortex_get_couchbase_edge_client() -> CouchbaseEdgeClient:
    """Return singleton CouchbaseEdgeClient instance."""
    global _edge_client
    if _edge_client is None:
        _edge_client = CouchbaseEdgeClient()
    return _edge_client
