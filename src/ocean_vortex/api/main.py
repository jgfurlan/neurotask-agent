from uuid import UUID

from fastapi import FastAPI
from langchain_core.messages import HumanMessage

from ..core.agent import AgentState, ocean_vortex_graph
from ..core.models import (
    ChatRequest,
    ChatResponse,
    FoodForecastRequest,
    FoodForecastResponse,
    GuestProfileResponse,
    NeptuneAnomalyResponse,
    NeptuneTelemetryRequest,
    ServiceOrderRequest,
    ServiceOrderResponse,
    SuggestedAction,
)
from ..mlops.neptune.inference import SageMakerInferenceMock
from ..providers.snowflake import get_snowflake_client

"""
OceanVortex FastAPI Router
Centralized routing and inference for the OceanMedallion ecosystem.
This module strictly enforces Agent-Legible naming conventions.
"""

app = FastAPI(
    title="OceanVortex Agent Service",
    description=(
        "Intelligence and multi-agent coordination layer for "
        "Carnival OceanMedallion ecosystem"
    ),
    version="0.1.0"
)



@app.get("/hello")
async def ocean_vortex_api_read_health_hello() -> dict[str, str]:
    """Basic health check endpoint."""
    return {"message": "Hello from OceanVortex Python Agent"}

@app.get("/ocean/guest/profile", response_model=GuestProfileResponse)
async def ocean_vortex_api_get_digital_genome_profile(guest_id: UUID) -> GuestProfileResponse:
    """Retrieves guest profile genome context matching a specific OceanMedallion ID."""
    client = get_snowflake_client()
    return client.get_guest_profile(guest_id)

@app.post("/ocean/chat", response_model=ChatResponse)
async def ocean_vortex_api_process_llm_chat(request: ChatRequest) -> ChatResponse:
    """Chats with the multi-agent orchestrator to guide reservations, schedules, or queries."""
    # Execute the stateful LangGraph workflow
    inputs: AgentState = {
        "guest_id": str(request.guest_id),
        "messages": [HumanMessage(content=request.message)],
        "next_node": "",
        "context": {},
        "reward": 0.0
    }
    
    result = ocean_vortex_graph.invoke(inputs)
    final_content = result["messages"][-1].content
    final_output = final_content if isinstance(final_content, str) else str(final_content)
    
    # Define suggested actions based on simple matches to showcase UI integrations
    actions = []
    if "snorkeling" in request.message.lower() or "excursion" in request.message.lower():
        actions.append(SuggestedAction(
            label="Book Excursion Now",
            action_type="reserve_excursion",
            params={"excursion_id": "EXC-902", "time": "09:00"}
        ))
    elif "mojito" in request.message.lower() or "order" in request.message.lower():
        actions.append(SuggestedAction(
            label="Confirm Mojito Order",
            action_type="order_item",
            params={"item_id": "BEV-004", "quantity": 1}
        ))
        
    return ChatResponse(
        response=f"Answer: {final_output} (Context: Processed message '{request.message}')",
        suggested_actions=actions
    )

@app.post("/ocean/services/order", response_model=ServiceOrderResponse)
async def ocean_vortex_api_dispatch_pos_order(request: ServiceOrderRequest) -> ServiceOrderResponse:
    """Dispatches on-demand deliveries or bookings via the OceanNow network."""
    return ServiceOrderResponse(
        order_id="ORD-882194",
        status="dispatched",
        estimated_delivery_minutes=8,
        message=(
            f"Your {request.item_name} has been ordered and is being "
            f"routed to deck {request.deliver_to_coordinates.deck}, "
            f"zone '{request.deliver_to_coordinates.zone}'!"
        )
    )

@app.post("/ocean/neptune/telemetry", response_model=NeptuneAnomalyResponse)
async def ocean_vortex_api_process_neptune_telemetry(request: NeptuneTelemetryRequest) -> NeptuneAnomalyResponse:
    """Processes Neptune maritime telemetry via SageMaker inference."""
    return SageMakerInferenceMock.predict_neptune_anomaly(request)

@app.post("/ocean/operations/food-forecast", response_model=FoodForecastResponse)
async def ocean_vortex_api_forecast_food_waste(request: FoodForecastRequest) -> FoodForecastResponse:
    """Predicts food consumption utilizing 'Less Left Over' ML models."""
    return SageMakerInferenceMock.predict_food_forecast(request)
