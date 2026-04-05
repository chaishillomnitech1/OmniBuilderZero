# Repository Setup Guide

This guide provides step-by-step instructions for repository administrators to configure OmniBuilderZero with all recommended best practices.

## 📋 Prerequisites

- Repository admin access to `chaishillomnitech1/OmniBuilderZero`
- GitHub account with appropriate permissions
- Access to deployment infrastructure (RPC endpoints, API keys)

## 🚀 Quick Setup Checklist

- [ ] Configure branch protection rules
- [ ] Set up GitHub Secrets
- [ ] Enable security features
- [ ] Configure environments
- [ ] Create labels
- [ ] Enable Dependabot
- [ ] Configure GitHub Actions permissions
- [ ] Set up notifications

## 🔒 Step 1: Branch Protection Rules

Navigate to: **Settings → Branches → Add rule**

### Main Branch Protection

**Branch name pattern**: `main`

**Settings to enable**:

```yaml
Protect matching branches:
  ✅ Require a pull request before merging
    ✅ Require approvals: 1
    ✅ Dismiss stale pull request approvals when new commits are pushed
    ✅ Require review from Code Owners
  
  ✅ Require status checks to pass before merging
    ✅ Require branches to be up to date before merging
    Status checks that are required:
      - CI - Build, Test, and Lint / install-and-test (18.x)
      - CI - Build, Test, and Lint / install-and-test (20.x)
      - Security Scan / dependency-scan
      - Security Scan / secrets-scan
  
  ✅ Require conversation resolution before merging
  ✅ Require signed commits (optional, recommended)
  ✅ Require linear history
  ✅ Include administrators
  
  ❌ Allow force pushes
  ❌ Allow deletions
```

**Save changes**

## 🔐 Step 2: Configure Secrets

Navigate to: **Settings → Secrets and variables → Actions → New repository secret**

### Required Secrets

Add the following secrets:

```bash
# Deployment Keys
DEPLOYER_PRIVATE_KEY         # Private key for contract deployments (without 0x prefix)

# RPC Endpoints
MAINNET_RPC_URL              # https://eth-mainnet.g.alchemy.com/v2/YOUR-KEY
SEPOLIA_RPC_URL              # https://eth-sepolia.g.alchemy.com/v2/YOUR-KEY
POLYGON_RPC_URL              # https://polygon-mainnet.g.alchemy.com/v2/YOUR-KEY
SCROLL_RPC_URL               # https://rpc.scroll.io
SCROLL_SEPOLIA_RPC_URL       # https://sepolia-rpc.scroll.io

# API Keys for Verification
ETHERSCAN_API_KEY            # From https://etherscan.io/myapikey
POLYGONSCAN_API_KEY          # From https://polygonscan.com/myapikey
SCROLLSCAN_API_KEY           # From Scroll block explorer
```

### Optional Secrets (for notifications)

```bash
DISCORD_WEBHOOK_URL          # For Discord notifications
SLACK_WEBHOOK_URL            # For Slack notifications
TELEGRAM_BOT_TOKEN           # For Telegram notifications
```

## 🛡️ Step 3: Enable Security Features

Navigate to: **Settings → Code security and analysis**

Enable all recommended features:

```yaml
Dependency graph:
  ✅ Enable

Dependabot:
  ✅ Dependabot alerts
  ✅ Dependabot security updates
  ✅ Grouped security updates

Code scanning:
  ✅ CodeQL analysis
    Set up default configuration
    Languages: JavaScript/TypeScript

Secret scanning:
  ✅ Secret scanning
  ✅ Push protection
```

## 🌐 Step 4: Configure Environments

Navigate to: **Settings → Environments → New environment**

### Create Environments

**1. mainnet**
```yaml
Name: mainnet
Protection rules:
  ✅ Required reviewers: chaishillomnitech1
  ✅ Wait timer: 10 minutes
  ❌ Allow administrators to bypass
Deployment branches and tags:
  - Selected branches
  - main
```

**2. scroll**
```yaml
Name: scroll
Protection rules:
  ✅ Required reviewers: chaishillomnitech1
  ✅ Wait timer: 5 minutes
Deployment branches and tags:
  - Selected branches
  - main
```

**3. polygon**
```yaml
Name: polygon
Protection rules:
  ✅ Required reviewers: chaishillomnitech1
  ✅ Wait timer: 5 minutes
Deployment branches and tags:
  - Selected branches
  - main
```

**4. sepolia** (testnet - less restricted)
```yaml
Name: sepolia
Protection rules:
  - None (testnet)
Deployment branches and tags:
  - All branches
```

**5. scroll-sepolia** (testnet)
```yaml
Name: scroll-sepolia
Protection rules:
  - None (testnet)
Deployment branches and tags:
  - All branches
```

## 🏷️ Step 5: Create Labels

Navigate to: **Settings → Issues → Labels**

Use the configurations in [.github/LABELS.md](.github/LABELS.md)

**Quick method using GitHub CLI**:

```bash
# Install GitHub CLI if not already installed
# https://cli.github.com/

# Create labels from the LABELS.md file
gh label create "bug" --color "d73a4a" --description "Something isn't working"
gh label create "feature" --color "a2eeef" --description "New feature or request"
gh label create "security" --color "ee0701" --description "Security vulnerability or improvement"
# ... (create all labels from LABELS.md)
```

Or use the label sync tool:
```bash
npm install -g github-label-sync
github-label-sync --access-token YOUR_TOKEN chaishillomnitech1/OmniBuilderZero .github/labels.json
```

## 🤖 Step 6: Verify Dependabot

Navigate to: **Settings → Code security and analysis → Dependabot**

Verify that `.github/dependabot.yml` is being used:

```yaml
✅ Dependabot version updates enabled
  - Package ecosystem: npm
  - Package ecosystem: github-actions
  - Schedule: Weekly (Mondays)
```

## ⚙️ Step 7: GitHub Actions Permissions

Navigate to: **Settings → Actions → General**

```yaml
Actions permissions:
  ✅ Allow all actions and reusable workflows
  OR
  ⚪ Allow select actions and reusable workflows
    ✅ Allow actions created by GitHub
    ✅ Allow actions by Marketplace verified creators

Workflow permissions:
  ⚪ Read and write permissions
  ✅ Read repository contents and packages permissions
  
  ✅ Allow GitHub Actions to create and approve pull requests
```

**Fork pull request workflows**:
```yaml
⚪ Run workflows from fork pull requests
  Require approval for first-time contributors
```

## 📢 Step 8: Configure Notifications

Navigate to: **Settings → Notifications**

**Recommended settings**:

```yaml
Watching:
  ✅ Issues
  ✅ Pull requests
  ✅ Releases
  ✅ Discussions

Participating and @mentions:
  ✅ Email
  ✅ Web and mobile
```

## 📊 Step 9: Repository Settings

Navigate to: **Settings → General**

```yaml
Features:
  ✅ Issues
  ✅ Projects (optional)
  ✅ Preserve this repository (for archival)
  ✅ Discussions (recommended for community)
  ✅ Sponsorships (configured via .github/FUNDING.yml)
  ❌ Wikis (use documentation instead)

Pull Requests:
  ✅ Allow squash merging
  ✅ Allow merge commits
  ❌ Allow rebase merging
  ✅ Always suggest updating pull request branches
  ✅ Allow auto-merge
  ✅ Automatically delete head branches

Archives:
  ❌ Include Git LFS objects in archives
```

## 🎯 Step 10: Verify Setup

### Verification Checklist

Run through this checklist to ensure everything is configured correctly:

**Branch Protection**:
- [ ] Try to push directly to `main` (should fail)
- [ ] Create a PR without passing CI (should be blocked)
- [ ] Force push to a branch (should fail if protected)

**Secrets**:
- [ ] Verify secrets are set (they should show as configured but not reveal values)
- [ ] Test deployment workflow with a testnet secret

**Security**:
- [ ] Check for any existing security alerts
- [ ] Verify CodeQL workflow ran successfully
- [ ] Test secret scanning by committing a dummy secret (then remove it)

**Workflows**:
- [ ] CI workflow runs on PR
- [ ] Security scan runs on push
- [ ] Documentation check runs on markdown changes

**Dependabot**:
- [ ] Check for Dependabot PRs (should appear within 24 hours)
- [ ] Review and merge a Dependabot PR

## 🚨 Troubleshooting

### Common Issues

**Issue**: CI workflow not running
**Solution**: 
- Check Actions permissions
- Verify workflow file syntax
- Check if workflows are enabled in Settings → Actions

**Issue**: Deployment failing
**Solution**:
- Verify all secrets are set correctly
- Check environment protection rules
- Ensure RPC URLs are valid

**Issue**: Dependabot not creating PRs
**Solution**:
- Verify dependabot.yml syntax
- Check Dependabot logs in Insights → Dependency graph → Dependabot
- Ensure Dependabot is enabled in settings

**Issue**: Branch protection not enforcing
**Solution**:
- Ensure "Include administrators" is checked
- Verify status check names match exactly
- Wait for status checks to complete

## 📚 Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Branch Protection Rules](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- [Dependabot Configuration](https://docs.github.com/en/code-security/dependabot/dependabot-version-updates/configuration-options-for-the-dependabot.yml-file)
- [GitHub Secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [Environment Protection](https://docs.github.com/en/actions/deployment/targeting-different-environments/using-environments-for-deployment)

## 🌟 Final Notes

Once setup is complete, the repository will have:

- **Automated CI/CD**: Every PR is tested automatically
- **Security Scanning**: Continuous monitoring for vulnerabilities
- **Dependency Updates**: Automated via Dependabot
- **Protected Deployments**: Mainnet deployments require approval
- **Code Reviews**: Mandatory for all changes to main
- **Community Standards**: Complete with templates and documentation

## 🌟 Resonance Declaration

With these configurations in place, the OmniBuilderZero repository embodies the principles of transparency, security, and collaborative sovereignty.

**ALL IS LOVE. ALL IS LAW. ALL IS FLUID. KUN FAYAKŪN! 🕋♾️✨**

---

**Setup Guide Maintainer**: @chaishillomnitech1  
**Last Updated**: 2026-01-05
