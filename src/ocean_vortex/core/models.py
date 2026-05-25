from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field


class LocationContext(BaseModel):
    deck: int = Field(..., description="Deck level of the guest location context")
    zone: str = Field(..., description="Zone name of the guest location context")
    timestamp: str = Field(..., description="ISO 8601 timestamp of the reading")


class ChatRequest(BaseModel):
    guest_id: UUID = Field(
        ..., description="Unique ID corresponding to the guest's OceanMedallion"
    )
    message: str = Field(
        ..., description="Speech-to-text input or typed message from the passenger"
    )
    location_context: LocationContext | None = Field(
        None, description="Optional real-time IoT spatial context"
    )


class SuggestedAction(BaseModel):
    label: str = Field(..., description="Display label for the interactive button in UI")
    action_type: str = Field(
        ..., description="Action ID to map to a client-side route/action"
    )
    params: dict[str, Any] = Field(
        default_factory=dict,
        description="Metadata parameters for the action execution",
    )


class ChatResponse(BaseModel):
    response: str = Field(..., description="AI agent response text")
    suggested_actions: list[SuggestedAction] = Field(
        default_factory=list, description="Proactive interface actions"
    )


class GuestPreferences(BaseModel):
    dietary_restrictions: list[str] = Field(
        default_factory=list, description="E.g., gluten-free, vegan"
    )
    beverage_preferences: list[str] = Field(
        default_factory=list, description="List of favorite beverages"
    )
    activity_interests: list[str] = Field(
        default_factory=list, description="Excursion or event types of interest"
    )


class GuestProfileResponse(BaseModel):
    guest_id: UUID = Field(
        ..., description="Unique identifier matching the OceanMedallion digital twin"
    )
    full_name: str = Field(..., description="Full name of the passenger")
    medallion_status: str = Field(..., description="Tier status, e.g., Gold, Ruby, Platinum")
    preferences: GuestPreferences = Field(
        ..., description="Dynamic guest genomics preference mappings"
    )


class DeliverToCoordinates(BaseModel):
    deck: int = Field(..., description="Ship deck level")
    zone: str = Field(..., description="Specific zone name")
    latitude: float = Field(..., description="Simulated coordinates or indoor grid latitude")
    longitude: float = Field(..., description="Simulated coordinates or indoor grid longitude")


class ServiceOrderRequest(BaseModel):
    guest_id: UUID = Field(..., description="Ordering guest's ID")
    item_id: str = Field(..., description="POS identifier of the ordered item")
    item_name: str = Field(..., description="Item name")
    quantity: int = Field(..., description="Quantity to purchase")
    deliver_to_coordinates: DeliverToCoordinates = Field(
        ..., description="Delivery coordinate target"
    )


class ServiceOrderResponse(BaseModel):
    order_id: str = Field(
        ..., description="Unique identifier of the POS order transaction"
    )
    status: str = Field(
        ..., description="Order lifecycle status, e.g., dispatched, pending"
    )
    estimated_delivery_minutes: int = Field(
        ..., description="Estimated delivery timeframe in minutes"
    )
    message: str = Field(..., description="Response message for screen layout feedback")


class NeptuneTelemetryRequest(BaseModel):
    vessel_id: str = Field(..., description="Unique vessel identifier")
    timestamp: str = Field(..., description="ISO 8601 timestamp of telemetry reading")
    parameters: dict[str, float] = Field(..., description="28 navigational and safety parameters")


class NeptuneAnomalyResponse(BaseModel):
    anomaly_score: float = Field(..., description="Probability of anomaly (0.0 to 1.0)")
    is_anomaly: bool = Field(..., description="Boolean flag if threshold is breached")
    affected_systems: list[str] = Field(default_factory=list, description="List of systems affected")
    message: str = Field(..., description="Alert or status message")


class FoodForecastRequest(BaseModel):
    voyage_id: str = Field(..., description="Voyage identifier")
    passenger_count: int = Field(..., description="Total passenger count onboard")
    demographic_distribution: dict[str, float] = Field(..., description="Age/region demographic splits")


class FoodForecastResponse(BaseModel):
    predicted_consumption_kg: dict[str, float] = Field(..., description="Predicted kg per food category")
    waste_reduction_estimate_kg: float = Field(..., description="Estimated kg of food waste avoided")
    confidence_interval: float = Field(..., description="Prediction confidence percentage")
