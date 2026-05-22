from typing import Any
from uuid import UUID

from fastapi import FastAPI, HTTPException, status
from langchain_core.messages import HumanMessage

from ocean_cortex_agent.agent import AgentState, ocean_cortex_graph
from ocean_cortex_agent.dto import (
    ChatRequest,
    ChatResponse,
    GuestPreferences,
    GuestProfileResponse,
    ServiceOrderRequest,
    ServiceOrderResponse,
    SuggestedAction,
)

app = FastAPI(
    title="OceanCortex Agent Service",
    description=(
        "Intelligence and multi-agent coordination layer for "
        "Carnival OceanMedallion ecosystem"
    ),
    version="0.1.0"
)

from ocean_cortex_agent.db import MOCK_GUEST_DATABASE


@app.get("/hello")
async def read_hello() -> dict[str, str]:
    """Basic health check endpoint."""
    return {"message": "Hello from OceanCortex Python Agent"}

@app.get("/ocean/guest/profile", response_model=GuestProfileResponse)
async def get_guest_profile(guest_id: UUID) -> GuestProfileResponse:
    """Retrieves guest profile genome context matching a specific OceanMedallion ID."""
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

@app.post("/ocean/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """Chats with the multi-agent orchestrator to guide reservations, schedules, or queries."""
    # Execute the stateful LangGraph workflow
    inputs: AgentState = {
        "guest_id": str(request.guest_id),
        "messages": [HumanMessage(content=request.message)],
        "next_node": "",
        "context": {}
    }
    
    result = ocean_cortex_graph.invoke(inputs)
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
async def create_order(request: ServiceOrderRequest) -> ServiceOrderResponse:
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
