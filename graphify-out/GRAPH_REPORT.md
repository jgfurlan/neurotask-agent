# Graph Report - .  (2026-05-23)

## Corpus Check
- Corpus is ~9,743 words - fits in a single context window. You may not need a graph.

## Summary
- 102 nodes · 104 edges · 24 communities (10 shown, 14 thin omitted)
- Extraction: 79% EXTRACTED · 21% INFERRED · 0% AMBIGUOUS · INFERRED: 22 edges (avg confidence: 0.76)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Community 16|Community 16]]
- [[_COMMUNITY_Community 17|Community 17]]
- [[_COMMUNITY_Community 18|Community 18]]
- [[_COMMUNITY_Community 19|Community 19]]
- [[_COMMUNITY_Community 20|Community 20]]
- [[_COMMUNITY_Community 21|Community 21]]
- [[_COMMUNITY_Community 22|Community 22]]
- [[_COMMUNITY_Community 23|Community 23]]

## God Nodes (most connected - your core abstractions)
1. `MockChatBedrockConverse` - 8 edges
2. `load_context_node()` - 6 edges
3. `GuestPreferences` - 6 edges
4. `GuestProfileResponse` - 6 edges
5. `AgentState` - 5 edges
6. `get_chat_model()` - 5 edges
7. `supervisor_node()` - 4 edges
8. `get_guest_profile()` - 4 edges
9. `chat()` - 4 edges
10. `supervisor_node` - 4 edges

## Surprising Connections (you probably didn't know these)
- `MockChatBedrockConverse` --implements--> `AWS Bedrock Integration`  [INFERRED]
  ocean_cortex_agent/agent.py → docs/architecture.md
- `supervisor_node` --implements--> `Supervisor Agent Concept`  [INFERRED]
  ocean_cortex_agent/agent.py → docs/architecture.md
- `guest_service_node` --implements--> `Guest Service Worker Concept`  [INFERRED]
  ocean_cortex_agent/agent.py → docs/architecture.md
- `anticipatory_advisor_node` --implements--> `Anticipatory Advisor Concept`  [INFERRED]
  ocean_cortex_agent/agent.py → docs/architecture.md
- `OceanCompass UI Integration` --calls--> `chat`  [INFERRED]
  docs/ui-context.md → ocean_cortex_agent/main.py

## Hyperedges (group relationships)
- **LangGraph Agent Nodes** — agent_load_context_node, agent_supervisor_node, agent_guest_service_node, agent_anticipatory_advisor_node [EXTRACTED 1.00]
- **OceanCortex API Endpoints** — main_get_guest_profile, main_chat, main_create_order [EXTRACTED 1.00]
- **ECR Setup Lifecycle Docs** — task_ecr_setup_tracker, implementation_plan_aws_ecr_setup, walkthrough_ecr_setup [INFERRED 0.90]

## Communities (24 total, 14 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.14
Nodes (21): BaseModel, AgentState, Represents the active routing and conversation state of the LangGraph flow., ChatRequest, ChatResponse, DeliverToCoordinates, GuestPreferences, GuestProfileResponse (+13 more)

### Community 1 - "Community 1"
Cohesion: 0.12
Nodes (16): BaseChatModel, anticipatory_advisor_node(), get_chat_model(), guest_service_node(), MockChatBedrockConverse, Return the real Bedrock model when AWS keys exist, otherwise the mock., Inspects guest profile context, binds tools to LLM, and invokes routing., Worker node that handles ordering beverages, food, or amenities. (+8 more)

### Community 2 - "Community 2"
Cohesion: 0.14
Nodes (4): load_context_node(), Pre-emptively loads the guest profile genomics context from the database., test_load_context_node_not_found(), test_load_context_node_success()

### Community 3 - "Community 3"
Cohesion: 0.33
Nodes (7): get_chat_model, MockChatBedrockConverse, route_to_anticipatory_advisor, route_to_guest_service, supervisor_node, AWS Bedrock Integration, Supervisor Agent Concept

### Community 4 - "Community 4"
Cohesion: 0.5
Nodes (4): load_context_node, MOCK_GUEST_DATABASE, GuestProfileResponse, get_guest_profile

### Community 5 - "Community 5"
Cohesion: 0.67
Nodes (3): ocean_cortex_graph, chat, OceanCompass UI Integration

### Community 6 - "Community 6"
Cohesion: 0.67
Nodes (3): AWS ECR Setup Implementation Plan, ECR Setup Task Tracker, ECR Setup Walkthrough

### Community 7 - "Community 7"
Cohesion: 0.67
Nodes (3): CI/CD Pipeline Implementation Plan, CI/CD Pipeline Task Tracker, CI/CD Pipeline Walkthrough

### Community 8 - "Community 8"
Cohesion: 1.0
Nodes (3): Add Job Description Asset Design Spec, Add Job Description Asset Implementation Plan, AI/ML Engineer Job Description PDF

## Knowledge Gaps
- **42 isolated node(s):** `Represents the active routing and conversation state of the LangGraph flow.`, `Pre-emptively loads the guest profile genomics context from the database.`, `Routes the guest to the service node to order items (drinks, towels, etc.).`, `Routes the guest to the advisor node to book/recommend excursions or activities.`, `Deterministic mock that pattern-matches user messages to routing tool calls.` (+37 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **14 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `load_context_node()` connect `Community 2` to `Community 0`, `Community 1`?**
  _High betweenness centrality (0.106) - this node is a cross-community bridge._
- **Why does `GuestPreferences` connect `Community 0` to `Community 1`, `Community 2`?**
  _High betweenness centrality (0.075) - this node is a cross-community bridge._
- **Why does `GuestProfileResponse` connect `Community 0` to `Community 1`, `Community 2`?**
  _High betweenness centrality (0.075) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `MockChatBedrockConverse` (e.g. with `GuestPreferences` and `GuestProfileResponse`) actually correct?**
  _`MockChatBedrockConverse` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `load_context_node()` (e.g. with `GuestProfileResponse` and `GuestPreferences`) actually correct?**
  _`load_context_node()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `GuestPreferences` (e.g. with `AgentState` and `MockChatBedrockConverse`) actually correct?**
  _`GuestPreferences` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `GuestProfileResponse` (e.g. with `AgentState` and `MockChatBedrockConverse`) actually correct?**
  _`GuestProfileResponse` has 4 INFERRED edges - model-reasoned connections that need verification._