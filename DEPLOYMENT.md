# OmniBuilderZero Deployment Guide

## Overview
This guide covers the deployment process for OmniBuilderZero, including Vercel deployment, smart contract deployment, and CI/CD pipeline setup.

## Prerequisites

### Required Tools
- Node.js 20.x or higher
- npm or yarn
- Git
- Hardhat
- Vercel CLI (optional)

### Required Accounts
- GitHub account with repository access
- Vercel account (for frontend deployment)
- Alchemy account (for RPC endpoints)
- Etherscan/Polygonscan/Scrollscan API keys (for contract verification)

## Environment Setup

### Local Development
1. Clone the repository:
   ```bash
   git clone https://github.com/chaishillomnitech1/OmniBuilderZero.git
   cd OmniBuilderZero
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Copy `.env.example` to `.env` and fill in your values:
   ```bash
   cp .env.example .env
   ```

4. Configure your private key and RPC URLs in `.env`

### Vercel Deployment

#### Initial Setup
1. Install Vercel CLI (optional):
   ```bash
   npm install -g vercel
   ```

2. Link your project to Vercel:
   ```bash
   vercel link
   ```

3. Configure environment variables in Vercel dashboard:
   - Go to Project Settings → Environment Variables
   - Add all secrets from `.env.example`

#### Automatic Deployment
- The repository is configured with GitHub Actions for automatic deployment
- Push to the main branch triggers a production deployment
- Pull requests trigger preview deployments

#### Manual Deployment
```bash
vercel --prod
```

## Smart Contract Deployment

### Test Networks

#### Scroll Sepolia
```bash
npm run deploy:scroll-sepolia
```

#### Ethereum Sepolia
```bash
npm run deploy:sepolia
```

#### Polygon Mumbai
```bash
npm run deploy:polygon
```

### Production Networks

#### Scroll Mainnet
```bash
npm run deploy:scroll
```

#### Ethereum Mainnet
```bash
npm run deploy:mainnet
```

#### Polygon Mainnet
```bash
npm run deploy:polygon
```

### Contract Verification
After deployment, verify your contracts:
```bash
npm run verify -- --network <network-name> <contract-address> <constructor-args>
```

## CI/CD Pipeline

### GitHub Actions Workflows

#### 1. Vercel Deploy (`vercel-deploy.yml`)
- Triggered on push to main and pull requests
- Deploys to Vercel automatically
- Runs build checks before deployment

#### 2. E2E Tests (`e2e.yml`)
- Runs end-to-end tests on pull requests
- Validates contract interactions
- Ensures deployment readiness

#### 3. AI PR Bot (`ai-pr-bot.yml`)
- Reviews pull requests automatically
- Provides code quality feedback
- Suggests improvements

#### 4. Reward and Mint (`reward-and-mint.yml`)
- Automated reward distribution
- NFT minting for contributors
- Test wallet validation

#### 5. Repo Sync (`repo-sync.yml`)
- Syncs with upstream repositories
- Keeps dependencies updated
- Maintains consistency across forks

## Required Secrets

### GitHub Secrets
Configure these in GitHub Settings → Secrets and Variables → Actions:

#### Vercel
- `VERCEL_TOKEN`: Vercel authentication token
- `VERCEL_ORG_ID`: Vercel organization ID
- `VERCEL_PROJECT_ID`: Vercel project ID

#### OpenAI (for AI PR Bot)
- `OPENAI_API_KEY`: OpenAI API key for GPT integration

#### Blockchain & Rewards
- `REWARDS_PRIVATE_KEY`: Private key for reward distribution (test wallet)
- `ALCHEMY_MUMBAI_URL`: Alchemy RPC URL for Mumbai testnet
- `REWARDS_API_KEY`: API key for rewards service
- `REWARDS_CONTRACT_ADDRESS`: Address of rewards contract
- `PILOT_TEST_WALLET`: Test wallet address for pilot program

#### Repository Sync
- `GITHUB_PAT`: Personal Access Token for repo sync operations

### Vercel Environment Variables
Configure these in Vercel dashboard:
- All blockchain RPC URLs
- API keys for external services
- Base URIs for metadata
- Treasury addresses

## Post-Deployment Checklist

### Verification Steps
- [ ] Vercel deployment successful
- [ ] All environment variables configured
- [ ] Smart contracts deployed and verified
- [ ] CI/CD pipelines running correctly
- [ ] AI PR bot responding to pull requests
- [ ] E2E tests passing
- [ ] Reward system functional (test mode)

### Monitoring
- Check Vercel deployment logs
- Monitor GitHub Actions workflow runs
- Review AI PR bot feedback
- Validate test transactions on testnets

### Troubleshooting
- Review deployment logs in Vercel dashboard
- Check GitHub Actions logs for workflow failures
- Verify environment variables are correctly set
- Ensure network RPC endpoints are accessible
- Confirm wallet addresses have sufficient test tokens

## Security Best Practices

1. **Never commit secrets to the repository**
2. **Use environment variables for all sensitive data**
3. **Rotate API keys and private keys regularly**
4. **Test on testnets before production deployment**
5. **Use separate wallets for test and production**
6. **Enable 2FA on all service accounts**
7. **Review and audit smart contracts before deployment**
8. **Monitor contract interactions and transactions**

## Support and Resources

- GitHub Issues: Report bugs and request features
- Documentation: Check README.md for project overview
- Community: Join discussions in pull requests
- Maintainer: @chaishillomnitech1

## Version History

### Phase 2 (Current)
- Vercel integration
- GitHub Actions automation
- AI PR bot implementation
- Reward and minting system
- Repository synchronization

### Phase 1
- Initial contract deployment
- Basic testing infrastructure
- Manual deployment process

---

For questions or issues, please contact the maintainer or open a GitHub issue.
