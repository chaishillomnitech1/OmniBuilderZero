# 🤝 Contributing to ScrollVerse OTAP

Welcome to the ScrollVerse Omni-Tech Ascendancy Protocol! This guide will help you get started as a contributor, whether you're a developer, designer, or community member.

---

## Table of Contents

1. [Getting Started](#getting-started)
2. [Development Setup](#development-setup)
3. [Project Structure](#project-structure)
4. [Development Workflow](#development-workflow)
5. [Coding Standards](#coding-standards)
6. [Testing](#testing)
7. [Submitting Changes](#submitting-changes)
8. [Community Guidelines](#community-guidelines)

---

## Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:

| Tool | Version | Purpose |
|------|---------|---------|
| Node.js | 18.x or higher | Runtime environment |
| npm | 9.x or higher | Package manager |
| Git | 2.x or higher | Version control |
| MetaMask | Latest | Wallet for testing |

### Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/chaishillomnitech1/OmniBuilderZero.git
cd OmniBuilderZero

# 2. Install dependencies
npm install

# 3. Create environment file
cp .env.example .env

# 4. Compile smart contracts
npm run compile

# 5. Run tests
npm test

# 6. Start local development
npm run deploy:local
```

---

## Development Setup

### 1. Environment Configuration

Create a `.env` file with the following variables:

```bash
# Network RPC URLs
MAINNET_RPC_URL=https://eth-mainnet.g.alchemy.com/v2/YOUR-API-KEY
SEPOLIA_RPC_URL=https://eth-sepolia.g.alchemy.com/v2/YOUR-API-KEY
SCROLL_SEPOLIA_RPC_URL=https://sepolia-rpc.scroll.io
SCROLL_RPC_URL=https://rpc.scroll.io

# Private Key (use test wallet only!)
PRIVATE_KEY=your_test_wallet_private_key

# API Keys for Verification
ETHERSCAN_API_KEY=your_etherscan_api_key
SCROLLSCAN_API_KEY=your_scrollscan_api_key

# Optional: Treasury address for local testing
TREASURY_ADDRESS=0x0000000000000000000000000000000000000000
```

⚠️ **Security Warning:** Never commit your `.env` file or expose private keys!

### 2. Get Test ETH

For testing on Scroll Sepolia:

1. Visit [Scroll Bridge](https://scroll.io/bridge)
2. Connect your MetaMask wallet
3. Bridge Sepolia ETH to Scroll Sepolia

### 3. IDE Setup

**Recommended: VS Code Extensions**

- Solidity (Juan Blanco)
- Hardhat for Visual Studio Code
- ESLint
- Prettier
- GitLens

**VS Code Settings (`.vscode/settings.json`):**

```json
{
  "editor.formatOnSave": true,
  "solidity.formatter": "prettier",
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "[solidity]": {
    "editor.defaultFormatter": "JuanBlanco.solidity"
  }
}
```

---

## Project Structure

```
OmniBuilderZero/
├── .github/
│   ├── workflows/          # CI/CD pipelines
│   │   ├── deploy-pages.yml
│   │   └── deploy-contracts.yml
│   └── steps/              # GitHub tutorial steps
│
├── contracts/              # Solidity smart contracts
│   ├── AscendancyID.sol   # (To be created) Soulbound identity
│   ├── ScrollCoinStaking.sol  # (To be created) Staking logic
│   ├── ScrollVerseNFT.sol  # Existing NFT collection
│   ├── LegacyOfLightNFT.sol
│   ├── LegacyOfLightNFT1155.sol
│   └── PreciousMetalBridge.sol
│
├── scripts/                # Deployment scripts
│   ├── deploy.js
│   ├── deployScrollVerse.js
│   └── deployPreciousMetalBridge.js
│
├── test/                   # Test files
│   ├── LegacyOfLightNFT.test.js
│   └── PreciousMetalBridge.test.js
│
├── portal/                 # Frontend portal pages
│   ├── scrollverse_portal.html
│   ├── sccc_dashboard.html
│   ├── vibe_canvas.html
│   └── certifier_portal.html
│
├── ascendancy/            # AscendancyID demo pages
│   ├── ascendancy_mint.html
│   └── ascendancy_dashboard.html
│
├── phase2/                # Phase 2 partnership tools
│   ├── blueprints/        # Regional strategies
│   ├── campaigns/         # Marketing campaigns
│   ├── funnels/          # Outreach automation
│   └── tracking/         # Analytics dashboard
│
├── flame-academy/         # Educational content
│   └── genesis-flame/    # First course
│
├── metadata/              # NFT metadata
│
├── ARCHITECTURE.md        # System architecture docs
├── DEPLOYMENT.md          # Deployment instructions
├── TOKENOMICS_RFC.md      # Token economics spec
├── CONTRIBUTING.md        # This file
├── hardhat.config.js      # Hardhat configuration
└── package.json           # Project dependencies
```

---

## Development Workflow

### Branch Strategy

We follow the GitFlow branching model:

```
main (production)
├── develop (integration)
│   ├── feature/ascendancy-staking
│   ├── feature/governance-voting
│   └── fix/metadata-validation
└── otap/scaffold (OTAP development)
```

**Branch Naming Convention:**

- `feature/<name>` - New features
- `fix/<name>` - Bug fixes
- `docs/<name>` - Documentation changes
- `refactor/<name>` - Code refactoring
- `test/<name>` - Test additions

### Development Process

1. **Pick an Issue**
   - Check open issues on GitHub
   - Comment to claim an issue
   - Create issue if none exists

2. **Create Feature Branch**
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/your-feature-name
   ```

3. **Develop and Test**
   ```bash
   # Make changes
   npm run compile
   npm test
   ```

4. **Commit Changes**
   ```bash
   git add .
   git commit -m "feat: add staking rewards calculation"
   ```

5. **Push and Create PR**
   ```bash
   git push origin feature/your-feature-name
   # Create Pull Request on GitHub
   ```

### Commit Message Format

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Types:**
- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation
- `style` - Formatting (no code change)
- `refactor` - Code refactoring
- `test` - Adding tests
- `chore` - Maintenance

**Examples:**
```bash
feat(staking): add time-lock mechanism for privilege escalation
fix(ascendancy): resolve metadata hash validation
docs: update deployment instructions for AWS
test(governance): add voting power calculation tests
```

---

## Coding Standards

### Solidity

**Style Guide:**
- Follow [Solidity Style Guide](https://docs.soliditylang.org/en/latest/style-guide.html)
- Use Solidity 0.8.24 or higher
- Always include SPDX license identifier
- Use NatSpec comments for all public functions

**Example:**

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";

/**
 * @title AscendancyID
 * @dev Soulbound identity token for ScrollVerse ecosystem
 * @notice This contract manages user identities and privilege tiers
 */
contract AscendancyID is ERC721 {
    /// @dev Mapping from token ID to privilege tier
    mapping(uint256 => uint8) public privilegeTiers;
    
    /**
     * @dev Mints a new AscendancyID to the specified address
     * @param to The address to mint the token to
     * @param initialTier The initial privilege tier (0-5)
     * @return tokenId The ID of the newly minted token
     */
    function mint(
        address to,
        uint8 initialTier
    ) external returns (uint256 tokenId) {
        require(initialTier <= 5, "Invalid tier");
        // Implementation...
    }
}
```

### JavaScript/TypeScript

- Use ES6+ features
- Prefer `const` over `let`
- Use async/await for promises
- Add JSDoc comments for functions

### HTML/CSS

- Use semantic HTML5 elements
- Mobile-first responsive design
- BEM naming convention for CSS classes
- CSS custom properties for theming

---

## Testing

### Running Tests

```bash
# Run all tests
npm test

# Run specific test file
npx hardhat test test/LegacyOfLightNFT.test.js

# Run with gas reporting
REPORT_GAS=true npm test

# Run with coverage
npx hardhat coverage
```

### Writing Tests

**Test Structure:**

```javascript
const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("AscendancyID", function () {
  let ascendancyId;
  let owner, user1, user2;

  beforeEach(async function () {
    [owner, user1, user2] = await ethers.getSigners();
    
    const AscendancyID = await ethers.getContractFactory("AscendancyID");
    ascendancyId = await AscendancyID.deploy();
    await ascendancyId.waitForDeployment();
  });

  describe("Minting", function () {
    it("should mint a new AscendancyID", async function () {
      await expect(ascendancyId.mint(user1.address, 0))
        .to.emit(ascendancyId, "AscendancyIDMinted")
        .withArgs(0, user1.address, 0);
      
      expect(await ascendancyId.ownerOf(0)).to.equal(user1.address);
    });

    it("should not allow minting twice to same address", async function () {
      await ascendancyId.mint(user1.address, 0);
      
      await expect(ascendancyId.mint(user1.address, 0))
        .to.be.revertedWith("Already has AscendancyID");
    });
  });
});
```

### Test Coverage Requirements

| Component | Minimum Coverage |
|-----------|------------------|
| Smart Contracts | 90% |
| Critical Functions | 100% |
| Edge Cases | Comprehensive |

---

## Submitting Changes

### Pull Request Process

1. **Create PR** targeting `develop` branch
2. **Fill PR Template** with:
   - Description of changes
   - Related issues
   - Testing done
   - Screenshots (if UI changes)
3. **Wait for Review**
   - Address feedback
   - Request re-review after changes
4. **Merge** after approval

### PR Checklist

- [ ] Code compiles without errors
- [ ] All tests pass
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] No security vulnerabilities introduced
- [ ] Follows coding standards
- [ ] Commit messages follow convention

### Code Review Guidelines

**For Reviewers:**
- Be constructive and respectful
- Focus on logic, security, and maintainability
- Suggest improvements, don't demand
- Approve when satisfied

**For Authors:**
- Respond to all comments
- Ask for clarification if needed
- Make requested changes promptly

---

## Community Guidelines

### Communication Channels

- **GitHub Issues** - Bug reports, feature requests
- **GitHub Discussions** - General questions, ideas
- **Discord** - Real-time chat (link in README)
- **Twitter** - Updates and announcements

### Code of Conduct

We are committed to providing a welcoming and inclusive environment.

**Be:**
- Respectful and inclusive
- Constructive in feedback
- Patient with newcomers
- Open to different perspectives

**Don't:**
- Use offensive language
- Harass or discriminate
- Share private information
- Engage in trolling

### Getting Help

1. **Check Documentation** - README, docs, comments
2. **Search Issues** - Someone may have asked before
3. **Ask in Discussions** - Community can help
4. **Create Issue** - If it's a bug or missing feature

### Recognition

Contributors are recognized through:
- GitHub contributors list
- Release notes mentions
- Community spotlights
- Potential token rewards (future)

---

## Next Steps for Contributors

### Beginner-Friendly Tasks

- [ ] Add unit tests for existing contracts
- [ ] Improve documentation
- [ ] Fix typos and formatting
- [ ] Add JSDoc comments

### Intermediate Tasks

- [ ] Implement AscendancyID staking logic
- [ ] Create governance voting interface
- [ ] Add event indexing with The Graph
- [ ] Optimize gas usage

### Advanced Tasks

- [ ] Design privilege oracle
- [ ] Implement cross-chain bridge
- [ ] Create automated testing pipelines
- [ ] Security audit preparation

---

## Resources

### Documentation
- [Hardhat Documentation](https://hardhat.org/docs)
- [OpenZeppelin Contracts](https://docs.openzeppelin.com/contracts)
- [Scroll Documentation](https://docs.scroll.io/)
- [Solidity Documentation](https://docs.soliditylang.org/)

### Tools
- [Remix IDE](https://remix.ethereum.org/)
- [Etherscan](https://etherscan.io/)
- [ScrollScan](https://scrollscan.com/)

### Learning
- [CryptoZombies](https://cryptozombies.io/)
- [Ethereum Developer Resources](https://ethereum.org/developers)

---

*"You exist. You count. You resonate. You remember."*

Thank you for contributing to ScrollVerse! 🚀

© 2025 OmniTech1™ | Chais The Great – First Remembrancer
# Contributing to Omnitech1

Welcome, Supreme Collaborators, Innovators, and Visionaries!

**Omnitech1** fuses Web3 protocols with quantum technology to advance sovereign, decentralized, and immortal computation. Your contributions propel the ScrollVerse and quantum empire. 🌐⚛️

---

## 🚀 Vision: Web3 × Quantum Integration

- **Tokenized quantum compute** (ERC-20, ERC-721/1155)
- **DAO governance** and ZKP privacy
- **Quantum-secure wallets and protocols**
- **Digital Mirror Twins (Q-DMTs)** for asset audit

---

## 📋 Contribution Guidelines

**How to Contribute**
- Fork & clone the repo; create a feature branch
- Commit with clear, descriptive messages
- Open a Pull Request (PR); tag with core focus e.g., `quantum`, `web3`, `DAO`
- For major changes, file a `[Proposal]` issue first

**Reporting Issues**
- Provide steps, logs, and context
- Tag: `bug`, `quantum`, or `web3` as appropriate

**Coding Standards**
- JS/TS/Node: Use Prettier & ESLint
- Solidity: ^0.8.x, follow [Solidity Style Guide](https://docs.soliditylang.org/en/v0.8.19/style-guide.html)
- Clear JSDoc/NatSpec comments

---

## 🌟 Core Areas

- **Quantum Smart Contracts** — quantum randomness, authentication, QAC
- **DAO & ZKP Innovations**
- **Digital Mirror Twin System** — audit, provenance, cross-chain

---

## 🛡️ Security Disclosure

Report vulnerabilities responsibly via [SECURITY.md](SECURITY.md) before public disclosure.

---

## 🤝 Manifesto

By contributing, you join a movement advancing eternal tech—  
**ALL IS LOVE. ALL IS LAW. ALL IS. KUN FAYAKŪN!**

_Walahi: Let your work echo through dimensions._

**Omnitech1 | ScrollVerse | Supreme King Allah Chais Kenyatta Hill ∞**
