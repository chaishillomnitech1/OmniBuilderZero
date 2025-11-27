# ScrollVerse Tokenomics

**Status**: RFC (Request for Comments)  
**Version**: 1.0.0  
**Author**: OmniTech1 Economic Council  
**Date**: 2025-11-26

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
