# ScrollVerse Tokenomics

**Status**: RFC (Request for Comments)  
**Version**: 1.0.0  
**Author**: OmniTech1 Economic Council  
**Date**: 2025-11-26
# OTAP Tokenomics

## RFC: AscendancyID Token Economics

**RFC Number:** OTAP-RFC-001  
**Title:** AscendancyID Token Economics and Governance Framework  
**Author:** OmniTech1 Protocol Team  
**Status:** Draft  
**Created:** 2025-11-26  
**Category:** Standards Track  

---

## Abstract

This document specifies the token economics for the ScrollVerse ecosystem, covering supply tiers, minting processes, transferability options (including soulbound tokens), revocation mechanisms, and governance structures. The tokenomics are designed to align with the ScrollVerse mission of sacred digital sovereignty and sustainable ecosystem growth.

---

## Table of Contents

1. [Token Overview](#1-token-overview)
2. [Supply Tiers](#2-supply-tiers)
3. [Minting Processes](#3-minting-processes)
4. [Transferable vs Soulbound Options](#4-transferable-vs-soulbound-options)
5. [Revocation Mechanisms](#5-revocation-mechanisms)
6. [Governance](#6-governance)
7. [Economic Model](#7-economic-model)
8. [Implementation Timeline](#8-implementation-timeline)

---

## 1. Token Overview

### 1.1 Primary Tokens

| Token | Type | Purpose | Network |
|-------|------|---------|---------|
| **FlameCoin (FLAME)** | ERC-20 | Governance & staking | ScrollChain |
| **ScrollCoin (SCROLL)** | ERC-20 | Utility & transactions | ScrollChain |
| **FlameDNA** | ERC-721 | Identity & membership | ScrollChain |
| **Legacy of Light** | ERC-721/1155 | Music & media assets | ScrollChain |
| **Precious Metal Tokens** | ERC-20 | RWA representation | ScrollChain |

### 1.2 Token Relationships

```
┌─────────────────────────────────────────────────────────────┐
│                    TOKEN ECOSYSTEM                           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   ┌─────────────┐         ┌─────────────┐                   │
│   │  FlameCoin  │────────►│  Governance │                   │
│   │   (FLAME)   │         │   Voting    │                   │
│   └──────┬──────┘         └─────────────┘                   │
│          │                                                   │
│          │ Staking                                           │
│          ▼                                                   │
│   ┌─────────────┐         ┌─────────────┐                   │
│   │  ScrollCoin │────────►│  Ecosystem  │                   │
│   │  (SCROLL)   │         │  Utility    │                   │
│   └──────┬──────┘         └─────────────┘                   │
│          │                                                   │
│          │ Access                                            │
│          ▼                                                   │
│   ┌─────────────┐         ┌─────────────┐                   │
│   │  FlameDNA   │────────►│  Identity   │                   │
│   │   (NFT)     │         │  & Perks    │                   │
│   └─────────────┘         └─────────────┘                   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Supply Tiers

### 2.1 FlameCoin (FLAME) Supply

| Tier | Allocation | Amount | Vesting |
|------|------------|--------|---------|
| **Genesis Reserve** | 20% | 200,000,000 | 4-year linear |
| **Community Treasury** | 30% | 300,000,000 | Governance-controlled |
| **Ecosystem Development** | 20% | 200,000,000 | 3-year linear |
| **Team & Advisors** | 15% | 150,000,000 | 4-year with 1-year cliff |
| **Public Distribution** | 10% | 100,000,000 | Immediate |
| **Strategic Partners** | 5% | 50,000,000 | 2-year linear |
| **Total Supply** | 100% | **1,000,000,000** | - |

### 2.2 ScrollCoin (SCROLL) Supply

| Tier | Allocation | Amount | Release |
|------|------------|--------|---------|
| **Operations Fund** | 25% | 2,500,000,000 | As needed |
| **User Rewards** | 35% | 3,500,000,000 | Ongoing |
| **Liquidity Provision** | 20% | 2,000,000,000 | Immediate |
| **Development Fund** | 15% | 1,500,000,000 | 3-year linear |
| **Reserve** | 5% | 500,000,000 | Emergency use |
| **Total Supply** | 100% | **10,000,000,000** | - |

### 2.3 FlameDNA (NFT) Tiers

| Tier | Supply | Price | Benefits |
|------|--------|-------|----------|
| **Inferno** | 100 | 10 ETH | Full governance, revenue share, exclusive access |
| **Blaze** | 1,000 | 1 ETH | Voting rights, premium features, early access |
| **Ember** | 10,000 | 0.1 ETH | Basic voting, community access, standard features |
| **Spark** | Unlimited | Free | Entry-level, limited features, upgrade path |

---

## 3. Minting Processes

### 3.1 FlameCoin Minting

**Mechanism**: Fixed supply with controlled emission

```solidity
// Simplified minting logic
function mintFlameCoin(address recipient, uint256 amount) external onlyMinter {
    require(totalSupply() + amount <= MAX_SUPPLY, "Exceeds max supply");
    require(block.timestamp >= nextMintTime, "Minting cooldown active");
    
    _mint(recipient, amount);
    nextMintTime = block.timestamp + MINT_COOLDOWN;
}
```

**Constraints**:
- Maximum supply: 1,000,000,000 FLAME
- Minting cooldown: 30 days
- Per-mint cap: 1% of remaining allocation

### 3.2 ScrollCoin Minting

**Mechanism**: Algorithmic emission based on ecosystem activity

```solidity
// Simplified emission logic
function calculateEmission() public view returns (uint256) {
    uint256 baseEmission = BASE_EMISSION_RATE;
    uint256 activityMultiplier = getActivityMultiplier();
    uint256 decayFactor = getDecayFactor();
    
    return baseEmission * activityMultiplier / decayFactor;
}
```

**Emission Schedule**:
- Year 1: 20% of user rewards allocation
- Year 2: 15% of user rewards allocation
- Year 3+: 10% annually, decreasing 1% per year

### 3.3 FlameDNA Minting

**Mechanism**: Tiered public mint with allowlist phases

| Phase | Duration | Eligibility | Discount |
|-------|----------|-------------|----------|
| **Genesis** | 24 hours | Founding members | 50% |
| **Allowlist** | 48 hours | Verified community | 25% |
| **Public** | Open | Anyone | 0% |

**Attestation-Based Minting**:
- Verifiable credentials required for certain tiers
- KMS-signed attestations validate eligibility
- On-chain verification before mint execution

---

## 4. Transferable vs Soulbound Options

### 4.1 Token Transferability Matrix

| Token | Default | Soulbound Option | Lock Period |
|-------|---------|------------------|-------------|
| **FlameCoin** | Transferable | Optional staking lock | 1-24 months |
| **ScrollCoin** | Transferable | No | N/A |
| **FlameDNA** | Tier-dependent | Inferno: Optional | Permanent |
| **Attestations** | Soulbound | Default | N/A |
| **Achievement Badges** | Soulbound | Default | N/A |

### 4.2 Soulbound Token Implementation

```solidity
// ERC-5192 Minimal Soulbound NFT
interface IERC5192 {
    event Locked(uint256 tokenId);
    event Unlocked(uint256 tokenId);
    
    function locked(uint256 tokenId) external view returns (bool);
}

contract SoulboundFlameDNA is ERC721, IERC5192 {
    mapping(uint256 => bool) private _locked;
    
    function _beforeTokenTransfer(
        address from,
        address to,
        uint256 tokenId
    ) internal override {
        require(
            from == address(0) || !_locked[tokenId],
            "Token is soulbound"
        );
        super._beforeTokenTransfer(from, to, tokenId);
    }
    
    function lockToken(uint256 tokenId) external {
        require(ownerOf(tokenId) == msg.sender, "Not owner");
        _locked[tokenId] = true;
        emit Locked(tokenId);
    }

    function locked(uint256 tokenId) external view override returns (bool) {
        return _locked[tokenId];
    }
}
```

### 4.3 Soulbound Use Cases

1. **Identity Attestations**: Non-transferable proof of identity
2. **Achievement Badges**: Earned accomplishments bound to achiever
3. **Governance Credentials**: Voting power tied to individuals
4. **Partnership Certificates**: Organization-bound partnerships
5. **Course Completions**: FlameAcademy certifications

---

## 5. Revocation Mechanisms

### 5.1 Revocation Types

| Type | Trigger | Process | Appeal |
|------|---------|---------|--------|
| **Administrative** | Terms violation | Multisig approval | 30 days |
| **Governance** | Community vote | Proposal + quorum | 14 days |
| **Expiration** | Time-based | Automatic | Re-application |
| **Self-Revocation** | Holder request | Immediate | N/A |

### 5.2 Credential Revocation

```solidity
// Revocation registry
contract RevocationRegistry {
    mapping(bytes32 => bool) public revoked;
    mapping(bytes32 => uint256) public revocationTime;
    
    event CredentialRevoked(bytes32 indexed credentialId, string reason);
    
    function revokeCredential(
        bytes32 credentialId,
        string calldata reason
    ) external onlyRevoker {
        require(!revoked[credentialId], "Already revoked");
        
        revoked[credentialId] = true;
        revocationTime[credentialId] = block.timestamp;
        
        emit CredentialRevoked(credentialId, reason);
    }
    
    function isRevoked(bytes32 credentialId) external view returns (bool) {
        return revoked[credentialId];
    }
}
```

### 5.3 Revocation Workflow

```
Violation Detected → Investigation → Evidence Review → 
Multisig Vote → Revocation Execution → Appeal Window → 
Final Status
```

### 5.4 Off-Chain Revocation (Verifiable Credentials)

- **Status List**: W3C Credential Status List 2021
- **Endpoint**: `https://scrollverse.io/credentials/status/{id}`
- **Update Frequency**: Real-time for critical, hourly batch for routine

---

## 6. Governance

### 6.1 Governance Structure

```
┌─────────────────────────────────────────────────────────────┐
│                    GOVERNANCE HIERARCHY                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   ┌─────────────────────────────────────────────────────┐   │
│   │              ScrollVerse Council                     │   │
│   │         (9 members, 2-year terms)                    │   │
│   │    Emergency powers, strategic direction             │   │
│   └────────────────────┬────────────────────────────────┘   │
│                        │                                     │
│   ┌────────────────────┼────────────────────┐               │
│   │                    │                    │               │
│   ▼                    ▼                    ▼               │
│ ┌──────────┐    ┌──────────┐    ┌──────────┐               │
│ │Technical │    │ Treasury │    │Community │               │
│ │Committee │    │Committee │    │Committee │               │
│ └──────────┘    └──────────┘    └──────────┘               │
│                        │                                     │
│                        ▼                                     │
│   ┌─────────────────────────────────────────────────────┐   │
│   │              Token Holder Assembly                   │   │
│   │    All FLAME holders with staked tokens              │   │
│   │    Proposal voting, delegate selection               │   │
│   └─────────────────────────────────────────────────────┘   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 6.2 Voting Power

| Token | Base Power | Multiplier Conditions |
|-------|------------|----------------------|
| **FLAME** | 1 vote/token | +50% for 1yr+ staking |
| **FlameDNA Inferno** | 10,000 votes | +100% for soulbound |
| **FlameDNA Blaze** | 1,000 votes | +50% for soulbound |
| **FlameDNA Ember** | 100 votes | +25% for soulbound |

### 6.3 Proposal Types

| Type | Quorum | Threshold | Timelock |
|------|--------|-----------|----------|
| **Parameter Change** | 4% | 50%+1 | 48 hours |
| **Treasury Spend** | 10% | 60% | 72 hours |
| **Protocol Upgrade** | 20% | 66% | 7 days |
| **Emergency Action** | Council only | 7/9 | Immediate |

### 6.4 Delegation

- Token holders can delegate voting power
- Delegation is revocable at any time
- Partial delegation supported
- Delegate accountability through on-chain records

---

## 7. Economic Model

### 7.1 Value Flows

```
┌─────────────────────────────────────────────────────────────┐
│                      VALUE CIRCULATION                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   Users ──── SCROLL ────► Services                          │
│      │                        │                              │
│      │                        │ Fees                         │
│      │                        ▼                              │
│      │                   ┌─────────┐                        │
│      │                   │Treasury │                        │
│      │                   └────┬────┘                        │
│      │                        │                              │
│      │        ┌───────────────┼───────────────┐             │
│      │        │               │               │             │
│      │        ▼               ▼               ▼             │
│      │   Buyback &       Development      Staking           │
│      │     Burn           Funding         Rewards           │
│      │        │               │               │             │
│      │        │               │               │             │
│      └────────┼───────────────┼───────────────┘             │
│               │               │                              │
│               ▼               ▼                              │
│          Deflation      Growth           Yield              │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 7.2 Fee Structure

| Action | Fee | Distribution |
|--------|-----|--------------|
| **NFT Mint** | 2.5% | 50% Treasury, 50% Creator |
| **Secondary Sale** | 5% | 60% Creator, 40% Treasury |
| **Token Swap** | 0.3% | 70% LPs, 30% Treasury |
| **Attestation** | 10 SCROLL | 100% Treasury |
| **Partnership** | Variable | Negotiated |

### 7.3 Sustainability Mechanisms

1. **Buyback & Burn**: Treasury uses fees to reduce supply
2. **Staking Rewards**: Incentivize long-term holding
3. **Liquidity Mining**: Bootstrap ecosystem liquidity
4. **Grant Programs**: Fund ecosystem development

---

## 8. Implementation Timeline

### Phase 1: Foundation (Q1 2025)
- [ ] Deploy FlameCoin contract
- [ ] Deploy ScrollCoin contract
- [ ] Implement basic governance

### Phase 2: NFT Launch (Q2 2025)
- [ ] Deploy FlameDNA collection
- [ ] Implement tiered minting
- [ ] Add soulbound options

### Phase 3: Governance Activation (Q3 2025)
- [ ] Launch council elections
- [ ] Enable proposal system
- [ ] Activate delegation

### Phase 4: Full Economy (Q4 2025)
- [ ] Enable all fee mechanisms
- [ ] Launch staking program
- [ ] Initiate buyback program

---

## Appendix A: Contract Addresses

*To be populated upon deployment*

| Contract | Network | Address |
|----------|---------|---------|
| FlameCoin | Scroll Mainnet | TBD |
| ScrollCoin | Scroll Mainnet | TBD |
| FlameDNA | Scroll Mainnet | TBD |
| Governance | Scroll Mainnet | TBD |
| Treasury | Scroll Mainnet | TBD |

---

## Appendix B: Glossary

- **FLAME**: FlameCoin, the governance token
- **SCROLL**: ScrollCoin, the utility token
- **FlameDNA**: NFT representing ecosystem membership
- **Soulbound**: Non-transferable token bound to an address
- **Quorum**: Minimum participation required for valid vote
- **Timelock**: Delay between approval and execution

---

## Appendix C: References

1. [SCROLLCHAIN_WHITEPAPER.md](./SCROLLCHAIN_WHITEPAPER.md)
2. [ARCHITECTURE.md](./ARCHITECTURE.md)
3. [EIP-5192: Minimal Soulbound NFTs](https://eips.ethereum.org/EIPS/eip-5192)
4. [W3C Verifiable Credentials](https://www.w3.org/TR/vc-data-model/)

---

*This RFC is open for community feedback. Submit comments via GitHub Issues or the ScrollVerse governance forum.*
This document specifies the token economics (tokenomics) for the AscendancyID system within the OmniTech Ascendancy Protocol (OTAP). It defines the identity token schema, supply mechanisms, minting rules, soulbound options, revocation procedures, metadata standards, and governance primitives.

## Motivation

The ScrollVerse ecosystem requires a robust identity layer that:

1. Provides verifiable on-chain identity
2. Enables governance participation
3. Supports credential attestations
4. Maintains economic sustainability
5. Respects user sovereignty and privacy

## Specification

### 1. AscendancyID Schema

#### Token Standard
- **Base Standard:** ERC-721 (Non-Fungible Token)
- **Extensions:** ERC-4973 (Account-Bound Tokens) for soulbound mode
- **Network:** Scroll (primary), with bridges to Ethereum and Polygon

#### Token Structure

```solidity
struct AscendancyID {
    uint256 tokenId;           // Unique identifier
    address holder;            // Current owner address
    uint256 tier;              // Supply tier (1-4)
    uint256 mintTimestamp;     // Creation timestamp
    bool isSoulbound;          // Transfer restriction flag
    bytes32 metadataHash;      // IPFS/Arweave content hash
    uint256 governanceWeight;  // Voting power multiplier
    bool isRevoked;            // Revocation status
}
```

#### Metadata Schema (JSON)

```json
{
  "name": "AscendancyID #12345",
  "description": "OmniTech Ascendancy Protocol Identity Token",
  "image": "ipfs://Qm.../ascendancy-id-12345.png",
  "external_url": "https://scrollverse.io/identity/12345",
  "attributes": [
    {
      "trait_type": "Tier",
      "value": "Genesis"
    },
    {
      "trait_type": "Soulbound",
      "value": "Yes"
    },
    {
      "trait_type": "Governance Weight",
      "value": 100,
      "display_type": "number"
    },
    {
      "trait_type": "Mint Date",
      "value": 1732608000,
      "display_type": "date"
    },
    {
      "trait_type": "Attestation Count",
      "value": 5,
      "display_type": "number"
    }
  ],
  "properties": {
    "tier": "genesis",
    "attestations": [
      "did:web:omnitech1.io/credentials/identity/12345",
      "did:web:omnitech1.io/credentials/shahadah/12345"
    ],
    "linkedDID": "did:ethr:scroll:0x1234...abcd"
  }
}
```

### 2. Supply Tiers

The AscendancyID system uses a tiered supply model to balance scarcity with accessibility.

| Tier | Name | Max Supply | Governance Weight | Minting Period |
|------|------|-----------|-------------------|----------------|
| 1 | Genesis | 1,000 | 100x | Launch - Month 3 |
| 2 | Founder | 10,000 | 50x | Month 3 - Month 6 |
| 3 | Pioneer | 100,000 | 10x | Month 6 - Month 12 |
| 4 | Citizen | Unlimited | 1x | Month 12+ |

#### Total Initial Supply Cap
- **Hard Cap (Year 1):** 111,000 tokens
- **Soft Cap (Ongoing):** No limit for Citizen tier

#### Supply Distribution

```
┌─────────────────────────────────────────────────────────┐
│                  AscendancyID Supply                    │
├─────────────────────────────────────────────────────────┤
│  Genesis (1,000)     ███                         0.9%   │
│  Founder (10,000)    ██████████                  9.0%   │
│  Pioneer (100,000)   ████████████████████████   90.1%   │
│  Citizen (∞)         [Unlimited after Year 1]          │
└─────────────────────────────────────────────────────────┘
```

### 3. Minting Rules

#### Eligibility Requirements

| Tier | Requirements |
|------|-------------|
| Genesis | Whitelist + 1 ETH equivalent stake |
| Founder | Whitelist OR community referral + 0.1 ETH stake |
| Pioneer | KYC attestation + 0.01 ETH stake |
| Citizen | Valid wallet address + gas fees only |

#### Minting Process

```mermaid
flowchart LR
    A[User Request] --> B{Tier Check}
    B -->|Genesis| C[Whitelist Verify]
    B -->|Founder| D[Referral Check]
    B -->|Pioneer| E[KYC Verify]
    B -->|Citizen| F[Wallet Valid]
    
    C --> G[Stake Required]
    D --> G
    E --> G
    F --> H[Gas Only]
    
    G --> I[Mint AscendancyID]
    H --> I
    I --> J[Emit Event]
```

#### Minting Fees

| Component | Genesis | Founder | Pioneer | Citizen |
|-----------|---------|---------|---------|---------|
| Protocol Fee | 0.5 ETH | 0.05 ETH | 0.005 ETH | 0 |
| Staking Requirement | 1 ETH | 0.1 ETH | 0.01 ETH | 0 |
| Gas (estimated) | ~0.01 ETH | ~0.01 ETH | ~0.01 ETH | ~0.01 ETH |

#### Fee Distribution

```
Protocol Fees Collected
        │
        ├── 40% → Treasury (DAO Governed)
        ├── 30% → Development Fund
        ├── 20% → Community Rewards Pool
        └── 10% → Insurance Reserve
```

### 4. Soulbound Mode

#### Overview

Soulbound AscendancyIDs are non-transferable tokens bound to a single address, providing stronger identity guarantees.

#### Soulbound Properties

| Property | Transferable | Soulbound |
|----------|-------------|-----------|
| Transfer | ✅ Allowed | ❌ Blocked |
| Sale | ✅ Allowed | ❌ Blocked |
| Delegate | ✅ Allowed | ✅ Allowed |
| Burn | ✅ By Owner | ✅ By Owner |
| Revoke | ✅ By Governance | ✅ By Governance |

#### Conversion Rules

- **Transferable → Soulbound:** Allowed (one-way, irreversible)
- **Soulbound → Transferable:** Not allowed
- **Default Mode:** User choice at mint time

#### Soulbound Benefits

1. **Enhanced Trust Score:** +25% credibility in matching
2. **Governance Bonus:** +10% voting weight
3. **Lower Insurance Requirement:** 50% reduction
4. **Priority Attestations:** Faster verification processing

### 5. Revocation

#### Revocation Triggers

| Trigger | Authority | Process |
|---------|-----------|---------|
| User Request | Token Holder | Immediate |
| Governance Vote | DAO (>66% majority) | 7-day timelock |
| Legal Compliance | Authorized Issuer | 48-hour notice |
| Security Breach | Emergency Council | Immediate |

#### Revocation Process

```solidity
// Revocation states
enum RevocationState {
    Active,           // Normal operation
    PendingRevocation, // In timelock period
    Revoked,          // Permanently revoked
    Suspended         // Temporarily disabled
}

// Revocation event
event AscendancyIDRevoked(
    uint256 indexed tokenId,
    address indexed holder,
    RevocationState newState,
    string reason,
    uint256 timestamp
);
```

#### Post-Revocation

- Token metadata updated with revocation status
- Governance weight set to 0
- Attestations linked to token marked as invalid
- Holder may appeal through governance process
- New AscendancyID may be minted after appeal period (90 days)

### 6. Metadata Fields

#### Core Fields (Required)

| Field | Type | Description |
|-------|------|-------------|
| `tokenId` | uint256 | Unique token identifier |
| `tier` | string | Supply tier name |
| `mintTimestamp` | uint256 | Unix timestamp of minting |
| `holder` | address | Current owner address |
| `isSoulbound` | boolean | Transfer restriction status |

#### Extended Fields (Optional)

| Field | Type | Description |
|-------|------|-------------|
| `displayName` | string | Human-readable name (encrypted) |
| `avatarURI` | string | Profile image URI |
| `linkedDID` | string | Associated DID identifier |
| `attestations` | string[] | Array of credential URIs |
| `socialLinks` | object | Verified social media links |
| `preferences` | object | User preference settings |

#### Privacy Considerations

- PII stored off-chain (IPFS/Arweave) with encryption
- On-chain data limited to hashes and public attributes
- Zero-knowledge proofs for selective disclosure (future)

### 7. Governance Primitives

#### Voting Power Calculation

```
Voting Power = Base Weight × Tier Multiplier × Soulbound Bonus × Time Factor

Where:
- Base Weight = 1
- Tier Multiplier = {Genesis: 100, Founder: 50, Pioneer: 10, Citizen: 1}
- Soulbound Bonus = {Yes: 1.1, No: 1.0}
- Time Factor = min(1.5, 1 + (days_held / 365) × 0.5)
```

#### Governance Actions

| Action | Quorum | Threshold | Timelock |
|--------|--------|-----------|----------|
| Parameter Change | 10% | 51% | 3 days |
| Treasury Spend (<$10K) | 5% | 51% | 1 day |
| Treasury Spend (>$10K) | 20% | 66% | 7 days |
| Protocol Upgrade | 25% | 75% | 14 days |
| Emergency Action | 1% | 90% | 0 days |

#### Delegation

- Voting power can be delegated to any valid address
- Delegation is revocable at any time
- Delegated votes do not transfer tier multipliers
- Self-delegation is the default state

### 8. Sample Economics

#### Year 1 Projections

| Metric | Conservative | Moderate | Optimistic |
|--------|-------------|----------|------------|
| Genesis Mints | 500 | 800 | 1,000 |
| Founder Mints | 3,000 | 6,000 | 10,000 |
| Pioneer Mints | 20,000 | 50,000 | 100,000 |
| Protocol Revenue | $125K | $350K | $750K |
| Treasury Value | $50K | $140K | $300K |

#### Token Value Drivers

1. **Utility Value:** Access to ecosystem services
2. **Governance Value:** Voting rights and influence
3. **Credential Value:** Attestation linkage
4. **Network Effects:** Growing ecosystem participation
5. **Scarcity:** Tiered supply limits

### 9. Issuance Schedule

#### Phase 1: Genesis Launch (Months 1-3)

```
Month 1: Genesis whitelist opens
         - Max 334 mints
         - Priority: Core contributors, partners

Month 2: Genesis public sale
         - Max 333 mints
         - First-come, first-served

Month 3: Genesis close, Founder opens
         - Final 333 Genesis mints
         - Founder whitelist begins
```

#### Phase 2: Founder Era (Months 3-6)

```
Month 3-4: Founder whitelist
           - Max 5,000 mints
           - Community referral program

Month 5-6: Founder public
           - Remaining 5,000 mints
           - Pioneer whitelist signup
```

#### Phase 3: Pioneer Expansion (Months 6-12)

```
Month 6-9: Pioneer early access
           - Max 50,000 mints
           - KYC integration launch

Month 9-12: Pioneer general
            - Remaining 50,000 mints
            - Citizen tier preparation
```

#### Phase 4: Citizen Era (Month 12+)

```
Month 12+: Citizen unlimited minting
           - No supply cap
           - Ongoing ecosystem growth
           - Governance fully active
```

### 10. Economic Sustainability

#### Revenue Streams

| Stream | Source | Allocation |
|--------|--------|------------|
| Minting Fees | New AscendancyID creation | Treasury (40%) |
| Transaction Fees | Marketplace trades | Development (30%) |
| Service Fees | Premium features | Rewards (20%) |
| Staking Returns | DeFi integrations | Insurance (10%) |

#### Sustainability Mechanisms

1. **Treasury Diversification:** Multi-asset holdings
2. **Burn Mechanism:** 1% of fees burned quarterly
3. **Inflation Control:** Citizen tier capped at 10% annual growth
4. **Reserve Requirements:** 6-month operational runway minimum

---

## Rationale

The tiered supply model balances:
- **Early adopter incentives** through Genesis/Founder scarcity
- **Broad accessibility** through Pioneer/Citizen availability
- **Governance stability** through weighted voting
- **Economic sustainability** through diversified revenue

## Backwards Compatibility

This specification is compatible with:
- ERC-721 standard interfaces
- ERC-4973 soulbound token standard
- Existing ScrollVerse smart contracts
- W3C Verifiable Credentials for attestations

## Security Considerations

1. **Sybil Resistance:** Tiered minting with KYC prevents mass creation
2. **Governance Attacks:** High quorums and timelocks protect treasury
3. **Key Management:** HSM-backed signing for protocol operations
4. **Revocation:** Multi-sig and timelock for irreversible actions

## References

- [EIP-721: Non-Fungible Token Standard](https://eips.ethereum.org/EIPS/eip-721)
- [EIP-4973: Account-bound Tokens](https://eips.ethereum.org/EIPS/eip-4973)
- [W3C Verifiable Credentials](https://www.w3.org/TR/vc-data-model/)
- [ScrollVerse Whitepaper](./SCROLLCHAIN_WHITEPAPER.md)

---

**Document Version:** 1.0.0  
**Last Updated:** 2025-11-26  
**Status:** Draft - Open for Community Review  

*This document is part of the OmniTech Ascendancy Protocol (OTAP) specification.*
