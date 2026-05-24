# OceanVortex Agent: Technical Onboarding Guide

Welcome to the **OceanVortex Agent** project! This document provides a high-level overview of our architecture, technology stack, and engineering standards to help you get up to speed quickly.

## 1. Project Context & Vision

OceanVortex is a multi-agent backend orchestrator designed to integrate with the **Carnival Corporation IoT ecosystem (MedallionClass)**. Our goal is to create an autonomous, hyper-personalized "Digital Concierge" for cruise ship guests, leveraging their digital twin data (Guest Genome) and edge-compatible LLM routing.

Because cruise ships often operate in edge environments with high latency to the cloud, the agent is designed as a stateless, containerized Python service capable of running on AWS ECS (Cloud) or xiOS Edge clusters.

## 2. Core Technology Stack

We use a modern, typed, and production-grade Python stack:
- **Language**: Python 3.12+ (Strict typing with `mypy`)
- **API Framework**: FastAPI & Uvicorn (Async, high-performance REST)
- **Agent Orchestration**: LangGraph & Langchain Core (State machines for multi-agent workflows)
- **Generative AI**: AWS Bedrock (Claude 3.5 Haiku) for LLM inference
- **Data Warehouse / RAG**: Snowflake Cortex AI (Guest Genome profiles and semantic queries)
- **Tooling**: Ruff (Linting/Formatting), Pytest (Testing), Docker (Containerization)

## 3. Architecture & Directory Structure

We use a professional `src/`-based package layout with layered boundaries. This prevents circular dependencies and separates concerns:

```text
src/ocean_vortex/
├── api/             # HTTP layer (FastAPI endpoints, routers, web server setup)
├── core/            # Domain logic (LangGraph state machines, Pydantic models/DTOs)
├── providers/       # Infrastructure layer (Snowflake clients, Mock DBs, AWS clients)
└── scripts/         # Administrative tools (CLI utilities, data migrations)
```

**Key Architectural Rules:**
1. **The Core is isolated:** `core/` contains business logic (`agent.py` and `models.py`). It should *never* import from `api/`.
2. **Dependency Injection:** The `api/` layer orchestrates connections by taking clients from `providers/` and passing them to `core/`.
3. **Protocols over Classes:** We use Python `typing.Protocol` (like `SnowflakeClientProtocol`) to define expected interfaces, making it trivial to swap Live implementations with Mocks during local testing.

## 4. The Agentic Workflow (LangGraph)

Our agent is built on a **Supervisor-Worker** topology:
1. **Load Context Node**: First fetches the user's "Guest Genome" profile via Snowflake.
2. **Supervisor Node (AWS Bedrock)**: Analyzes the prompt alongside the profile. It binds available tools to the LLM. If a tool is chosen, execution routes to a specialized Worker Node.
3. **Worker Nodes**: 
   - `guest_service`: For handling physical orders (beverages, amenities) to coordinates on the ship.
   - `anticipatory_advisor`: For personalized excursion matching and recommendations.

## 5. Local Development Environment

We provide a hermetic, fully-mocked local environment via Docker Compose so you can test agent logic without racking up AWS or Snowflake bills.

**To run the live-reloading agent:**
```bash
docker compose up
```

**To run the CI test suite locally (Pytest, Ruff, Mypy):**
```bash
docker compose --profile test up --build
```
> **Note**: Both environments automatically inject `USE_MOCK_SNOWFLAKE=true` and `USE_MOCK_BEDROCK=true` to utilize our local Mock providers instead of live endpoints.

## 6. Development Workflow (CI/CD)

1. **Linting First**: We use `ruff`. Run `ruff check .` to catch unused imports and `ruff format .` to auto-format code.
2. **Strict Typing**: Run `mypy src tests` before committing.
3. **Testing**: `pytest tests/` must pass 100%. We enforce this in GitHub Actions (`.github/workflows/ci-cd.yml`).
4. **Docs**: Any architectural change or phase transition must be logged in `docs/progress-tracker.md` and `docs/walkthrough.md`.

Welcome aboard! 🚢
