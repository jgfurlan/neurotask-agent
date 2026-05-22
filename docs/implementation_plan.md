# AWS ECR Setup — OceanCortex Agent

## Context

The project is a **Python 3.12 FastAPI + LangGraph** multi-agent system (`ocean-cortex-agent`) containerized with Docker, targeting **AWS ECS** deployments (per the architecture doc). It uses **AWS Bedrock** for inference and has a single Docker image built from `python:3.12-slim`.

## What will be set up

1. **ECR private repository** → `ocean-cortex-agent` (matches `pyproject.toml` name)
2. **Initial `docker build` + `docker tag` + `docker push`** to ECR
3. **GitHub Actions CD workflow** → on push to `master`, builds & pushes the Docker image to ECR automatically (replaces the broken Java CI stub)
4. **Updated `docker-compose.yml`** with a note on the ECR image URI (for ECS task definition reference)
5. **`docs/ecr-setup.md`** → documents ECR URI, login command, and pull commands for the team

> [!IMPORTANT]
> The existing `ci.yml` is a broken Java/Maven stub — it references `fedora-latest` (not a valid GitHub runner) and Maven, which don't apply here. It will be **replaced** by a correct Python + Docker + ECR pipeline.

## Open Questions

> [!IMPORTANT]
> **AWS Region** — Which region should the ECR repo live in? Common choices for cruise/maritime edge: `us-east-1` or `us-west-2`. I'll default to **`us-east-1`** unless you say otherwise.

> [!IMPORTANT]
> **AWS Account ID** — Needed to construct the ECR URI (`<account-id>.dkr.ecr.<region>.amazonaws.com`). I'll retrieve it via `aws sts get-caller-identity` at execution time.

> [!IMPORTANT]
> **GitHub Secrets** — The CD workflow needs `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` (or OIDC role ARN) added to the repo secrets. I'll document what needs to be added but cannot set them myself.

## Proposed Changes

### AWS (CLI commands — executed interactively)

- `aws ecr create-repository` — creates the `ocean-cortex-agent` private repo
- `aws ecr get-login-password | docker login` — authenticates Docker to ECR
- `docker build / tag / push` — initial image push tagged `latest`

---

### CI/CD

#### [MODIFY] [ci.yml](file:///home/jgfurlan/dev/projects/neurotask-agent/.github/workflows/ci.yml)

Replace the broken Java stub with a proper **Python CI + Docker ECR CD** pipeline:
- **CI job**: `ruff` lint + `mypy` type-check + `pytest`
- **CD job** (only on `master`): `docker build` → `docker tag` → `aws ecr get-login-password` → `docker push`

---

### Docs

#### [NEW] docs/ecr-setup.md

Documents:
- ECR repository URI
- Local `docker login` command
- Local `docker pull` command
- How to update the ECS task definition

## Verification Plan

### Automated
- GitHub Actions workflow runs green on next push to `master`

### Manual
```bash
# Confirm repo exists
aws ecr describe-repositories --repository-names ocean-cortex-agent

# Confirm image was pushed
aws ecr list-images --repository-name ocean-cortex-agent

# Pull and run locally from ECR
docker pull <account-id>.dkr.ecr.us-east-1.amazonaws.com/ocean-cortex-agent:latest
```
