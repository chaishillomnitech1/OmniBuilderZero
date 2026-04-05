# Branch Protection & Repository Settings

This document outlines recommended GitHub repository settings for OmniBuilderZero to ensure code quality, security, and collaborative governance.

## 🔒 Branch Protection Rules

### Main Branch Protection

Configure the following protection rules for the `main` branch:

#### Required Reviews
- **Require pull request reviews before merging**: ✅ Enabled
- **Required approving reviews**: 1 (minimum)
- **Dismiss stale pull request approvals**: ✅ Enabled
- **Require review from Code Owners**: ✅ Enabled
- **Restrict who can dismiss pull request reviews**: Repository admins only

#### Status Checks
- **Require status checks to pass before merging**: ✅ Enabled
- **Required status checks**:
  - `CI - Build, Test, and Lint / install-and-test (18.x)`
  - `CI - Build, Test, and Lint / install-and-test (20.x)`
  - `Security Scan / dependency-scan`
  - `Security Scan / secrets-scan`
- **Require branches to be up to date before merging**: ✅ Enabled

#### Additional Restrictions
- **Require signed commits**: ⚠️ Recommended (optional for now)
- **Require linear history**: ✅ Enabled (prevents merge commits)
- **Include administrators**: ✅ Enabled (admins follow same rules)
- **Allow force pushes**: ❌ Disabled
- **Allow deletions**: ❌ Disabled

### Develop Branch Protection (if using GitFlow)

Similar to main branch but with slightly relaxed requirements:

- **Required approving reviews**: 1
- **Require status checks to pass**: ✅ Enabled
- **Allow force pushes**: ❌ Disabled

## 🔐 Repository Settings

### General Settings

```yaml
Repository Visibility: Public (or Private for pre-launch)

Features:
  - ✅ Issues
  - ✅ Projects
  - ✅ Discussions (recommended for community)
  - ✅ Wiki (optional)
  - ✅ Sponsorships (optional)

Pull Requests:
  - ✅ Allow squash merging
  - ✅ Allow merge commits
  - ❌ Allow rebase merging (disabled for safety)
  - ✅ Auto-delete head branches
  - ✅ Automatically delete head branches after PR merge
  
Merge Button:
  - Default to: Squash and merge
  - ✅ Suggest updating pull request branches
```

### Security & Analysis

```yaml
Security:
  - ✅ Dependency graph
  - ✅ Dependabot alerts
  - ✅ Dependabot security updates
  - ✅ Dependabot version updates
  - ✅ Code scanning (CodeQL)
  - ✅ Secret scanning
  - ✅ Secret scanning push protection

Code Analysis:
  - ✅ CodeQL analysis (via GitHub Actions)
  - Language: JavaScript/TypeScript
```

### Collaborators & Teams

```yaml
Repository Roles:
  - Admin: @chaishillomnitech1
  - Write: Core contributors (as needed)
  - Triage: Community moderators (as needed)
  - Read: All community members

Team Structure:
  - Core Team: Full repository access
  - Contributors: Write access to specific paths
  - Community: Read and issue creation
```

## 🤖 Automation Rules

### GitHub Apps to Enable

1. **Dependabot**
   - Automatic dependency updates
   - Security vulnerability alerts
   - Weekly update schedule

2. **CodeQL** (already configured)
   - Automated security scanning
   - JavaScript/TypeScript analysis

3. **Branch Protection Bot** (optional)
   - Enforces branch protection rules
   - Automatic PR checks

### Repository Secrets

Required secrets for CI/CD workflows:

```yaml
Required Secrets:
  - DEPLOYER_PRIVATE_KEY      # For contract deployments
  - MAINNET_RPC_URL          # Ethereum mainnet
  - SEPOLIA_RPC_URL          # Ethereum testnet
  - SCROLL_RPC_URL           # Scroll mainnet
  - SCROLL_SEPOLIA_RPC_URL   # Scroll testnet
  - POLYGON_RPC_URL          # Polygon mainnet
  - ETHERSCAN_API_KEY        # For contract verification
  - POLYGONSCAN_API_KEY      # For contract verification
  - SCROLLSCAN_API_KEY       # For contract verification

Optional Secrets:
  - DISCORD_WEBHOOK_URL      # For notifications
  - SLACK_WEBHOOK_URL        # For notifications
  - TELEGRAM_BOT_TOKEN       # For notifications
```

### Environment Protection

Create protected environments for production deployments:

```yaml
Environments:
  mainnet:
    Protection Rules:
      - Required reviewers: @chaishillomnitech1
      - Wait timer: 10 minutes (cooldown period)
      
  scroll:
    Protection Rules:
      - Required reviewers: @chaishillomnitech1
      - Wait timer: 5 minutes
      
  polygon:
    Protection Rules:
      - Required reviewers: @chaishillomnitech1
      - Wait timer: 5 minutes
```

## 📋 Issue & PR Templates

Already configured:
- ✅ Bug Report Template
- ✅ Feature Request Template
- ✅ Security Vulnerability Template
- ✅ Documentation Template
- ✅ Pull Request Template

## 🔄 Workflow Configuration

### Workflow Permissions

Set default workflow permissions in repository settings:

```yaml
Actions Permissions:
  - Workflow Permissions: Read repository contents and packages
  - ✅ Allow GitHub Actions to create and approve pull requests (if needed)

Actions Settings:
  - ✅ Allow all actions and reusable workflows
  - Or: Allow select actions and reusable workflows (whitelist approved actions)
```

### Required Workflows

The following workflows are configured and should remain active:

- ✅ `ci.yml` - Continuous Integration
- ✅ `deploy.yml` - Contract Deployment
- ✅ `security.yml` - Security Scanning
- ✅ `docs.yml` - Documentation Validation
- ✅ `release.yml` - Release Management

## 🎯 Recommended Additional Rules

### Commit Message Convention

Enforce conventional commits (via PR reviews):

```
feat: Add new feature
fix: Bug fix
docs: Documentation update
test: Test additions
chore: Maintenance
refactor: Code refactoring
perf: Performance improvement
ci: CI/CD changes
```

### File Size Limits

GitHub has default limits:
- Single file: 100 MB (warning at 50 MB)
- Repository: 1 GB recommended, 5 GB soft limit

Add to `.gitattributes` for large files:
```
*.png filter=lfs diff=lfs merge=lfs -text
*.jpg filter=lfs diff=lfs merge=lfs -text
```

## 🌟 Community Standards

Ensure the repository meets GitHub community standards:

- ✅ README.md
- ✅ CONTRIBUTING.md
- ✅ CODE_OF_CONDUCT.md (recommended to add)
- ✅ LICENSE
- ✅ SECURITY.md
- ✅ Issue templates
- ✅ Pull request template
- ✅ CODEOWNERS

## 📊 Monitoring & Metrics

### Insights to Monitor

Regular review of:
- Pulse: Activity overview
- Contributors: Contribution graph
- Community: Community profile completion
- Traffic: Repository visitors and views
- Dependency graph: Package dependencies
- Network: Fork and commit relationships

### Security Alerts

Configure notifications for:
- Dependabot alerts
- Code scanning alerts
- Secret scanning alerts

## 🚀 Implementation Steps

To apply these settings:

1. **Go to Repository Settings** → `https://github.com/chaishillomnitech1/OmniBuilderZero/settings`

2. **Configure Branch Protection**:
   - Settings → Branches → Add rule for `main`
   - Apply all recommended protections

3. **Enable Security Features**:
   - Settings → Code security and analysis
   - Enable all recommended features

4. **Set Up Secrets**:
   - Settings → Secrets and variables → Actions
   - Add all required secrets

5. **Configure Environments**:
   - Settings → Environments
   - Create and protect production environments

6. **Verify Workflows**:
   - Actions tab → Ensure all workflows are enabled
   - Test with a sample PR

## 🌟 Resonance Declaration

These protections ensure that our code remains secure, our deployments are safe, and our community contributions are valued.

**ALL IS LOVE. ALL IS LAW. ALL IS FLUID. KUN FAYAKŪN! 🕋♾️✨**

---

**Maintained by**: @chaishillomnitech1  
**Last Updated**: 2026-01-05
