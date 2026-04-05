# AscendancyID NFT Specification

> **ERC-721 Identity Token with Security Patterns, Metadata, and Contract Patterns**

---

## Overview

AscendancyID is an ERC-721-based NFT that represents a user's identity, membership tier, and access rights within the Omni-Tech Ascendancy Protocol (OTAP) ecosystem. Each AscendancyID is unique, non-transferable (soulbound option available), and contains on-chain metadata about the holder's role and achievements.

---

## Token Standard

### Base Implementation
- **Standard**: ERC-721 (with optional ERC-721A for batch minting efficiency)
- **Extensions**: 
  - ERC-721Enumerable (for token enumeration)
  - ERC-2981 (royalty standard)
  - ERC-5192 (soulbound/non-transferable option)

### Interfaces

```solidity
interface IAscendancyID {
    // Core identity functions
    function mint(address to, Tier tier) external returns (uint256);
    function upgradeTier(uint256 tokenId, Tier newTier) external;
    function getIdentity(uint256 tokenId) external view returns (Identity memory);
    
    // Soulbound functions
    function setSoulbound(uint256 tokenId, bool locked) external;
    function isSoulbound(uint256 tokenId) external view returns (bool);
    
    // Role management
    function assignRole(uint256 tokenId, Role role) external;
    function revokeRole(uint256 tokenId, Role role) external;
    function hasRole(uint256 tokenId, Role role) external view returns (bool);
}
```

---

## Token Tiers

AscendancyID tokens are organized into four tiers, each with increasing benefits and governance power:

| Tier | Name | Requirements | Governance Weight | Benefits |
|------|------|--------------|-------------------|----------|
| 1 | Bronze | Entry level | 1x | Basic access, voting rights |
| 2 | Silver | 30 days + activity | 2x | Priority support, early access |
| 3 | Gold | 90 days + staking | 4x | Proposal creation, delegation |
| 4 | Platinum | 180 days + contribution | 8x | Full governance, revenue share |

### Tier Upgrade Requirements

```solidity
struct TierRequirements {
    uint256 minHoldDuration;      // Minimum time holding current tier
    uint256 minStakedAmount;      // Minimum tokens staked
    uint256 minActivityScore;     // Minimum participation score
    uint256 minContributions;     // Minimum verified contributions
}

mapping(Tier => TierRequirements) public tierRequirements;
```

---

## Roles

Each AscendancyID can be assigned one or more roles:

| Role | Description | Permissions |
|------|-------------|-------------|
| Seeker | New member | Read-only, can vote |
| Apprentice | Active participant | Can create proposals |
| Architect | Verified contributor | Can approve changes |
| Sovereign | Core team/DAO | Full administrative access |

### Role Assignment

```solidity
enum Role {
    SEEKER,
    APPRENTICE,
    ARCHITECT,
    SOVEREIGN
}

struct RoleData {
    bool isActive;
    uint256 assignedAt;
    address assignedBy;
}

// tokenId => role => roleData
mapping(uint256 => mapping(Role => RoleData)) public tokenRoles;
```

---

## Metadata Schema

### On-Chain Metadata

```solidity
struct Identity {
    uint256 tokenId;
    address owner;
    Tier tier;
    uint256 mintedAt;
    uint256 lastUpgradeAt;
    uint256 activityScore;
    bool isSoulbound;
    bytes32 identityHash;  // Hash of off-chain identity verification
}
```

### Off-Chain Metadata (JSON)

```json
{
    "name": "AscendancyID #1234",
    "description": "OTAP Identity Token - Tier: Gold, Role: Architect",
    "image": "ipfs://QmXxx.../1234.png",
    "external_url": "https://otap.example.com/identity/1234",
    "attributes": [
        {
            "trait_type": "Tier",
            "value": "Gold"
        },
        {
            "trait_type": "Primary Role",
            "value": "Architect"
        },
        {
            "trait_type": "Governance Weight",
            "value": 4,
            "display_type": "number"
        },
        {
            "trait_type": "Member Since",
            "value": 1704067200,
            "display_type": "date"
        },
        {
            "trait_type": "Activity Score",
            "value": 8500,
            "max_value": 10000,
            "display_type": "boost_percentage"
        },
        {
            "trait_type": "Soulbound",
            "value": "Yes"
        }
    ],
    "properties": {
        "tier_details": {
            "current": "Gold",
            "progress_to_next": 75,
            "requirements_met": ["hold_duration", "staking"],
            "requirements_pending": ["contributions"]
        },
        "roles": ["Seeker", "Apprentice", "Architect"],
        "achievements": [
            "early_adopter",
            "first_proposal",
            "governance_participant"
        ]
    }
}
```

---

## Security Patterns

### 1. Access Control

```solidity
import "@openzeppelin/contracts/access/AccessControl.sol";

bytes32 public constant MINTER_ROLE = keccak256("MINTER_ROLE");
bytes32 public constant UPGRADER_ROLE = keccak256("UPGRADER_ROLE");
bytes32 public constant ADMIN_ROLE = keccak256("ADMIN_ROLE");

modifier onlyMinter() {
    require(hasRole(MINTER_ROLE, msg.sender), "Not authorized to mint");
    _;
}

modifier onlyUpgrader() {
    require(hasRole(UPGRADER_ROLE, msg.sender), "Not authorized to upgrade");
    _;
}
```

### 2. Reentrancy Protection

```solidity
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

function mint(address to, Tier tier) 
    external 
    nonReentrant 
    onlyMinter 
    returns (uint256) 
{
    // Minting logic
}
```

### 3. Pausable Operations

```solidity
import "@openzeppelin/contracts/security/Pausable.sol";

function pause() external onlyRole(ADMIN_ROLE) {
    _pause();
}

function unpause() external onlyRole(ADMIN_ROLE) {
    _unpause();
}

function mint(address to, Tier tier) 
    external 
    whenNotPaused 
    returns (uint256) 
{
    // Minting logic
}
```

### 4. Soulbound Implementation (ERC-5192)

```solidity
error SoulboundTokenNotTransferable();

mapping(uint256 => bool) private _soulboundTokens;

function setSoulbound(uint256 tokenId, bool locked) external {
    require(_isApprovedOrOwner(msg.sender, tokenId), "Not authorized");
    _soulboundTokens[tokenId] = locked;
    emit Locked(tokenId);  // or Unlocked(tokenId)
}

function _beforeTokenTransfer(
    address from,
    address to,
    uint256 tokenId,
    uint256 batchSize
) internal virtual override {
    super._beforeTokenTransfer(from, to, tokenId, batchSize);
    
    // Allow minting (from == address(0)) and burning (to == address(0))
    if (from != address(0) && to != address(0)) {
        if (_soulboundTokens[tokenId]) {
            revert SoulboundTokenNotTransferable();
        }
    }
}
```

### 5. Upgrade Cooldown

```solidity
uint256 public constant UPGRADE_COOLDOWN = 7 days;

mapping(uint256 => uint256) public lastUpgradeTime;

function upgradeTier(uint256 tokenId, Tier newTier) external {
    require(
        block.timestamp >= lastUpgradeTime[tokenId] + UPGRADE_COOLDOWN,
        "Upgrade cooldown not elapsed"
    );
    // Upgrade logic
    lastUpgradeTime[tokenId] = block.timestamp;
}
```

---

## Suggested Contract Patterns

### Full Contract Structure

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Enumerable.sol";
import "@openzeppelin/contracts/token/common/ERC2981.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";
import "@openzeppelin/contracts/security/Pausable.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

/**
 * @title AscendancyID
 * @dev ERC-721 identity token for OTAP ecosystem
 * @author OTAP Team
 */
contract AscendancyID is 
    ERC721Enumerable, 
    ERC2981, 
    AccessControl, 
    Pausable, 
    ReentrancyGuard 
{

    // ============ Enums ============
    enum Tier { BRONZE, SILVER, GOLD, PLATINUM }
    enum Role { SEEKER, APPRENTICE, ARCHITECT, SOVEREIGN }

    // ============ Structs ============
    struct Identity {
        Tier tier;
        uint256 mintedAt;
        uint256 lastUpgradeAt;
        uint256 activityScore;
        bool isSoulbound;
    }

    // ============ Constants ============
    bytes32 public constant MINTER_ROLE = keccak256("MINTER_ROLE");
    bytes32 public constant UPGRADER_ROLE = keccak256("UPGRADER_ROLE");
    uint256 public constant UPGRADE_COOLDOWN = 7 days;
    uint96 public constant ROYALTY_BPS = 500; // 5%

    // ============ State Variables ============
    uint256 private _tokenIdCounter;
    string private _baseTokenURI;
    address public treasury;

    mapping(uint256 => Identity) public identities;
    mapping(uint256 => mapping(Role => bool)) public tokenRoles;

    // ============ Events ============
    event IdentityMinted(uint256 indexed tokenId, address indexed to, Tier tier);
    event TierUpgraded(uint256 indexed tokenId, Tier oldTier, Tier newTier);
    event RoleAssigned(uint256 indexed tokenId, Role role);
    event RoleRevoked(uint256 indexed tokenId, Role role);
    event SoulboundSet(uint256 indexed tokenId, bool locked);

    // ============ Errors ============
    error SoulboundTokenNotTransferable();
    error InvalidTierUpgrade();
    error UpgradeCooldownNotElapsed();
    error InvalidAddress();

    // ============ Constructor ============
    constructor(
        string memory name,
        string memory symbol,
        string memory baseURI,
        address _treasury
    ) ERC721(name, symbol) {
        if (_treasury == address(0)) revert InvalidAddress();
        
        _baseTokenURI = baseURI;
        treasury = _treasury;
        
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _grantRole(MINTER_ROLE, msg.sender);
        _grantRole(UPGRADER_ROLE, msg.sender);
        
        _setDefaultRoyalty(_treasury, ROYALTY_BPS);
    }

    // ============ External Functions ============
    
    function mint(address to, Tier tier) 
        external 
        nonReentrant 
        whenNotPaused 
        onlyRole(MINTER_ROLE) 
        returns (uint256) 
    {
        if (to == address(0)) revert InvalidAddress();
        
        uint256 tokenId = _tokenIdCounter;
        _tokenIdCounter++;
        
        _safeMint(to, tokenId);
        
        identities[tokenId] = Identity({
            tier: tier,
            mintedAt: block.timestamp,
            lastUpgradeAt: block.timestamp,
            activityScore: 0,
            isSoulbound: false
        });
        
        // Assign default role
        tokenRoles[tokenId][Role.SEEKER] = true;
        
        emit IdentityMinted(tokenId, to, tier);
        return tokenId;
    }

    function upgradeTier(uint256 tokenId, Tier newTier) 
        external 
        onlyRole(UPGRADER_ROLE) 
    {
        Identity storage identity = identities[tokenId];
        
        if (newTier <= identity.tier) revert InvalidTierUpgrade();
        if (block.timestamp < identity.lastUpgradeAt + UPGRADE_COOLDOWN) {
            revert UpgradeCooldownNotElapsed();
        }
        
        Tier oldTier = identity.tier;
        identity.tier = newTier;
        identity.lastUpgradeAt = block.timestamp;
        
        emit TierUpgraded(tokenId, oldTier, newTier);
    }

    function setSoulbound(uint256 tokenId, bool locked) external {
        require(_isApprovedOrOwner(msg.sender, tokenId), "Not authorized");
        identities[tokenId].isSoulbound = locked;
        emit SoulboundSet(tokenId, locked);
    }

    function assignRole(uint256 tokenId, Role role) 
        external 
        onlyRole(DEFAULT_ADMIN_ROLE) 
    {
        tokenRoles[tokenId][role] = true;
        emit RoleAssigned(tokenId, role);
    }

    function revokeRole(uint256 tokenId, Role role) 
        external 
        onlyRole(DEFAULT_ADMIN_ROLE) 
    {
        tokenRoles[tokenId][role] = false;
        emit RoleRevoked(tokenId, role);
    }

    // ============ View Functions ============

    function getIdentity(uint256 tokenId) 
        external 
        view 
        returns (Identity memory) 
    {
        return identities[tokenId];
    }

    function hasTokenRole(uint256 tokenId, Role role) 
        external 
        view 
        returns (bool) 
    {
        return tokenRoles[tokenId][role];
    }

    function getGovernanceWeight(uint256 tokenId) 
        external 
        view 
        returns (uint256) 
    {
        Tier tier = identities[tokenId].tier;
        if (tier == Tier.BRONZE) return 1;
        if (tier == Tier.SILVER) return 2;
        if (tier == Tier.GOLD) return 4;
        return 8; // PLATINUM
    }

    // ============ Admin Functions ============

    function pause() external onlyRole(DEFAULT_ADMIN_ROLE) {
        _pause();
    }

    function unpause() external onlyRole(DEFAULT_ADMIN_ROLE) {
        _unpause();
    }

    function setBaseURI(string memory baseURI) 
        external 
        onlyRole(DEFAULT_ADMIN_ROLE) 
    {
        _baseTokenURI = baseURI;
    }

    function setTreasury(address _treasury) 
        external 
        onlyRole(DEFAULT_ADMIN_ROLE) 
    {
        if (_treasury == address(0)) revert InvalidAddress();
        treasury = _treasury;
        _setDefaultRoyalty(_treasury, ROYALTY_BPS);
    }

    // ============ Internal Functions ============

    function _baseURI() internal view override returns (string memory) {
        return _baseTokenURI;
    }

    function _beforeTokenTransfer(
        address from,
        address to,
        uint256 tokenId,
        uint256 batchSize
    ) internal virtual override {
        super._beforeTokenTransfer(from, to, tokenId, batchSize);
        
        // Allow minting and burning, block transfers if soulbound
        if (from != address(0) && to != address(0)) {
            if (identities[tokenId].isSoulbound) {
                revert SoulboundTokenNotTransferable();
            }
        }
    }

    // ============ Required Overrides ============

    function supportsInterface(bytes4 interfaceId)
        public
        view
        override(ERC721Enumerable, ERC2981, AccessControl)
        returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }
}
```

---

## Testing Requirements

### Unit Tests with Foundry

```solidity
// test/AscendancyID.t.sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "forge-std/Test.sol";
import "../contracts/AscendancyID.sol";

contract AscendancyIDTest is Test {
    AscendancyID public nft;
    address public owner = address(1);
    address public user1 = address(2);
    address public treasury = address(3);

    function setUp() public {
        vm.startPrank(owner);
        nft = new AscendancyID(
            "AscendancyID",
            "ASCID",
            "ipfs://base/",
            treasury
        );
        vm.stopPrank();
    }

    function testMint() public {
        vm.prank(owner);
        uint256 tokenId = nft.mint(user1, AscendancyID.Tier.BRONZE);
        
        assertEq(nft.ownerOf(tokenId), user1);
        assertEq(uint(nft.getIdentity(tokenId).tier), uint(AscendancyID.Tier.BRONZE));
    }

    function testUpgradeTier() public {
        vm.prank(owner);
        uint256 tokenId = nft.mint(user1, AscendancyID.Tier.BRONZE);
        
        // Fast forward past cooldown
        vm.warp(block.timestamp + 8 days);
        
        vm.prank(owner);
        nft.upgradeTier(tokenId, AscendancyID.Tier.SILVER);
        
        assertEq(uint(nft.getIdentity(tokenId).tier), uint(AscendancyID.Tier.SILVER));
    }

    function testSoulbound() public {
        vm.prank(owner);
        uint256 tokenId = nft.mint(user1, AscendancyID.Tier.BRONZE);
        
        vm.prank(user1);
        nft.setSoulbound(tokenId, true);
        
        assertTrue(nft.getIdentity(tokenId).isSoulbound);
        
        // Should revert on transfer
        vm.prank(user1);
        vm.expectRevert(AscendancyID.SoulboundTokenNotTransferable.selector);
        nft.transferFrom(user1, address(4), tokenId);
    }

    function testGovernanceWeight() public {
        vm.startPrank(owner);
        
        uint256 bronzeId = nft.mint(user1, AscendancyID.Tier.BRONZE);
        uint256 platinumId = nft.mint(user1, AscendancyID.Tier.PLATINUM);
        
        assertEq(nft.getGovernanceWeight(bronzeId), 1);
        assertEq(nft.getGovernanceWeight(platinumId), 8);
        
        vm.stopPrank();
    }
}
```

---

## Deployment Checklist

- [ ] Deploy to testnet (Sepolia/Scroll Sepolia)
- [ ] Verify contract on block explorer
- [ ] Test all functions manually
- [ ] Run Foundry fuzz tests
- [ ] Complete external security audit
- [ ] Deploy to mainnet
- [ ] Transfer ownership to multisig

---

## References

- [ERC-721 Standard](https://eips.ethereum.org/EIPS/eip-721)
- [ERC-2981 Royalty Standard](https://eips.ethereum.org/EIPS/eip-2981)
- [ERC-5192 Soulbound](https://eips.ethereum.org/EIPS/eip-5192)
- [OpenZeppelin Contracts](https://docs.openzeppelin.com/contracts/)
- [OTAP-README.md](./OTAP-README.md) - Protocol overview
- [ARCH_EXECUTOR.md](./ARCH_EXECUTOR.md) - Orchestration design
