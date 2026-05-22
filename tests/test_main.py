from fastapi.testclient import TestClient

from ocean_cortex_agent.main import app

client = TestClient(app)

def test_hello_endpoint() -> None:
    response = client.get("/hello")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello from OceanCortex Python Agent"}

def test_get_guest_profile_success() -> None:
    guest_id = "4a7114b0-681b-4b20-9430-863a15234de1"
    response = client.get(f"/ocean/guest/profile?guest_id={guest_id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["guest_id"] == guest_id
    assert data["full_name"] == "Alexander Mercer"
    assert "gluten-free" in data["preferences"]["dietary_restrictions"]
    assert "Mojito" in data["preferences"]["beverage_preferences"]

def test_get_guest_profile_not_found() -> None:
    guest_id = "00000000-0000-0000-0000-000000000000"
    response = client.get(f"/ocean/guest/profile?guest_id={guest_id}")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]

def test_chat_endpoint_excursion() -> None:
    guest_id = "4a7114b0-681b-4b20-9430-863a15234de1"
    payload = {
        "guest_id": guest_id,
        "message": "I want to go snorkeling tomorrow",
        "location_context": {
            "deck": 11,
            "zone": "Lido Pool Side",
            "timestamp": "2026-05-22T08:29:00Z"
        }
    }
    response = client.post("/ocean/chat", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    assert "suggested_actions" in data
    assert len(data["suggested_actions"]) == 1
    assert data["suggested_actions"][0]["action_type"] == "reserve_excursion"

def test_chat_endpoint_order() -> None:
    guest_id = "4a7114b0-681b-4b20-9430-863a15234de1"
    payload = {
        "guest_id": guest_id,
        "message": "Order a Mojito for me",
        "location_context": {
            "deck": 11,
            "zone": "Lido Pool Side",
            "timestamp": "2026-05-22T08:29:00Z"
        }
    }
    response = client.post("/ocean/chat", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    assert "suggested_actions" in data
    assert len(data["suggested_actions"]) == 1
    assert data["suggested_actions"][0]["action_type"] == "order_item"

def test_create_service_order() -> None:
    guest_id = "4a7114b0-681b-4b20-9430-863a15234de1"
    payload = {
        "guest_id": guest_id,
        "item_id": "BEV-004",
        "item_name": "Mojito",
        "quantity": 1,
        "deliver_to_coordinates": {
            "deck": 11,
            "zone": "Lido Pool Side",
            "latitude": 20.5015,
            "longitude": -86.9452
        }
    }
    response = client.post("/ocean/services/order", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    assert data["order_id"] == "ORD-882194"
    assert data["status"] == "dispatched"
    assert data["estimated_delivery_minutes"] == 8


def test_mock_guest_database_import() -> None:
    from ocean_cortex_agent.db import MOCK_GUEST_DATABASE
    assert MOCK_GUEST_DATABASE is not None
    assert "4a7114b0-681b-4b20-9430-863a15234de1" in [str(k) for k in MOCK_GUEST_DATABASE.keys()]

