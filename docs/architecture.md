# Architecture: OceanVortex Multi-Agent System

This document outlines the architecture, coordination patterns, and data integration boundaries for the OceanVortex Agent.

## System Topology

```mermaid
graph TD
    User([Guest / OceanCompass App]) -->|REST API / WebSocket| WebAPI[FastAPI Backend]
    WebAPI -->|Stateful Workflow| Graph[LangGraph Orchestrator]
    
    subgraph Multi-Agent Network
        Graph --> Supervisor[Supervisor Agent]
        Supervisor -->|Delegate| GuestWorker[Guest Service Worker]
        Supervisor -->|Delegate| AdviceWorker[Anticipatory Advisor]
        
        GuestWorker -->|Database Tool Call| Snowflake[(Snowflake Cortex AI)]
        AdviceWorker -->|Vector Search / RAG| Snowflake
    end
    
    subgraph LLM Provider
        Supervisor -->|inference| AWSBedrock[AWS Bedrock - Claude 3.5 Sonnet]
        GuestWorker -->|inference| AWSBedrock
        AdviceWorker -->|inference| AWSBedrock
    end
    
    subgraph Observability & Guardrails
        Verifier[Verifier Agent] -->|Audit DB State| Snowflake
        Verifier -->|Record RLVR Reward| RewardTable[(Snowflake Telemetry Table)]
        Verifier -->|Increment Metrics| Prometheus[Prometheus Metrics]
    end
```

## Tech Stack & System Components

### 1. Stateful Multi-Agent Workflow (LangGraph)
- **Supervisor Node**: Analyzes incoming messages and routes control to the appropriate worker agent based on intent.
- **Guest Service Worker**: Accesses tools to query or mutate bookings, request onboard deliveries (OceanNow), or handle payment options (MedallionPay).
- **Anticipatory Advisor**: Implements RAG (Retrieval-Augmented Generation) pipelines to scan current shipboard activities and guest preferences, outputting personalized dining or excursion recommendations.

### 2. LLM & Cloud Layer (AWS Bedrock)
- Standardizes on **Claude 3.5 Sonnet** (for heavy reasoning/Supervisor task decomposition) and **Claude 3.5 Haiku** (for fast, structured text classification).
- Connections managed using the AWS SDK (`boto3`) and securely authenticated using IAM roles on ECS tasks.

### 3. Data Warehouse & AI Analytics (Snowflake Cortex AI)
- Guest Genomics, booking profiles, real-time activity catalogs, and vector embeddings are stored in **Snowflake**.
- **Snowflake Cortex AI** functions are used to query vector tables for context-rich similarity matching during recommendations.

### 4. Reinforcement Learning from Verifiable Rewards (RLVR)
- To ensure agent operations are safe and reliable, the **Verifier Agent** audits database state after every write action.
- A numerical reward is calculated:
  - `+1.0` if the action successfully updated database state without error.
  - `-0.5` if the agent attempted an invalid state change (e.g. double booking, formatting error, or constraint violation).
- These logs are recorded in the `AGENT_EXECUTION_LOGS` table in Snowflake for fine-tuning and performance analysis.
