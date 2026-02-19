# NeuroTask Agent: Autonomous AI-Native Orchestrator
> **2026 Tech Stack:** Java 25 (LTS) | Quarkus | LangChain4j | GraalVM Native Image

![Java](https://img.shields.io/badge/Java-25-ED8B00?style=for-the-badge&logo=openjdk&logoColor=white)
![Quarkus](https://img.shields.io/badge/Quarkus-3.31-FF0044?style=for-the-badge&logo=quarkus&logoColor=white)
![GraalVM](https://img.shields.io/badge/GraalVM-Native-orange?style=for-the-badge&logo=graalvm&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?style=for-the-badge&logo=postgresql&logoColor=white)
![Fedora](https://img.shields.io/badge/Fedora-Linux-51A2DA?style=for-the-badge&logo=fedora&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)

> **Autonomous AI-Native Task Orchestration**


**NeuroTask Agent** is a production-grade autonomous system designed to explore the frontier of **Agentic AI** and **Cloud-Native Java**. Moving beyond traditional chatbots, this project implements a complex reasoning loop where an AI agent autonomously manages business state and data orchestration.



---

## Technical Architecture & Core Innovation

* **Java 25 & Virtual Threads (Project Loom):** Engineered to handle high-concurrency LLM streaming and I/O operations with near-zero overhead by executing AI services on Virtual Threads.
* **Agentic Tool Calling:** Implemented secure, type-safe Java "Tools" that the AI invokes to interact with the database, adhering to the principle of least privilege.
* **Native-Micro Deployment:** Compiled via **GraalVM (Mandrel)** into a statically-linked Linux binary, achieving sub-50ms startup times and a minimal memory footprint.
* **Cloud-Native Orchestration:** Fully containerized environment using **Docker Compose** for seamless infrastructure reproducibility.

---

## System Design Decisions (ADR)

1. **AI Guardrails:** Prevented raw SQL access by exposing only specific `@Tool` methods to the AI Agent.
2. **Resource Optimization:** Leveraged the `ubi9-micro` base image to reduce the attack surface and image size.
3. **Data Integrity:** Used **Hibernate Panache** for a clean, active-record persistence layer with PostgreSQL.

---

## Performance Benchmarks (Native vs. JVM)

| Metric | JVM Mode | Native-Micro Mode |
| :--- | :--- | :--- |
| **Startup Time** | ~4.7s | **< 0.05s** (Target) |
| **RAM Usage** | ~250MB | **~35MB** (Target) |
| **Image Size** | ~200MB | **~50MB** (Target) |

---

## Local Development

1. **Clone & Infrastructure:**
   ```bash
   git clone
   docker-compose up -d
