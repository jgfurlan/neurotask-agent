# Implement CI/CD Pipeline

Build pipeline from approved spec. 

## Proposed Changes

### Workflows
#### [DELETE] [ci.yml](file:///home/jgfurlan/dev/projects/ocean-vortex/.github/workflows/ci.yml)
Remove bad Java CI.

#### [NEW] [ci-cd.yml](file:///home/jgfurlan/dev/projects/ocean-vortex/.github/workflows/ci-cd.yml)
Add OIDC-based CI/CD workflow.
- Lint (ruff), Typecheck (mypy), Test (pytest).
- Build/Push to ECR (OIDC auth).
- Deploy to ECS (needs manual approval).

### Environment
#### [MODIFY] [docker-compose.yml](file:///home/jgfurlan/dev/projects/ocean-vortex/docker-compose.yml)
Remove hardcoded DB creds. Use `.env` vars.

#### [NEW] [.env.example](file:///home/jgfurlan/dev/projects/ocean-vortex/.env.example)
Template for local dev. Bedrock/Snowflake/Postgres vars.

## User Review Required
> [!IMPORTANT]
> Need to create AWS resources first? OIDC role, ECR repo, ECS cluster. I do code, you do AWS setup. OK?

## Verification Plan
1. Check `docker-compose up` works with `.env`.
2. Commit changes. Check GitHub Actions runs.
3. Review OIDC auth step in GH Actions logs.
