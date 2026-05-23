# AWS Account Migration & ECS Fargate Deployment Implementation Plan

We are migrating our AWS infrastructure to a new AWS account. This plan covers re-setting up ECR on the new account, deploying the containerized application to ECS Fargate, configuring IAM roles and secrets, and updating the CI/CD pipeline.

## User Action Required

> [!IMPORTANT]
> You must configure your local AWS CLI with the new AWS credentials. Please run `aws configure` in your terminal and enter your new **AWS Access Key ID**, **AWS Secret Access Key**, and set the default region to **`us-east-1`**.

## Proposed Changes

### Phase 1: ECR Migration
1. **Retrieve New Account ID & Region**: Verify connectivity via `aws sts get-caller-identity`.
2. **Create ECR Repository**: Create private repository `ocean-vortex-agent` in the new account.
3. **Re-authenticate Docker**: Run `aws ecr get-login-password | docker login` for the new registry.
4. **Push Docker Image**: Tag and push the current Docker image to the new ECR repository URI (`<new-account-id>.dkr.ecr.us-east-1.amazonaws.com/ocean-vortex-agent:latest`).

---

### Phase 2: ECS Fargate Setup
1. **IAM Role Creation**:
   - Create **ECS Task Execution Role** (`ocean-vortex-execution-role`) with `AmazonECSTaskExecutionRolePolicy` and permissions to read Secrets Manager.
   - Create **ECS Task Role** (`ocean-vortex-task-role`) allowing container runtime access to AWS Bedrock.
2. **Secrets Manager Setup**:
   - Store application secrets (DB credentials, Snowflake connectivity keys) in AWS Secrets Manager under name `ocean-vortex-secrets`.
3. **ECS Cluster**:
   - Create a Fargate ECS Cluster named `ocean-vortex-cluster`.
4. **ECS Task Definition**:
   - Define a task using Fargate, matching `0.5 vCPU` and `1 GB RAM`.
   - Add container referencing the new ECR image URI.
   - Map port `8000` (FastAPI web app).
   - Inject environment variables from AWS Secrets Manager.
5. **ECS Service**:
   - Create service `ocean-vortex-service` running 1 task copy inside default VPC subnets.

---

### Phase 3: CI/CD & Verification
1. **GitHub CD Secrets Update**:
   - Document new AWS Account ID and ECS parameters for OIDC deployment.
2. **Local Pull Verification**:
   - Verify image pull works from the new registry.
3. **FastAPI Web Service Verification**:
   - Verify health check endpoint `/hello` on the ECS service.

## Verification Plan

### Automated
- Test suite runs green (`pytest`).
- GitHub Actions workflow runs and successfully pushes to the new ECR registry.

### Manual
```bash
# Confirm repo and image in new account
aws ecr describe-repositories --repository-names ocean-vortex-agent --region us-east-1
aws ecr list-images --repository-name ocean-vortex-agent --region us-east-1

# Verify ECS task runs
aws ecs list-tasks --cluster ocean-vortex-cluster
```
