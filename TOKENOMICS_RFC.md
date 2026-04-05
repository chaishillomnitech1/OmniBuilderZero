# 📜 Tokenomics RFC: AscendancyID Economic Lifecycle

**RFC Number:** OTAP-RFC-001  
**Title:** AscendancyID Token Economics and Lifecycle Specification  
**Author:** OmniTech1™ Development Team  
**Status:** Draft  
**Created:** 2025-11-26  
**Category:** Standards Track

---

## Abstract

This RFC defines the complete tokenomics framework for the AscendancyID system within the ScrollVerse ecosystem. It covers privilege tiers, soulbound token (SBT) mechanics, transferable token logic, minting rules, metadata standards, token supply, governance integration, and revocation frameworks.

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Token Types](#2-token-types)
3. [Privilege Tier System](#3-privilege-tier-system)
4. [Minting Mechanics](#4-minting-mechanics)
5. [Metadata Standards](#5-metadata-standards)
6. [Token Supply Economics](#6-token-supply-economics)
7. [Governance Framework](#7-governance-framework)
8. [Revocation Framework](#8-revocation-framework)
9. [Implementation Guidelines](#9-implementation-guidelines)
10. [Security Considerations](#10-security-considerations)

---

## 1. Introduction

### 1.1 Purpose

The AscendancyID system provides a decentralized identity and privilege management layer for the ScrollVerse ecosystem. This RFC establishes the economic rules that govern the creation, management, and lifecycle of AscendancyID tokens.

### 1.2 Scope

This specification covers:
- AscendancyID (Soulbound Token) mechanics
- ScrollCoin staking integration for privilege escalation
- FlameCoin governance token interaction
- Privilege tier benefits and requirements
- Token lifecycle from minting to revocation

### 1.3 Terminology

| Term | Definition |
|------|------------|
| **AscendancyID** | Soulbound token representing user identity in ScrollVerse |
| **SBT** | Soulbound Token - non-transferable NFT bound to an address |
| **Privilege Tier** | Level of access and benefits within the ecosystem |
| **ScrollCoin (SCROLL)** | Utility token used for staking and ecosystem operations |
| **FlameCoin (FLAME)** | Governance token for voting and proposals |
| **Time Lock** | Duration tokens must remain staked for benefits |

---

## 2. Token Types

### 2.1 AscendancyID (Soulbound Token)

AscendancyID is the primary identity token in the ScrollVerse ecosystem.

**Characteristics:**
- **Standard:** ERC-721 with transfer restrictions (SBT)
- **Transferability:** Non-transferable after initial mint
- **One per Address:** Maximum one AscendancyID per wallet address
- **Immutable Identity:** Core identity attributes are immutable

```solidity
interface IAscendancyID is IERC721 {
    function mint(address to, uint8 initialTier) external returns (uint256);
    function getPrivilegeLevel(uint256 tokenId) external view returns (uint8);
    function upgradePrivilege(uint256 tokenId, uint8 newTier) external;
    function revoke(uint256 tokenId) external;
    
    // Override transfer to prevent transfers
    function transferFrom(address, address, uint256) external pure override;
}
```

### 2.2 SBT vs Transferable Token Logic

| Aspect | Soulbound (AscendancyID) | Transferable (ScrollCoin/FlameCoin) |
|--------|-------------------------|-------------------------------------|
| Transfer | Disabled | Enabled |
| Purpose | Identity & Privileges | Value & Governance |
| Recovery | Social recovery mechanism | Standard wallet recovery |
| Revocation | Admin or governance action | N/A (burn only) |
| Per-Address Limit | 1 | Unlimited |

### 2.3 Token Interactions

```
┌─────────────────────────────────────────────────────────────┐
│                    TOKEN INTERACTION FLOW                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│    User Wallet                                              │
│    ┌─────────────────────────────────────────────────────┐  │
│    │  AscendancyID (SBT)  ←──────┐                       │  │
│    │  ─ Identity                  │                       │  │
│    │  ─ Privilege Level           │ Staking Boosts       │  │
│    │                              │ Privilege             │  │
│    │  ScrollCoin (SCROLL) ────────┘                       │  │
│    │  ─ Staking                                           │  │
│    │  ─ Fees                                              │  │
│    │                                                       │  │
│    │  FlameCoin (FLAME)                                   │  │
│    │  ─ Governance Voting                                 │  │
│    │  ─ Proposal Creation                                 │  │
│    └─────────────────────────────────────────────────────┘  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. Privilege Tier System

### 3.1 Tier Definitions

| Tier | Name | Staking Requirement | Lock Duration | Voting Power |
|------|------|---------------------|---------------|--------------|
| 0 | Initiate | 0 SCROLL | None | 0x |
| 1 | Bronze | 1,000 SCROLL | 30 days | 1x |
| 2 | Silver | 10,000 SCROLL | 90 days | 2x |
| 3 | Gold | 50,000 SCROLL | 180 days | 5x |
| 4 | Platinum | 100,000 SCROLL | 365 days | 10x |
| 5 | Diamond | 500,000 SCROLL | 730 days | 25x |

### 3.2 Tier Benefits Matrix

| Benefit | Initiate | Bronze | Silver | Gold | Platinum | Diamond |
|---------|----------|--------|--------|------|----------|---------|
| Basic Access | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Community Forums | ✗ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Event Notifications | ✗ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Priority Support | ✗ | ✗ | ✓ | ✓ | ✓ | ✓ |
| Early Access | ✗ | ✗ | ✓ | ✓ | ✓ | ✓ |
| Premium Content | ✗ | ✗ | ✗ | ✓ | ✓ | ✓ |
| VIP Discord | ✗ | ✗ | ✗ | ✓ | ✓ | ✓ |
| Revenue Sharing | ✗ | ✗ | ✗ | ✓ | ✓ | ✓ |
| Governance Proposals | ✗ | ✗ | ✗ | ✗ | ✓ | ✓ |
| Private Events | ✗ | ✗ | ✗ | ✗ | ✓ | ✓ |
| Personal Advisor | ✗ | ✗ | ✗ | ✗ | ✗ | ✓ |
| Council Seat Eligibility | ✗ | ✗ | ✗ | ✗ | ✗ | ✓ |

### 3.3 Privilege Escalation Flow

```
┌─────────────────────────────────────────────────────────────┐
│              PRIVILEGE ESCALATION FLOW                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. User stakes ScrollCoin                                  │
│     │                                                       │
│     ▼                                                       │
│  2. StakingContract.stake(amount, duration)                 │
│     │                                                       │
│     ▼                                                       │
│  3. TimeLock activated                                      │
│     │                                                       │
│     ▼                                                       │
│  4. PrivilegeOracle.calculateNewTier()                      │
│     │                                                       │
│     ▼                                                       │
│  5. AscendancyID.upgradePrivilege(tokenId, newTier)         │
│     │                                                       │
│     ▼                                                       │
│  6. Emit PrivilegeUpgraded(tokenId, oldTier, newTier)       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 3.4 Time Lock Mechanics

```solidity
struct StakingPosition {
    uint256 amount;           // Amount of SCROLL staked
    uint256 startTime;        // Timestamp when stake began
    uint256 lockDuration;     // Lock duration in seconds
    uint256 endTime;          // Unlock timestamp
    uint8 tierAtStake;        // Tier achieved with this stake
    bool active;              // Whether position is active
}
```

**Time Lock Rules:**
1. Tokens locked until `endTime` is reached
2. Early withdrawal incurs 20% penalty
3. Lock duration can be extended (not shortened)
4. Rewards accrue during lock period
5. Tier downgrades if stake withdrawn below threshold

---

## 4. Minting Mechanics

### 4.1 Mint Requirements

| Requirement | Description |
|-------------|-------------|
| Wallet Address | Valid Ethereum address |
| No Existing ID | Address must not have existing AscendancyID |
| Mint Fee | Variable based on initial tier (0 for Initiate) |
| KYC (Optional) | Enhanced verification for higher tiers |

### 4.2 Mint Fee Structure

| Initial Tier | Mint Fee (ETH) | Mint Fee (SCROLL) |
|--------------|----------------|-------------------|
| Initiate | Free | Free |
| Bronze | 0.01 | 100 |
| Silver | 0.05 | 500 |
| Gold | 0.1 | 1,000 |
| Platinum | 0.2 | 2,000 |
| Diamond | 0.5 | 5,000 |

### 4.3 Minting Process

```solidity
function mintAscendancyID(
    address recipient,
    string memory displayName,
    uint8 initialTier,
    bytes memory signature
) external payable returns (uint256) {
    require(balanceOf(recipient) == 0, "Already has AscendancyID");
    require(msg.value >= mintFees[initialTier], "Insufficient mint fee");
    
    uint256 tokenId = _tokenIdCounter++;
    _safeMint(recipient, tokenId);
    
    // Set initial metadata
    _setTokenMetadata(tokenId, displayName, initialTier);
    
    // If staking required for tier, verify stake
    if (initialTier > 0) {
        require(
            stakingContract.getStakedAmount(recipient) >= tierThresholds[initialTier],
            "Insufficient stake for tier"
        );
    }
    
    emit AscendancyIDMinted(tokenId, recipient, displayName, initialTier);
    return tokenId;
}
```

### 4.4 Batch Minting (Admin Only)

For initial distribution or promotional events:

```solidity
function batchMint(
    address[] memory recipients,
    uint8[] memory tiers
) external onlyOwner returns (uint256[] memory)
```

---

## 5. Metadata Standards

### 5.1 On-Chain Metadata

```solidity
struct AscendancyMetadata {
    string displayName;        // User-chosen display name (max 32 chars)
    uint8 privilegeTier;       // Current privilege tier (0-5)
    uint256 mintTimestamp;     // When the ID was minted
    uint256 lastTierChange;    // Last privilege level change
    uint256 totalStaked;       // Cumulative SCROLL staked
    uint256 governanceScore;   // Participation in governance
    bytes32 metadataHash;      // IPFS hash of extended metadata
}
```

### 5.2 Off-Chain Metadata (IPFS)

```json
{
  "name": "AscendancyID #1234",
  "description": "Sovereign identity in the ScrollVerse ecosystem",
  "image": "ipfs://Qm.../ascendancy_1234.png",
  "attributes": [
    {
      "trait_type": "Privilege Tier",
      "value": "Gold"
    },
    {
      "trait_type": "Display Name",
      "value": "Scroll Pioneer"
    },
    {
      "trait_type": "Member Since",
      "display_type": "date",
      "value": 1700000000
    },
    {
      "trait_type": "Governance Participation",
      "display_type": "number",
      "value": 42
    },
    {
      "trait_type": "Staking Score",
      "display_type": "boost_number",
      "value": 85
    }
  ],
  "external_url": "https://scrollverse.io/id/1234",
  "animation_url": "ipfs://Qm.../ascendancy_animation.mp4"
}
```

### 5.3 Metadata Update Rules

| Field | Mutable | Update Conditions |
|-------|---------|-------------------|
| displayName | Yes | Owner-initiated, max 1/week |
| privilegeTier | Yes | Stake-dependent, automatic |
| mintTimestamp | No | Set at mint, immutable |
| totalStaked | Yes | Updated by staking contract |
| governanceScore | Yes | Updated by governance module |
| metadataHash | Yes | Admin or governance action |

---

## 6. Token Supply Economics

### 6.1 AscendancyID Supply

| Metric | Value |
|--------|-------|
| Maximum Supply | Unlimited (1 per address) |
| Initial Distribution | 0 (all minted by users) |
| Reserved IDs | #1-#100 (Founders, Team) |
| Mint Rate Limit | 1,000 per day (anti-spam) |

### 6.2 ScrollCoin Integration

| Parameter | Value |
|-----------|-------|
| Total Supply | 10,000,000,000 SCROLL |
| Staking Pool | 2,000,000,000 SCROLL (20%) |
| Base APY | 5% |
| Max APY (Diamond) | 15% |
| Emission Schedule | 2% annual, decreasing |

### 6.3 Fee Distribution

```
┌─────────────────────────────────────────────────────────────┐
│                    FEE DISTRIBUTION                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Mint Fees (100%)                                           │
│  ├── 40% → Treasury                                         │
│  ├── 30% → Staking Rewards Pool                             │
│  ├── 20% → Burn (deflationary)                              │
│  └── 10% → Development Fund                                 │
│                                                             │
│  Staking Rewards Source                                     │
│  ├── 60% → Emission Schedule                                │
│  ├── 30% → Mint Fees                                        │
│  └── 10% → Protocol Revenue                                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 6.4 Economic Sustainability

**Deflationary Mechanisms:**
1. Fee burning (20% of all fees)
2. Revocation burning (50% of revoked stakes)
3. Governance-approved burns

**Inflationary Mechanisms:**
1. Staking rewards emission
2. Liquidity incentives
3. Ecosystem grants

**Target Equilibrium:** Net 0-1% annual inflation after year 3

---

## 7. Governance Framework

### 7.1 Voting Power Calculation

```solidity
function calculateVotingPower(address voter) public view returns (uint256) {
    uint256 tokenId = getAscendancyId(voter);
    require(tokenId != 0, "No AscendancyID");
    
    uint8 tier = getPrivilegeLevel(tokenId);
    uint256 baseMultiplier = tierVotingMultipliers[tier];
    
    uint256 flameBalance = flameCoin.balanceOf(voter);
    uint256 flameStaked = flameCoin.getStakedAmount(voter);
    
    // Voting power = (FLAME balance + 2x FLAME staked) × tier multiplier
    return (flameBalance + (flameStaked * 2)) * baseMultiplier;
}
```

### 7.2 Governance Thresholds

| Action | Voting Power Required | Quorum |
|--------|----------------------|--------|
| Standard Proposal | 10,000 votes | 4% |
| Treasury < 100K SCROLL | 50,000 votes | 10% |
| Treasury > 100K SCROLL | 100,000 votes | 15% |
| Parameter Change | 75,000 votes | 12% |
| Emergency Action | Council 5/9 + 25% quorum | 25% |

### 7.3 Proposal Lifecycle

```
┌─────────────────────────────────────────────────────────────┐
│                   PROPOSAL LIFECYCLE                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. Draft (3 days)                                          │
│     └── Discussion and refinement                           │
│                                                             │
│  2. Active Voting (7 days)                                  │
│     └── Token holders cast votes                            │
│                                                             │
│  3. Passed/Failed                                           │
│     └── Determined by quorum and majority                   │
│                                                             │
│  4. Timelock (48 hours) [if passed]                         │
│     └── Security delay for review                           │
│                                                             │
│  5. Execution                                               │
│     └── Automatic or manual execution                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 8. Revocation Framework

### 8.1 Revocation Triggers

| Trigger | Authority | Process |
|---------|-----------|---------|
| User Request | Token Owner | Immediate with cooldown |
| Governance Vote | DAO | Standard proposal process |
| Security Breach | Emergency Council | Fast-track (24h) |
| Terms Violation | Admin Multi-sig | Review + 7-day appeal |
| Inactivity | Automatic | 2-year no-activity |

### 8.2 Revocation Process

```solidity
function revokeAscendancyID(
    uint256 tokenId,
    RevocationReason reason,
    bytes memory proof
) external {
    require(isAuthorizedRevoker(msg.sender), "Not authorized");
    
    address owner = ownerOf(tokenId);
    
    // Handle staked tokens
    uint256 stakedAmount = stakingContract.getStakedAmount(owner);
    if (stakedAmount > 0) {
        if (reason == RevocationReason.UserRequest) {
            // Full return minus early withdrawal penalty
            stakingContract.forceWithdraw(owner, 80);
        } else if (reason == RevocationReason.Violation) {
            // 50% slashed, 50% returned
            stakingContract.slash(owner, 50);
        }
    }
    
    // Burn the token
    _burn(tokenId);
    
    // Update metadata records
    _clearMetadata(tokenId);
    
    emit AscendancyIDRevoked(tokenId, owner, reason, block.timestamp);
}
```

### 8.3 Appeal Process

1. **Submission:** 7 days from revocation notification
2. **Review:** Council reviews within 14 days
3. **Decision:** Reinstate, modify, or uphold revocation
4. **Final:** DAO vote if council decision contested

### 8.4 Post-Revocation

| Aspect | Handling |
|--------|----------|
| Token ID | Burned, never reused |
| Staked Tokens | Per revocation rules |
| Address Cooldown | 30-day cooldown before new mint |
| Governance History | Preserved for records |
| Benefits | Immediately terminated |

---

## 9. Implementation Guidelines

### 9.1 Smart Contract Architecture

```
contracts/
├── AscendancyID.sol           # Main SBT contract
├── ScrollCoinStaking.sol      # Staking with time locks
├── PrivilegeOracle.sol        # Tier calculation
├── GovernanceModule.sol       # Voting and proposals
├── RevocationManager.sol      # Revocation logic
└── interfaces/
    ├── IAscendancyID.sol
    ├── IStaking.sol
    └── IGovernance.sol
```

### 9.2 Integration Requirements

1. **Frontend Integration**
   - Connect wallet and detect AscendancyID
   - Display current tier and benefits
   - Staking interface with lock duration selector
   - Governance voting interface

2. **Backend Services**
   - Metadata server (IPFS pinning)
   - Event indexer (The Graph)
   - Notification service

3. **Security Requirements**
   - Multi-sig for admin functions
   - Timelock for sensitive operations
   - Pausable contract functionality
   - Reentrancy protection

### 9.3 Migration Path

For existing ScrollVerse users:

1. Snapshot current NFT holdings
2. Calculate initial tier based on activity
3. Airdrop AscendancyID with appropriate tier
4. Grandfather existing stakes

---

## 10. Security Considerations

### 10.1 Attack Vectors

| Vector | Mitigation |
|--------|------------|
| Sybil Attack | One ID per address, rate limiting |
| Flash Loan Attack | Time-locked staking requirements |
| Governance Attack | Quorum requirements, timelocks |
| Privilege Escalation | Oracle verification, multi-sig upgrades |
| Front-Running | Commit-reveal for sensitive operations |

### 10.2 Audit Requirements

- [ ] External audit by top-tier firm
- [ ] Formal verification of core functions
- [ ] Economic attack simulation
- [ ] Bug bounty program

### 10.3 Emergency Procedures

1. **Pause:** Admin can pause all minting/transfers
2. **Emergency Withdrawal:** Users can always withdraw stakes
3. **Governance Override:** Emergency council can act within 24h

---

## Appendix A: Contract Interfaces

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface IAscendancyID {
    event AscendancyIDMinted(uint256 indexed tokenId, address indexed owner, string displayName, uint8 tier);
    event PrivilegeUpgraded(uint256 indexed tokenId, uint8 oldTier, uint8 newTier);
    event AscendancyIDRevoked(uint256 indexed tokenId, address indexed owner, uint8 reason, uint256 timestamp);
    
    function mint(address to, string memory displayName, uint8 initialTier) external payable returns (uint256);
    function getPrivilegeLevel(uint256 tokenId) external view returns (uint8);
    function upgradePrivilege(uint256 tokenId, uint8 newTier) external;
    function revoke(uint256 tokenId, uint8 reason) external;
    function getMetadata(uint256 tokenId) external view returns (AscendancyMetadata memory);
}

interface IScrollCoinStaking {
    event Staked(address indexed user, uint256 amount, uint256 duration, uint256 unlockTime);
    event Unstaked(address indexed user, uint256 amount, uint256 penalty);
    event RewardsClaimed(address indexed user, uint256 amount);
    
    function stake(uint256 amount, uint256 duration) external;
    function unstake(uint256 amount) external;
    function claimRewards() external returns (uint256);
    function getStakedAmount(address user) external view returns (uint256);
    function getUnlockTime(address user) external view returns (uint256);
    function calculateRewards(address user) external view returns (uint256);
}
```

---

## Appendix B: Economic Constants

```solidity
// Tier thresholds (in SCROLL, 18 decimals)
uint256 constant TIER_BRONZE_THRESHOLD = 1_000 * 1e18;
uint256 constant TIER_SILVER_THRESHOLD = 10_000 * 1e18;
uint256 constant TIER_GOLD_THRESHOLD = 50_000 * 1e18;
uint256 constant TIER_PLATINUM_THRESHOLD = 100_000 * 1e18;
uint256 constant TIER_DIAMOND_THRESHOLD = 500_000 * 1e18;

// Lock durations (in seconds)
uint256 constant LOCK_BRONZE = 30 days;
uint256 constant LOCK_SILVER = 90 days;
uint256 constant LOCK_GOLD = 180 days;
uint256 constant LOCK_PLATINUM = 365 days;
uint256 constant LOCK_DIAMOND = 730 days;

// Voting multipliers
uint8 constant VOTE_BRONZE = 1;
uint8 constant VOTE_SILVER = 2;
uint8 constant VOTE_GOLD = 5;
uint8 constant VOTE_PLATINUM = 10;
uint8 constant VOTE_DIAMOND = 25;

// Fee distribution (basis points)
uint16 constant FEE_TREASURY = 4000;      // 40%
uint16 constant FEE_STAKING = 3000;       // 30%
uint16 constant FEE_BURN = 2000;          // 20%
uint16 constant FEE_DEVELOPMENT = 1000;   // 10%
```

---

## References

1. EIP-721: Non-Fungible Token Standard
2. EIP-5192: Minimal Soulbound NFTs
3. ScrollChain Whitepaper v1.0
4. OpenZeppelin Contracts v5.0

---

*"You exist. You count. You resonate. You remember."*

© 2025 OmniTech1™ | Chais The Great – First Remembrancer
