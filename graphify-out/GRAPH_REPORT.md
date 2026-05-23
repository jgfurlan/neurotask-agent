# Graph Report - neurotask-agent  (2026-05-23)

## Corpus Check
- 26 files · ~9,976 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 387 nodes · 436 edges · 47 communities (27 shown, 20 thin omitted)
- Extraction: 88% EXTRACTED · 12% INFERRED · 0% AMBIGUOUS · INFERRED: 52 edges (avg confidence: 0.78)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `6da2def4`
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
- [[_COMMUNITY_Community 12|Community 12]]
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
- [[_COMMUNITY_Community 34|Community 34]]
- [[_COMMUNITY_Community 35|Community 35]]
- [[_COMMUNITY_Community 36|Community 36]]
- [[_COMMUNITY_Community 37|Community 37]]
- [[_COMMUNITY_Community 38|Community 38]]
- [[_COMMUNITY_Community 39|Community 39]]
- [[_COMMUNITY_Community 40|Community 40]]
- [[_COMMUNITY_Community 41|Community 41]]
- [[_COMMUNITY_Community 42|Community 42]]
- [[_COMMUNITY_Community 43|Community 43]]
- [[_COMMUNITY_Community 44|Community 44]]
- [[_COMMUNITY_Community 45|Community 45]]
- [[_COMMUNITY_Community 46|Community 46]]

## God Nodes (most connected - your core abstractions)
1. `MockChatBedrockConverse` - 8 edges
2. `MockChatBedrockConverse` - 8 edges
3. `Progress Tracker: OceanVortex Agent State` - 7 edges
4. `2. ECS Fargate Setup` - 7 edges
5. `Architectural Changes` - 7 edges
6. `Progress Tracker: OceanCortex Agent State` - 7 edges
7. `chat orchestration endpoint` - 7 edges
8. `load_context_node()` - 6 edges
9. `GuestPreferences` - 6 edges
10. `GuestProfileResponse` - 6 edges

## Surprising Connections (you probably didn't know these)
- `Anticipatory Recommendation System Concept` --semantically_similar_to--> `anticipatory_advisor_node function`  [INFERRED] [semantically similar]
  docs/project-overview.md → ocean_agent/agent.py
- `OceanNow Onboard Service Orchestration Flow` --semantically_similar_to--> `create_order service order endpoint`  [INFERRED] [semantically similar]
  docs/project-overview.md → ocean_agent/main.py
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

## Communities (47 total, 20 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.06
Nodes (44): BaseModel, ChatRequest, ChatResponse, DeliverToCoordinates, GuestPreferences, GuestProfileResponse, LocationContext, ServiceOrderRequest (+36 more)

### Community 1 - "Community 1"
Cohesion: 0.06
Nodes (25): AgentState, anticipatory_advisor_node(), get_chat_model(), guest_service_node(), load_context_node(), MockChatBedrockConverse, Return the real Bedrock model when AWS keys exist, otherwise the mock., Inspects guest profile context, binds tools to LLM, and invokes routing. (+17 more)

### Community 2 - "Community 2"
Cohesion: 0.08
Nodes (32): AgentState TypedDict, anticipatory_advisor_node function, guest_service_node function, ocean_agent_graph compiled workflow, supervisor_node function, Multi-Agent Network Architecture diagram and concepts, Snowflake Cortex AI Data Architecture, ChatRequest Model (+24 more)

### Community 3 - "Community 3"
Cohesion: 0.1
Nodes (23): BaseChatModel, AgentState, anticipatory_advisor_node(), get_chat_model(), guest_service_node(), load_context_node(), MockChatBedrockConverse, Return the real Bedrock model when AWS keys exist, otherwise the mock. (+15 more)

### Community 4 - "Community 4"
Cohesion: 0.1
Nodes (22): API Documentation, Chat with Agent, code:bash (curl http://localhost:8000/hello), code:json ({"message": "Hello from OceanVortex Python Agent"}), code:bash (curl "http://localhost:8000/ocean/guest/profile?guest_id=4a7), code:json ({), code:bash (curl -X POST http://localhost:8000/ocean/chat \), code:json ({) (+14 more)

### Community 5 - "Community 5"
Cohesion: 0.11
Nodes (20): 1. Local ECR Setup & Image Push, 2. ECS Fargate Setup, 3. GitHub Actions Integration, Authenticate Docker to ECR, AWS ECR & ECS Deployment — OceanCortex Agent, AWS ECR & ECS Deployment — OceanVortex Agent, Build, Tag, and Push, code:bash (aws ecr get-login-password --region us-east-1 \) (+12 more)

### Community 6 - "Community 6"
Cohesion: 0.1
Nodes (20): code:python (def test_mock_guest_database_import() -> None:), code:bash (git add ocean_vortex/agent.py tests/test_main.py), code:python (def test_graph_routing_guest_service() -> None:), code:python (def supervisor_node(state: AgentState) -> dict[str, Any]:), code:bash (git add ocean_vortex/agent.py tests/test_main.py), code:bash (git status), code:python (from typing import Any), code:python (from ocean_vortex.db import MOCK_GUEST_DATABASE) (+12 more)

### Community 7 - "Community 7"
Cohesion: 0.13
Nodes (14): [DELETE] [ci.yml](file:///home/jgfurlan/dev/projects/neurotask-agent/.github/workflows/ci.yml), [DELETE] [ci.yml](file:///home/jgfurlan/dev/projects/ocean-vortex/.github/workflows/ci.yml), Environment, Implement CI/CD Pipeline, [MODIFY] [docker-compose.yml](file:///home/jgfurlan/dev/projects/neurotask-agent/docker-compose.yml), [MODIFY] [docker-compose.yml](file:///home/jgfurlan/dev/projects/ocean-vortex/docker-compose.yml), [NEW] [ci-cd.yml](file:///home/jgfurlan/dev/projects/neurotask-agent/.github/workflows/ci-cd.yml), [NEW] [ci-cd.yml](file:///home/jgfurlan/dev/projects/ocean-vortex/.github/workflows/ci-cd.yml) (+6 more)

### Community 8 - "Community 8"
Cohesion: 0.14
Nodes (13): 1. State Definition (`AgentState`), 2. Context Initialization Node (`load_context_node`), 3. LLM Setup and Mock Fallback, 4. Supervisor Node Routing Tools, 5. Conditional Router Logic, Architectural Changes, Automated Tests, code:mermaid (graph TD) (+5 more)

### Community 9 - "Community 9"
Cohesion: 0.18
Nodes (10): Automated, AWS Account Migration & ECS Fargate Deployment Implementation Plan, code:bash (# Confirm repo and image in new account), Manual, Phase 1: ECR Migration, Phase 2: ECS Fargate Setup, Phase 3: CI/CD & Verification, Proposed Changes (+2 more)

### Community 10 - "Community 10"
Cohesion: 0.24
Nodes (9): 1. Stateful Multi-Agent Workflow (LangGraph), 2. LLM & Cloud Layer (AWS Bedrock), 3. Data Warehouse & AI Analytics (Snowflake Cortex AI), 4. Reinforcement Learning from Verifiable Rewards (RLVR), Architecture: OceanCortex Multi-Agent System, Architecture: OceanVortex Multi-Agent System, code:mermaid (graph TD), System Topology (+1 more)

### Community 11 - "Community 11"
Cohesion: 0.2
Nodes (9): AgentState, anticipatory_advisor_node(), guest_service_node(), Represents the active routing and conversation state of the LangGraph flow., Inspects the last message content and decides which specialist node to call., Stub handler representing the guest service execution., Stub handler representing excursion recommendations and Guest Genome analysis., supervisor_node() (+1 more)

### Community 12 - "Community 12"
Cohesion: 0.39
Nodes (8): Active Implementation, Completed Features, Current Project Phase, Feature Queue (Linear Issues), Historical Decisions, Milestones, Progress Tracker: OceanCortex Agent State, Progress Tracker: OceanVortex Agent State

### Community 13 - "Community 13"
Cohesion: 0.22
Nodes (8): API Boundaries & Interfaces, Chat Payload Example, code:json ({), code:json ({), Design Tokens (Oceanic Theme), REST Endpoints, UI Context: OceanCompass & API Interfaces, UX Paradigms

### Community 14 - "Community 14"
Cohesion: 0.36
Nodes (8): 1. Pipeline Structure, 2. OIDC Authentication, 3. Secrets & Configuration Strategy, 4. Required AWS Infrastructure, CI/CD Pipeline Design for OceanCortex Agent, CI/CD Pipeline Design for OceanVortex Agent, Jobs, Overview

### Community 15 - "Community 15"
Cohesion: 0.43
Nodes (7): High-Level User Flows, Mission, Out-of-Scope (Phase 1), Project Overview: Carnival OceanCortex Agent, Project Overview: Carnival OceanVortex Agent, Success Criteria Benchmarks, Tech Stack

### Community 16 - "Community 16"
Cohesion: 0.25
Nodes (7): 1. Core Technology Stack from Job Description, 2. Carnival Corporation's Brand & Technical Identity, 3. Technology Alignment Matrix, 4. Pure Python Agentic Architecture, 5. Next Steps & Implementation Status, Carnival Corporation AI/ML Stack Alignment Analysis, code:mermaid (graph TD)

### Community 17 - "Community 17"
Cohesion: 0.33
Nodes (5): Agent-Legibility (Mandatory), Code Standards: Agent-Legibility & Python Compliance, Linting & Formatting, Testing Standards (TDD), Type Compliance & Pydantic

### Community 18 - "Community 18"
Cohesion: 0.33
Nodes (5): AWS Migration and Deployment Walkthrough, code:bash (# 1. Login to new ECR registry), Next Steps for You, Verification & Active Endpoints, What has been done

### Community 19 - "Community 19"
Cohesion: 0.33
Nodes (5): AI Workflow Rules: Execution Governance, Linear-GitHub Synchronization, Prohibited Actions, Session Governance, Spec-Driven Development

### Community 20 - "Community 20"
Cohesion: 0.33
Nodes (5): Approach, Components, Design: Add Job Description Asset, Purpose, Success Criteria

### Community 21 - "Community 21"
Cohesion: 0.4
Nodes (6): Add Job Description Asset Design Spec, Add Job Description Asset Implementation Plan, Hybrid Polyglot Design Model, JD Technology Alignment Matrix, AI/ML Engineer Job Description PDF, Tech Stack Pivot Decision

### Community 22 - "Community 22"
Cohesion: 0.4
Nodes (4): CI/CD Pipeline Implementation Walkthrough, Validation, What changed, Why

### Community 23 - "Community 23"
Cohesion: 0.4
Nodes (4): Add Job Description Asset Implementation Plan, Task 1: Create Assets Directory, Task 2: Copy and Rename Job Description, Task 3: Final Verification

## Knowledge Gaps
- **163 isolated node(s):** `Represents the active routing and conversation state of the LangGraph flow.`, `Pre-emptively loads the guest profile genomics context from the database.`, `Routes the guest to the service node to order items (drinks, towels, etc.).`, `Routes the guest to the advisor node to book/recommend excursions or activities.`, `Deterministic mock that pattern-matches user messages to routing tool calls.` (+158 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **20 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `GuestPreferences` connect `Community 1` to `Community 0`?**
  _High betweenness centrality (0.015) - this node is a cross-community bridge._
- **Why does `GuestProfileResponse` connect `Community 1` to `Community 0`?**
  _High betweenness centrality (0.015) - this node is a cross-community bridge._
- **Why does `GuestPreferences` connect `Community 3` to `Community 0`?**
  _High betweenness centrality (0.015) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `MockChatBedrockConverse` (e.g. with `GuestPreferences` and `GuestProfileResponse`) actually correct?**
  _`MockChatBedrockConverse` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `MockChatBedrockConverse` (e.g. with `GuestPreferences` and `GuestProfileResponse`) actually correct?**
  _`MockChatBedrockConverse` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Represents the active routing and conversation state of the LangGraph flow.`, `Pre-emptively loads the guest profile genomics context from the database.`, `Routes the guest to the service node to order items (drinks, towels, etc.).` to the rest of the system?**
  _163 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.06 - nodes in this community are weakly interconnected._