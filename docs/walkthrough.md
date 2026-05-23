# AWS Migration and Deployment Walkthrough

We have successfully migrated and deployed the rebranded containerized application to AWS ECS Fargate on the new AWS account (`952078552240`).

## What has been done

1. **ECR Repository Creation**:
   - Created private repository `ocean-vortex-agent` in the `us-east-1` region.
   - Pushed Docker image tagged `latest` (Digest: `sha256:04c032c7e5b03782a98d076458dcf748f46068d5f72ea4a59c5d8cee9155e8ee`).
2. **ECS Fargate Cluster**:
   - Created ECS Fargate cluster named `ocean-vortex-cluster`.
3. **ECS IAM Roles**:
   - Created **ECS Task Execution Role** (`ocean-vortex-execution-role`) and attached `AmazonECSTaskExecutionRolePolicy`.
   - Created **ECS Task Role** (`ocean-vortex-task-role`) and attached `AmazonBedrockFullAccess`.
   - Configured execution role inline policy (`SecretsExecutionPolicy`) for Secrets Manager access.
4. **Secrets Manager Setup**:
   - Created secret store `ocean-vortex-secrets` in Secrets Manager to store DB and Snowflake credentials.
5. **ECS Task Definition & Service**:
   - Registered task definition `ocean-vortex-task:1` (injecting secrets from Secrets Manager).
   - Pre-created CloudWatch log group `/ecs/ocean-vortex-agent`.
   - Deployed ECS Service `ocean-vortex-service` running 1 replica task.
   - Allowed inbound TCP port `8000` in the default security group.
6. **Documentation & Rebranding Sync**:
   - Updated [docs/ecr-setup.md](file:///home/jgfurlan/dev/projects/neurotask-agent/docs/ecr-setup.md) with registry coordinates and ECS deployment instructions.
   - Replaced all references of `ocean-cortex` with `ocean-vortex` across 10 markdown documentation files and `pyproject.toml`.
   - Re-generated knowledge graph files (`graph.json`, `graph.html`, `GRAPH_REPORT.md`).

---

## Verification & Active Endpoints

- **ECS Task Status**: Running successfully.
- **Task Public IP**: `3.236.150.62`
- **FastAPI Public Endpoint**: [http://3.236.150.62:8000/hello](http://3.236.150.62:8000/hello)
- **FastAPI OpenAPI Docs**: [http://3.236.150.62:8000/docs](http://3.236.150.62:8000/docs)
