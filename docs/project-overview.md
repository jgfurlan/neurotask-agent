# Project Overview: Carnival OceanCortex Agent

## Mission
Develop a state-of-the-art, autonomous multi-agent orchestration platform that acts as the intelligent backend for Carnival Corporation's **OceanMedallion** and **xIoT (Experience Internet of Things)** ecosystem. The platform leverages modern generative AI, stateful workflows, and enterprise data warehouses to deliver a frictionless, personalized, and proactive guest experience ("Guest Genomics") across Carnival's global fleet.

## High-Level User Flows

1. **Guest Sync & Identity (Trust Anchor):**
   - The guest authenticates and syncs their wearable **OceanMedallion**.
   - The agent fetches the guest's profile, preferences, and historical interactions ("Guest Genomics") from **Snowflake Cortex AI**.

2. **Onboard Service Orchestration (OceanNow):**
   - The guest requests services (e.g. food, drinks, amenities delivery to their current shipboard location) via the OceanCompass app.
   - The **OceanCortex** supervisor delegates execution to specialized worker agents (e.g., location tracking, galley routing, and crew task dispatching).

3. **Proactive Recommendation System (Anticipatory Design):**
   - The system monitors real-time context (time of day, ship location, weather, and dining room capacity).
   - The system suggests personalized activities, dining reservations, or shore excursions directly to the guest before they ask, helping prevent bottlenecks and improving satisfaction.

## Success Criteria Benchmarks

- **Verifiable Outcomes (RLVR)**: Every agent action (bookings, orders, coordinates tracking) must return a deterministic reward signal (`+1.0` for successful execution/order, `-0.5` for collision or invalid database updates).
- **Agent-Legibility**: The codebase must be highly searchable, modular, and use descriptive, globally unique function prefixes to prevent LLM search confusion.
- **Low-Latency Performance**: End-to-end agentic reasoning and tool execution loop must return a response in under 200ms to maintain real-time interactive UI standards on mobile and wearable interfaces.
- **Resilience**: The system must operate seamlessly on edge nodes aboard cruise vessels with intermittent satellite connection.

## Out-of-Scope (Phase 1)
- Off-ship third-party payment gateways (using simulated onboard medallion account balances).
- Dynamic fleet-wide multi-ship routing optimization.
- Crew shift management interfaces (handled via mock responses for now).

## Tech Stack
- **Backend Framework**: Python 3.12+ (FastAPI)
- **Agent Orchestration**: **LangGraph** (Stateful, multi-agent workflows)
- **AI / LLM Services**: **AWS Bedrock** (Claude 3.5 Sonnet / Claude 3.5 Haiku)
- **Database & Data Warehousing**: **Snowflake Cortex AI** & Snowflake ML
- **Container Infrastructure**: Docker & AWS ECS (Elastic Container Service)
