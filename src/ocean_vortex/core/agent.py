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

from ocean_vortex.core.models import GuestPreferences, GuestProfileResponse
from ocean_vortex.providers.snowflake import get_snowflake_client


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
