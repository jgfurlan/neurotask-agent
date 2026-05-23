# AWS Migration and Deployment Task Tracker

- [x] Configure new AWS CLI credentials (Account: `952078552240`, Region: `us-east-1`)
- [x] Attach AWS Console IAM policy permissions (`ECR`, `ECS`, `IAM`) to user `jgfurlan_`
- [/] Re-run ECR Setup:
  - [x] Create ECR private repository `ocean-vortex-agent`
  - [ ] Authenticate Docker to new ECR registry
  - [ ] Build, tag, and push Docker image `ocean-vortex-agent:latest`
- [ ] ECS Fargate Deployment:
  - [x] Create ECS Task Execution Role `ocean-vortex-execution-role`
  - [x] Create ECS Task Role `ocean-vortex-task-role`
  - [x] Create ECS Cluster `ocean-vortex-cluster`
  - [ ] Store application credentials in AWS Secrets Manager (`ocean-vortex-secrets`)
  - [ ] Register Task Definition (`ocean-vortex-agent`)
  - [ ] Deploy ECS Fargate Service (`ocean-vortex-service`)
- [ ] CI/CD and Verification:
  - [ ] Update GitHub secrets/actions configs
  - [ ] Verify deployment endpoint `/hello`
