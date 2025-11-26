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
