# Progress Tracker: OceanVortex Agent State

## Current Project Phase
**Phase 1: Medallion Agent Tracer Bullet** (May – Jun 2026)
*Goal: Setup a Python/FastAPI/LangGraph pipeline on AWS ECS with mock Bedrock/Snowflake connections.*

## Active Implementation
- **Current Task**: Adapt template guidelines to Carnival Corporation tech stack.
- **Status**: Core docs established in `docs/`. Ready to transition codebase to Python.

## Completed Features
- ✅ Deep research on Carnival Corporation IoT technology (OceanMedallion, xIoT).
- ✅ Analysis of job description stack requirements (Python, LangGraph, Bedrock, Snowflake).
- ✅ Customization of project overview, architecture, code standards, UI, and workflow rules.

## Historical Decisions
- **2026-05-22**: Decided to pivot project from Java 25 / Quarkus to Python 3.12, LangGraph, AWS Bedrock, and Snowflake Cortex AI to match the JD requirements.
- **2026-05-22**: Documented a new `docs/` guidelines structure to maintain project legibility.

## Milestones
- **M1: Tech Stack Pivot & Core Guidelines** (Target: 2026-05-22) — *Status: Completed*
- **M2: Python Backend Skeleton & LangGraph Pipeline** (Target: 2026-06-05) — *Status: Planned*
- **M3: Snowflake Integration & Mock Bedrock Environment** (Target: 2026-06-20)
- **M4: Production Deployment on AWS ECS** (Target: 2026-07-15)

## Feature Queue (Linear Issues)
1. `[Scaffold] Initialize Python FastAPI project with pyproject.toml / poetry` (MED-25)
2. `[Agent] Define base LangGraph state machine & Supervisor agent` (MED-26)
3. `[Database] Establish Snowflake connector utility and mock client` (MED-27)
4. `[Infra] Configure Dockerfile and local docker-compose for PostgreSQL/Snowflake mock testing` (MED-28)
