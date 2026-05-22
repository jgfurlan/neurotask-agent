# AI Workflow Rules: Execution Governance

This document governs how software changes, features, and fixes are developed and tracked.

## Spec-Driven Development
To avoid code bloat and drift, every code change must follow a structured feature specification process.

1. **Atomic Feature Specs**: Prior to writing any code, draft an Atomic Spec file in `docs/specs/` containing:
   - **Isolated Goal**: Define a single clear target output.
   - **Design Decisions**: Detail the classes, methods, and configurations involved.
   - **Implementation Map**: A chronological step-by-step checklist of edits.
   - **Verification Array**: Tests and compilation steps required for success.
2. **Review Gate**: Obtain developer review on the spec before modifying files.

## Session Governance
- **TDD (Test-Driven Development)**: Write failing tests before writing any execution logic.
- **Verification**: Run local tests and linters before completing a task.

## Linear-GitHub Synchronization
Linear is the "Source of Truth" for system planning; GitHub is the source of truth for the codebase.

1. **Issue Mapping**: Each branch must address exactly one Linear issue.
2. **Branch Naming**: Format branch names as `<issue-id>-<short-description>` (e.g. `MED-12-add-snowflake-connector`).
3. **Commit Messages**: Reference the Linear issue ID in every commit:
   - Example: `feat: [MED-12] add Snowflake DB credentials and integration clients`
4. **State Transition**:
   - **In Progress**: Move issue to "In Progress" when branch creation starts.
   - **In Review**: Move issue to "In Review" when a PR is opened.
   - **Done**: Move issue to "Done" when the PR is merged.

## Prohibited Actions
- **No Direct DB Querying**: Agents must never execute raw SQL against Snowflake. All writes and reads must go through defined API methods or helper clients.
- **No Unmocked Calls in Test Suites**: All tests must mock responses from AWS Bedrock and Snowflake Cortex AI. Running unmocked tests in normal test suites leads to flaky builds and unexpected API costs.
- **No Silent Failures**: Never write catch blocks that swallow exceptions (e.g. `except Exception: pass`). Use proper logging and raise clean HTTPException errors.
