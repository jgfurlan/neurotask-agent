from typing import Any
from uuid import UUID

# Mock databases for Guest Genome
MOCK_GUEST_DATABASE: dict[UUID, dict[str, Any]] = {
    UUID("4a7114b0-681b-4b20-9430-863a15234de1"): {
        "full_name": "Alexander Mercer",
        "medallion_status": "Ruby",
        "preferences": {
            "dietary_restrictions": ["gluten-free"],
            "beverage_preferences": ["Mojito", "Sparkling Water"],
            "activity_interests": ["Snorkeling", "Live Music", "Wine Tasting"]
        }
    },
    UUID("5b8225c1-792c-4c31-8541-974a26355ef2"): {
        "full_name": "Junior Mercer",
        "medallion_status": "Gold",
        "preferences": {
            "dietary_restrictions": ["alcohol-free"],
            "beverage_preferences": ["Cola", "Juice"],
            "activity_interests": ["Arcade", "Water Slide"]
        }
    }
}
