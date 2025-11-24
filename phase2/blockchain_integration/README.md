# Blockchain Integration Infrastructure

## Overview

The ScrollVerse blockchain integration layer provides the Web3 infrastructure for Guardian NFTs, partnership verification, decentralized governance, and multi-chain operations. This system enables trustless, transparent, and immutable partnership management.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│            ScrollVerse Blockchain Infrastructure             │
└─────────────────────────────────────────────────────────────┘

┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   Ethereum   │    │   Polygon    │    │    Scroll    │
│   (Mainnet)  │    │    (L2)      │    │   (zkEVM)    │
└──────┬───────┘    └──────┬───────┘    └──────┬───────┘
       │                   │                    │
       └───────────────────┼────────────────────┘
                           │
              ┌────────────▼────────────┐
              │   Multi-Chain Bridge    │
              └────────────┬────────────┘
                           │
       ┌───────────────────┼───────────────────┐
       │                   │                   │
┌──────▼──────┐   ┌────────▼────────┐  ┌──────▼──────┐
│  Guardian   │   │  Partnership    │  │   Oracle    │
│    NFTs     │   │   Agreements    │  │  Network    │
└─────────────┘   └─────────────────┘  └─────────────┘
```

## Multi-Chain Strategy

### Supported Blockchains

#### 1. Ethereum Mainnet
**Purpose**: High-value partnerships and primary governance

**Use Cases:**
- Sony, HYBE, major corporate partnerships
- ScrollVerse DAO governance tokens
- High-stakes partnership agreements
- Treasury management

**Configuration:**
```json
{
  "chain_id": 1,
  "name": "Ethereum Mainnet",
  "rpc_url": "https://eth-mainnet.g.alchemy.com/v2/{api_key}",
  "explorer": "https://etherscan.io",
  "native_currency": {
    "name": "Ether",
    "symbol": "ETH",
    "decimals": 18
  },
  "contracts": {
    "guardian_nft": "0x...",
    "partnership_agreement": "0x...",
    "governance_dao": "0x..."
  }
}
```

#### 2. Polygon PoS
**Purpose**: Cost-efficient operations and community engagement

**Use Cases:**
- Community Guardian NFTs (Emissary Bot participants)
- Frequent partnership milestone updates
- Academy certification NFTs
- Micro-transactions and rewards

**Configuration:**
```json
{
  "chain_id": 137,
  "name": "Polygon PoS",
  "rpc_url": "https://polygon-mainnet.g.alchemy.com/v2/{api_key}",
  "explorer": "https://polygonscan.com",
  "native_currency": {
    "name": "MATIC",
    "symbol": "MATIC",
    "decimals": 18
  },
  "contracts": {
    "guardian_batch": "0x...",
    "certification_nft": "0x..."
  }
}
```

#### 3. Scroll zkEVM
**Purpose**: Zero-knowledge privacy and scalability

**Use Cases:**
- Private partnership negotiations
- Confidential resonance score storage
- Anonymous community contributions
- Future privacy-preserving features

**Configuration:**
```json
{
  "chain_id": 534352,
  "name": "Scroll",
  "rpc_url": "https://rpc.scroll.io",
  "explorer": "https://scrollscan.com",
  "native_currency": {
    "name": "Ether",
    "symbol": "ETH",
    "decimals": 18
  },
  "contracts": {
    "private_guardian": "0x...",
    "zkp_verifier": "0x..."
  }
}
```

### Cross-Chain Communication

**Bridge Strategy:**
- LayerZero for omnichain NFT transfers
- Chainlink CCIP for message passing
- Native bridges for asset transfers

**Example: Cross-Chain Guardian Transfer**
```solidity
// Transfer Guardian NFT from Ethereum to Polygon
function bridgeGuardianNFT(
    uint256 tokenId,
    uint16 destinationChainId,
    address destinationAddress
) external onlyTokenOwner(tokenId) {
    // Lock NFT on source chain
    _lockToken(tokenId);
    
    // Send message to LayerZero endpoint
    ILayerZeroEndpoint(lzEndpoint).send{value: msg.value}(
        destinationChainId,
        abi.encodePacked(destinationAddress),
        abi.encode(tokenId, tokenURI(tokenId)),
        payable(msg.sender),
        address(0),
        bytes("")
    );
    
    emit NFTBridged(tokenId, destinationChainId, destinationAddress);
}
```

## Smart Contract Suite

### Core Contracts

#### 1. GuardianNFT.sol
Primary ERC-721 contract for partnership credentials
- See [NFT Development](../nft_development/README.md)

#### 2. PartnershipAgreement.sol
On-chain partnership terms and conditions

**Features:**
- Immutable partnership terms storage
- Milestone-based payment releases
- Multi-signature approval requirements
- Dispute resolution mechanisms

**Key Functions:**
```solidity
// Create new partnership agreement
function createAgreement(
    address partner,
    uint256 guardianTokenId,
    bytes32 termsHash,
    address[] memory approvers
) external returns (uint256 agreementId)

// Record milestone completion
function completeMilestone(
    uint256 agreementId,
    uint256 milestoneIndex,
    bytes memory proof
) external

// Release payment upon milestone
function releasePayment(
    uint256 agreementId,
    uint256 milestoneIndex
) external onlyApproved
```

#### 3. ResonanceOracle.sol
Chainlink oracle for off-chain resonance data

**Purpose**: Bring Star Dust frequency calculations on-chain

**Implementation:**
```solidity
// Request resonance score from off-chain calculator
function requestResonanceScore(
    string memory partnerName,
    string memory dataHash
) external returns (bytes32 requestId)

// Chainlink fulfills resonance score
function fulfillResonanceScore(
    bytes32 requestId,
    uint256 resonanceScore
) external onlyOracle
```

#### 4. GovernanceDAO.sol
Decentralized governance for ScrollVerse decisions

**Features:**
- Proposal creation and voting
- Guardian NFT-weighted voting power
- Timelock execution for security
- Treasury management

**Governance Process:**
```
1. Proposal Created → 2-day review period
2. Voting Open → 7-day voting period
3. Quorum Check → 10% of Guardian holders must vote
4. Execution → 2-day timelock → Execute if passed
```

## Oracle Integration

### Chainlink Integration

**Use Cases:**
- Resonance score on-chain verification
- Partnership milestone validation
- Real-world event triggers (e.g., revenue milestones)
- Price feeds for payment calculations

**Directory Structure:**
```
oracle_integrations/
├── chainlink/
│   ├── ResonanceOracle.sol
│   ├── MilestoneVerifier.sol
│   └── PriceFeeds.sol
├── api3/
│   └── AlternativeOracle.sol
└── configs/
    ├── chainlink-config.json
    └── oracle-endpoints.json
```

**Configuration:**
```json
{
  "chainlink": {
    "eth_mainnet": {
      "link_token": "0x514910771AF9Ca656af840dff83E8264EcF986CA",
      "oracle": "0x...",
      "job_id": "resonance_calculator",
      "fee": "0.1 LINK"
    },
    "polygon": {
      "link_token": "0x53E0bca35eC356BD5ddDFebbD1Fc0fD03FaBad39",
      "oracle": "0x...",
      "job_id": "resonance_calculator",
      "fee": "0.01 LINK"
    }
  }
}
```

### Custom Oracle Network

For ScrollVerse-specific data:
- Star Dust frequency calculations
- Partnership engagement metrics
- Cultural fit assessments
- Real-time funnel data

**Implementation:**
```javascript
// oracle_integrations/scrollverse-oracle/server.js
const express = require('express');
const { ethers } = require('ethers');

const app = express();

app.post('/calculate-resonance', async (req, res) => {
  const { partnerName, requestId } = req.body;
  
  // Calculate resonance using Star Dust frequencies
  const resonance = await calculateResonance(partnerName);
  
  // Fulfill on-chain request
  await oracleContract.fulfillResonanceScore(
    requestId,
    Math.floor(resonance.overall_score * 100)
  );
  
  res.json({ success: true, score: resonance.overall_score });
});

app.listen(3000);
```

## Wallet Integration

### Supported Wallets

**Desktop/Browser:**
- MetaMask
- WalletConnect
- Coinbase Wallet
- Rainbow Wallet

**Mobile:**
- MetaMask Mobile
- Trust Wallet
- Coinbase Wallet Mobile
- Rainbow Mobile

**Institutional:**
- Gnosis Safe (Multi-sig)
- Fireblocks
- Copper

### Web3 Connection Library

```typescript
// wallet_connectors/web3-connector.ts
import { ethers } from 'ethers';
import WalletConnectProvider from '@walletconnect/web3-provider';

export class Web3Connector {
  private provider: ethers.providers.Web3Provider | null = null;
  
  async connectMetaMask(): Promise<ethers.providers.Web3Provider> {
    if (!window.ethereum) {
      throw new Error('MetaMask not installed');
    }
    
    await window.ethereum.request({ method: 'eth_requestAccounts' });
    this.provider = new ethers.providers.Web3Provider(window.ethereum);
    
    return this.provider;
  }
  
  async connectWalletConnect(): Promise<ethers.providers.Web3Provider> {
    const provider = new WalletConnectProvider({
      rpc: {
        1: process.env.ETHEREUM_RPC_URL,
        137: process.env.POLYGON_RPC_URL,
        534352: process.env.SCROLL_RPC_URL
      }
    });
    
    await provider.enable();
    this.provider = new ethers.providers.Web3Provider(provider);
    
    return this.provider;
  }
  
  async getGuardianNFTs(address: string): Promise<any[]> {
    if (!this.provider) throw new Error('Not connected');
    
    const guardianContract = new ethers.Contract(
      GUARDIAN_NFT_ADDRESS,
      GUARDIAN_NFT_ABI,
      this.provider
    );
    
    const balance = await guardianContract.balanceOf(address);
    const nfts = [];
    
    for (let i = 0; i < balance; i++) {
      const tokenId = await guardianContract.tokenOfOwnerByIndex(address, i);
      const uri = await guardianContract.tokenURI(tokenId);
      nfts.push({ tokenId, uri });
    }
    
    return nfts;
  }
}
```

## Gas Optimization

### Strategies

1. **Batch Operations**: Mint multiple NFTs in single transaction
2. **Storage Optimization**: Pack data into fewer storage slots
3. **Event Emission**: Store large data in events, not storage
4. **Layer 2 Usage**: Use Polygon for frequent operations
5. **Upgradeable Proxies**: Fix bugs without redeployment

**Example: Batch Minting**
```solidity
// Gas-optimized batch minting
function batchMintGuardian(
    address[] calldata recipients,
    string[] calldata partnerNames,
    uint256[] calldata resonanceScores
) external onlyRole(MINTER_ROLE) {
    require(
        recipients.length == partnerNames.length &&
        partnerNames.length == resonanceScores.length,
        "Array length mismatch"
    );
    
    uint256 currentTokenId = _tokenIdCounter;
    
    for (uint256 i = 0; i < recipients.length; i++) {
        _safeMint(recipients[i], currentTokenId);
        
        // Emit event instead of storing in mapping (gas saving)
        emit GuardianMinted(
            currentTokenId,
            recipients[i],
            partnerNames[i],
            resonanceScores[i]
        );
        
        currentTokenId++;
    }
    
    _tokenIdCounter = currentTokenId;
}
```

## Security Best Practices

### Access Control
```solidity
// Role-based access control
bytes32 public constant MINTER_ROLE = keccak256("MINTER_ROLE");
bytes32 public constant UPDATER_ROLE = keccak256("UPDATER_ROLE");
bytes32 public constant ADMIN_ROLE = keccak256("ADMIN_ROLE");

// Multi-sig requirement for critical operations
modifier requiresMultiSig() {
    require(
        multiSigApprovals[msg.sig] >= REQUIRED_APPROVALS,
        "Insufficient approvals"
    );
    _;
}
```

### Upgrade Safety
```solidity
// Use OpenZeppelin upgradeable contracts
import "@openzeppelin/contracts-upgradeable/proxy/utils/Initializable.sol";
import "@openzeppelin/contracts-upgradeable/proxy/utils/UUPSUpgradeable.sol";

contract GuardianNFT is Initializable, UUPSUpgradeable {
    function initialize() public initializer {
        __UUPSUpgradeable_init();
        // Initialization logic
    }
    
    function _authorizeUpgrade(address) internal override onlyRole(ADMIN_ROLE) {}
}
```

### Audit Checklist
- [ ] Reentrancy protection on all external calls
- [ ] Integer overflow/underflow checks
- [ ] Access control on privileged functions
- [ ] Input validation on all user inputs
- [ ] Events for all state changes
- [ ] Proper use of visibility modifiers
- [ ] Safe external contract interactions
- [ ] Emergency pause mechanism

## Testing Infrastructure

### Unit Tests
```javascript
// test/GuardianNFT.test.js
const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("GuardianNFT Integration", function() {
  let guardian, partnership, oracle;
  let owner, minter, partner;
  
  beforeEach(async function() {
    [owner, minter, partner] = await ethers.getSigners();
    
    // Deploy contracts
    const Guardian = await ethers.getContractFactory("GuardianNFT");
    guardian = await Guardian.deploy();
    
    const Partnership = await ethers.getContractFactory("PartnershipAgreement");
    partnership = await Partnership.deploy(guardian.address);
    
    const Oracle = await ethers.getContractFactory("ResonanceOracle");
    oracle = await Oracle.deploy();
  });
  
  it("End-to-end partnership flow", async function() {
    // 1. Request resonance score from oracle
    await oracle.requestResonanceScore("Sony", "dataHash");
    
    // 2. Mint Guardian NFT
    await guardian.mintGuardian(partner.address, "Sony", "JP", 877, 1);
    
    // 3. Create partnership agreement
    await partnership.createAgreement(
      partner.address,
      1, // tokenId
      ethers.utils.id("termsHash"),
      [owner.address]
    );
    
    // 4. Verify NFT ownership grants access
    expect(await guardian.balanceOf(partner.address)).to.equal(1);
  });
});
```

### Integration Tests
Test cross-contract interactions and multi-chain scenarios

### Testnet Deployment
- Goerli (Ethereum)
- Mumbai (Polygon)
- Scroll Sepolia

## Monitoring & Analytics

### On-Chain Analytics
Track:
- Total Guardian NFTs minted
- Partnership agreements created
- Milestone completion rate
- Average resonance scores
- Regional distribution

### Dune Analytics Dashboard
Custom SQL queries for ScrollVerse metrics:
```sql
-- Total Guardian NFTs by region
SELECT
  region,
  COUNT(*) as guardian_count,
  AVG(resonance_score) as avg_resonance
FROM guardian_nft_events
GROUP BY region
ORDER BY guardian_count DESC;
```

## Related Documentation

- [Guardian NFT Development](../nft_development/README.md)
- [Emissary Bots](../emissary_bots/README.md)
- [Main README](../../README.md)
- [REPOSITORY_MAP](../../REPOSITORY_MAP.md)

---

*Last Updated: 2025-11-24*  
*Version: 1.0.0*  
*Maintained by: ScrollVerse Blockchain Team*
