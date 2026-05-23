from fastapi.testclient import TestClient

from ocean_vortex.main import app

client = TestClient(app)

def test_hello_endpoint() -> None:
    response = client.get("/hello")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello from OceanVortex Python Agent"}

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
    from ocean_vortex.db import MOCK_GUEST_DATABASE
    assert MOCK_GUEST_DATABASE is not None
    assert "4a7114b0-681b-4b20-9430-863a15234de1" in [str(k) for k in MOCK_GUEST_DATABASE.keys()]


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


def test_load_context_node_success() -> None:
    from langchain_core.messages import HumanMessage

    from ocean_vortex.agent import AgentState, load_context_node

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
    from langchain_core.messages import HumanMessage

    from ocean_vortex.agent import AgentState, load_context_node

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


def test_graph_routing_guest_service() -> None:
    from langchain_core.messages import HumanMessage

    from ocean_vortex.agent import AgentState, ocean_cortex_graph

    guest_id = "4a7114b0-681b-4b20-9430-863a15234de1"
    inputs: AgentState = {
        "guest_id": guest_id,
        "messages": [HumanMessage(content="Order a Mojito drink for me")],
        "next_node": "",
        "context": {}
    }

    result = ocean_cortex_graph.invoke(inputs)
    assert len(result["messages"]) >= 3
    final_msg = result["messages"][-1].content
    assert "Mojito" in final_msg
    assert "processed" in final_msg.lower()


def test_graph_routing_anticipatory_advisor() -> None:
    from langchain_core.messages import HumanMessage

    from ocean_vortex.agent import AgentState, ocean_cortex_graph

    guest_id = "4a7114b0-681b-4b20-9430-863a15234de1"
    inputs: AgentState = {
        "guest_id": guest_id,
        "messages": [HumanMessage(content="Are there snorkeling excursions?")],
        "next_node": "",
        "context": {}
    }

    result = ocean_cortex_graph.invoke(inputs)
    assert len(result["messages"]) >= 3
    final_msg = result["messages"][-1].content
    assert "Snorkeling" in final_msg
    assert "recommendation" in final_msg.lower()


def test_graph_routing_chit_chat() -> None:
    from langchain_core.messages import HumanMessage

    from ocean_vortex.agent import AgentState, ocean_cortex_graph

    guest_id = "4a7114b0-681b-4b20-9430-863a15234de1"
    inputs: AgentState = {
        "guest_id": guest_id,
        "messages": [HumanMessage(content="Hi, how is the weather today?")],
        "next_node": "",
        "context": {}
    }

    result = ocean_cortex_graph.invoke(inputs)
    # load_context adds no message, supervisor adds the chit-chat AIMessage → 2 total
    assert len(result["messages"]) == 2
    final_msg = result["messages"][-1].content
    assert "digital assistant" in final_msg.lower() or "help" in final_msg.lower()
