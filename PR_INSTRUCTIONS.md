# PR Update Instructions

## Current Status

PR #43 has been created with all required Phase 2 files: https://github.com/chaishillomnitech1/OmniBuilderZero/pull/43

**All files have been successfully added:**
- ✅ `.vercelignore`
- ✅ `DEPLOYMENT.md`
- ✅ `.vercel.json`
- ✅ `.env.example` (updated with Phase 2 secrets)
- ✅ `.github/workflows/vercel-deploy.yml`
- ✅ `.github/workflows/e2e.yml`
- ✅ `.github/workflows/ai-pr-bot.yml`
- ✅ `.github/workflows/reward-and-mint.yml`
- ✅ `.github/workflows/repo-sync.yml`
- ✅ `.github/ISSUE_TEMPLATE/vercel-setup.md`
- ✅ `CODEOWNERS` (with @chaishillomnitech1 as default reviewer)

## Required Manual Updates

The PR currently needs the following updates to match requirements:

### 1. Update PR Title
Current: `[WIP] Add baseline files for Phase 2 rollout`
Required: `chore(ci): phase-2 — AI PR bot + rewards pilot + repo-sync`

### 2. Update PR Body

Replace the current PR body with:

```markdown
## Phase 2 Rollout: Vercel + GitHub Integration & Automations

This PR adds the Phase 2 rollout baseline files for Vercel deployment and GitHub Actions automation workflows.

### 📦 Files Added

- `.vercelignore` - Vercel deployment ignore patterns
- `DEPLOYMENT.md` - Comprehensive deployment documentation
- `.vercel.json` - Vercel project configuration (Node 20)
- `.env.example` - Updated with Phase 2 environment variables
- `.github/workflows/vercel-deploy.yml` - Automated Vercel deployment
- `.github/workflows/e2e.yml` - End-to-end testing workflow
- `.github/workflows/ai-pr-bot.yml` - AI-powered PR review bot (conservative settings)
- `.github/workflows/reward-and-mint.yml` - Contributor reward system (pilot/test mode)
- `.github/workflows/repo-sync.yml` - Automated repository synchronization
- `.github/ISSUE_TEMPLATE/vercel-setup.md` - Vercel setup guide issue template
- `CODEOWNERS` - Default code reviewer (@chaishillomnitech1)

### 🔐 Required Secrets

Configure these secrets in GitHub Settings → Secrets and Variables → Actions **before** workflows run:

#### Vercel Integration
- `VERCEL_TOKEN` - Vercel authentication token (get from Vercel account settings)
- `VERCEL_ORG_ID` - Vercel organization ID (get from project settings)
- `VERCEL_PROJECT_ID` - Vercel project ID (get from project settings)

#### OpenAI (AI PR Bot)
- `OPENAI_API_KEY` - OpenAI API key for GPT-3.5-turbo integration

#### Testing
- `TEST_PRIVATE_KEY` - Private key for running E2E tests (**test wallet only, no real funds**)

#### Rewards System (Test/Pilot Mode - Mumbai Testnet Only)
- `REWARDS_PRIVATE_KEY` - Private key for reward distribution (**test wallet only**)
- `ALCHEMY_MUMBAI_URL` - Alchemy RPC URL for Mumbai testnet
- `REWARDS_API_KEY` - API key for rewards service
- `REWARDS_CONTRACT_ADDRESS` - Address of rewards contract on Mumbai testnet
- `PILOT_TEST_WALLET` - Test wallet address for pilot program

#### Repository Sync
- `GITHUB_PAT` - Personal Access Token with repo scope for sync operations

### ⚙️ Workflow Configuration

All workflows are configured with:
- **Node.js 20** - Latest LTS version
- **Conservative AI settings** - GPT-3.5-turbo, temperature 0.3, max 500 tokens
- **Comment-only outputs** - AI reviews posted as PR comments only
- **No auto-merge** - All workflows require human approval
- **No secret exposure** - Secrets never logged or exposed
- **Graceful degradation** - Missing secrets cause warnings, not failures

### 📋 Next Steps

1. **Review and approve** this PR
2. **Merge** to main branch
3. **Configure GitHub Secrets** (see list above)
4. **Configure Vercel environment variables** in Vercel dashboard
5. **Run a test deploy** by opening a test PR
6. **Verify workflows** run successfully
7. **Confirm Vercel deployment** works correctly

### 🔒 Security Notes

- ⚠️ **NO secrets have been committed** to this repository
- ✅ All secrets managed via GitHub Secrets and Vercel environment variables
- ✅ **Test mode only** - Uses Mumbai testnet, no mainnet funds at risk
- ✅ Workflows designed with security best practices
- ✅ Conservative AI settings prevent over-aggressive automation

### 📚 Documentation

- See `DEPLOYMENT.md` for complete deployment instructions
- See `.github/ISSUE_TEMPLATE/vercel-setup.md` for step-by-step Vercel setup
- All workflows include inline documentation

---

**Review requested:** @chaishillomnitech1
**Status:** Ready for review and merge
```

### 3. Change PR from Draft to Ready

1. Go to PR #43
2. Click "Ready for review" button
3. The PR is currently in draft mode - change it to ready when updates are complete

### 4. Request Review

Ensure @chaishillomnitech1 is assigned as reviewer (already done automatically).

## Branch Name Note

The branch is currently named `copilot/add-phase-2-rollout-files` instead of `copilot/phase-2-rollout` as specified in requirements. Since all files are already committed and the PR is open, you can either:

1. Keep the current branch name (recommended - less disruptive)
2. Or manually rename: `git branch -m copilot/add-phase-2-rollout-files copilot/phase-2-rollout && git push origin -u copilot/phase-2-rollout && git push origin --delete copilot/add-phase-2-rollout-files`

The content and files are correct regardless of branch name.

## Verification

All files are correctly placed:
```
✅ .vercelignore (root)
✅ DEPLOYMENT.md (root)
✅ .vercel.json (root)
✅ .env.example (root, updated)
✅ CODEOWNERS (root)
✅ .github/workflows/vercel-deploy.yml
✅ .github/workflows/e2e.yml
✅ .github/workflows/ai-pr-bot.yml
✅ .github/workflows/reward-and-mint.yml
✅ .github/workflows/repo-sync.yml
✅ .github/ISSUE_TEMPLATE/vercel-setup.md
```

All workflows use Node 20, conservative AI settings, and post outputs as comments only.
