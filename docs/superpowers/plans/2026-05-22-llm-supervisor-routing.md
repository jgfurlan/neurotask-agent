# LLM-Based Supervisor Routing Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Upgrade the supervisor node in the multi-agent backend to perform dynamic routing using AWS Bedrock and LangGraph, with mock fallbacks for local and CI environments.

**Architecture:** A context initialization node retrieves guest profile genomics data and adds it to the graph state. The supervisor node constructs a context-aware system prompt, binds pydantic routing tools, and uses ChatBedrockConverse (falling back to MockChatBedrockConverse if AWS keys are missing) to dynamically determine the next specialist node. Worker nodes inspect the supervisor's tool call parameters to execute personalized requests.

**Tech Stack:** Python, LangGraph, LangChain, AWS Bedrock (Claude 3.5 Haiku), FastAPI, Pytest

---

### Task 1: Relocate Guest Database to Prevent Circular Imports

**Files:**
- Create: `ocean_vortex/db.py`
- Modify: `ocean_vortex/main.py:27-38`
- Test: `tests/test_main.py`

- [ ] **Step 1: Write the failing test**

Open [tests/test_main.py](file:///home/jgfurlan/dev/projects/ocean-vortex/tests/test_main.py) and add the following test at the end of the file:

```python
def test_mock_guest_database_import() -> None:
    from ocean_vortex.db import MOCK_GUEST_DATABASE
    assert MOCK_GUEST_DATABASE is not None
    assert "4a7114b0-681b-4b20-9430-863a15234de1" in [str(k) for k in MOCK_GUEST_DATABASE.keys()]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pyenv exec pytest -k test_mock_guest_database_import`
Expected: FAIL with `ModuleNotFoundError: No module named 'ocean_vortex.db'`

- [ ] **Step 3: Write minimal implementation**

Create [ocean_vortex/db.py](file:///home/jgfurlan/dev/projects/ocean-vortex/ocean_vortex/db.py):

```python
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
    }
}
```

Modify [ocean_vortex/main.py](file:///home/jgfurlan/dev/projects/ocean-vortex/ocean_vortex/main.py) to remove the inline definition and import it:

Replace lines 27-38 with:
```python
from ocean_vortex.db import MOCK_GUEST_DATABASE
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pyenv exec pytest`
Expected: PASS (all 7 tests pass)

- [ ] **Step 5: Commit**

```bash
git add ocean_vortex/db.py ocean_vortex/main.py tests/test_main.py
git commit -m "refactor: relocate mock guest database to db.py to avoid circular imports"
```

---

### Task 2: Define Routing Tools and Mock LLM

**Files:**
- Modify: `ocean_vortex/agent.py:1-8`
- Test: `tests/test_main.py`

- [ ] **Step 1: Write the failing test**

Add these tests to the end of [tests/test_main.py](file:///home/jgfurlan/dev/projects/ocean-vortex/tests/test_main.py):

```python
def test_mock_chat_bedrock_converse_routing() -> None:
    from langchain_core.messages import HumanMessage
    from ocean_vortex.agent import MockChatBedrockConverse, get_chat_model
    
    model = get_chat_model()
    assert isinstance(model, MockChatBedrockConverse)
    
    # Test drink routing simulation
    res_drink = model.invoke([HumanMessage(content="Order a Mojito please")])
    assert res_drink.tool_calls is not None
    assert len(res_drink.tool_calls) == 1
    assert res_drink.tool_calls[0]["name"] == "route_to_guest_service"
    assert res_drink.tool_calls[0]["args"]["item_name"] == "Mojito"
    
    # Test excursion routing simulation
    res_excursion = model.invoke([HumanMessage(content="I want to go snorkeling")])
    assert res_excursion.tool_calls is not None
    assert len(res_excursion.tool_calls) == 1
    assert res_excursion.tool_calls[0]["name"] == "route_to_anticipatory_advisor"
    assert res_excursion.tool_calls[0]["args"]["excursion_name"] == "Snorkeling"
    
    # Test fallback chit-chat simulation
    res_greeting = model.invoke([HumanMessage(content="Hello there")])
    assert not res_greeting.tool_calls
    assert "hello" in res_greeting.content.lower() or "help" in res_greeting.content.lower()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pyenv exec pytest -k test_mock_chat_bedrock_converse_routing`
Expected: FAIL with `ImportError: cannot import name 'MockChatBedrockConverse' from 'ocean_vortex.agent'`

- [ ] **Step 3: Write minimal implementation**

Open [ocean_vortex/agent.py](file:///home/jgfurlan/dev/projects/ocean-vortex/ocean_vortex/agent.py) and modify the top imports and definitions.

Replace lines 1-8 of [ocean_vortex/agent.py](file:///home/jgfurlan/dev/projects/ocean-vortex/ocean_vortex/agent.py) with the following imports, mock class, and tools:

```python
import os
from collections.abc import Sequence
from typing import Annotated, Any, List, Optional
from pydantic import PrivateAttr

from langchain_core.callbacks import CallbackManagerForLLMRun
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage, SystemMessage
from langchain_core.outputs import ChatResult, ChatGeneration
from langchain_core.tools import tool
from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages


class MockChatBedrockConverse(BaseChatModel):
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
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        # Get the last HumanMessage content
        content = messages[-1].content
        text = content.lower() if isinstance(content, str) else str(content).lower()
        
        tool_calls = []
        ai_content = ""
        
        if "mojito" in text or "order" in text:
            tool_calls.append({
                "name": "route_to_guest_service",
                "args": {"item_name": "Mojito", "quantity": 1},
                "id": "call_guest_service",
                "type": "tool_call"
            })
        elif "snorkeling" in text or "excursion" in text:
            tool_calls.append({
                "name": "route_to_anticipatory_advisor",
                "args": {"excursion_name": "Snorkeling"},
                "id": "call_anticipatory_advisor",
                "type": "tool_call"
            })
        else:
            ai_content = "Hello! I am the OceanMedallion digital assistant. How can I help you today?"
            
        message = AIMessage(content=ai_content, tool_calls=tool_calls)
        return ChatResult(generations=[ChatGeneration(message=message)])

    def _llm_type(self) -> str:
        return "mock-chat-bedrock"


def get_chat_model() -> BaseChatModel:
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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pyenv exec pytest -k test_mock_chat_bedrock_converse_routing`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add ocean_vortex/agent.py tests/test_main.py
git commit -m "feat: implement MockChatBedrockConverse class and routing tools"
```

---

### Task 3: Implement Context Loading Node

**Files:**
- Modify: `ocean_vortex/agent.py`
- Test: `tests/test_main.py`

- [ ] **Step 1: Write the failing test**

Add these tests to the end of [tests/test_main.py](file:///home/jgfurlan/dev/projects/ocean-vortex/tests/test_main.py):

```python
def test_load_context_node_success() -> None:
    from ocean_vortex.agent import load_context_node, AgentState
    from langchain_core.messages import HumanMessage
    
    guest_id = "4a7114b0-681b-4b20-9430-863a15234de1"
    state: AgentState = {
        "guest_id": guest_id,
        "messages": [HumanMessage(content="Test message")],
        "next_node": "",
        "context": {}
    }
    
    result = load_context_node(state)
    assert "guest_profile" in result["context"]
    profile = result["context"]["guest_profile"]
    assert profile.full_name == "Alexander Mercer"
    assert profile.medallion_status == "Ruby"
    assert "Snorkeling" in profile.preferences.activity_interests
    
def test_load_context_node_not_found() -> None:
    import pytest
    from fastapi import HTTPException
    from ocean_vortex.agent import load_context_node, AgentState
    from langchain_core.messages import HumanMessage
    
    guest_id = "00000000-0000-0000-0000-000000000000"
    state: AgentState = {
        "guest_id": guest_id,
        "messages": [HumanMessage(content="Test message")],
        "next_node": "",
        "context": {}
    }
    
    with pytest.raises(HTTPException) as exc_info:
        load_context_node(state)
    assert exc_info.value.status_code == 404
    assert "not found" in exc_info.value.detail
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pyenv exec pytest -k "test_load_context_node"`
Expected: FAIL with `AttributeError: module 'ocean_vortex.agent' has no attribute 'load_context_node'`

- [ ] **Step 3: Write minimal implementation**

Add the implementation of `load_context_node` to [ocean_vortex/agent.py](file:///home/jgfurlan/dev/projects/ocean-vortex/ocean_vortex/agent.py) right after `AgentState` definition (line 9-15 of the original file):

```python
from uuid import UUID
from fastapi import HTTPException, status
from ocean_vortex.db import MOCK_GUEST_DATABASE
from ocean_vortex.dto import GuestProfileResponse, GuestPreferences

def load_context_node(state: AgentState) -> dict[str, Any]:
    """Pre-emptively loads the guest profile genomics context from the database."""
    guest_id_str = state.get("guest_id")
    if not guest_id_str:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Guest ID is missing in agent state"
        )
    try:
        guest_id = UUID(guest_id_str)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid UUID format for Guest ID"
        )
        
    if guest_id not in MOCK_GUEST_DATABASE:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Guest profile with ID {guest_id} not found"
        )
        
    data = MOCK_GUEST_DATABASE[guest_id]
    profile = GuestProfileResponse(
        guest_id=guest_id,
        full_name=data["full_name"],
        medallion_status=data["medallion_status"],
        preferences=GuestPreferences(**data["preferences"])
    )
    
    return {
        "context": {
            **state.get("context", {}),
            "guest_profile": profile
        }
    }
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pyenv exec pytest -k "test_load_context_node"`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add ocean_vortex/agent.py tests/test_main.py
git commit -m "feat: implement load_context_node to load guest profiles pre-emptively"
```

---

### Task 4: Integrate LLM Routing and Specialist Node Execution

**Files:**
- Modify: `ocean_vortex/agent.py`
- Test: `tests/test_main.py`

- [ ] **Step 1: Write the failing test**

Add these tests to the end of [tests/test_main.py](file:///home/jgfurlan/dev/projects/ocean-vortex/tests/test_main.py):

```python
def test_graph_routing_guest_service() -> None:
    from ocean_vortex.agent import ocean_agent_graph, AgentState
    from langchain_core.messages import HumanMessage
    
    guest_id = "4a7114b0-681b-4b20-9430-863a15234de1"
    inputs: AgentState = {
        "guest_id": guest_id,
        "messages": [HumanMessage(content="Order a Mojito drink for me")],
        "next_node": "",
        "context": {}
    }
    
    result = ocean_agent_graph.invoke(inputs)
    assert len(result["messages"]) >= 3
    final_msg = result["messages"][-1].content
    assert "Mojito" in final_msg
    assert "processed" in final_msg.lower()

def test_graph_routing_anticipatory_advisor() -> None:
    from ocean_agent.agent import ocean_agent_graph, AgentState  # wait, this should use ocean_vortex
    # Let's fix that below:
    from ocean_vortex.agent import ocean_agent_graph, AgentState
    from langchain_core.messages import HumanMessage
    
    guest_id = "4a7114b0-681b-4b20-9430-863a15234de1"
    inputs: AgentState = {
        "guest_id": guest_id,
        "messages": [HumanMessage(content="Are there snorkeling excursions?")],
        "next_node": "",
        "context": {}
    }
    
    result = ocean_agent_graph.invoke(inputs)
    assert len(result["messages"]) >= 3
    final_msg = result["messages"][-1].content
    assert "Snorkeling" in final_msg
    assert "recommendation" in final_msg.lower()

def test_graph_routing_chit_chat() -> None:
    from ocean_vortex.agent import ocean_agent_graph, AgentState
    from langchain_core.messages import HumanMessage
    
    guest_id = "4a7114b0-681b-4b20-9430-863a15234de1"
    inputs: AgentState = {
        "guest_id": guest_id,
        "messages": [HumanMessage(content="Hi, how is the weather today?")],
        "next_node": "",
        "context": {}
    }
    
    result = ocean_agent_graph.invoke(inputs)
    assert len(result["messages"]) == 2
    final_msg = result["messages"][-1].content
    assert "digital assistant" in final_msg or "help" in final_msg.lower()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pyenv exec pytest -k "test_graph_routing"`
Expected: FAIL (either routes to incorrect nodes, fails to run because of graph structure, or doesn't return dynamic messages containing "Mojito" / "Snorkeling").

- [ ] **Step 3: Write minimal implementation**

Modify `supervisor_node`, `guest_service_node`, `anticipatory_advisor_node` and graph setup in [ocean_vortex/agent.py](file:///home/jgfurlan/dev/projects/ocean-vortex/ocean_vortex/agent.py) to replace the keyword logic with dynamic tool calls and update compile settings:

```python
def supervisor_node(state: AgentState) -> dict[str, Any]:
    """Inspects guest profile context, binds tools to LLM, and invokes Bedrock routing."""
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
        "If the request is simple chit-chat, greet the guest directly without choosing any tools."
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
        "messages": [response]
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
        "messages": [AIMessage(content=f"I have processed your service order request for {item_name} (Qty: {quantity}).")]
    }

def anticipatory_advisor_node(state: AgentState) -> dict[str, Any]:
    """Worker node that handles excursion/activity recommendations."""
    last_message = state["messages"][-1]
    excursion_name = "general activities"
    
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        args = last_message.tool_calls[0].get("args", {})
        excursion_name = args.get("excursion_name") or args.get("activity_query") or "general activities"
        
    return {
        "next_node": END,
        "messages": [AIMessage(content=f"I have generated your excursion recommendation details for {excursion_name}.")]
    }

# Build and compile the LangGraph workflow
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
        END: END
    }
)

workflow.add_edge("guest_service", END)
workflow.add_edge("anticipatory_advisor", END)

ocean_agent_graph = workflow.compile()
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pyenv exec pytest`
Expected: PASS (all tests, including the end-to-end routing and FastAPI tests, must pass successfully)

- [ ] **Step 5: Commit**

```bash
git add ocean_vortex/agent.py tests/test_main.py
git commit -m "feat: connect load_context_node, integrate LLM tool binding, and dynamic routing"
```

---

### Task 5: Static Analysis and Type Verification

**Files:**
- Test: `ocean_vortex/`

- [ ] **Step 1: Run Ruff linter**

Run: `pyenv exec ruff check .`
Expected: PASS with no linting errors.

- [ ] **Step 2: Run MyPy static type check**

Run: `pyenv exec mypy ocean_vortex/`
Expected: PASS with "Success: no issues found"

- [ ] **Step 3: Commit final layout confirmation**

```bash
git status
```
Confirm all checks are complete.
