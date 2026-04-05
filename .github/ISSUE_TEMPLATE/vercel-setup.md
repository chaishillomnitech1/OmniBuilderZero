---
name: Vercel Setup
about: Guide for setting up Vercel deployment
title: '[SETUP] Vercel Deployment Configuration'
labels: ['setup', 'vercel', 'deployment']
assignees: ['chaishillomnitech1']
---

## Vercel Setup Checklist

### Prerequisites
- [ ] GitHub account with repository access
- [ ] Vercel account created
- [ ] Vercel CLI installed (optional)

### Step 1: Connect Repository to Vercel

1. **Login to Vercel**
   - Go to [vercel.com](https://vercel.com)
   - Sign in with your GitHub account

2. **Import Project**
   - Click "Add New..." → "Project"
   - Select `OmniBuilderZero` repository
   - Click "Import"

3. **Configure Project Settings**
   - **Framework Preset:** Other (Node.js)
   - **Build Command:** `npm run compile` (or leave empty)
   - **Output Directory:** Leave default
   - **Install Command:** `npm install`

### Step 2: Configure Environment Variables

Add the following environment variables in Vercel Dashboard (Settings → Environment Variables):

#### Required for Deployment
```
NODE_VERSION=20
NODE_ENV=production
```

#### Blockchain Configuration
```
PRIVATE_KEY=<your_deployment_private_key>
KUN_COIN_TREASURY=<treasury_address>
SCROLLVERSE_TREASURY=<treasury_address>
```

#### RPC Endpoints
```
MAINNET_RPC_URL=https://eth-mainnet.g.alchemy.com/v2/<YOUR-API-KEY>
SEPOLIA_RPC_URL=https://eth-sepolia.g.alchemy.com/v2/<YOUR-API-KEY>
POLYGON_RPC_URL=https://polygon-rpc.com
MUMBAI_RPC_URL=https://rpc-mumbai.maticvigil.com
SCROLL_SEPOLIA_RPC_URL=https://sepolia-rpc.scroll.io
SCROLL_RPC_URL=https://rpc.scroll.io
ALCHEMY_MUMBAI_URL=https://polygon-mumbai.g.alchemy.com/v2/<YOUR-API-KEY>
```

#### API Keys
```
ETHERSCAN_API_KEY=<your_etherscan_api_key>
POLYGONSCAN_API_KEY=<your_polygonscan_api_key>
SCROLLSCAN_API_KEY=<your_scrollscan_api_key>
```

#### Metadata
```
BASE_URI=ipfs://
```

### Step 3: Configure GitHub Secrets

Add the following secrets in GitHub (Settings → Secrets and Variables → Actions):

#### Vercel Integration
```
VERCEL_TOKEN=<get_from_vercel_account_settings>
VERCEL_ORG_ID=<get_from_vercel_project_settings>
VERCEL_PROJECT_ID=<get_from_vercel_project_settings>
```

#### OpenAI (for AI PR Bot)
```
OPENAI_API_KEY=<your_openai_api_key>
```

#### Rewards System (Test Mode)
```
REWARDS_PRIVATE_KEY=<test_wallet_private_key>
ALCHEMY_MUMBAI_URL=https://polygon-mumbai.g.alchemy.com/v2/<YOUR-API-KEY>
REWARDS_API_KEY=<your_rewards_api_key>
REWARDS_CONTRACT_ADDRESS=<rewards_contract_address>
PILOT_TEST_WALLET=<test_wallet_address>
```

#### Repository Sync
```
GITHUB_PAT=<personal_access_token_with_repo_scope>
```

### Step 4: Get Vercel Tokens

#### VERCEL_TOKEN
1. Go to Vercel Dashboard → Settings → Tokens
2. Click "Create Token"
3. Name it "GitHub Actions"
4. Copy the token and add to GitHub Secrets

#### VERCEL_ORG_ID and VERCEL_PROJECT_ID
1. Go to your Vercel project settings
2. Scroll to "General"
3. Copy "Project ID"
4. For Org ID, use the Vercel CLI:
   ```bash
   vercel link
   ```
   This creates `.vercel/project.json` with both IDs

### Step 5: Test Deployment

1. **Manual Deploy (Optional)**
   ```bash
   npm install -g vercel
   vercel login
   vercel --prod
   ```

2. **Trigger GitHub Actions**
   - Create a test branch
   - Make a small change
   - Open a pull request
   - Verify the `vercel-deploy` workflow runs
   - Check for deployment preview URL in PR comments

3. **Merge to Main**
   - Merge the PR
   - Verify production deployment

### Step 6: Verify Workflows

Check that the following workflows are running:
- [ ] `vercel-deploy.yml` - Deploys on push and PR
- [ ] `e2e.yml` - Runs tests on PR
- [ ] `ai-pr-bot.yml` - Reviews PRs with AI
- [ ] `reward-and-mint.yml` - Rewards merged PRs
- [ ] `repo-sync.yml` - Syncs with upstream (if configured)

### Troubleshooting

#### Deployment Fails
- Check Vercel logs in the Dashboard
- Verify environment variables are set correctly
- Ensure Node version is set to 20
- Check build command completes successfully

#### Workflow Failures
- Verify all required secrets are added to GitHub
- Check workflow logs in Actions tab
- Ensure token permissions are correct

#### Missing Secrets
If workflows fail due to missing secrets, they will skip gracefully with warnings rather than failing entirely.

### Security Notes

⚠️ **IMPORTANT:**
- Never commit `.env` file to the repository
- Use separate wallets for test and production
- Rotate API keys and tokens regularly
- Test on testnets before production deployment
- Review all environment variables before deployment

### Support

For issues or questions:
- Open a GitHub issue
- Tag @chaishillomnitech1
- Check `DEPLOYMENT.md` for detailed documentation

---

### Post-Setup Verification

After completing all steps, verify:
- [ ] Vercel project is connected
- [ ] All environment variables are configured
- [ ] GitHub secrets are added
- [ ] Test deployment succeeds
- [ ] Production deployment succeeds
- [ ] All workflows pass
- [ ] PR comments appear correctly

**Status:** _Update this issue with your progress_

---

This issue template is part of the Phase 2 deployment automation.
