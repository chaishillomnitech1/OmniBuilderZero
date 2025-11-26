# Infrastructure Component

The Infrastructure module contains deployment configurations, CI/CD pipelines, and operational tooling for the ScrollVerse ecosystem.

## Purpose

- **Deployment Automation**: Terraform/Pulumi infrastructure as code
- **CI/CD Pipelines**: GitHub Actions workflows for testing and deployment
- **Monitoring**: Observability stack configuration
- **Security**: Secrets management and access control configurations

## Directory Structure

```
infra/
├── README.md           # This file
├── terraform/          # Infrastructure as Code
├── kubernetes/         # K8s manifests (if applicable)
├── monitoring/         # Prometheus, Grafana configs
├── secrets/            # Secrets management templates
└── ci/                 # CI/CD pipeline configurations
```

## Deployment Targets

### Development
- Local Hardhat network for smart contract testing
- Docker Compose for service orchestration

### Staging
- Scroll Sepolia testnet for contract deployments
- Staging cloud infrastructure

### Production
- Scroll mainnet for production contracts
- Production-grade cloud infrastructure with HA

## CI/CD Workflows

### Smart Contracts
- Compile and test on every PR
- Deploy to testnet on merge to `develop`
- Deploy to mainnet via release tags

### Services
- Lint and test on every PR
- Build container images on merge
- Deploy to staging automatically
- Promote to production via approval gates

## Status

🚧 **Under Development** - This component is part of the OTAP scaffold phase.

## Related Documentation

- [ARCHITECTURE.md](../ARCHITECTURE.md) - System architecture overview
- [DEPLOYMENT_CHECKLIST.md](../DEPLOYMENT_CHECKLIST.md) - Deployment checklist
- [hardhat.config.js](../hardhat.config.js) - Hardhat configuration
