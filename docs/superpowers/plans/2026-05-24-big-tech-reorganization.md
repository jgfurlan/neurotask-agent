# Big Tech Reorganization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reorganize the project into a professional `src/` layout with layered architecture and zero noise.

**Architecture:** Transition to a `src/ocean_vortex` package with `api/`, `core/`, and `providers/` sub-packages. Update all configurations (build, lint, docker) to match.

**Tech Stack:** Python 3.12, FastAPI, Ruff, Pytest, Docker.

---

### Task 1: Foundation & Cleanup

**Files:**
- Create: `src/ocean_vortex/api/__init__.py`, `src/ocean_vortex/core/__init__.py`, `src/ocean_vortex/providers/__init__.py`, `src/ocean_vortex/scripts/__init__.py`
- Modify: `.gitignore`
- Remove: `graphify-out/`, `run_id.txt`, `.antigravitycli/`

- [x] **Step 1: Scorch the earth**
Remove all transient and residue files.
```bash
rm -rf graphify-out/ .antigravitycli/ run_id.txt
```

- [x] **Step 2: Create new directory hierarchy**
```bash
mkdir -p src/ocean_vortex/api src/ocean_vortex/core src/ocean_vortex/providers src/ocean_vortex/scripts
touch src/ocean_vortex/__init__.py src/ocean_vortex/api/__init__.py src/ocean_vortex/core/__init__.py src/ocean_vortex/providers/__init__.py src/ocean_vortex/scripts/__init__.py
```

- [x] **Step 3: Refine .gitignore**
Remove Java/Quarkus residue and add `graphify-out/`.
```bash
# Edit .gitignore to remove Maven/Eclipse/IntelliJ/NetBeans sections
# and add graphify-out/
```

- [x] **Step 4: Commit cleanup and foundation**
```bash
git add .gitignore src/
git commit -m "chore: initialize src layout and cleanup transient artifacts"
```

---

### Task 2: Core Migration (Domain Logic)

**Files:**
- Modify: `ocean_vortex/agent.py` -> `src/ocean_vortex/core/agent.py`
- Modify: `ocean_vortex/dto.py` -> `src/ocean_vortex/core/models.py`

- [ ] **Step 1: Move and rename DTOs to models**
```bash
mv ocean_vortex/dto.py src/ocean_vortex/core/models.py
```

- [ ] **Step 2: Move agent logic**
```bash
mv ocean_vortex/agent.py src/ocean_vortex/core/agent.py
```

- [ ] **Step 3: Update imports in agent.py**
```python
# Change from:
# from ocean_vortex import dto
# To:
# from ocean_vortex.core import models
```

- [ ] **Step 4: Commit core migration**
```bash
git add src/ocean_vortex/core/
git commit -m "refactor: migrate core domain logic and models"
```

---

### Task 3: Provider Migration (Integrations)

**Files:**
- Modify: `ocean_vortex/db.py` -> `src/ocean_vortex/providers/db.py`
- Modify: `ocean_vortex/snowflake_client.py` -> `src/ocean_vortex/providers/snowflake.py`

- [ ] **Step 1: Move DB utility**
```bash
mv ocean_vortex/db.py src/ocean_vortex/providers/db.py
```

- [ ] **Step 2: Move Snowflake client**
```bash
mv ocean_vortex/snowflake_client.py src/ocean_vortex/providers/snowflake.py
```

- [ ] **Step 3: Update imports in snowflake.py**
Update any internal imports to the new structure.

- [ ] **Step 4: Commit provider migration**
```bash
git add src/ocean_vortex/providers/
git commit -m "refactor: migrate external providers (snowflake, db)"
```

---

### Task 4: API & Entrypoint Migration

**Files:**
- Modify: `ocean_vortex/main.py` -> `src/ocean_vortex/api/main.py`
- Remove: `ocean_vortex/` (once empty)

- [ ] **Step 1: Move FastAPI app**
```bash
mv ocean_vortex/main.py src/ocean_vortex/api/main.py
```

- [ ] **Step 2: Update imports in main.py**
```python
# Update all relative or absolute imports:
# from ocean_vortex.core import agent, models
# from ocean_vortex.providers import db, snowflake
```

- [ ] **Step 3: Remove old package directory**
```bash
rm -rf ocean_vortex/
```

- [ ] **Step 4: Commit API migration**
```bash
git add src/ocean_vortex/api/
git rm -r ocean_vortex/
git commit -m "refactor: migrate api layer and remove old package structure"
```

---

### Task 5: Build & Test Configuration

**Files:**
- Modify: `pyproject.toml`
- Modify: `Dockerfile`
- Modify: `tests/test_main.py`

- [ ] **Step 1: Update pyproject.toml**
Configure tools to look in `src/`.
```toml
[tool.ruff]
src = ["src"]

[tool.mypy]
mypy_path = "src"
```

- [ ] **Step 2: Update Dockerfile**
Update `COPY` commands and `CMD` to point to `src/ocean_vortex/api/main.py`.

- [ ] **Step 3: Update tests**
Fix imports in `tests/test_main.py` to point to `ocean_vortex.api.main`.

- [ ] **Step 4: Run verification**
```bash
# Run ruff, mypy, and pytest to ensure everything is correct
ruff check src tests
mypy src tests
pytest tests
```

- [ ] **Step 5: Final Commit**
```bash
git add pyproject.toml Dockerfile tests/
git commit -m "chore: update build config and tests for src layout"
```
