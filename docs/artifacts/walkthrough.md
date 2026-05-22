# CI/CD Pipeline Implementation Walkthrough

## What changed
1. **Removed `ci.yml`**: Deleted the bad Java/Maven workflow.
2. **Added `ci-cd.yml`**: Created new 3-stage GitHub Actions pipeline:
   - **CI**: runs `ruff`, `mypy`, `pytest` on push/PR to main.
   - **Build-push**: builds Docker image and pushes to ECR using OIDC auth.
   - **Deploy**: updates ECS task definition and service, requires manual approval.
3. **Updated `docker-compose.yml`**: Removed hardcoded Postgres credentials (`Uno234$$6`). Used variable interpolation with safe defaults.
4. **Added `.env.example`**: Created template for required environment variables (DB, AWS, Bedrock, Snowflake).

## Why
- OIDC eliminates static AWS keys in GitHub Secrets.
- Pipeline matches enterprise CD patterns with a manual approval gate for prod.
- Hardcoded passwords in git are a security risk (even if gitignored, the compose file wasn't).

## Validation
- Checked file contents.
- Committed to Git.
- Next step for you: create OIDC role and ECS cluster in AWS console.
