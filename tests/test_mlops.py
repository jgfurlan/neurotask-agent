import pytest
from fastapi.testclient import TestClient

from ocean_vortex.api.main import app

client = TestClient(app)

def test_neptune_telemetry_normal() -> None:
    response = client.post(
        "/ocean/neptune/telemetry",
        json={
            "vessel_id": "VESSEL-001",
            "timestamp": "2026-05-25T12:00:00Z",
            "parameters": {
                "fuel_consumption": 50.0,
                "speed_knots": 15.0
            }
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["is_anomaly"] is False
    assert data["anomaly_score"] <= 0.8
    assert "normal" in data["message"].lower()

def test_neptune_telemetry_anomaly() -> None:
    response = client.post(
        "/ocean/neptune/telemetry",
        json={
            "vessel_id": "VESSEL-001",
            "timestamp": "2026-05-25T12:00:00Z",
            "parameters": {
                "fuel_consumption": 95.0,
                "speed_knots": 25.0
            }
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["is_anomaly"] is True
    assert data["anomaly_score"] > 0.8
    assert "CRITICAL" in data["message"]

def test_food_forecast() -> None:
    response = client.post(
        "/ocean/operations/food-forecast",
        json={
            "voyage_id": "VOY-777",
            "passenger_count": 4000,
            "demographic_distribution": {
                "gen_z": 0.2,
                "millennials": 0.4,
                "boomers": 0.4
            }
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["confidence_interval"] == 92.5
    assert data["waste_reduction_estimate_kg"] > 0
    assert "proteins_kg" in data["predicted_consumption_kg"]
