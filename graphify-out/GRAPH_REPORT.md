# Graph Report - neurotask-agent  (2026-05-22)

## Corpus Check
- 9 files · ~5,111 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 192 nodes · 182 edges · 33 communities (16 shown, 17 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 24 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `372dd565`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

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
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Community 15|Community 15]]
- [[_COMMUNITY_Community 16|Community 16]]
- [[_COMMUNITY_Community 17|Community 17]]
- [[_COMMUNITY_Community 18|Community 18]]
- [[_COMMUNITY_Community 19|Community 19]]
- [[_COMMUNITY_Community 20|Community 20]]
- [[_COMMUNITY_Community 21|Community 21]]
- [[_COMMUNITY_Community 22|Community 22]]
- [[_COMMUNITY_Community 23|Community 23]]
- [[_COMMUNITY_Community 24|Community 24]]
- [[_COMMUNITY_Community 25|Community 25]]
- [[_COMMUNITY_Community 26|Community 26]]
- [[_COMMUNITY_Community 27|Community 27]]
- [[_COMMUNITY_Community 28|Community 28]]
- [[_COMMUNITY_Community 29|Community 29]]
- [[_COMMUNITY_Community 30|Community 30]]
- [[_COMMUNITY_Community 31|Community 31]]
- [[_COMMUNITY_Community 32|Community 32]]

## God Nodes (most connected - your core abstractions)
1. `Progress Tracker: OceanCortex Agent State` - 7 edges
2. `chat orchestration endpoint` - 7 edges
3. `Project Overview: Carnival OceanCortex Agent` - 6 edges
4. `Carnival Corporation AI/ML Stack Alignment Analysis` - 6 edges
5. `LLM-Based Supervisor Routing Implementation Plan` - 6 edges
6. `app FastAPI instance` - 6 edges
7. `get_guest_profile endpoint` - 6 edges
8. `Code Standards: Agent-Legibility & Python Compliance` - 5 edges
9. `AI Workflow Rules: Execution Governance` - 5 edges
10. `Tech Stack & System Components` - 5 edges

## Surprising Connections (you probably didn't know these)
- `OceanNow Onboard Service Orchestration Flow` --semantically_similar_to--> `create_order service order endpoint`  [INFERRED] [semantically similar]
  docs/project-overview.md → ocean_agent/main.py
- `Anticipatory Recommendation System Concept` --semantically_similar_to--> `anticipatory_advisor_node function`  [INFERRED] [semantically similar]
  docs/project-overview.md → ocean_agent/agent.py
- `get_guest_profile endpoint` --implements--> `Guest Genomics Concept`  [INFERRED]
  ocean_agent/main.py → docs/project-overview.md
- `supervisor_node function` --implements--> `Multi-Agent Network Architecture diagram and concepts`  [INFERRED]
  ocean_agent/agent.py → docs/architecture.md
- `supervisor_node function` --conceptually_related_to--> `OceanNow Onboard Service Orchestration Flow`  [INFERRED]
  ocean_agent/agent.py → docs/project-overview.md

## Hyperedges (group relationships)
- **Stateful Agent Routing Loop** — agent_supervisor_node, agent_guest_service_node, agent_anticipatory_advisor_node, agent_ocean_agent_graph, main_chat [EXTRACTED 1.00]
- **Order Delivery & Booking Flow** — main_create_order, dto_serviceorderrequest, dto_serviceorderresponse, project_overview_ocean_now [INFERRED 0.85]
- **Guest Genomics Flow Integration** — main_get_guest_profile, agent_anticipatory_advisor_node, dto_guestprofileresponse, architecture_snowflake_cortex [INFERRED 0.80]

## Communities (33 total, 17 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.1
Nodes (20): code:python (def test_mock_guest_database_import() -> None:), code:bash (git add ocean_cortex_agent/agent.py tests/test_main.py), code:python (def test_graph_routing_guest_service() -> None:), code:python (def supervisor_node(state: AgentState) -> dict[str, Any]:), code:bash (git add ocean_cortex_agent/agent.py tests/test_main.py), code:bash (git status), code:python (from typing import Any), code:python (from ocean_cortex_agent.db import MOCK_GUEST_DATABASE) (+12 more)

### Community 1 - "Community 1"
Cohesion: 0.16
Nodes (18): BaseModel, ChatRequest, ChatResponse, DeliverToCoordinates, GuestPreferences, GuestProfileResponse, LocationContext, ServiceOrderRequest (+10 more)

### Community 2 - "Community 2"
Cohesion: 0.12
Nodes (18): Snowflake Cortex AI Data Architecture, DeliverToCoordinates Model, GuestPreferences Model, GuestProfileResponse Model, ServiceOrderRequest Model, ServiceOrderResponse Model, app FastAPI instance, create_order service order endpoint (+10 more)

### Community 3 - "Community 3"
Cohesion: 0.19
Nodes (14): AgentState TypedDict, anticipatory_advisor_node function, guest_service_node function, ocean_agent_graph compiled workflow, supervisor_node function, Multi-Agent Network Architecture diagram and concepts, ChatRequest Model, ChatResponse Model (+6 more)

### Community 4 - "Community 4"
Cohesion: 0.17
Nodes (11): API Documentation, code:bash (git clone <repository-url>), code:bash (docker-compose up --build -d), code:bash (curl http://localhost:8000/hello), Interactive Documentation, Local Development, OceanCortex Agent: Autonomous AI-Native Orchestrator, Prerequisites (+3 more)

### Community 5 - "Community 5"
Cohesion: 0.2
Nodes (10): Chat with Agent, code:bash (curl http://localhost:8000/hello), code:json ({"message": "Hello from OceanCortex Python Agent"}), code:bash (curl "http://localhost:8000/ocean/guest/profile?guest_id=4a7), code:json ({), code:bash (curl -X POST http://localhost:8000/ocean/chat \), code:json ({), Example API Usage (+2 more)

### Community 6 - "Community 6"
Cohesion: 0.2
Nodes (9): AgentState, anticipatory_advisor_node(), guest_service_node(), Represents the active routing and conversation state of the LangGraph flow., Inspects the last message content and decides which specialist node to call., Stub handler representing the guest service execution., Stub handler representing excursion recommendations and Guest Genome analysis., supervisor_node() (+1 more)

### Community 7 - "Community 7"
Cohesion: 0.22
Nodes (8): API Boundaries & Interfaces, Chat Payload Example, code:json ({), code:json ({), Design Tokens (Oceanic Theme), REST Endpoints, UI Context: OceanCompass & API Interfaces, UX Paradigms

### Community 8 - "Community 8"
Cohesion: 0.22
Nodes (8): 1. Stateful Multi-Agent Workflow (LangGraph), 2. LLM & Cloud Layer (AWS Bedrock), 3. Data Warehouse & AI Analytics (Snowflake Cortex AI), 4. Reinforcement Learning from Verifiable Rewards (RLVR), Architecture: OceanCortex Multi-Agent System, code:mermaid (graph TD), System Topology, Tech Stack & System Components

### Community 9 - "Community 9"
Cohesion: 0.25
Nodes (7): Active Implementation, Completed Features, Current Project Phase, Feature Queue (Linear Issues), Historical Decisions, Milestones, Progress Tracker: OceanCortex Agent State

### Community 10 - "Community 10"
Cohesion: 0.25
Nodes (7): 1. Core Technology Stack from Job Description, 2. Carnival Corporation's Brand & Technical Identity, 3. Technology Alignment Matrix, 4. Pure Python Agentic Architecture, 5. Next Steps & Implementation Status, Carnival Corporation AI/ML Stack Alignment Analysis, code:mermaid (graph TD)

### Community 11 - "Community 11"
Cohesion: 0.29
Nodes (6): High-Level User Flows, Mission, Out-of-Scope (Phase 1), Project Overview: Carnival OceanCortex Agent, Success Criteria Benchmarks, Tech Stack

### Community 13 - "Community 13"
Cohesion: 0.33
Nodes (5): Agent-Legibility (Mandatory), Code Standards: Agent-Legibility & Python Compliance, Linting & Formatting, Testing Standards (TDD), Type Compliance & Pydantic

### Community 14 - "Community 14"
Cohesion: 0.33
Nodes (5): AI Workflow Rules: Execution Governance, Linear-GitHub Synchronization, Prohibited Actions, Session Governance, Spec-Driven Development

### Community 15 - "Community 15"
Cohesion: 0.4
Nodes (6): Add Job Description Asset Design Spec, Add Job Description Asset Implementation Plan, Hybrid Polyglot Design Model, JD Technology Alignment Matrix, AI/ML Engineer Job Description PDF, Tech Stack Pivot Decision

## Knowledge Gaps
- **98 isolated node(s):** `Technical Architecture & Core Innovation`, `Interactive Documentation`, `REST Endpoints`, `code:bash (curl http://localhost:8000/hello)`, `code:json ({"message": "Hello from OceanCortex Python Agent"})` (+93 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **17 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `chat orchestration endpoint` connect `Community 3` to `Community 2`?**
  _High betweenness centrality (0.012) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `chat orchestration endpoint` (e.g. with `test_chat_endpoint_excursion` and `test_chat_endpoint_order`) actually correct?**
  _`chat orchestration endpoint` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Technical Architecture & Core Innovation`, `Interactive Documentation`, `REST Endpoints` to the rest of the system?**
  _98 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.1 - nodes in this community are weakly interconnected._
- **Should `Community 2` be split into smaller, more focused modules?**
  _Cohesion score 0.12 - nodes in this community are weakly interconnected._