# AWS ECR — OceanCortex Agent

## Repository Details

| Field | Value |
|-------|-------|
| **Registry** | `280429950087.dkr.ecr.us-east-1.amazonaws.com` |
| **Repository** | `ocean-cortex-agent` |
| **Full URI** | `280429950087.dkr.ecr.us-east-1.amazonaws.com/ocean-cortex-agent` |
| **Region** | `us-east-1` |
| **Scan on push** | ✅ enabled |

---

## First-time setup (already done)

```bash
# 1. Create the ECR repository
aws ecr create-repository \
  --repository-name ocean-cortex-agent \
  --region us-east-1 \
  --image-scanning-configuration scanOnPush=true \
  --image-tag-mutability MUTABLE
```

---

## Local Docker Workflow

### Authenticate Docker to ECR

Run this before every `docker push` or `docker pull` (token expires in 12 h):

```bash
aws ecr get-login-password --region us-east-1 \
  | docker login --username AWS --password-stdin \
    280429950087.dkr.ecr.us-east-1.amazonaws.com
```

### Build, tag & push

```bash
ECR=280429950087.dkr.ecr.us-east-1.amazonaws.com/ocean-cortex-agent

docker build -t ocean-cortex-agent:latest .
docker tag ocean-cortex-agent:latest $ECR:latest
docker push $ECR:latest
```

### Pull the latest image

```bash
docker pull 280429950087.dkr.ecr.us-east-1.amazonaws.com/ocean-cortex-agent:latest
```

---

## GitHub Actions (automated CD)

The `ci.yml` workflow automatically builds and pushes on every merge to `master`.

### Required GitHub Secrets

Go to **Settings → Secrets and variables → Actions** and add:

| Secret name | Description |
|-------------|-------------|
| `AWS_ACCESS_KEY_ID` | IAM user `jgfurlan_` access key ID |
| `AWS_SECRET_ACCESS_KEY` | IAM user `jgfurlan_` secret access key |

> **Tip:** For production, replace static keys with **OIDC** (GitHub's `aws-actions/configure-aws-credentials` supports it — set `role-to-assume` instead of key ID/secret).

---

## ECS Task Definition

Use this image URI in your ECS task definition's container definition:

```json
{
  "image": "280429950087.dkr.ecr.us-east-1.amazonaws.com/ocean-cortex-agent:latest"
}
```

The ECS task role must have the `AmazonEC2ContainerRegistryReadOnly` policy attached so ECS can pull the image at deploy time.

---

## Useful inspection commands

```bash
# List all images in the repo
aws ecr list-images --repository-name ocean-cortex-agent --region us-east-1

# Describe the repository
aws ecr describe-repositories --repository-names ocean-cortex-agent --region us-east-1

# View scan findings for the latest image
aws ecr describe-image-scan-findings \
  --repository-name ocean-cortex-agent \
  --image-id imageTag=latest \
  --region us-east-1
```
