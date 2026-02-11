# 🤖 Project: NeuroTask Architect
**An Autonomous Task Management System powered by Java 25 & LangChain4j Agents.**

## 🎯 Overview
NeuroTask isn't a simple To-Do list. It's an **Agentic System** that understands natural language intent, decomposes complex goals into sub-tasks, and autonomously manages a PostgreSQL state.

## 🏗️ Architecture
- **Language:** Java 25 (LTS) with Virtual Threads (Project Loom).
- **Framework:** Quarkus 3.31 (Native-first).
- **AI Orchestration:** LangChain4j + Spring AI 2.0.
- **Memory:** Milvus (Vector DB) for long-term context retrieval (RAG).
- **Database:** PostgreSQL with pgvector for hybrid search.
- **Deployment:** Containerized with Docker; CI/CD via GitHub Actions.

## 🛠️ Key Technical Decisions (ADR)
1. **Virtual Threads over Platform Threads:** Used to handle high-concurrency LLM streaming calls without blocking the OS threads.
2. **Tool/Function Calling:** The AI Agent is restricted to a set of Java "Tools" to prevent hallucinations and ensure type-safe database mutations.
3. **RAG (Retrieval-Augmented Generation):** Implemented to allow the agent to "remember" user preferences and past project contexts stored in the Vector DB.

## 🚀 How to Run (Architect's CLI)
1. Clone the repo.
2. Spin up the infrastructure: `docker-compose up -d`.
3. Compile to Native: `./mvnw package -Pnative`.
4. Run the binary: `./target/neurotask-runner`.

## 📈 Worldwide Masterclass Compliance
- [x] Clean Code / SOLID Principles.
- [x] 90%+ Test Coverage (JUnit 5 / Testcontainers).
- [x] OpenAPI/Swagger documented.
- [x] Observability integrated (OpenTelemetry).
