# Graph Report - .  (2026-05-22)

## Corpus Check
- Corpus is ~5,010 words - fits in a single context window. You may not need a graph.

## Summary
- 96 nodes · 95 edges · 25 communities (8 shown, 17 thin omitted)
- Extraction: 75% EXTRACTED · 25% INFERRED · 0% AMBIGUOUS · INFERRED: 24 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_OceanAgent Main & DTOs|OceanAgent Main & DTOs]]
- [[_COMMUNITY_LangGraph Agent Nodes & State|LangGraph Agent Nodes & State]]
- [[_COMMUNITY_FastAPI Endpoints & Integration Tests|FastAPI Endpoints & Integration Tests]]
- [[_COMMUNITY_Multi-Agent System Architecture|Multi-Agent System Architecture]]
- [[_COMMUNITY_Guest Profiling & Genomics Integration|Guest Profiling & Genomics Integration]]
- [[_COMMUNITY_Job Description Alignment Spec & Plans|Job Description Alignment Spec & Plans]]
- [[_COMMUNITY_Service Order Delivery Orchestration|Service Order Delivery Orchestration]]
- [[_COMMUNITY_OceanAgent Initialization Module|OceanAgent Initialization Module]]
- [[_COMMUNITY_Docker Deployment Infrastructure|Docker Deployment Infrastructure]]
- [[_COMMUNITY_AI Governance & Coding Standards|AI Governance & Coding Standards]]
- [[_COMMUNITY_RLVR Reward Mechanisms|RLVR Reward Mechanisms]]
- [[_COMMUNITY_Project Main Readme|Project Main Readme]]
- [[_COMMUNITY_JVM vs Native Performance|JVM vs Native Performance]]
- [[_COMMUNITY_Agent Tooling Documentation|Agent Tooling Documentation]]
- [[_COMMUNITY_Medallion Agent Progress Tracker|Medallion Agent Progress Tracker]]
- [[_COMMUNITY_Type Compliance Guidelines|Type Compliance Guidelines]]
- [[_COMMUNITY_TDD Testing Methodology|TDD Testing Methodology]]
- [[_COMMUNITY_UI Design Tokens|UI Design Tokens]]
- [[_COMMUNITY_UX Design Paradigms|UX Design Paradigms]]
- [[_COMMUNITY_Web Accessibility WCAG Compliance|Web Accessibility WCAG Compliance]]
- [[_COMMUNITY_Spec-Driven Development Flow|Spec-Driven Development Flow]]
- [[_COMMUNITY_Synchronization Guidelines|Synchronization Guidelines]]
- [[_COMMUNITY_AWS Bedrock Infrastructure|AWS Bedrock Infrastructure]]
- [[_COMMUNITY_OceanTask Agent Initial Concept|OceanTask Agent Initial Concept]]

## God Nodes (most connected - your core abstractions)
1. `chat orchestration endpoint` - 7 edges
2. `app FastAPI instance` - 6 edges
3. `get_guest_profile endpoint` - 6 edges
4. `ocean_agent_graph compiled workflow` - 5 edges
5. `get_guest_profile()` - 4 edges
6. `chat()` - 4 edges
7. `create_order service order endpoint` - 4 edges
8. `Multi-Agent Network Architecture diagram and concepts` - 4 edges
9. `AgentState` - 3 edges
10. `create_order()` - 3 edges

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

## Communities (25 total, 17 thin omitted)

### Community 0 - "OceanAgent Main & DTOs"
Cohesion: 0.16
Nodes (18): BaseModel, ChatRequest, ChatResponse, DeliverToCoordinates, GuestPreferences, GuestProfileResponse, LocationContext, ServiceOrderRequest (+10 more)

### Community 1 - "LangGraph Agent Nodes & State"
Cohesion: 0.2
Nodes (9): AgentState, anticipatory_advisor_node(), guest_service_node(), Represents the active routing and conversation state of the LangGraph flow., Inspects the last message content and decides which specialist node to call., Stub handler representing the guest service execution., Stub handler representing excursion recommendations and Guest Genome analysis., supervisor_node() (+1 more)

### Community 2 - "FastAPI Endpoints & Integration Tests"
Cohesion: 0.24
Nodes (10): ChatRequest Model, ChatResponse Model, LocationContext Model, SuggestedAction Model, app FastAPI instance, chat orchestration endpoint, read_hello endpoint, test_chat_endpoint_excursion (+2 more)

### Community 3 - "Multi-Agent System Architecture"
Cohesion: 0.28
Nodes (9): AgentState TypedDict, anticipatory_advisor_node function, guest_service_node function, ocean_agent_graph compiled workflow, supervisor_node function, Multi-Agent Network Architecture diagram and concepts, Anticipatory Recommendation System Concept, Carnival OceanTask Agent Mission (+1 more)

### Community 4 - "Guest Profiling & Genomics Integration"
Cohesion: 0.29
Nodes (8): Snowflake Cortex AI Data Architecture, GuestPreferences Model, GuestProfileResponse Model, get_guest_profile endpoint, MOCK_GUEST_DATABASE guest genome database, Guest Genomics Concept, test_get_guest_profile_not_found, test_get_guest_profile_success

### Community 6 - "Job Description Alignment Spec & Plans"
Cohesion: 0.4
Nodes (6): Add Job Description Asset Design Spec, Add Job Description Asset Implementation Plan, Hybrid Polyglot Design Model, JD Technology Alignment Matrix, AI/ML Engineer Job Description PDF, Tech Stack Pivot Decision

### Community 7 - "Service Order Delivery Orchestration"
Cohesion: 0.4
Nodes (5): DeliverToCoordinates Model, ServiceOrderRequest Model, ServiceOrderResponse Model, create_order service order endpoint, test_create_service_order

## Knowledge Gaps
- **37 isolated node(s):** `Represents the active routing and conversation state of the LangGraph flow.`, `Inspects the last message content and decides which specialist node to call.`, `Stub handler representing the guest service execution.`, `Stub handler representing excursion recommendations and Guest Genome analysis.`, `Basic health check endpoint.` (+32 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **17 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `app FastAPI instance` connect `FastAPI Endpoints & Integration Tests` to `Guest Profiling & Genomics Integration`, `Service Order Delivery Orchestration`?**
  _High betweenness centrality (0.058) - this node is a cross-community bridge._
- **Why does `chat orchestration endpoint` connect `FastAPI Endpoints & Integration Tests` to `Multi-Agent System Architecture`?**
  _High betweenness centrality (0.048) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `chat orchestration endpoint` (e.g. with `test_chat_endpoint_excursion` and `test_chat_endpoint_order`) actually correct?**
  _`chat orchestration endpoint` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `get_guest_profile endpoint` (e.g. with `Guest Genomics Concept` and `test_get_guest_profile_success`) actually correct?**
  _`get_guest_profile endpoint` has 3 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Represents the active routing and conversation state of the LangGraph flow.`, `Inspects the last message content and decides which specialist node to call.`, `Stub handler representing the guest service execution.` to the rest of the system?**
  _37 weakly-connected nodes found - possible documentation gaps or missing edges._