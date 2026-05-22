import os
from collections.abc import Sequence
from typing import Annotated, Any, TypedDict
from uuid import UUID

from fastapi import HTTPException, status

from pydantic import PrivateAttr

from langchain_core.callbacks import CallbackManagerForLLMRun
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage
from langchain_core.outputs import ChatGeneration, ChatResult
from langchain_core.tools import tool
from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages

from ocean_cortex_agent.db import MOCK_GUEST_DATABASE
from ocean_cortex_agent.dto import GuestPreferences, GuestProfileResponse


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
        )

    if guest_id not in MOCK_GUEST_DATABASE:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Guest profile with ID {guest_id} not found",
        )

    data = MOCK_GUEST_DATABASE[guest_id]
    profile = GuestProfileResponse(
        guest_id=guest_id,
        full_name=data["full_name"],
        medallion_status=data["medallion_status"],
        preferences=GuestPreferences(**data["preferences"]),
    )

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
    _bound_tools: list = PrivateAttr(default_factory=list)

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
                model_id="anthropic.claude-3-5-haiku-20241022-v1:0"
            )
        except Exception:
            return MockChatBedrockConverse()
    else:
        return MockChatBedrockConverse()


# ---------------------------------------------------------------------------
# Graph nodes
# ---------------------------------------------------------------------------

def supervisor_node(state: AgentState) -> dict[str, Any]:
    """Inspects the last message content and decides which specialist node to call."""
    content = state["messages"][-1].content
    last_message = content.lower() if isinstance(content, str) else str(content).lower()

    # Simple routing logic (will be replaced by LLM in Task 4)
    if "snorkeling" in last_message or "excursion" in last_message:
        next_node = "anticipatory_advisor"
    elif "mojito" in last_message or "order" in last_message:
        next_node = "guest_service"
    else:
        next_node = END

    return {
        "next_node": next_node,
        "messages": [AIMessage(content=f"[Supervisor] Routing to {next_node}")]
    }

def guest_service_node(state: AgentState) -> dict[str, Any]:
    """Stub handler representing the guest service execution."""
    return {
        "next_node": END,
        "messages": [AIMessage(content="I have processed your service order request.")]
    }

def anticipatory_advisor_node(state: AgentState) -> dict[str, Any]:
    """Stub handler representing excursion recommendations and Guest Genome analysis."""
    return {
        "next_node": END,
        "messages": [AIMessage(content="I have generated your excursion recommendation details.")]
    }

# Build and compile the LangGraph workflow
workflow = StateGraph(AgentState)

workflow.add_node("supervisor", supervisor_node)
workflow.add_node("guest_service", guest_service_node)
workflow.add_node("anticipatory_advisor", anticipatory_advisor_node)

workflow.set_entry_point("supervisor")

# Configure conditional edges
workflow.add_conditional_edges(
    "supervisor",
    lambda state: state["next_node"],
    {
        "guest_service": "guest_service",
        "anticipatory_advisor": "anticipatory_advisor",
        END: END
    }
)

workflow.add_edge("guest_service", END)
workflow.add_edge("anticipatory_advisor", END)

ocean_cortex_graph = workflow.compile()
