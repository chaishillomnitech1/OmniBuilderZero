# ScrollVerse Repository Map & Integration Guide

This document provides a comprehensive map of the ScrollVerse ecosystem repositories and their interconnections.

## 🗺️ Repository Ecosystem Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                         SCROLLVERSE ECOSYSTEM                        │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                        OmniBuilderZero (Hub)                         │
│  • Core infrastructure & documentation                               │
│  • Phase 2 partnership automation                                    │
│  • Star Dust frequency protocols                                     │
│  • Regional blueprint definitions                                    │
└──────────┬──────────────────┬──────────────────┬─────────────────────┘
           │                  │                  │
           ▼                  ▼                  ▼
┌──────────────────┐  ┌──────────────┐  ┌─────────────────┐
│ ScrollVerse-     │  │ ScrollVerse- │  │ ScrollVerse-    │
│ NFT-Core         │  │ Contracts    │  │ Dashboard       │
│                  │  │              │  │                 │
│ • Guardian NFTs  │  │ • Partnership│  │ • Tracking UI   │
│ • ERC-721/1155   │  │   agreements │  │ • Star Dust viz │
│ • Metadata       │  │ • Multi-chain│  │ • Web3 connect  │
└────────┬─────────┘  └───────┬──────┘  └────────┬────────┘
         │                    │                   │
         └────────────────────┼───────────────────┘
                              ▼
                   ┌─────────────────────┐
                   │ ScrollVerse-Academy │
                   │ • Education platform│
                   │ • Certification NFTs│
                   │ • Learning paths    │
                   └─────────────────────┘
```

## 📚 Repository Details

### 1. OmniBuilderZero (Central Hub)
**Status**: ✅ Active  
**URL**: https://github.com/chaishillomnitech1/OmniBuilderZero  
**Purpose**: Core infrastructure and documentation hub for ScrollVerse

#### Key Components
- **Phase 2 Partnership System**: Automated outreach, regional blueprints
- **Star Dust Frequencies**: Resonance-based partnership scoring
- **Emissary Bots**: AI-powered partnership engagement agents
- **NŪR Protocol**: Truth-alignment verification system
- **Multi-region Localization**: JP/KR/SG cultural adaptation

#### Directory Structure
```
/phase2
  /emissary_bots         - Outreach automation
  /star_dust_frequencies - Resonance algorithms
  /nft_development       - Guardian NFT specs
  /blockchain_integration- Web3 infrastructure
  /blueprints            - Regional strategies
  /tracking              - Analytics dashboards
  /localization          - Cultural configs
```

#### Dependencies
- **Provides to**: All other repos (source of truth)
- **Consumes from**: None (root repository)

#### Key Files
- `README.md` - Main documentation
- `REPOSITORY_MAP.md` - This file
- `phase2/protocols/nur_global_integration.md` - Core protocol spec
- `phase2/emissary_bots/outreach_automation.py` - Main automation engine

---

### 2. ScrollVerse-NFT-Core
**Status**: 🔄 Planned  
**URL**: https://github.com/chaishillomnitech1/ScrollVerse-NFT-Core (to be created)  
**Purpose**: Guardian NFT smart contract implementations

#### Key Components
- **Guardian NFT Contracts**: ERC-721 and ERC-1155 implementations
- **Metadata Standards**: JSON schemas for NFT attributes
- **IPFS Integration**: Decentralized metadata storage
- **Minting Logic**: Partnership verification and NFT creation
- **Access Control**: Role-based permissions for NFT features

#### Planned Directory Structure
```
/contracts
  /GuardianNFT.sol       - Main ERC-721 contract
  /GuardianBatch.sol     - ERC-1155 for batch minting
  /AccessControl.sol     - Permission management
/metadata
  /schemas               - JSON metadata standards
  /templates             - Template generators
/scripts
  /deploy.js             - Deployment automation
  /mint.js               - Minting scripts
/test
  /GuardianNFT.test.js   - Contract tests
```

#### Dependencies
- **Depends on**: OmniBuilderZero for partnership data and specifications
- **Provides to**: Dashboard (NFT display), Contracts (NFT references)

#### Integration Points
- Reads partnership status from OmniBuilderZero tracking system
- Provides NFT contract addresses to Dashboard
- Emits events consumed by tracking systems

#### Example Flow
```javascript
// When partnership reaches "PARTNERSHIP" status in OmniBuilderZero:
1. Emissary bot triggers mintGuardianNFT()
2. Smart contract verifies partnership data from oracle
3. NFT minted with metadata: {
     partner: "Sony Corporation",
     region: "JP",
     resonance_score: 8.7,
     activated_at: timestamp
   }
4. Event emitted → Dashboard updates → Partner receives NFT
```

---

### 3. ScrollVerse-Contracts
**Status**: 🔄 Planned  
**URL**: https://github.com/chaishillomnitech1/ScrollVerse-Contracts (to be created)  
**Purpose**: Multi-chain smart contract infrastructure

#### Key Components
- **Partnership Agreements**: On-chain partnership terms
- **Multi-chain Deployment**: Ethereum, Polygon, Scroll zkEVM
- **Oracle Integration**: Chainlink for off-chain data
- **DAO Governance**: Decentralized partnership decisions
- **Payment Contracts**: Automated partnership compensation

#### Planned Directory Structure
```
/contracts
  /core
    /PartnershipAgreement.sol  - Agreement logic
    /ResonanceOracle.sol       - Star Dust oracle
    /GovernanceDAO.sol         - DAO voting
  /integrations
    /ChainlinkConsumer.sol     - Oracle integration
    /MultiChainBridge.sol      - Cross-chain comms
/deployments
  /ethereum                    - Mainnet deployments
  /polygon                     - L2 deployments
  /scroll                      - zkEVM deployments
/scripts
  /deploy-all-chains.js        - Multi-chain deployment
```

#### Dependencies
- **Depends on**: OmniBuilderZero (blueprint specs), NFT-Core (NFT references)
- **Provides to**: Dashboard (contract data), Academy (certification logic)

#### Integration Points
- Deploys contracts based on OmniBuilderZero blueprint specifications
- References Guardian NFT contracts for access control
- Provides contract addresses to Dashboard for UI interaction

---

### 4. ScrollVerse-Dashboard
**Status**: 🔄 Planned  
**URL**: https://github.com/chaishillomnitech1/ScrollVerse-Dashboard (to be created)  
**Purpose**: Web3-enabled partnership tracking interface

#### Key Components
- **Real-time Tracking**: Live partnership funnel visualization
- **Star Dust Visualization**: Interactive resonance score displays
- **Web3 Wallet Integration**: MetaMask, WalletConnect
- **Guardian NFT Gallery**: Display partner NFTs
- **Analytics Dashboard**: Metrics and KPIs

#### Planned Tech Stack
- **Frontend**: React + TypeScript + Vite
- **Web3**: ethers.js / wagmi
- **Styling**: Tailwind CSS + shadcn/ui
- **Charts**: Recharts / D3.js for Star Dust visualization
- **State**: Zustand + React Query

#### Planned Directory Structure
```
/src
  /components
    /PartnershipFunnel      - Funnel visualization
    /ResonanceVisualizer    - Star Dust charts
    /GuardianNFTGallery     - NFT display
    /Web3Connect            - Wallet integration
  /hooks
    /usePartnershipData     - Fetch from OmniBuilderZero APIs
    /useContracts           - Smart contract interactions
  /pages
    /Dashboard              - Main dashboard
    /Partnerships           - Partnership list
    /Analytics              - Detailed metrics
```

#### Dependencies
- **Depends on**: OmniBuilderZero (tracking APIs), Contracts (on-chain data), NFT-Core (NFT display)
- **Provides to**: End users (UI interface)

#### Integration Points
- Fetches partnership data from OmniBuilderZero tracking APIs
- Reads smart contract data from ScrollVerse-Contracts
- Displays Guardian NFTs from NFT-Core contracts
- Real-time updates via WebSocket or polling

---

### 5. ScrollVerse-Academy
**Status**: 🔄 Planned  
**URL**: https://github.com/chaishillomnitech1/ScrollVerse-Academy (to be created)  
**Purpose**: Global education matrix for ScrollVerse principles

#### Key Components
- **Learning Paths**: Structured courses on ScrollVerse technology
- **Certification System**: NFT-based course completion certificates
- **Interactive Tutorials**: Hands-on Web3 education
- **Community Forum**: Discussion and knowledge sharing
- **Resource Library**: Documentation and guides

#### Planned Courses
1. **Introduction to ScrollVerse**: Vision and principles
2. **Star Dust Frequencies**: Understanding resonance scoring
3. **Guardian NFTs**: NFT technology and use cases
4. **Partnership Automation**: Emissary bot configuration
5. **Blockchain Fundamentals**: Web3 basics

#### Planned Directory Structure
```
/courses
  /intro-to-scrollverse
  /star-dust-frequencies
  /guardian-nfts
  /partnership-automation
  /blockchain-fundamentals
/platform
  /frontend                  - Learning platform UI
  /backend                   - Course API and auth
  /certification             - NFT minting for completion
```

#### Dependencies
- **Depends on**: OmniBuilderZero (protocol docs), NFT-Core (certification NFTs), Contracts (certification logic)
- **Provides to**: Community (education and onboarding)

#### Integration Points
- Uses OmniBuilderZero documentation as course material
- Mints certification NFTs via NFT-Core contracts
- Records completion on-chain via Contracts

---

## 🔄 Integration Patterns

### Pattern 1: Partnership to NFT Flow
```
OmniBuilderZero (Partnership Status Change)
    ↓
    │ API Call / Event
    ↓
ScrollVerse-Contracts (Verify & Trigger Mint)
    ↓
    │ Contract Call
    ↓
ScrollVerse-NFT-Core (Mint Guardian NFT)
    ↓
    │ Event Emitted
    ↓
ScrollVerse-Dashboard (Display NFT to Partner)
```

### Pattern 2: Star Dust Resonance Calculation
```
OmniBuilderZero (New Partnership Opportunity)
    ↓
    │ Run Resonance Algorithm
    ↓
phase2/star_dust_frequencies/resonance_calculator.py
    ↓
    │ Score Calculated
    ↓
phase2/emissary_bots/outreach_automation.py
    ↓
    │ Automated Outreach Triggered
    ↓
ScrollVerse-Dashboard (Display in Funnel)
```

### Pattern 3: Multi-Chain Deployment
```
OmniBuilderZero (Blueprint Specifications)
    ↓
    │ Contract Parameters
    ↓
ScrollVerse-Contracts (Deploy Contracts)
    ↓
    ├─→ Ethereum Mainnet
    ├─→ Polygon L2
    └─→ Scroll zkEVM
    ↓
    │ Contract Addresses
    ↓
ScrollVerse-Dashboard (Connect to Contracts)
```

### Pattern 4: Educational Certification
```
ScrollVerse-Academy (Course Completion)
    ↓
    │ Verify Completion
    ↓
ScrollVerse-Contracts (Certification Logic)
    ↓
    │ Mint Certificate NFT
    ↓
ScrollVerse-NFT-Core (Certificate NFT Contract)
    ↓
    │ NFT Issued
    ↓
Student Wallet (Owns Certificate NFT)
```

---

## 🛠️ Development Workflow

### Setting Up Multi-Repo Development

1. **Clone All Repositories**
```bash
# Create workspace
mkdir scrollverse-workspace && cd scrollverse-workspace

# Clone repos (as they become available)
git clone https://github.com/chaishillomnitech1/OmniBuilderZero.git
git clone https://github.com/chaishillomnitech1/ScrollVerse-NFT-Core.git
git clone https://github.com/chaishillomnitech1/ScrollVerse-Contracts.git
git clone https://github.com/chaishillomnitech1/ScrollVerse-Dashboard.git
git clone https://github.com/chaishillomnitech1/ScrollVerse-Academy.git
```

2. **Install Dependencies**
```bash
# OmniBuilderZero (Python)
cd OmniBuilderZero/phase2
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt  # (to be created)

# NFT-Core & Contracts (Hardhat)
cd ../ScrollVerse-NFT-Core
npm install

cd ../ScrollVerse-Contracts
npm install

# Dashboard (React)
cd ../ScrollVerse-Dashboard
npm install

# Academy (Platform specific)
cd ../ScrollVerse-Academy
npm install
```

3. **Configure Environment Variables**
```bash
# Each repo should have .env.example
# Copy and configure for local development
cp .env.example .env
# Edit .env with your local settings
```

### Cross-Repository Testing

When making changes that affect multiple repos:

1. **Test Integration Locally**
   - Use local contract deployments (Hardhat network)
   - Mock APIs between repos
   - Verify data flow end-to-end

2. **Update Documentation**
   - Update REPOSITORY_MAP.md when adding integration points
   - Update README.md in affected repos
   - Add cross-repo references

3. **Coordinate Deployments**
   - Smart contracts deploy first (Contracts, NFT-Core)
   - Backend APIs update next (OmniBuilderZero)
   - Frontend last (Dashboard, Academy)

---

## 📋 Version Compatibility Matrix

| OmniBuilderZero | NFT-Core | Contracts | Dashboard | Academy |
|----------------|----------|-----------|-----------|---------|
| v2.0.0 (current) | v1.0.0 (planned) | v1.0.0 (planned) | v1.0.0 (planned) | v1.0.0 (planned) |

---

## 🚀 Deployment Strategy

### Phase 1: Foundation (Current)
- ✅ OmniBuilderZero: Active and documented
- ✅ Partnership automation operational
- ✅ Regional blueprints defined

### Phase 2: Smart Contracts (Next)
- 🔄 Deploy ScrollVerse-NFT-Core
- 🔄 Deploy ScrollVerse-Contracts
- 🔄 Test on testnets (Goerli, Mumbai, Scroll Sepolia)
- 🔄 Audit and security review

### Phase 3: Frontend (Following)
- 🔄 Launch ScrollVerse-Dashboard
- 🔄 Integrate Web3 wallet connections
- 🔄 Connect to deployed contracts

### Phase 4: Education (Final)
- 🔄 Launch ScrollVerse-Academy
- 🔄 Create initial course content
- 🔄 Implement certification system

---

## 🤝 Contributing Across Repositories

### Guidelines
1. **Read Documentation First**: Each repo has specific contribution guidelines
2. **Use Feature Branches**: `feature/description` naming convention
3. **Cross-Reference Issues**: Use `owner/repo#issue` syntax for cross-repo references
4. **Integration Testing**: Test changes across affected repos
5. **Documentation Updates**: Update REPOSITORY_MAP.md for architectural changes

### Example: Adding a New Partnership Region

**Changes Required Across Repos:**

1. **OmniBuilderZero**
   - Add new region enum
   - Create regional blueprint
   - Add localization files
   - Update documentation

2. **ScrollVerse-Contracts**
   - Update region validation in smart contracts
   - Deploy region-specific contracts if needed

3. **ScrollVerse-Dashboard**
   - Add region to UI filters
   - Update visualizations
   - Add regional flags/icons

4. **ScrollVerse-Academy**
   - Create region-specific course content
   - Translate materials

---

## 📞 Support & Communication

### Issue Tracking
- **OmniBuilderZero Issues**: Infrastructure, automation, documentation
- **NFT-Core Issues**: Smart contract bugs, NFT functionality
- **Contracts Issues**: Partnership contracts, oracle issues
- **Dashboard Issues**: UI bugs, Web3 connection problems
- **Academy Issues**: Course content, certification issues

### Cross-Repository Discussions
Use GitHub Discussions in OmniBuilderZero for:
- Architecture decisions affecting multiple repos
- Integration strategy planning
- Feature requests spanning multiple systems

---

## 📖 Additional Resources

- **Main Documentation**: [OmniBuilderZero README](./README.md)
- **NŪR Protocol**: [phase2/protocols/nur_global_integration.md](./phase2/protocols/nur_global_integration.md)
- **Partnership Blueprints**: [phase2/blueprints/](./phase2/blueprints/)
- **Emissary Bot System**: [phase2/emissary_bots/](./phase2/emissary_bots/)

---

*Last Updated: 2025-11-24*  
*Maintained by: ScrollVerse Infrastructure Team*  
*Version: 1.0.0*
