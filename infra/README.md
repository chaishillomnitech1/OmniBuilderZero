# Infrastructure

## Purpose

This directory contains Infrastructure as Code (IaC) configurations for deploying and managing the OTAP (OmniTech Ascendancy Protocol) ecosystem components. The infrastructure supports:

- **Matchmaker Service** deployment
- **Attestation Layer** services
- **Insights UI** hosting
- **Database and caching** infrastructure
- **Monitoring and observability** stack

## IaC Options

### Terraform (Recommended)

Terraform is the primary IaC tool for cloud infrastructure provisioning.

```
infra/
├── terraform/
│   ├── main.tf              # Main configuration
│   ├── variables.tf         # Input variables
│   ├── outputs.tf           # Output values
│   ├── providers.tf         # Provider configurations
│   └── modules/
│       ├── networking/      # VPC, subnets, security groups
│       ├── compute/         # ECS/EKS/GKE configurations
│       ├── database/        # RDS/Cloud SQL setup
│       └── monitoring/      # CloudWatch/Stackdriver
```

### Supported Cloud Providers

#### AWS
- ECS/EKS for container orchestration
- RDS PostgreSQL for database
- ElastiCache for Redis
- ALB for load balancing
- CloudWatch for monitoring

#### Google Cloud Platform (GCP)
- GKE for Kubernetes
- Cloud SQL for PostgreSQL
- Memorystore for Redis
- Cloud Load Balancing
- Cloud Monitoring

#### Azure
- AKS for Kubernetes
- Azure Database for PostgreSQL
- Azure Cache for Redis
- Azure Load Balancer
- Azure Monitor

### Kubernetes (Helm Charts)

For Kubernetes deployments:

```
infra/
├── helm/
│   ├── matchmaker/
│   │   ├── Chart.yaml
│   │   ├── values.yaml
│   │   └── templates/
│   ├── attestations/
│   │   ├── Chart.yaml
│   │   ├── values.yaml
│   │   └── templates/
│   └── insights-ui/
│       ├── Chart.yaml
│       ├── values.yaml
│       └── templates/
```

### Pulumi (Alternative)

For teams preferring TypeScript/Python IaC:

```typescript
// Example Pulumi configuration
import * as aws from "@pulumi/aws";

const cluster = new aws.ecs.Cluster("otap-cluster");
const service = new aws.ecs.Service("matchmaker", {
    cluster: cluster.arn,
    desiredCount: 2,
    // ...
});
```

## Environment Structure

```
┌─────────────────────────────────────────────────────────┐
│                    Production (prod)                     │
│  - High availability (multi-AZ/region)                  │
│  - Auto-scaling enabled                                 │
│  - Full monitoring and alerting                         │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                    Staging (staging)                     │
│  - Production-like configuration                        │
│  - Used for pre-production testing                      │
│  - Limited scaling                                      │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                  Development (dev)                       │
│  - Minimal resources                                    │
│  - Single instance deployments                          │
│  - Cost-optimized                                       │
└─────────────────────────────────────────────────────────┘
```

## Quick Start

### Prerequisites

1. Install Terraform >= 1.5.0
2. Configure cloud provider credentials
3. Set up remote state backend (S3/GCS/Azure Blob)

### Initialize Terraform

```bash
cd infra/terraform
terraform init

# Select workspace
terraform workspace select dev  # or staging, prod

# Plan changes
terraform plan -var-file=environments/dev.tfvars

# Apply changes
terraform apply -var-file=environments/dev.tfvars
```

## Security Requirements

- All secrets managed via cloud secret managers (AWS Secrets Manager, GCP Secret Manager, Azure Key Vault)
- Network isolation with private subnets
- TLS termination at load balancer
- Regular security scanning of infrastructure
- Principle of least privilege for IAM roles

## CI/CD Integration

Infrastructure changes should flow through:

1. **Pull Request** - Terraform plan output as PR comment
2. **Approval** - Required for production changes
3. **Apply** - Automated apply on merge to main

## TODOs

- [ ] Create base Terraform modules
- [ ] Set up remote state backend
- [ ] Define environment-specific variable files
- [ ] Create Helm charts for Kubernetes deployments
- [ ] Implement secret management integration
- [ ] Add monitoring and alerting configurations
- [ ] Create disaster recovery procedures
- [ ] Document scaling policies
- [ ] Set up cost monitoring and budgets

---

*This component is part of the OmniTech Ascendancy Protocol (OTAP) ecosystem.*
