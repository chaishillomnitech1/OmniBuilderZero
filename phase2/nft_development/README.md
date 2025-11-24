# Guardian NFT Development

## Overview

Guardian NFTs are blockchain-based digital credentials that represent verified partnerships within the ScrollVerse ecosystem. These NFTs serve as immutable proof of partnership authenticity, grant access to exclusive features, and enable on-chain reputation tracking.

## Purpose

Guardian NFTs provide:
- **Verification**: Immutable proof of partnership agreement
- **Access Control**: Token-gated access to ScrollVerse partnership portal
- **Reputation**: On-chain track record of partnership milestones
- **Incentives**: Unlock benefits based on partnership performance
- **Governance**: Voting rights in ScrollVerse DAO decisions

## Guardian NFT Types

### 1. Partnership Guardian NFT (ERC-721)
**Purpose**: Unique credential for major strategic partnerships

**Attributes:**
- Partner name and logo
- Region (JP/KR/SG/Global)
- Star Dust resonance score at partnership inception
- Activation timestamp
- Partnership tier (Platinum/Gold/Silver)
- Milestone achievements (on-chain metadata updates)

**Example Metadata:**
```json
{
  "name": "Guardian NFT: Sony Corporation",
  "description": "ScrollVerse Partnership Guardian for Sony Corporation - Japan Region",
  "image": "ipfs://QmX.../sony-guardian.png",
  "attributes": [
    {
      "trait_type": "Partner",
      "value": "Sony Corporation"
    },
    {
      "trait_type": "Region",
      "value": "Japan"
    },
    {
      "trait_type": "Industry",
      "value": "Technology & Entertainment"
    },
    {
      "trait_type": "Resonance Score",
      "value": 8.77,
      "display_type": "number"
    },
    {
      "trait_type": "Partnership Tier",
      "value": "Platinum"
    },
    {
      "trait_type": "Activated Date",
      "value": 1732425600,
      "display_type": "date"
    },
    {
      "trait_type": "Milestones Completed",
      "value": 5,
      "display_type": "number"
    }
  ],
  "external_url": "https://scrollverse.com/partners/sony",
  "background_color": "1A1A2E"
}
```

### 2. Emissary Bot Guardian NFT (ERC-1155)
**Purpose**: Batch credentials for automated outreach campaign participants

**Use Cases:**
- Event attendees who engaged with Emissary Bot
- Beta testers of partnership features
- Community ambassadors
- Regional partnership coordinators

**Metadata Schema:**
```json
{
  "name": "Emissary Guardian #{token_id}",
  "description": "Recognition for contributing to ScrollVerse partnership ecosystem",
  "image": "ipfs://QmY.../emissary-guardian.png",
  "attributes": [
    {
      "trait_type": "Role",
      "value": "Beta Tester"
    },
    {
      "trait_type": "Region",
      "value": "Global"
    },
    {
      "trait_type": "Contribution Score",
      "value": 250,
      "display_type": "number"
    }
  ]
}
```

### 3. Academy Certification NFT (ERC-721)
**Purpose**: Completion certificates for ScrollVerse Academy courses

**Planned Implementation**: Q2 2026 (See ScrollVerse-Academy repo)

## Smart Contract Architecture

### Directory Structure
```
smart_contracts/
├── GuardianNFT.sol           # Main ERC-721 contract
├── GuardianBatch.sol         # ERC-1155 for batch minting
├── GuardianAccessControl.sol # Role-based permissions
├── GuardianMetadata.sol      # On-chain metadata management
└── interfaces/
    ├── IGuardianNFT.sol
    └── IGuardianBatch.sol
```

### GuardianNFT.sol (ERC-721) Specification

**Key Features:**
- Soulbound option (non-transferable for institutional partners)
- Upgradeable metadata via IPFS hash updates
- Milestone tracking and updates
- Partnership tier management
- Integration with Star Dust resonance scores

**Core Functions:**
```solidity
// Mint new Guardian NFT (admin only)
function mintGuardian(
    address partnerAddress,
    string memory partnerName,
    string memory region,
    uint256 resonanceScore,
    uint8 tier
) external onlyRole(MINTER_ROLE) returns (uint256 tokenId)

// Update milestone completion
function recordMilestone(
    uint256 tokenId,
    string memory milestoneDescription
) external onlyRole(UPDATER_ROLE)

// Get partnership data
function getPartnershipData(uint256 tokenId) 
    external view returns (
        string memory partnerName,
        string memory region,
        uint256 resonanceScore,
        uint8 tier,
        uint256 activatedAt,
        uint256 milestonesCompleted
    )

// Update metadata URI (for IPFS hash changes)
function updateTokenURI(uint256 tokenId, string memory newURI) 
    external onlyRole(METADATA_ROLE)
```

### GuardianBatch.sol (ERC-1155) Specification

**Key Features:**
- Batch minting for efficiency
- Multiple token types (roles/tiers)
- Flexible supply management
- Lower gas costs for community distributions

**Core Functions:**
```solidity
// Mint batch of Guardian NFTs
function mintBatch(
    address[] memory recipients,
    uint256 tokenType,
    uint256[] memory amounts
) external onlyRole(MINTER_ROLE)

// Create new token type
function createTokenType(
    string memory name,
    string memory uri,
    bool fungible
) external onlyRole(ADMIN_ROLE) returns (uint256 tokenType)
```

## Metadata Management

### IPFS Integration

All Guardian NFT images and metadata stored on IPFS for decentralization and immutability.

**Metadata Structure:**
```
metadata/
├── schemas/
│   ├── guardian-nft-schema.json      # JSON schema for validation
│   ├── emissary-guardian-schema.json
│   └── certification-schema.json
├── templates/
│   ├── partnership-template.json     # Template generator inputs
│   └── emissary-template.json
└── examples/
    ├── sony-guardian.json            # Real examples
    ├── hybe-guardian.json
    └── singapore-guardian.json
```

**Upload Workflow:**
```bash
# 1. Generate metadata from template
python generate_metadata.py --partner "Sony" --region "JP" --score 8.77

# 2. Upload image to IPFS
ipfs add guardian-images/sony-guardian.png
# Returns: QmX.../sony-guardian.png

# 3. Update metadata with IPFS image hash
# Edit JSON file with image CID

# 4. Upload metadata to IPFS
ipfs add metadata/sony-guardian.json
# Returns: QmY.../sony-guardian.json

# 5. Use metadata CID in smart contract mint function
```

## Deployment Strategy

### Multi-Chain Deployment

Guardian NFTs deployed across multiple chains for accessibility and cost optimization:

| Chain | Network | Use Case | Status |
|-------|---------|----------|--------|
| Ethereum | Mainnet | High-value partnerships (Sony, HYBE) | Planned |
| Polygon | PoS | Community and batch distributions | Planned |
| Scroll | zkEVM | Zero-knowledge privacy features | Planned |
| Base | L2 | Creator partnerships | Future |

### Deployment Scripts

```
deployment_scripts/
├── deploy-guardian-nft.js      # Hardhat deployment script
├── deploy-multi-chain.js       # Deploy to all chains
├── verify-contracts.js         # Etherscan verification
└── configure-roles.js          # Set up access control
```

**Example Deployment:**
```javascript
// deployment_scripts/deploy-guardian-nft.js
const { ethers } = require("hardhat");

async function main() {
  // Deploy GuardianNFT
  const GuardianNFT = await ethers.getContractFactory("GuardianNFT");
  const guardian = await GuardianNFT.deploy(
    "ScrollVerse Guardian",
    "GUARDIAN",
    "https://metadata.scrollverse.com/guardian/"
  );
  
  await guardian.deployed();
  console.log("GuardianNFT deployed to:", guardian.address);
  
  // Setup roles
  const MINTER_ROLE = await guardian.MINTER_ROLE();
  await guardian.grantRole(MINTER_ROLE, process.env.MINTER_ADDRESS);
  
  console.log("Roles configured");
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
```

## Integration with ScrollVerse Systems

### With Emissary Bots
```python
# When partnership reaches "PARTNERSHIP" status
from web3 import Web3
from emissary_bots import OutreachFunnel

funnel = OutreachFunnel()

# Monitor for partnership status changes
for opportunity in funnel.opportunities:
    if opportunity.status == "PARTNERSHIP" and not opportunity.nft_minted:
        # Trigger NFT minting
        mint_guardian_nft(
            partner_address=opportunity.wallet_address,
            partner_name=opportunity.name,
            region=opportunity.region.value,
            resonance_score=int(opportunity.resonance.overall_score * 100),
            tier=calculate_tier(opportunity)
        )
        
        opportunity.nft_minted = True
        funnel.save_data()
```

### With Dashboard
```typescript
// Dashboard displays Guardian NFTs
import { useGuardianNFTs } from '@/hooks/useGuardianNFTs';

function PartnerDashboard({ partnerAddress }) {
  const { nfts, loading } = useGuardianNFTs(partnerAddress);
  
  return (
    <div>
      {nfts.map(nft => (
        <GuardianNFTCard 
          key={nft.tokenId}
          metadata={nft.metadata}
          resonanceScore={nft.attributes.resonance_score}
          milestones={nft.attributes.milestones_completed}
        />
      ))}
    </div>
  );
}
```

### With Smart Contracts
```solidity
// Access control using Guardian NFT ownership
contract PartnershipPortal {
    IGuardianNFT public guardianNFT;
    
    modifier onlyGuardianHolder() {
        require(
            guardianNFT.balanceOf(msg.sender) > 0,
            "Must hold Guardian NFT"
        );
        _;
    }
    
    function accessExclusiveFeature() external onlyGuardianHolder {
        // Only Guardian NFT holders can access
    }
}
```

## Milestone System

### On-Chain Milestone Tracking

Guardian NFTs track partnership milestones on-chain:

**Milestone Types:**
1. **Technical Integration**: API connected, SDK implemented
2. **Content Launch**: First NFT drop, campaign launch
3. **User Acquisition**: 1K, 10K, 100K users reached
4. **Revenue**: Partnership revenue milestones
5. **Collaboration**: Joint events, co-marketing campaigns

**Implementation:**
```solidity
struct Milestone {
    string description;
    uint256 timestamp;
    bool verified;
}

mapping(uint256 => Milestone[]) public tokenMilestones;

function recordMilestone(
    uint256 tokenId,
    string memory description
) external onlyRole(UPDATER_ROLE) {
    tokenMilestones[tokenId].push(Milestone({
        description: description,
        timestamp: block.timestamp,
        verified: true
    }));
    
    emit MilestoneRecorded(tokenId, description, block.timestamp);
}
```

## Security Considerations

### Access Control
- **MINTER_ROLE**: Can mint new Guardian NFTs
- **UPDATER_ROLE**: Can update milestones and metadata
- **METADATA_ROLE**: Can update token URIs
- **ADMIN_ROLE**: Full contract administration

### Soulbound Implementation
```solidity
// Prevent transfers for institutional partners
mapping(uint256 => bool) public soulbound;

function _beforeTokenTransfer(
    address from,
    address to,
    uint256 tokenId
) internal override {
    if (soulbound[tokenId]) {
        require(
            from == address(0) || to == address(0),
            "Soulbound: transfer not allowed"
        );
    }
    super._beforeTokenTransfer(from, to, tokenId);
}
```

### Audit Requirements
- Professional smart contract audit before mainnet deployment
- Bug bounty program post-deployment
- Multi-sig wallet for admin operations
- Timelock for critical parameter changes

## Testing Strategy

```javascript
// test/GuardianNFT.test.js
describe("GuardianNFT", function() {
  it("Should mint Guardian NFT with correct attributes", async function() {
    const { guardian, minter, partner } = await loadFixture(deployFixture);
    
    await guardian.connect(minter).mintGuardian(
      partner.address,
      "Sony Corporation",
      "JP",
      877, // resonance score * 100
      1    // Platinum tier
    );
    
    const data = await guardian.getPartnershipData(1);
    expect(data.partnerName).to.equal("Sony Corporation");
    expect(data.resonanceScore).to.equal(877);
  });
  
  it("Should record milestones correctly", async function() {
    // Test implementation
  });
  
  it("Should enforce soulbound for flagged tokens", async function() {
    // Test implementation
  });
});
```

## Roadmap

### Phase 1: Foundation (Q1 2026)
- [ ] Smart contract development
- [ ] Metadata schema finalization
- [ ] IPFS integration setup
- [ ] Test deployment on Goerli

### Phase 2: Testnet Launch (Q2 2026)
- [ ] Deploy to Polygon Mumbai
- [ ] Deploy to Scroll Sepolia
- [ ] Integration testing with Emissary Bots
- [ ] Dashboard NFT display implementation

### Phase 3: Security & Audit (Q3 2026)
- [ ] Professional smart contract audit
- [ ] Bug fixes and optimizations
- [ ] Bug bounty program launch
- [ ] Multi-sig setup

### Phase 4: Mainnet Launch (Q4 2026)
- [ ] Ethereum mainnet deployment
- [ ] Polygon PoS deployment
- [ ] Scroll zkEVM deployment
- [ ] First Guardian NFT minting (Sony, HYBE, Singapore)

## Related Documentation

- [Main README](../../README.md)
- [Emissary Bots](../emissary_bots/README.md)
- [Blockchain Integration](../blockchain_integration/README.md)
- [REPOSITORY_MAP](../../REPOSITORY_MAP.md)

---

*Last Updated: 2025-11-24*  
*Version: 1.0.0*  
*Maintained by: ScrollVerse NFT Development Team*
