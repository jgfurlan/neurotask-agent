# AWS Migration and Deployment Walkthrough

We have successfully migrated and set up the foundational cloud infrastructure on the new AWS account (`952078552240`).

## What has been done

1. **ECR Repository Creation**:
   - Created private repository `ocean-vortex-agent` in the `us-east-1` region of the new AWS account.
2. **ECS Fargate Cluster**:
   - Created ECS Fargate cluster named `ocean-vortex-cluster`.
3. **ECS IAM Roles**:
   - Created **ECS Task Execution Role** (`ocean-vortex-execution-role`) and attached `AmazonECSTaskExecutionRolePolicy`.
   - Created **ECS Task Role** (`ocean-vortex-task-role`) and attached `AmazonBedrockFullAccess` to permit AWS Bedrock model execution.
4. **Documentation Sync**:
   - Updated [docs/ecr-setup.md](file:///home/jgfurlan/dev/projects/ocean-vortex/docs/ecr-setup.md) with registry coordinates and command listings.

---

## Next Steps for You

Please run these commands in your local terminal to complete the ECR push:

```bash
# 1. Login to new ECR registry
aws ecr get-login-password --region us-east-1 \
  | sudo docker login --username AWS --password-stdin \
    952078552240.dkr.ecr.us-east-1.amazonaws.com

# 2. Build local Docker image
sudo docker build -t ocean-vortex-agent:latest .

# 3. Tag and push to new ECR
ECR=952078552240.dkr.ecr.us-east-1.amazonaws.com/ocean-vortex-agent
sudo docker tag ocean-vortex-agent:latest $ECR:latest
sudo docker push $ECR:latest
```
