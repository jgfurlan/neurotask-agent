# Code Standards: Agent-Legibility & Python Compliance

## Agent-Legibility (Mandatory)
The LLM is the primary consumer and code generator for this repository. Code must be structured for deterministic discovery, searchability, and minimal ambiguity.

1. **Global Uniqueness (Anti-Ambiguity):**
   - Prefix function names with `{module}_{action}` to make symbols globally search-friendly (e.g. `guest_service_get_genomics_profile` instead of generic `get_profile`).
2. **Explicit Error Paths:**
   - Bare `try...except` and silent failures (e.g., `pass`) are strictly prohibited.
   - Every exception must be caught explicitly, logged, and return a structured error status (to support negative rewards in the RLVR loop).
3. **Single Query Interfaces:**
   - Centralize all Snowflake Cortex AI queries and interactions within a single access layer (e.g., `lib/snowflake_client.py`) to prevent logic fragmentation.

## Type Compliance & Pydantic
- **Strict Typing**: Use Python `typing` type hints for all function signatures and inputs.
- **Data Validation**: Utilize **Pydantic v2** models for all API request/response structures and configuration validations. Do not use raw dictionary inputs for structured schemas.

## Linting & Formatting
- **Linter/Formatter**: **Ruff** is the mandatory tool for codebase formatting, import sorting, and linting.
- **Rule Enforcements**:
  - Max line length is set to 88 characters.
  - Mandatory docstrings on all public modules, classes, and helper tools to provide context to the code-generation agent.

## Testing Standards (TDD)
- **Framework**: **Pytest** with async support (`pytest-asyncio`).
- **TDD Workflow**:
  1. **RED**: Write a test demonstrating the new feature or reproducing a bug.
  2. **GREEN**: Write minimal code to make the test pass.
  3. **REFACTOR**: Clean up code and imports while ensuring the test stays green.
- **Verification Rule**: No Pull Request can be merged without accompanying unit tests achieving at least 80% coverage on new features, and all tests must be mocked to avoid hitting actual live AWS Bedrock and Snowflake API endpoints during standard CI/CD.
