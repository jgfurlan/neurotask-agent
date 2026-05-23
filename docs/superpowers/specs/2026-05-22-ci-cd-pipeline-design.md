# CI/CD Pipeline Design for OceanVortex Agent

## Overview
This design outlines a production-grade CI/CD pipeline and secrets management strategy for the OceanVortex Agent. The goal is to provide a realistic, enterprise-ready workflow that mirrors Carnival Corporation's actual stack, deploying to AWS ECS via GitHub Actions, using secure OIDC authentication.

## 1. Pipeline Structure
A single unified workflow file `.github/workflows/ci-cd.yml` will be used, replacing the current broken Java CI.

### Jobs
- **CI (Linting & Testing):**
  - Triggers on: All pushes and Pull Requests.
  - Steps: `ruff` (linting), `mypy` (type-checking), and `pytest` (unit tests).
- **Build & Push:**
  - Triggers on: Merge to `main`.
  - Depends on: CI passing.
  - Steps: Build Docker image, tag with git SHA and `latest`, push to Amazon ECR.
  - Authentication: OIDC (no static AWS keys).
- **Deploy:**
  - Triggers on: Successful Build & Push.
  - Environment: `production` (Requires manual approval gate in GitHub Actions).
  - Steps: Update ECS task definition with the new image SHA, redeploy ECS Fargate service.

## 2. OIDC Authentication
The pipeline will use GitHub OIDC to authenticate with AWS, eliminating the need to store long-lived static AWS access keys in GitHub Secrets.

- **GitHub Workflow:** Uses `aws-actions/configure-aws-credentials@v4` with a role ARN.
- **AWS Setup:**
  - OIDC Identity Provider (`token.actions.githubusercontent.com`).
  - IAM Role (`github-actions-ocean-vortex`).
  - Trust Policy: Strictly scoped to `repo:jgfurlan/ocean-vortex:ref:refs/heads/main`.
  - Permissions: Scoped to ECR pushing and ECS service updates.

## 3. Secrets & Configuration Strategy
A layered approach to configuration and secrets management will be implemented to separate development environments from production runtime.

- **Local Development:**
  - A `.env.example` file will be created and committed to the repository, containing all required environment variables.
  - The actual `.env` file will remain gitignored.
  - `docker-compose.yml` will be updated to read variables from the environment instead of hardcoded values.
- **GitHub Actions (Pipeline Config):**
  - Non-sensitive configuration (e.g., `AWS_REGION`, `ECR_REGISTRY`, ECS Cluster/Service names) will be stored in GitHub Secrets/Variables.
- **ECS Runtime (Production):**
  - Sensitive runtime values (Snowflake credentials, Bedrock models, Database URL) will be stored in AWS Secrets Manager.
  - The ECS task definition will be configured to inject these secrets securely into the container at startup.

## 4. Required AWS Infrastructure
To support the pipeline and the deployment target, the following AWS resources must exist (or be provisioned):
- **IAM:** OIDC Provider and the `github-actions-ocean-vortex` Role.
- **ECR:** Repository `ocean-vortex-agent` (already created).
- **ECS:** Fargate cluster (`ocean-vortex-cluster`), Task Definition (`ocean-vortex-task`), and Service (`ocean-vortex-service`).
- **Secrets Manager:** Secrets referenced by the ECS task.
