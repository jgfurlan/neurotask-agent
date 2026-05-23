# AWS Migration and Deployment Task Tracker

- [x] Configure new AWS CLI credentials (Account: `952078552240`, Region: `us-east-1`)
- [x] Attach AWS Console IAM policy permissions (`ECR`, `ECS`, `IAM`) to user `jgfurlan_`
- [x] Re-run ECR Setup:
  - [x] Create ECR private repository `ocean-vortex-agent`
  - [x] Authenticate Docker to new ECR registry
  - [x] Build, tag, and push Docker image `ocean-vortex-agent:latest`
- [x] ECS Fargate Deployment:
  - [x] Create ECS Task Execution Role `ocean-vortex-execution-role`
  - [x] Create ECS Task Role `ocean-vortex-task-role`
  - [x] Create ECS Cluster `ocean-vortex-cluster`
  - [x] Store application credentials in AWS Secrets Manager (`ocean-vortex-secrets`)
  - [x] Register Task Definition (`ocean-vortex-task`)
  - [x] Deploy ECS Fargate Service (`ocean-vortex-service`)
- [ ] CI/CD and Verification:
  - [ ] Configure AWS OIDC Trust for GitHub Actions in AWS console
  - [ ] Add new GitHub Secrets for the CD runner
  - [x] Verify deployment endpoint `/hello`
