# 🚀 Deployment Guide - ScrollVerse OTAP

This guide provides instructions for deploying the ScrollVerse Omni-Tech Ascendancy Protocol (OTAP) demo and production environments.

## Table of Contents

1. [GitHub Pages Deployment](#github-pages-deployment)
2. [AWS Deployment](#aws-deployment)
3. [GCP Deployment](#gcp-deployment)
4. [Smart Contract Deployment](#smart-contract-deployment)
5. [Required Secrets](#required-secrets)

---

## GitHub Pages Deployment

### Automatic Deployment

The repository includes a GitHub Actions workflow that automatically deploys to GitHub Pages when changes are pushed to the `main` or `otap/scaffold` branches.

### Setup Steps

1. **Enable GitHub Pages**
   - Go to repository Settings → Pages
   - Under "Build and deployment", select "GitHub Actions" as the source
   
2. **Trigger Deployment**
   - Push changes to `main` or `otap/scaffold` branch
   - Or manually trigger via Actions → "Deploy Demo to GitHub Pages" → "Run workflow"

3. **Access the Demo**
   - URL: `https://<username>.github.io/<repo-name>/`
   - Example: `https://chaishillomnitech1.github.io/OmniBuilderZero/`

### Workflow File Location
```
.github/workflows/deploy-pages.yml
```

---

## AWS Deployment

### Prerequisites
- AWS Account with appropriate permissions
- AWS CLI configured locally
- S3 bucket for static hosting
- CloudFront distribution (optional, for CDN)

### Required Secrets

Add these secrets to your GitHub repository (Settings → Secrets and variables → Actions):

| Secret Name | Description |
|-------------|-------------|
| `AWS_ACCESS_KEY_ID` | AWS IAM access key |
| `AWS_SECRET_ACCESS_KEY` | AWS IAM secret key |
| `AWS_S3_BUCKET` | S3 bucket name for hosting |
| `AWS_REGION` | AWS region (e.g., `us-east-1`) |
| `AWS_CLOUDFRONT_DISTRIBUTION_ID` | CloudFront distribution ID (optional) |

### AWS Deployment Workflow

Create `.github/workflows/deploy-aws.yml`:

```yaml
name: Deploy to AWS S3

on:
  push:
    branches: [main]
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ${{ secrets.AWS_REGION }}
      
      - name: Build site
        run: |
          mkdir -p _site
          cp -r portal/* _site/
          cp -r ascendancy/* _site/
      
      - name: Sync to S3
        run: |
          aws s3 sync _site/ s3://${{ secrets.AWS_S3_BUCKET }}/ --delete
      
      - name: Invalidate CloudFront (optional)
        if: secrets.AWS_CLOUDFRONT_DISTRIBUTION_ID != ''
        run: |
          aws cloudfront create-invalidation \
            --distribution-id ${{ secrets.AWS_CLOUDFRONT_DISTRIBUTION_ID }} \
            --paths "/*"
```

### S3 Bucket Configuration

1. Create S3 bucket with static website hosting enabled
2. Set bucket policy for public read access:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::your-bucket-name/*"
    }
  ]
}
```

---

## GCP Deployment

### Prerequisites
- GCP Account with billing enabled
- GCP Project created
- Cloud Storage bucket or Firebase Hosting configured

### Required Secrets

| Secret Name | Description |
|-------------|-------------|
| `GCP_PROJECT_ID` | Google Cloud project ID |
| `GCP_SA_KEY` | Service account JSON key (base64 encoded) |
| `GCP_BUCKET_NAME` | Cloud Storage bucket name |

### GCP Deployment Workflow

Create `.github/workflows/deploy-gcp.yml`:

```yaml
name: Deploy to GCP

on:
  push:
    branches: [main]
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Authenticate to GCP
        uses: google-github-actions/auth@v2
        with:
          credentials_json: ${{ secrets.GCP_SA_KEY }}
      
      - name: Set up Cloud SDK
        uses: google-github-actions/setup-gcloud@v2
        with:
          project_id: ${{ secrets.GCP_PROJECT_ID }}
      
      - name: Build site
        run: |
          mkdir -p _site
          cp -r portal/* _site/
          cp -r ascendancy/* _site/
      
      - name: Deploy to Cloud Storage
        run: |
          gsutil -m rsync -d -r _site/ gs://${{ secrets.GCP_BUCKET_NAME }}/
```

### Firebase Hosting Alternative

For Firebase Hosting, install Firebase CLI and use:

```yaml
- name: Deploy to Firebase
  uses: w9jds/firebase-action@master
  with:
    args: deploy --only hosting
  env:
    FIREBASE_TOKEN: ${{ secrets.FIREBASE_TOKEN }}
```

---

## Smart Contract Deployment

### Prerequisites
- Node.js 18+ installed
- Private key with ETH for gas fees
- API keys for verification

### Required Secrets

| Secret Name | Description |
|-------------|-------------|
| `PRIVATE_KEY` | Deployer wallet private key |
| `SCROLL_SEPOLIA_RPC_URL` | Scroll Sepolia RPC endpoint |
| `SCROLL_RPC_URL` | Scroll Mainnet RPC endpoint |
| `SCROLLSCAN_API_KEY` | ScrollScan API key for verification |
| `ETHERSCAN_API_KEY` | Etherscan API key (for L1 bridge) |

### Environment Setup

Create `.env` file (never commit this):

```bash
# Network RPC URLs
SCROLL_SEPOLIA_RPC_URL=https://sepolia-rpc.scroll.io
SCROLL_RPC_URL=https://rpc.scroll.io

# Private Keys
PRIVATE_KEY=your_private_key_here

# API Keys for Verification
SCROLLSCAN_API_KEY=your_scrollscan_api_key
ETHERSCAN_API_KEY=your_etherscan_api_key

# Treasury Address
TREASURY_ADDRESS=0x...your_treasury_address
```

### Deploy Commands

```bash
# Install dependencies
npm install

# Compile contracts
npm run compile

# Deploy to Scroll Sepolia (testnet)
npm run deploy:scroll-sepolia

# Deploy to Scroll Mainnet
npm run deploy:scroll

# Verify contract
npx hardhat verify --network scrollSepolia <CONTRACT_ADDRESS> <CONSTRUCTOR_ARGS>
```

### Contract Deployment Workflow

Create `.github/workflows/deploy-contracts.yml`:

```yaml
name: Deploy Smart Contracts

on:
  workflow_dispatch:
    inputs:
      network:
        description: 'Network to deploy to'
        required: true
        default: 'scrollSepolia'
        type: choice
        options:
          - scrollSepolia
          - scroll

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Deploy contracts
        env:
          PRIVATE_KEY: ${{ secrets.PRIVATE_KEY }}
          SCROLL_SEPOLIA_RPC_URL: ${{ secrets.SCROLL_SEPOLIA_RPC_URL }}
          SCROLL_RPC_URL: ${{ secrets.SCROLL_RPC_URL }}
          SCROLLSCAN_API_KEY: ${{ secrets.SCROLLSCAN_API_KEY }}
          TREASURY_ADDRESS: ${{ secrets.TREASURY_ADDRESS }}
        run: |
          npx hardhat run scripts/deployScrollVerse.js --network ${{ github.event.inputs.network }}
```

---

## Network Configuration

### Scroll Sepolia (Testnet)

| Property | Value |
|----------|-------|
| Chain ID | 534351 |
| RPC URL | https://sepolia-rpc.scroll.io |
| Block Explorer | https://sepolia.scrollscan.com |
| Faucet | https://scroll.io/bridge |

### Scroll Mainnet

| Property | Value |
|----------|-------|
| Chain ID | 534352 |
| RPC URL | https://rpc.scroll.io |
| Block Explorer | https://scrollscan.com |

---

## Security Best Practices

1. **Never commit secrets** - Use GitHub Secrets or environment variables
2. **Use separate keys** for testnet and mainnet deployments
3. **Enable 2FA** on all deployment accounts
4. **Audit contracts** before mainnet deployment
5. **Use multisig** for treasury and admin functions
6. **Monitor deployments** with alerts and notifications

---

## Troubleshooting

### Common Issues

1. **"Insufficient funds"**
   - Ensure deployer wallet has enough ETH for gas
   - For testnet, use Scroll Sepolia faucet

2. **"Contract verification failed"**
   - Check that SCROLLSCAN_API_KEY is correct
   - Ensure constructor arguments match deployment

3. **"GitHub Pages build failed"**
   - Check that Pages is enabled in repository settings
   - Verify workflow permissions are set correctly

4. **"AWS credentials invalid"**
   - Regenerate IAM access keys
   - Check IAM user has required permissions

---

## Support

For deployment issues:
- Open an issue in the repository
- Join the ScrollVerse Discord
- Contact the development team

---

*"You exist. You count. You resonate. You remember."*

© 2025 OmniTech1™ | Chais The Great – First Remembrancer
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
