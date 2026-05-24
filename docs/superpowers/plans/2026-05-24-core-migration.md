# Core Migration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Migrate core domain logic and models to the new layout.

**Architecture:** Move DTOs to `core/models.py` and agent logic to `core/agent.py`, updating internal imports to maintain functionality.

**Tech Stack:** Python, LangGraph, Pydantic

---

### Task 1: Migrate DTOs to Models

**Files:**
- Create: `src/ocean_vortex/core/models.py`
- Delete: `ocean_vortex/dto.py`

- [ ] **Step 1: Create models.py with content from dto.py**

```python
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
```

- [ ] **Step 2: Delete old dto.py**

Run: `rm ocean_vortex/dto.py`

- [ ] **Step 3: Commit migration of models**

```bash
git add src/ocean_vortex/core/models.py ocean_vortex/dto.py
git commit -m "refactor: migrate DTOs to src/ocean_vortex/core/models.py"
```

### Task 2: Migrate Agent Logic

**Files:**
- Create: `src/ocean_vortex/core/agent.py`
- Delete: `ocean_vortex/agent.py`

- [ ] **Step 1: Create agent.py with content from old agent.py and update imports**

```python
import os
from collections.abc import Sequence
from typing import Annotated, Any, TypedDict
from uuid import UUID

from fastapi import HTTPException, status
from langchain_core.callbacks import CallbackManagerForLLMRun
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage
from langchain_core.outputs import ChatGeneration, ChatResult
from langchain_core.tools import tool
from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages
from pydantic import PrivateAttr

from ocean_vortex.snowflake_client import get_snowflake_client


class AgentState(TypedDict):
    """Represents the active routing and conversation state of the LangGraph flow."""
    guest_id: str
    messages: Annotated[Sequence[BaseMessage], add_messages]
    next_node: str
    context: dict[str, Any]


# ---------------------------------------------------------------------------
# Pre-emptive context loading
# ---------------------------------------------------------------------------

def load_context_node(state: AgentState) -> dict[str, Any]:
    """Pre-emptively loads the guest profile genomics context from the database."""
    guest_id_str = state.get("guest_id")
    if not guest_id_str:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Guest ID is missing in agent state",
        )
    try:
        guest_id = UUID(guest_id_str)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid UUID format for Guest ID",
        ) from None

    client = get_snowflake_client()
    profile = client.get_guest_profile(guest_id)

    return {
        "context": {
            **state.get("context", {}),
            "guest_profile": profile,
        }
    }


# ---------------------------------------------------------------------------
# Routing tools – these define the contract the LLM uses to signal intent.
# ---------------------------------------------------------------------------

@tool
def route_to_guest_service(item_name: str, quantity: int = 1) -> str:
    """Routes the guest to the service node to order items (drinks, towels, etc.)."""
    return "Routing to guest service node"


@tool
def route_to_anticipatory_advisor(
    excursion_name: str | None = None,
    activity_query: str | None = None
) -> str:
    """Routes the guest to the advisor node to book/recommend excursions or activities."""
    return "Routing to anticipatory advisor node"


# ---------------------------------------------------------------------------
# Mock LLM – deterministic stand-in when AWS credentials are absent.
# ---------------------------------------------------------------------------

class MockChatBedrockConverse(BaseChatModel):
    """Deterministic mock that pattern-matches user messages to routing tool calls."""
    model_id: str = "mock-model"
    _bound_tools: list[Any] = PrivateAttr(default_factory=list)

    def bind_tools(
        self,
        tools: Sequence[Any],
        **kwargs: Any,
    ) -> "MockChatBedrockConverse":
        self._bound_tools = list(tools)
        return self

    def _generate(
        self,
        messages: list[BaseMessage],
        stop: list[str] | None = None,
        run_manager: CallbackManagerForLLMRun | None = None,
        **kwargs: Any,
    ) -> ChatResult:
        # Get the last HumanMessage content
        content = messages[-1].content
        text = content.lower() if isinstance(content, str) else str(content).lower()

        tool_calls: list[dict[str, Any]] = []
        ai_content = ""

        if "mojito" in text or "order" in text:
            tool_calls.append({
                "name": "route_to_guest_service",
                "args": {"item_name": "Mojito", "quantity": 1},
                "id": "call_guest_service",
                "type": "tool_call",
            })
        elif "snorkeling" in text or "excursion" in text:
            tool_calls.append({
                "name": "route_to_anticipatory_advisor",
                "args": {"excursion_name": "Snorkeling"},
                "id": "call_anticipatory_advisor",
                "type": "tool_call",
            })
        else:
            ai_content = (
                "Hello! I am the OceanMedallion digital assistant. "
                "How can I help you today?"
            )

        message = AIMessage(content=ai_content, tool_calls=tool_calls)
        return ChatResult(generations=[ChatGeneration(message=message)])

    @property
    def _llm_type(self) -> str:
        return "mock-chat-bedrock"


def get_chat_model() -> BaseChatModel:
    """Return the real Bedrock model when AWS keys exist, otherwise the mock."""
    has_aws_keys = (
        os.environ.get("AWS_ACCESS_KEY_ID") is not None
        and os.environ.get("AWS_SECRET_ACCESS_KEY") is not None
    ) or os.environ.get("AWS_PROFILE") is not None

    if has_aws_keys and os.environ.get("USE_MOCK_LLM") != "true":
        try:
            from langchain_aws import ChatBedrockConverse
            return ChatBedrockConverse(
                model="anthropic.claude-3-5-haiku-20241022-v1:0"
            )
        except Exception:
            return MockChatBedrockConverse()
    else:
        return MockChatBedrockConverse()


# ---------------------------------------------------------------------------
# Graph nodes
# ---------------------------------------------------------------------------

def supervisor_node(state: AgentState) -> dict[str, Any]:
    """Inspects guest profile context, binds tools to LLM, and invokes routing."""
    from langchain_core.messages import SystemMessage

    profile = state["context"].get("guest_profile")
    profile_str = ""
    if profile:
        profile_str = (
            f"Guest Name: {profile.full_name}\n"
            f"Medallion Status: {profile.medallion_status}\n"
            f"Interests: {', '.join(profile.preferences.activity_interests)}\n"
            f"Beverages: {', '.join(profile.preferences.beverage_preferences)}\n"
            f"Dietary: {', '.join(profile.preferences.dietary_restrictions)}"
        )

    system_prompt = (
        "You are the central supervisor node for the OceanMedallion guest experience.\n"
        "Your task is to route the user's message to the correct worker node.\n"
        "Use the following guest profile context if relevant:\n"
        f"{profile_str}\n\n"
        "Select the appropriate tool based on the user's query.\n"
        "If the request is simple chit-chat, greet the guest directly without "
        "choosing any tools."
    )

    model = get_chat_model()
    tools = [route_to_guest_service, route_to_anticipatory_advisor]
    model_with_tools = model.bind_tools(tools)

    messages = [SystemMessage(content=system_prompt)] + list(state["messages"])
    response = model_with_tools.invoke(messages)

    next_node = END
    if response.tool_calls:
        tool_name = response.tool_calls[0]["name"]
        if tool_name == "route_to_guest_service":
            next_node = "guest_service"
        elif tool_name == "route_to_anticipatory_advisor":
            next_node = "anticipatory_advisor"

    return {
        "next_node": next_node,
        "messages": [response],
    }


def guest_service_node(state: AgentState) -> dict[str, Any]:
    """Worker node that handles ordering beverages, food, or amenities."""
    last_message = state["messages"][-1]
    item_name = "unknown item"
    quantity = 1

    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        args = last_message.tool_calls[0].get("args", {})
        item_name = args.get("item_name", "unknown item")
        quantity = args.get("quantity", 1)

    return {
        "next_node": END,
        "messages": [
            AIMessage(
                content=(
                    f"I have processed your service order request "
                    f"for {item_name} (Qty: {quantity})."
                )
            )
        ],
    }


def anticipatory_advisor_node(state: AgentState) -> dict[str, Any]:
    """Worker node that handles excursion/activity recommendations."""
    last_message = state["messages"][-1]
    excursion_name = "general activities"

    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        args = last_message.tool_calls[0].get("args", {})
        excursion_name = (
            args.get("excursion_name")
            or args.get("activity_query")
            or "general activities"
        )

    return {
        "next_node": END,
        "messages": [
            AIMessage(
                content=(
                    f"I have generated your excursion recommendation "
                    f"details for {excursion_name}."
                )
            )
        ],
    }


# ---------------------------------------------------------------------------
# Build and compile the LangGraph workflow
# ---------------------------------------------------------------------------

workflow = StateGraph(AgentState)

workflow.add_node("load_context", load_context_node)
workflow.add_node("supervisor", supervisor_node)
workflow.add_node("guest_service", guest_service_node)
workflow.add_node("anticipatory_advisor", anticipatory_advisor_node)

workflow.set_entry_point("load_context")
workflow.add_edge("load_context", "supervisor")

workflow.add_conditional_edges(
    "supervisor",
    lambda state: state["next_node"],
    {
        "guest_service": "guest_service",
        "anticipatory_advisor": "anticipatory_advisor",
        END: END,
    },
)

workflow.add_edge("guest_service", END)
workflow.add_edge("anticipatory_advisor", END)

ocean_vortex_graph = workflow.compile()
```

- [ ] **Step 2: Delete old agent.py**

Run: `rm ocean_vortex/agent.py`

- [ ] **Step 3: Commit migration of agent logic**

```bash
git add src/ocean_vortex/core/agent.py ocean_vortex/agent.py
git commit -m "refactor: migrate agent logic to src/ocean_vortex/core/agent.py"
```

### Task 3: Update snowflake_client.py Imports

**Files:**
- Modify: `ocean_vortex/snowflake_client.py`

- [ ] **Step 1: Update imports from ocean_vortex.dto to ocean_vortex.core.models**

```python
<<<<
from ocean_vortex.dto import GuestPreferences, GuestProfileResponse
====
from ocean_vortex.core.models import GuestPreferences, GuestProfileResponse
>>>>
```

- [ ] **Step 2: Commit changes to snowflake_client.py**

```bash
git add ocean_vortex/snowflake_client.py
git commit -m "refactor: update snowflake_client imports for core migration"
```

### Task 4: Update main.py Imports

**Files:**
- Modify: `ocean_vortex/main.py`

- [ ] **Step 1: Update imports from ocean_vortex.agent and ocean_vortex.dto**

```python
<<<<
from ocean_vortex.agent import AgentState, ocean_vortex_graph
from ocean_vortex.dto import (
    ChatRequest,
    ChatResponse,
    GuestProfileResponse,
    ServiceOrderRequest,
    ServiceOrderResponse,
    SuggestedAction,
)
====
from ocean_vortex.core.agent import AgentState, ocean_vortex_graph
from ocean_vortex.core.models import (
    ChatRequest,
    ChatResponse,
    GuestProfileResponse,
    ServiceOrderRequest,
    ServiceOrderResponse,
    SuggestedAction,
)
>>>>
```

- [ ] **Step 2: Commit changes to main.py**

```bash
git add ocean_vortex/main.py
git commit -m "refactor: update main.py imports for core migration"
```

### Task 5: Verify Changes

- [ ] **Step 1: Run pytest to ensure everything still works**

Run: `pytest tests/test_main.py`
Expected: PASS
