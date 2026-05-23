# AWS ECR & ECS Deployment — OceanVortex Agent

This document details the configuration and deployment commands for AWS ECR and ECS Fargate in our active AWS account.

## Registry & Repository Details

| Field | Value |
|-------|-------|
| **Account ID** | `952078552240` |
| **Registry** | `952078552240.dkr.ecr.us-east-1.amazonaws.com` |
| **Repository** | `ocean-vortex-agent` |
| **Full URI** | `952078552240.dkr.ecr.us-east-1.amazonaws.com/ocean-vortex-agent` |
| **Region** | `us-east-1` |
| **Scan on push** | ✅ enabled |

---

## 1. Local ECR Setup & Image Push

Run the following commands in your local terminal to build the Docker container and push it to the new registry.

### Authenticate Docker to ECR

```bash
aws ecr get-login-password --region us-east-1 \
  | sudo docker login --username AWS --password-stdin \
    952078552240.dkr.ecr.us-east-1.amazonaws.com
```

### Build, Tag, and Push

```bash
ECR=952078552240.dkr.ecr.us-east-1.amazonaws.com/ocean-vortex-agent

sudo docker build -t ocean-vortex-agent:latest .
sudo docker tag ocean-vortex-agent:latest $ECR:latest
sudo docker push $ECR:latest
```

---

## 2. ECS Fargate Setup

### IAM Roles (Already Created)
- **Task Execution Role**: `ocean-vortex-execution-role` (allows pulling from ECR, logging to CloudWatch).
- **Task Role**: `ocean-vortex-task-role` (allows container code to invoke AWS Bedrock models).

### Create ECS Cluster
```bash
aws ecs create-cluster --cluster-name ocean-vortex-cluster --region us-east-1
```

### Store App Secrets (AWS Secrets Manager)
Run this to create the secrets store for DB and Snowflake credentials:
```bash
aws secretsmanager create-secret \
  --name ocean-vortex-secrets \
  --description "OceanVortex Application Secrets" \
  --secret-string '{"POSTGRES_USER":"jgfurlan","POSTGRES_PASSWORD":"secure_password_here","POSTGRES_DB":"neurotask","DATABASE_URL":"","SNOWFLAKE_ACCOUNT":"","SNOWFLAKE_USER":"","SNOWFLAKE_PASSWORD":"","SNOWFLAKE_DATABASE":"","SNOWFLAKE_WAREHOUSE":""}' \
  --region us-east-1
```

### Define Task Definition
Create a `task-definition.json` file:
```json
{
  "family": "ocean-vortex-agent",
  "networkMode": "awsvpc",
  "executionRoleArn": "arn:aws:iam::952078552240:role/ocean-vortex-execution-role",
  "taskRoleArn": "arn:aws:iam::952078552240:role/ocean-vortex-task-role",
  "containerDefinitions": [
    {
      "name": "ocean-vortex-agent",
      "image": "952078552240.dkr.ecr.us-east-1.amazonaws.com/ocean-vortex-agent:latest",
      "cpu": 512,
      "memory": 1024,
      "portMappings": [
        {
          "containerPort": 8000,
          "hostPort": 8000,
          "protocol": "tcp"
        }
      ],
      "essential": true,
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/ocean-vortex-agent",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs",
          "awslogs-create-group": "true"
        }
      }
    }
  ],
  "requiresCompatibilities": [
    "FARGATE"
  ],
  "cpu": "512",
  "memory": "1024"
}
```

Register the task:
```bash
aws ecs register-task-definition --cli-input-json file://task-definition.json --region us-east-1
```

### Create Fargate Service
Deploy the service in your VPC's public subnets:
```bash
aws ecs create-service \
  --cluster ocean-vortex-cluster \
  --service-name ocean-vortex-service \
  --task-definition ocean-vortex-agent \
  --desired-count 1 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[SUBNET_ID_1,SUBNET_ID_2],securityGroups=[SG_ID],assignPublicIp=ENABLED}" \
  --region us-east-1
```

---

## 3. GitHub Actions Integration

Update GitHub secrets for your actions runner:

| Secret Name | Value |
|-------------|-------|
| `AWS_ACCESS_KEY_ID` | Access key of your IAM user |
| `AWS_SECRET_ACCESS_KEY` | Secret access key of your IAM user |
| `AWS_ACCOUNT_ID` | `952078552240` |
