# Design Spec: Big Tech Project Reorganization (Senior Standard)

- **Date:** 2026-05-24
- **Topic:** Codebase Reorganization & Standardization
- **Status:** Draft

## 1. Objective
Elevate the `ocean-vortex` codebase to "Big Tech" senior-level standards. This involves adopting a `src/` layout, enforcing clear architectural boundaries (Clean Architecture / Domain-Driven Design principles), and purging technical debt/residue from previous iterations (Java/Quarkus remains, transient tool outputs).

## 2. Proposed Architecture

### 2.1 Directory Structure (The "Blueprint")
We will transition to a surgical, modular structure that separates concerns and prevents circular dependencies.

```text
ocean-vortex/
├── .github/                # CI/CD pipelines (GitHub Actions)
├── docs/                   # System-level documentation & architecture
├── src/                    # Source root (prevents root-level import noise)
│   └── ocean_vortex/       # Core package
│       ├── api/            # Transport/Entrypoints (FastAPI routes, middlewares)
│       ├── core/           # Domain/Business Logic (Models, Agents, State machines)
│       ├── providers/      # External Clients/Integrations (Snowflake, AWS Bedrock)
│       └── scripts/        # Internal CLI utilities & maintenance scripts
├── tests/                  # Parallel testing hierarchy
│   ├── unit/               # Fast, isolated tests for core logic
│   └── integration/        # Tests for API & External Provider integrations
├── .env.example            # Environment configuration template
├── .gitignore              # Refined Python-specific ignore rules
├── Dockerfile              # Multi-stage production-ready build
├── pyproject.toml          # Modern PEP 517 build & dependency config
└── README.md               # Technical onboarding & contribution guide
```

### 2.2 Component Mapping
Existing files will be migrated as follows:
- `ocean_vortex/main.py` -> `src/ocean_vortex/api/main.py`
- `ocean_vortex/agent.py` -> `src/ocean_vortex/core/agent.py`
- `ocean_vortex/dto.py` -> `src/ocean_vortex/core/models.py`
- `ocean_vortex/db.py` -> `src/ocean_vortex/providers/db.py`
- `ocean_vortex/snowflake_client.py` -> `src/ocean_vortex/providers/snowflake.py`

## 3. Cleanup & Standardization

### 3.1 Noise Reduction
- **Remove:** `graphify-out/` (Transient tool output; should be in `.gitignore` if used).
- **Remove:** `run_id.txt` (Transient session artifact).
- **Remove:** `.antigravitycli/` (Internal tool residue).
- **Cleanup:** Purge Java/Quarkus/Maven references from `.gitignore` and `Dockerfile`.

### 3.2 Standards Enforcement
- Update `pyproject.toml` to reflect the `src/` layout (crucial for `ruff` and `mypy`).
- Ensure `FastAPI` app instantiation uses the new nested paths.
- Standardize on `pytest` and `ruff` for all quality checks.

## 4. Success Criteria
1. The project builds and runs successfully in Docker.
2. All tests pass with the new layout.
3. `mypy` and `ruff` pass with strict settings.
4. No residue of Java or transient artifacts remains in the root.

## 5. Review Checklist (Self-Review)
- [x] No "TBD" placeholders.
- [x] Consistent layering (API -> Core -> Providers).
- [x] Logical migration path for all existing files.
- [x] Scope is focused on reorganization, not refactoring internal logic.
