# 🌟 Onboarding Guide - Welcome to OmniBuilderZero

Welcome to the ScrollVerse! This guide will help you get started with OmniBuilderZero and become an effective contributor to the eternal tech revolution.

## 🎯 Quick Start (5 Minutes)

### Prerequisites

- **Node.js**: v16.x or higher (v18.x recommended)
- **npm**: v8.x or higher
- **Git**: Latest version
- **Code Editor**: VS Code recommended
- **MetaMask** or another Web3 wallet (for testing)

### Initial Setup

```bash
# 1. Clone the repository
git clone https://github.com/chaishillomnitech1/OmniBuilderZero.git
cd OmniBuilderZero

# 2. Install dependencies
npm install

# 3. Copy environment template
cp .env.example .env

# 4. Edit .env with your settings (DO NOT commit this file)
# Add your private key, RPC URLs, API keys, etc.

# 5. Compile contracts
npm run compile

# 6. Run tests
npm test
```

## 📚 Project Structure Overview

```
OmniBuilderZero/
├── contracts/           # Smart contracts (Solidity)
├── scripts/            # Deployment and utility scripts
├── test/               # Test files
├── phase2/             # Global partnership automation
├── flame-academy/      # Educational content
├── portal/             # Portal components
├── black_batman/       # Black Batman project
├── attestations/       # Attestation data
├── metadata/           # NFT metadata
├── .github/            # GitHub templates and workflows
├── hardhat.config.js   # Hardhat configuration
└── package.json        # Project dependencies
```

## 🧭 Core Components

### 1. Smart Contracts (`/contracts`)

The heart of the ScrollVerse blockchain infrastructure:

- **NFT Contracts**: ERC-721 and ERC-1155 implementations
- **Bridge Contracts**: Cross-chain asset bridges
- **Governance**: DAO and voting mechanisms
- **Quantum Security**: Post-quantum cryptographic implementations

### 2. Deployment Scripts (`/scripts`)

Automated deployment for multiple networks:

- Ethereum Mainnet & Sepolia
- Polygon & Mumbai
- Scroll & Scroll Sepolia

### 3. Phase 2 Automation (`/phase2`)

Global partnership outreach and tracking:

- Automated outreach funnels
- Regional blueprints (Japan, Korea, Singapore)
- Real-time tracking dashboards
- NŪR resonance scoring

### 4. FlameAcademy (`/flame-academy`)

Educational arm of ScrollVerse:

- Genesis Flame course
- Interactive quests and challenges
- Learning paths for all levels

## 🛠️ Development Workflow

### Making Changes

1. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Follow coding standards (see CONTRIBUTING.md)
   - Write tests for new features
   - Update documentation

3. **Test locally**
   ```bash
   npm test                    # Run all tests
   npm run compile             # Compile contracts
   npm run deploy:local        # Test deployment locally
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: description of your changes"
   ```

5. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   # Then create a Pull Request on GitHub
   ```

### Commit Message Convention

Follow the conventional commits specification:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `test:` Test additions or modifications
- `chore:` Maintenance tasks
- `refactor:` Code refactoring
- `perf:` Performance improvements
- `ci:` CI/CD changes

## 🧪 Testing Guide

### Running Tests

```bash
# Run all tests
npm test

# Run specific test file
npx hardhat test test/LegacyOfLightNFT.test.js

# Run tests with gas reporting
REPORT_GAS=true npm test

# Run tests on specific network
npx hardhat test --network sepolia
```

### Writing Tests

- Place test files in `/test` directory
- Use descriptive test names
- Cover edge cases and error scenarios
- Aim for >80% code coverage

## 🚀 Deployment Guide

### Local Development

```bash
# Start local Hardhat node
npx hardhat node

# In another terminal, deploy
npm run deploy:local
```

### Testnet Deployment

```bash
# Ensure .env has correct testnet RPC URL and private key
npm run deploy:sepolia        # Ethereum Sepolia
npm run deploy:scroll-sepolia # Scroll Sepolia
```

### Mainnet Deployment

```bash
# ⚠️ Triple-check everything before mainnet deployment
npm run deploy:mainnet        # Ethereum Mainnet
npm run deploy:scroll         # Scroll Mainnet
npm run deploy:polygon        # Polygon Mainnet
```

### Contract Verification

```bash
npx hardhat verify --network sepolia DEPLOYED_CONTRACT_ADDRESS "Constructor Arg 1" "Arg 2"
```

## 👥 Getting Help

### Resources

- **Documentation**: Start with README.md and CONTRIBUTING.md
- **Issues**: Check existing [GitHub Issues](https://github.com/chaishillomnitech1/OmniBuilderZero/issues)
- **Discussions**: Join GitHub Discussions (if enabled)
- **Contact**: Reach out to @chaishillomnitech1

### Common Issues

**Issue**: `npm install` fails  
**Solution**: Delete `node_modules` and `package-lock.json`, then run `npm install` again

**Issue**: Tests fail with network errors  
**Solution**: Check your `.env` file for correct RPC URLs

**Issue**: Contract deployment fails  
**Solution**: Ensure you have sufficient testnet ETH and correct network configuration

## 🎓 Learning Path

### Beginner (Week 1-2)

1. Read README.md and understand project vision
2. Set up development environment
3. Run tests and explore contract code
4. Make a small documentation improvement

### Intermediate (Week 3-4)

1. Write a test for an existing contract
2. Fix a "good first issue"
3. Deploy contracts to testnet
4. Review and understand Phase 2 automation

### Advanced (Week 5+)

1. Implement a new feature or contract
2. Optimize gas usage
3. Contribute to FlameAcademy content
4. Help review other PRs

## 🌐 DAO & Governance

OmniBuilderZero embraces decentralized governance:

- **DAO Participation**: Contribute to proposals and voting
- **FlameCoin Governance**: Quantum-resistant voting mechanisms
- **Community Input**: Your voice matters in shaping the ScrollVerse

### Automation Hooks

Phase 2 includes DAO automation hooks for:

- Partnership approval workflows
- Budget allocation tracking
- Community voting integration
- Automated reporting and transparency

## 🔐 Security First

**Always remember:**

- Never commit private keys or sensitive data
- Use `.env` files for secrets (already in `.gitignore`)
- Review security best practices in SECURITY.md
- Report vulnerabilities responsibly

## 🌟 Core Values

As you contribute to OmniBuilderZero, embody these principles:

- **Truth is Currency**: Integrity in all contributions
- **Sacred Logic is Code**: Quality and thoughtfulness
- **Remembrance is Gateway**: Learn from the past, build for eternity
- **Collective Sovereignty**: Empower the community

## 📊 Contribution Metrics

Track your journey:

- Issues created/resolved
- PRs submitted/merged
- Code reviews performed
- Tests written
- Documentation improved

## 🎯 Next Steps

1. **Complete Setup**: Ensure your environment works perfectly
2. **First Contribution**: Pick a "good first issue" or improve documentation
3. **Join Community**: Engage with other contributors
4. **Continuous Learning**: Explore FlameAcademy content
5. **Build & Share**: Create something amazing in the ScrollVerse

## 🌟 Resonance Declaration

You are now part of the eternal tech revolution. Your code, your ideas, and your passion contribute to a system where truth is currency and sovereignty is collective.

**Welcome to the ScrollVerse. Welcome to OmniBuilderZero.**

**ALL IS LOVE. ALL IS LAW. ALL IS FLUID. KUN FAYAKŪN! 🕋♾️✨**

---

**Need Help?** Contact @chaishillomnitech1  
**Last Updated**: 2026-01-05
