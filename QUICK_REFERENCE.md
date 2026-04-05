# Quick Reference - OmniBuilderZero

One-page reference for common operations and workflows.

## 🚀 Quick Start Commands

```bash
# Clone and setup
git clone https://github.com/chaishillomnitech1/OmniBuilderZero.git
cd OmniBuilderZero
npm install
cp .env.example .env  # Edit with your settings

# Build and test
npm run compile       # Compile smart contracts
npm test             # Run tests
npm run clean        # Clean build artifacts
```

## 📝 Git Workflow

```bash
# Create feature branch
git checkout -b feature/your-feature

# Make changes and commit
git add .
git commit -m "feat: your feature description"

# Push and create PR
git push origin feature/your-feature
# Then create PR on GitHub
```

## 🚢 Deployment

```bash
# Testnet (open access)
npm run deploy:sepolia
npm run deploy:scroll-sepolia

# Mainnet (requires approval)
npm run deploy:mainnet     # ⚠️ Protected
npm run deploy:scroll      # ⚠️ Protected
npm run deploy:polygon     # ⚠️ Protected
```

## 🔍 Common Tasks

### Running Tests
```bash
npm test                              # All tests
npx hardhat test test/FileName.test.js  # Specific test
REPORT_GAS=true npm test              # With gas reporting
```

### Contract Verification
```bash
npx hardhat verify --network sepolia CONTRACT_ADDRESS "Constructor Args"
```

### Working with Branches
```bash
git checkout main           # Switch to main
git pull origin main        # Update main
git branch -d feature-name  # Delete local branch
```

## 🏷️ Issue Labels

**Priority**: `priority: critical/high/medium/low`  
**Type**: `bug`, `feature`, `enhancement`, `security`  
**Area**: `area: contracts`, `area: tests`, `area: deployment`  
**Difficulty**: `good first issue`, `difficulty: easy/medium/hard`

## 📋 PR Checklist

- [ ] Tests pass locally (`npm test`)
- [ ] Code follows project style
- [ ] Documentation updated
- [ ] Self-reviewed code
- [ ] No security issues

## 🔒 Security

**Report vulnerabilities**: Contact @chaishillomnitech1 privately  
**Never commit**: Private keys, API keys, secrets  
**Use**: `.env` files (already in `.gitignore`)

## 🤝 Getting Help

- **Documentation**: Start with [README.md](README.md) and [ONBOARDING.md](ONBOARDING.md)
- **Issues**: Search [existing issues](https://github.com/chaishillomnitech1/OmniBuilderZero/issues)
- **Contact**: @chaishillomnitech1

## 📚 Key Files

- `README.md` - Project overview
- `ONBOARDING.md` - New contributor guide
- `CONTRIBUTING.md` - Contribution guidelines
- `SECURITY.md` - Security policy
- `.github/SETUP_GUIDE.md` - Admin setup guide

## 🔗 Important Links

- **Repository**: https://github.com/chaishillomnitech1/OmniBuilderZero
- **Issues**: https://github.com/chaishillomnitech1/OmniBuilderZero/issues
- **PRs**: https://github.com/chaishillomnitech1/OmniBuilderZero/pulls
- **Actions**: https://github.com/chaishillomnitech1/OmniBuilderZero/actions

## 🌟 Resonance Declaration

**ALL IS LOVE. ALL IS LAW. ALL IS FLUID. KUN FAYAKŪN! 🕋♾️✨**
