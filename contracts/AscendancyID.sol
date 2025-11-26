// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";
import "@openzeppelin/contracts/utils/Pausable.sol";

/**
 * @title AscendancyID
 * @dev Soulbound Token (SBT) for ScrollVerse identity and privilege management
 * @notice AscendancyID is non-transferable and represents user identity in the ecosystem
 */
contract AscendancyID is ERC721, ERC721URIStorage, Ownable, ReentrancyGuard, Pausable {
    // Token ID counter
    uint256 private _tokenIdCounter;

    // Staking contract reference for privilege verification
    address public stakingContract;

    // Metadata structure
    struct AscendancyMetadata {
        string displayName;        // User-chosen display name (max 32 chars)
        uint8 privilegeTier;       // Current privilege tier (0-5)
        uint256 mintTimestamp;     // When the ID was minted
        uint256 lastTierChange;    // Last privilege level change
        uint256 governanceScore;   // Participation in governance
        bool isActive;             // Whether the ID is active
    }

    // Token ID to metadata mapping
    mapping(uint256 => AscendancyMetadata) public metadata;

    // Address to token ID mapping (one ID per address)
    mapping(address => uint256) public addressToTokenId;

    // Check if address has an ID
    mapping(address => bool) public hasAscendancyId;

    // Mint fees per tier (in wei)
    mapping(uint8 => uint256) public mintFees;

    // Treasury address for fee collection
    address public treasury;

    // Authorized privilege updaters (staking contract, governance)
    mapping(address => bool) public privilegeUpdaters;

    // Revocation reasons
    enum RevocationReason {
        UserRequest,
        GovernanceVote,
        SecurityBreach,
        TermsViolation,
        Inactivity
    }

    // Events
    event AscendancyIDMinted(
        uint256 indexed tokenId,
        address indexed owner,
        string displayName,
        uint8 initialTier
    );
    event PrivilegeUpgraded(
        uint256 indexed tokenId,
        uint8 oldTier,
        uint8 newTier
    );
    event PrivilegeDowngraded(
        uint256 indexed tokenId,
        uint8 oldTier,
        uint8 newTier
    );
    event DisplayNameChanged(
        uint256 indexed tokenId,
        string oldName,
        string newName
    );
    event AscendancyIDRevoked(
        uint256 indexed tokenId,
        address indexed owner,
        RevocationReason reason
    );
    event GovernanceScoreUpdated(
        uint256 indexed tokenId,
        uint256 oldScore,
        uint256 newScore
    );
    event PrivilegeUpdaterSet(address indexed updater, bool authorized);
    event StakingContractUpdated(address oldContract, address newContract);
    event TreasuryUpdated(address oldTreasury, address newTreasury);
    event MintFeeUpdated(uint8 tier, uint256 oldFee, uint256 newFee);

    /**
     * @dev Constructor
     * @param _treasury Address of treasury for fee collection
     */
    constructor(
        address _treasury
    ) ERC721("AscendancyID", "ASCID") Ownable(msg.sender) {
        require(_treasury != address(0), "Invalid treasury");
        treasury = _treasury;

        // Set default mint fees (can be updated by owner)
        mintFees[0] = 0;                    // Initiate: Free
        mintFees[1] = 0.01 ether;           // Bronze
        mintFees[2] = 0.05 ether;           // Silver
        mintFees[3] = 0.1 ether;            // Gold
        mintFees[4] = 0.2 ether;            // Platinum
        mintFees[5] = 0.5 ether;            // Diamond
    }

    /**
     * @dev Mint a new AscendancyID
     * @param displayName User's chosen display name
     * @param initialTier Initial privilege tier (0-5)
     * @return tokenId The minted token ID
     */
    function mint(
        string memory displayName,
        uint8 initialTier
    ) external payable nonReentrant whenNotPaused returns (uint256) {
        require(!hasAscendancyId[msg.sender], "Already has AscendancyID");
        require(initialTier <= 5, "Invalid tier");
        require(bytes(displayName).length <= 32, "Name too long");
        require(msg.value >= mintFees[initialTier], "Insufficient mint fee");

        // If tier > 0, verify staking requirements
        if (initialTier > 0 && stakingContract != address(0)) {
            uint8 stakedTier = _getStakedTier(msg.sender);
            require(stakedTier >= initialTier, "Insufficient stake for tier");
        }

        uint256 tokenId = _tokenIdCounter++;

        // Mint the token
        _safeMint(msg.sender, tokenId);

        // Set metadata
        metadata[tokenId] = AscendancyMetadata({
            displayName: displayName,
            privilegeTier: initialTier,
            mintTimestamp: block.timestamp,
            lastTierChange: block.timestamp,
            governanceScore: 0,
            isActive: true
        });

        // Track ownership
        addressToTokenId[msg.sender] = tokenId;
        hasAscendancyId[msg.sender] = true;

        // Send fee to treasury
        if (msg.value > 0) {
            (bool success, ) = treasury.call{value: msg.value}("");
            require(success, "Fee transfer failed");
        }

        emit AscendancyIDMinted(tokenId, msg.sender, displayName, initialTier);

        return tokenId;
    }

    /**
     * @dev Upgrade privilege tier (called by staking contract or privileged updater)
     * @param tokenId Token ID to upgrade
     * @param newTier New privilege tier
     */
    function upgradePrivilege(
        uint256 tokenId,
        uint8 newTier
    ) external {
        require(privilegeUpdaters[msg.sender] || msg.sender == owner(), "Not authorized");
        require(_ownerOf(tokenId) != address(0), "Token does not exist");
        require(metadata[tokenId].isActive, "Token not active");
        require(newTier <= 5, "Invalid tier");

        uint8 oldTier = metadata[tokenId].privilegeTier;
        require(newTier > oldTier, "Can only upgrade tier");

        metadata[tokenId].privilegeTier = newTier;
        metadata[tokenId].lastTierChange = block.timestamp;

        emit PrivilegeUpgraded(tokenId, oldTier, newTier);
    }

    /**
     * @dev Downgrade privilege tier (called when stake is reduced)
     * @param tokenId Token ID to downgrade
     * @param newTier New privilege tier
     */
    function downgradePrivilege(
        uint256 tokenId,
        uint8 newTier
    ) external {
        require(privilegeUpdaters[msg.sender] || msg.sender == owner(), "Not authorized");
        require(_ownerOf(tokenId) != address(0), "Token does not exist");
        require(metadata[tokenId].isActive, "Token not active");

        uint8 oldTier = metadata[tokenId].privilegeTier;
        require(newTier < oldTier, "Can only downgrade tier");

        metadata[tokenId].privilegeTier = newTier;
        metadata[tokenId].lastTierChange = block.timestamp;

        emit PrivilegeDowngraded(tokenId, oldTier, newTier);
    }

    /**
     * @dev Update display name
     * @param tokenId Token ID to update
     * @param newName New display name
     */
    function updateDisplayName(
        uint256 tokenId,
        string memory newName
    ) external {
        require(ownerOf(tokenId) == msg.sender, "Not token owner");
        require(bytes(newName).length <= 32, "Name too long");
        require(metadata[tokenId].isActive, "Token not active");

        string memory oldName = metadata[tokenId].displayName;
        metadata[tokenId].displayName = newName;

        emit DisplayNameChanged(tokenId, oldName, newName);
    }

    /**
     * @dev Update governance score
     * @param tokenId Token ID to update
     * @param newScore New governance score
     */
    function updateGovernanceScore(
        uint256 tokenId,
        uint256 newScore
    ) external {
        require(privilegeUpdaters[msg.sender] || msg.sender == owner(), "Not authorized");
        require(_ownerOf(tokenId) != address(0), "Token does not exist");

        uint256 oldScore = metadata[tokenId].governanceScore;
        metadata[tokenId].governanceScore = newScore;

        emit GovernanceScoreUpdated(tokenId, oldScore, newScore);
    }

    /**
     * @dev Revoke an AscendancyID (burn)
     * @param tokenId Token ID to revoke
     * @param reason Revocation reason
     */
    function revoke(
        uint256 tokenId,
        RevocationReason reason
    ) external {
        address tokenOwner = ownerOf(tokenId);
        
        // Only owner can revoke their own token, or admin/governance for violations
        if (reason == RevocationReason.UserRequest) {
            require(tokenOwner == msg.sender, "Only owner can request revocation");
        } else {
            require(msg.sender == owner() || privilegeUpdaters[msg.sender], "Not authorized");
        }

        // Clear tracking
        hasAscendancyId[tokenOwner] = false;
        delete addressToTokenId[tokenOwner];

        // Burn the token
        _burn(tokenId);

        emit AscendancyIDRevoked(tokenId, tokenOwner, reason);
    }

    /**
     * @dev Get privilege level for a token
     * @param tokenId Token ID to check
     * @return Current privilege tier
     */
    function getPrivilegeLevel(uint256 tokenId) external view returns (uint8) {
        require(_ownerOf(tokenId) != address(0), "Token does not exist");
        return metadata[tokenId].privilegeTier;
    }

    /**
     * @dev Get privilege level for an address
     * @param user Address to check
     * @return Current privilege tier (0 if no AscendancyID)
     */
    function getPrivilegeLevelByAddress(address user) external view returns (uint8) {
        if (!hasAscendancyId[user]) {
            return 0;
        }
        return metadata[addressToTokenId[user]].privilegeTier;
    }

    /**
     * @dev Get full metadata for a token
     * @param tokenId Token ID to check
     * @return AscendancyMetadata struct
     */
    function getMetadata(uint256 tokenId) external view returns (AscendancyMetadata memory) {
        require(_ownerOf(tokenId) != address(0), "Token does not exist");
        return metadata[tokenId];
    }

    /**
     * @dev Get token ID for an address
     * @param user Address to check
     * @return Token ID (0 if none)
     */
    function getTokenId(address user) external view returns (uint256) {
        require(hasAscendancyId[user], "No AscendancyID");
        return addressToTokenId[user];
    }

    /**
     * @dev Total supply of minted tokens
     * @return Total number of tokens minted
     */
    function totalSupply() external view returns (uint256) {
        return _tokenIdCounter;
    }

    /**
     * @dev Check if token exists
     * @param tokenId Token ID to check
     */
    function exists(uint256 tokenId) external view returns (bool) {
        return _ownerOf(tokenId) != address(0);
    }

    // Internal helper to get staked tier from staking contract
    function _getStakedTier(address user) internal view returns (uint8) {
        if (stakingContract == address(0)) {
            return 0;
        }
        // Call staking contract to get tier
        (bool success, bytes memory data) = stakingContract.staticcall(
            abi.encodeWithSignature("getCurrentTier(address)", user)
        );
        if (success && data.length >= 32) {
            return uint8(abi.decode(data, (uint256)));
        }
        return 0;
    }

    // ========== SOULBOUND RESTRICTIONS ==========
    // Override transfer functions to make token soulbound (non-transferable)

    /**
     * @dev Override transferFrom to prevent transfers
     */
    function transferFrom(
        address,
        address,
        uint256
    ) public pure override(ERC721, IERC721) {
        revert("AscendancyID: Soulbound token cannot be transferred");
    }

    /**
     * @dev Override safeTransferFrom to prevent transfers
     */
    function safeTransferFrom(
        address,
        address,
        uint256,
        bytes memory
    ) public pure override(ERC721, IERC721) {
        revert("AscendancyID: Soulbound token cannot be transferred");
    }

    /**
     * @dev Override approve to prevent approvals
     */
    function approve(address, uint256) public pure override(ERC721, IERC721) {
        revert("AscendancyID: Soulbound token cannot be approved");
    }

    /**
     * @dev Override setApprovalForAll to prevent approvals
     */
    function setApprovalForAll(address, bool) public pure override(ERC721, IERC721) {
        revert("AscendancyID: Soulbound token cannot be approved");
    }

    // ========== ADMIN FUNCTIONS ==========

    /**
     * @dev Set staking contract address
     * @param newContract New staking contract address
     */
    function setStakingContract(address newContract) external onlyOwner {
        address oldContract = stakingContract;
        stakingContract = newContract;
        
        // Auto-authorize staking contract as privilege updater
        if (newContract != address(0)) {
            privilegeUpdaters[newContract] = true;
        }
        
        emit StakingContractUpdated(oldContract, newContract);
    }

    /**
     * @dev Set privilege updater authorization
     * @param updater Address to authorize/deauthorize
     * @param authorized Whether to authorize
     */
    function setPrivilegeUpdater(address updater, bool authorized) external onlyOwner {
        privilegeUpdaters[updater] = authorized;
        emit PrivilegeUpdaterSet(updater, authorized);
    }

    /**
     * @dev Update treasury address
     * @param newTreasury New treasury address
     */
    function setTreasury(address newTreasury) external onlyOwner {
        require(newTreasury != address(0), "Invalid treasury");
        address oldTreasury = treasury;
        treasury = newTreasury;
        emit TreasuryUpdated(oldTreasury, newTreasury);
    }

    /**
     * @dev Update mint fee for a tier
     * @param tier Tier to update
     * @param fee New fee in wei
     */
    function setMintFee(uint8 tier, uint256 fee) external onlyOwner {
        require(tier <= 5, "Invalid tier");
        uint256 oldFee = mintFees[tier];
        mintFees[tier] = fee;
        emit MintFeeUpdated(tier, oldFee, fee);
    }

    /**
     * @dev Pause minting
     */
    function pause() external onlyOwner {
        _pause();
    }

    /**
     * @dev Unpause minting
     */
    function unpause() external onlyOwner {
        _unpause();
    }

    /**
     * @dev Set token URI
     * @param tokenId Token ID
     * @param uri New URI
     */
    function setTokenURI(uint256 tokenId, string memory uri) external onlyOwner {
        _setTokenURI(tokenId, uri);
    }

    // ========== REQUIRED OVERRIDES ==========

    function tokenURI(uint256 tokenId)
        public
        view
        override(ERC721, ERC721URIStorage)
        returns (string memory)
    {
        return super.tokenURI(tokenId);
    }

    function supportsInterface(bytes4 interfaceId)
        public
        view
        override(ERC721, ERC721URIStorage)
        returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }
}
