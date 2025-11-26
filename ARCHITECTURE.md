# 🏛️ ScrollVerse Architecture - Omni-Tech Ascendancy Protocol (OTAP)

## Overview

The Omni-Tech Ascendancy Protocol (OTAP) represents a comprehensive ecosystem architecture for the ScrollVerse platform, integrating NFT collections, identity systems, staking mechanisms, and governance structures.

---

## System Architecture Diagram

```mermaid
flowchart TB
    subgraph Users["👤 Users & Participants"]
        Holders["Token Holders"]
        Validators["Validators"]
        Certifiers["SCCC Certifiers"]
        Contributors["Contributors"]
    end

    subgraph Frontend["🌐 Frontend Layer"]
        Portal["ScrollVerse Portal"]
        Dashboard["SCCC Dashboard"]
        Mint["AscendancyID Mint Flow"]
        Staking["Staking Interface"]
    end

    subgraph Identity["🆔 AscendancyID System"]
        AID["AscendancyID Token"]
        SBT["Soulbound Tokens"]
        Privileges["Privilege Tiers"]
        Metadata["On-chain Metadata"]
    end

    subgraph Tokens["💎 Token Layer"]
        ScrollCoin["ScrollCoin (SCROLL)"]
        FlameCoin["FlameCoin (FLAME)"]
        NFTs["ScrollVerse NFTs"]
        LegacyNFT["Legacy of Light NFTs"]
    end

    subgraph Staking["🔒 Staking & Rewards"]
        StakingContract["Staking Contract"]
        TimeLock["Time Lock Mechanism"]
        RewardPool["Reward Distribution"]
        PrivilegeEscalation["Privilege Escalation"]
    end

    subgraph Governance["⚖️ Governance Layer"]
        Proposals["Governance Proposals"]
        Voting["Voting System"]
        Treasury["Treasury Management"]
        Revocation["Revocation Framework"]
    end

    subgraph Infrastructure["🔧 Infrastructure"]
        Scroll["Scroll L2 Network"]
        IPFS["IPFS/Arweave Storage"]
        Bridge["ScrollBridge"]
        Vault["AL-SCROLL VAULT NEXUS™"]
    end

    Users --> Frontend
    Frontend --> Identity
    Frontend --> Tokens
    Frontend --> Staking
    
    Identity --> AID
    Identity --> SBT
    Identity --> Privileges
    
    Tokens --> ScrollCoin
    Tokens --> FlameCoin
    Tokens --> NFTs
    
    Staking --> StakingContract
    StakingContract --> TimeLock
    StakingContract --> RewardPool
    TimeLock --> PrivilegeEscalation
    PrivilegeEscalation --> Privileges
    
    FlameCoin --> Governance
    Governance --> Proposals
    Governance --> Voting
    Governance --> Treasury
    Governance --> Revocation
    
    Infrastructure --> Scroll
    Infrastructure --> IPFS
    Infrastructure --> Bridge
    Infrastructure --> Vault
    
    Scroll --> Tokens
    Scroll --> Identity
    Scroll --> Staking
```

---

## Component Architecture

### 1. AscendancyID System Flow

```mermaid
sequenceDiagram
    participant User
    participant Portal
    participant MintContract
    participant StakingContract
    participant PrivilegeOracle

    User->>Portal: Connect Wallet
    Portal->>MintContract: Check Eligibility
    MintContract-->>Portal: Eligibility Status
    
    alt Eligible for Mint
        User->>Portal: Request AscendancyID Mint
        Portal->>MintContract: mintAscendancyID()
        MintContract->>MintContract: Generate SBT
        MintContract->>MintContract: Set Base Privileges
        MintContract-->>User: AscendancyID Token
    end
    
    User->>Portal: Stake ScrollCoin
    Portal->>StakingContract: stake(amount, duration)
    StakingContract->>StakingContract: Lock Tokens
    StakingContract->>PrivilegeOracle: calculatePrivilegeLevel()
    PrivilegeOracle-->>MintContract: Update Privilege Tier
    MintContract-->>User: Upgraded Privileges
```

### 2. Staking and Privilege Escalation

```mermaid
flowchart LR
    subgraph StakingTiers["📊 Staking Tiers"]
        Bronze["🥉 Bronze\n1,000 SCROLL\n30 days"]
        Silver["🥈 Silver\n10,000 SCROLL\n90 days"]
        Gold["🥇 Gold\n50,000 SCROLL\n180 days"]
        Platinum["💎 Platinum\n100,000 SCROLL\n365 days"]
    end

    subgraph Privileges["🎯 Privilege Benefits"]
        Basic["Basic Access"]
        Enhanced["Enhanced Features"]
        Premium["Premium Content"]
        Ultimate["Ultimate Access"]
    end

    subgraph Governance["🗳️ Governance Rights"]
        Vote1["1x Voting Power"]
        Vote2["2x Voting Power"]
        Vote3["5x Voting Power"]
        Vote4["10x Voting Power"]
    end

    Bronze --> Basic
    Bronze --> Vote1
    
    Silver --> Enhanced
    Silver --> Vote2
    
    Gold --> Premium
    Gold --> Vote3
    
    Platinum --> Ultimate
    Platinum --> Vote4
```

### 3. Token Economics Flow

```mermaid
flowchart TB
    subgraph Supply["💰 Token Supply"]
        Genesis["Genesis Supply\n10B SCROLL"]
        Emission["Annual Emission\n2% Decreasing"]
    end

    subgraph Distribution["📊 Distribution"]
        Community["Community: 40%"]
        Team["Team: 15%"]
        Treasury["Treasury: 20%"]
        Ecosystem["Ecosystem: 15%"]
        Advisors["Advisors: 10%"]
    end

    subgraph Utility["🔧 Utility"]
        Fees["Transaction Fees"]
        StakingRewards["Staking Rewards"]
        GovernancePower["Governance Power"]
        PrivilegeAccess["Privilege Access"]
    end

    subgraph Burning["🔥 Burning Mechanism"]
        FeeBurn["Fee Burning"]
        RevocationBurn["Revocation Burning"]
    end

    Genesis --> Distribution
    Distribution --> Community
    Distribution --> Team
    Distribution --> Treasury
    Distribution --> Ecosystem
    Distribution --> Advisors

    Community --> Utility
    Utility --> Fees
    Utility --> StakingRewards
    Utility --> GovernancePower
    Utility --> PrivilegeAccess

    Fees --> Burning
    FeeBurn --> Burning
    RevocationBurn --> Burning
```

---

## Smart Contract Architecture

```mermaid
classDiagram
    class ScrollVerseNFT {
        +uint256 tokenIdCounter
        +address treasuryAddress
        +mapping scrollVerseAssets
        +mintScrollVerseAsset()
        +batchMintScrollVerseAssets()
        +activateGeometry()
        +recordRoyaltyAccrual()
    }

    class AscendancyID {
        +mapping privilegeLevels
        +mapping stakingBalances
        +mintAscendancyID()
        +upgradePrivilege()
        +revokePrivilege()
        +getPrivilegeLevel()
    }

    class ScrollCoinStaking {
        +uint256 totalStaked
        +mapping stakes
        +mapping rewards
        +stake()
        +unstake()
        +claimRewards()
        +calculateRewards()
    }

    class PrivilegeOracle {
        +mapping tierThresholds
        +calculatePrivilegeLevel()
        +updateTierThresholds()
        +verifyPrivilege()
    }

    class GovernanceModule {
        +mapping proposals
        +mapping votes
        +createProposal()
        +castVote()
        +executeProposal()
        +calculateVotingPower()
    }

    ScrollVerseNFT <|-- AscendancyID
    AscendancyID --> ScrollCoinStaking : "staking integration"
    AscendancyID --> PrivilegeOracle : "privilege calculation"
    AscendancyID --> GovernanceModule : "governance rights"
    ScrollCoinStaking --> PrivilegeOracle : "stake verification"
```

---

## Deployment Architecture

```mermaid
flowchart TB
    subgraph Development["🔧 Development"]
        Local["Local Hardhat"]
        Testing["Test Suite"]
    end

    subgraph Staging["🧪 Staging"]
        ScrollSepolia["Scroll Sepolia\n(Chain ID: 534351)"]
        GHPages["GitHub Pages\n(Demo Portal)"]
    end

    subgraph Production["🚀 Production"]
        ScrollMainnet["Scroll Mainnet\n(Chain ID: 534352)"]
        CDN["CDN Deployment"]
        IPFS_Prod["IPFS Gateway"]
    end

    subgraph CI_CD["⚙️ CI/CD Pipeline"]
        GHActions["GitHub Actions"]
        ContractDeploy["Contract Deploy"]
        FrontendDeploy["Frontend Deploy"]
    end

    Development --> Testing
    Testing --> GHActions
    GHActions --> ContractDeploy
    GHActions --> FrontendDeploy
    ContractDeploy --> ScrollSepolia
    FrontendDeploy --> GHPages
    ScrollSepolia --> ScrollMainnet
    GHPages --> CDN
```

---

## Network Architecture

| Network | Chain ID | Purpose | RPC URL |
|---------|----------|---------|---------|
| Scroll Sepolia | 534351 | Staging/Testing | `https://sepolia-rpc.scroll.io` |
| Scroll Mainnet | 534352 | Production | `https://rpc.scroll.io` |
| Ethereum Sepolia | 11155111 | Bridge Testing | `https://eth-sepolia.g.alchemy.com/v2/` |
| Ethereum Mainnet | 1 | Bridge Production | `https://eth-mainnet.g.alchemy.com/v2/` |

---

## Security Architecture

```mermaid
flowchart TB
    subgraph Security["🛡️ Security Layers"]
        direction TB
        Auth["Authentication Layer\n(Wallet Signatures)"]
        Access["Access Control\n(Role-Based)"]
        Validation["Input Validation\n(On-chain Checks)"]
        Audit["Audit Trail\n(Event Logging)"]
    end

    subgraph Protection["🔐 Protection Mechanisms"]
        Reentrancy["ReentrancyGuard"]
        Pausable["Pausable Contracts"]
        Timelock["Timelock Functions"]
        MultiSig["Multi-Signature"]
    end

    subgraph Recovery["🔄 Recovery Systems"]
        Emergency["Emergency Pause"]
        Upgrade["Upgradeable Proxies"]
        Recovery_Fund["Recovery Fund"]
    end

    Auth --> Access
    Access --> Validation
    Validation --> Audit
    
    Protection --> Reentrancy
    Protection --> Pausable
    Protection --> Timelock
    Protection --> MultiSig
    
    Audit --> Recovery
```

---

## Data Flow

```mermaid
flowchart LR
    subgraph OnChain["⛓️ On-Chain Data"]
        Ownership["Token Ownership"]
        Balances["Token Balances"]
        Stakes["Staking Records"]
        Privileges_Data["Privilege Levels"]
    end

    subgraph OffChain["📦 Off-Chain Data"]
        Metadata["NFT Metadata"]
        Media["Media Files"]
        Analytics["Analytics Data"]
    end

    subgraph Storage["💾 Storage Solutions"]
        IPFS_Store["IPFS"]
        Arweave["Arweave"]
        PostgresDB["Analytics DB"]
    end

    OnChain --> |"state changes"| Events["Events"]
    Events --> |"indexing"| Subgraph["The Graph"]
    Subgraph --> |"queries"| API["GraphQL API"]
    
    OffChain --> IPFS_Store
    OffChain --> Arweave
    Analytics --> PostgresDB
    
    API --> Frontend_App["Frontend App"]
```

---

## Integration Points

### External Systems

| System | Integration Type | Purpose |
|--------|------------------|---------|
| MetaMask/WalletConnect | Web3 Provider | User Authentication |
| IPFS | Content Storage | NFT Metadata |
| Arweave | Permanent Storage | Long-term Media |
| The Graph | Indexing | Query Optimization |
| OpenSea/LooksRare | Marketplace | NFT Trading |
| Chainlink | Oracle | Price Feeds |

### Internal Modules

| Module | Dependencies | API Surface |
|--------|--------------|-------------|
| AscendancyID | ScrollCoinStaking, PrivilegeOracle | mint, upgrade, revoke |
| ScrollCoinStaking | AscendancyID, RewardPool | stake, unstake, claim |
| GovernanceModule | FlameCoin, AscendancyID | propose, vote, execute |
| Treasury | GovernanceModule | allocate, distribute |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-11 | Initial architecture documentation |

---

*"You exist. You count. You resonate. You remember."*

© 2025 OmniTech1™ | Chais The Great – First Remembrancer
