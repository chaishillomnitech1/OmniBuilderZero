// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Royalty.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";

/**
 * @title ScrollVerseNFT
 * @dev NFT Collection for ScrollVerse ecosystem with treasury monitoring and real-time royalty computation
 * @notice Deployed on Scroll Sepolia network with passive income conversion integration
 */
contract ScrollVerseNFT is ERC721, ERC721URIStorage, ERC721Royalty, Ownable, ReentrancyGuard {
    // Token ID counter
    uint256 private _tokenIdCounter;
    
    // ScrollVerse Deployment Timestamp - Protocol Marker
    uint256 public immutable scrollVerseDeploymentTimestamp;
    
    // Treasury address for royalty collection
    address public treasuryAddress;
    
    // Royalty percentage (in basis points, e.g., 1000 = 10%)
    uint96 public constant ROYALTY_BASIS_POINTS = 1000; // 10%
    
    // Passive Income Conversion Rate (in basis points)
    uint96 public passiveIncomeRate;
    
    // SCCC Certifier authorized addresses
    mapping(address => bool) public certifierAuthorized;
    
    // Frequency Forge activation status
    bool public frequencyForgeActive;
    
    // Geometry activation levels
    mapping(uint256 => uint8) public geometryActivationLevel;
    
    // ScrollVerse asset structure
    struct ScrollVerseAsset {
        string title;
        string creator;
        uint256 catalogNumber;
        uint256 creationTimestamp;
        string metadataURI;
        uint8 geometryType; // 0: Sacred, 1: Harmonic, 2: Fractal, 3: Divine
        bool isActive;
    }
    
    mapping(uint256 => ScrollVerseAsset) public scrollVerseAssets;
    
    // Treasury monitoring data
    struct TreasuryMetrics {
        uint256 totalRoyaltiesAccrued;
        uint256 lastUpdateTimestamp;
        uint256 transactionCount;
    }
    
    TreasuryMetrics public treasuryMetrics;
    
    // Events
    event ScrollVerseAssetMinted(
        uint256 indexed tokenId,
        address indexed recipient,
        string title,
        uint256 catalogNumber,
        uint8 geometryType
    );
    
    event CertifierAuthorized(address indexed account, bool authorized);
    event TreasuryUpdated(address indexed oldTreasury, address indexed newTreasury);
    event FrequencyForgeActivated(bool active);
    event GeometryActivated(uint256 indexed tokenId, uint8 level);
    event PassiveIncomeRateUpdated(uint96 oldRate, uint96 newRate);
    event RoyaltyAccrued(uint256 indexed tokenId, uint256 amount, uint256 timestamp);
    
    /**
     * @dev Constructor sets up the NFT collection with ScrollVerse parameters
     * @param _treasuryAddress Address of the treasury for royalty collection
     */
    constructor(address _treasuryAddress) ERC721("ScrollVerse Genesis Collection", "SVGC") Ownable(msg.sender) {
        require(_treasuryAddress != address(0), "Invalid treasury address");
        
        // Set ScrollVerse Deployment Timestamp as protocol marker
        scrollVerseDeploymentTimestamp = block.timestamp;
        
        // Initialize treasury
        treasuryAddress = _treasuryAddress;
        
        // Set default royalty to treasury
        _setDefaultRoyalty(_treasuryAddress, ROYALTY_BASIS_POINTS);
        
        // Initialize passive income rate at 5%
        passiveIncomeRate = 500;
        
        // Authorize contract deployer as first certifier
        certifierAuthorized[msg.sender] = true;
        emit CertifierAuthorized(msg.sender, true);
        
        // Activate Frequency Forge
        frequencyForgeActive = true;
        emit FrequencyForgeActivated(true);
        
        // Initialize treasury metrics
        treasuryMetrics = TreasuryMetrics({
            totalRoyaltiesAccrued: 0,
            lastUpdateTimestamp: block.timestamp,
            transactionCount: 0
        });
    }
    
    /**
     * @dev Mints a new ScrollVerse asset NFT
     * @param recipient Address to receive the NFT
     * @param title Title of the asset
     * @param creator Creator name
     * @param catalogNumber Catalog number
     * @param metadataURI Metadata URI (IPFS/Arweave)
     * @param geometryType Type of geometry activation
     */
    function mintScrollVerseAsset(
        address recipient,
        string memory title,
        string memory creator,
        uint256 catalogNumber,
        string memory metadataURI,
        uint8 geometryType
    ) public onlyOwner returns (uint256) {
        require(recipient != address(0), "Invalid recipient");
        require(bytes(title).length > 0, "Title required");
        require(bytes(metadataURI).length > 0, "Metadata URI required");
        require(geometryType <= 3, "Invalid geometry type");
        
        uint256 tokenId = _tokenIdCounter;
        _tokenIdCounter++;
        
        // Mint the NFT
        _safeMint(recipient, tokenId);
        
        // Set token URI
        _setTokenURI(tokenId, metadataURI);
        
        // Store ScrollVerse asset data
        scrollVerseAssets[tokenId] = ScrollVerseAsset({
            title: title,
            creator: creator,
            catalogNumber: catalogNumber,
            creationTimestamp: block.timestamp,
            metadataURI: metadataURI,
            geometryType: geometryType,
            isActive: true
        });
        
        // Initialize geometry activation
        geometryActivationLevel[tokenId] = 1;
        
        // Set royalty for this token
        _setTokenRoyalty(tokenId, treasuryAddress, ROYALTY_BASIS_POINTS);
        
        emit ScrollVerseAssetMinted(tokenId, recipient, title, catalogNumber, geometryType);
        emit GeometryActivated(tokenId, 1);
        
        return tokenId;
    }
    
    /**
     * @dev Batch mint multiple ScrollVerse assets
     */
    function batchMintScrollVerseAssets(
        address[] memory recipients,
        string[] memory titles,
        string[] memory creators,
        uint256[] memory catalogNumbers,
        string[] memory metadataURIs,
        uint8[] memory geometryTypes
    ) external onlyOwner returns (uint256[] memory) {
        require(recipients.length == titles.length, "Array length mismatch");
        require(recipients.length == creators.length, "Array length mismatch");
        require(recipients.length == catalogNumbers.length, "Array length mismatch");
        require(recipients.length == metadataURIs.length, "Array length mismatch");
        require(recipients.length == geometryTypes.length, "Array length mismatch");
        
        uint256[] memory tokenIds = new uint256[](recipients.length);
        
        for (uint256 i = 0; i < recipients.length; i++) {
            tokenIds[i] = mintScrollVerseAsset(
                recipients[i],
                titles[i],
                creators[i],
                catalogNumbers[i],
                metadataURIs[i],
                geometryTypes[i]
            );
        }
        
        return tokenIds;
    }
    
    /**
     * @dev Activate geometry for a token (SCCC Certifier function)
     * @param tokenId Token ID
     * @param level Activation level (1-10)
     */
    function activateGeometry(uint256 tokenId, uint8 level) external {
        require(certifierAuthorized[msg.sender], "Not authorized certifier");
        require(_ownerOf(tokenId) != address(0), "Token does not exist");
        require(level > 0 && level <= 10, "Invalid activation level");
        
        geometryActivationLevel[tokenId] = level;
        emit GeometryActivated(tokenId, level);
    }
    
    /**
     * @dev Authorize or deauthorize a SCCC certifier
     * @param account Address to modify authorization
     * @param authorized Authorization status
     */
    function setCertifierAuthorization(address account, bool authorized) external onlyOwner {
        require(account != address(0), "Invalid address");
        certifierAuthorized[account] = authorized;
        emit CertifierAuthorized(account, authorized);
    }
    
    /**
     * @dev Update treasury address
     * @param newTreasury New treasury address
     */
    function updateTreasury(address newTreasury) external onlyOwner {
        require(newTreasury != address(0), "Invalid treasury address");
        address oldTreasury = treasuryAddress;
        treasuryAddress = newTreasury;
        
        // Update default royalty recipient
        _setDefaultRoyalty(newTreasury, ROYALTY_BASIS_POINTS);
        
        emit TreasuryUpdated(oldTreasury, newTreasury);
    }
    
    /**
     * @dev Update passive income rate
     * @param newRate New rate in basis points
     */
    function updatePassiveIncomeRate(uint96 newRate) external onlyOwner {
        require(newRate <= 10000, "Rate cannot exceed 100%");
        uint96 oldRate = passiveIncomeRate;
        passiveIncomeRate = newRate;
        emit PassiveIncomeRateUpdated(oldRate, newRate);
    }
    
    /**
     * @dev Toggle Frequency Forge activation
     */
    function toggleFrequencyForge() external onlyOwner {
        frequencyForgeActive = !frequencyForgeActive;
        emit FrequencyForgeActivated(frequencyForgeActive);
    }
    
    /**
     * @dev Record royalty accrual (called by external royalty handler)
     * @param tokenId Token ID
     * @param amount Royalty amount in wei
     * @notice Only authorized certifiers or owner can call this function.
     * This is used for off-chain royalty tracking integration. The amount is
     * not validated on-chain as royalties are collected through marketplace
     * mechanisms (EIP-2981) rather than through this contract directly.
     */
    function recordRoyaltyAccrual(uint256 tokenId, uint256 amount) external {
        require(certifierAuthorized[msg.sender] || msg.sender == owner(), "Not authorized");
        require(amount > 0, "Amount must be greater than zero");
        
        treasuryMetrics.totalRoyaltiesAccrued += amount;
        treasuryMetrics.lastUpdateTimestamp = block.timestamp;
        treasuryMetrics.transactionCount++;
        
        emit RoyaltyAccrued(tokenId, amount, block.timestamp);
    }
    
    /**
     * @dev Get ScrollVerse asset details
     * @param tokenId Token ID
     */
    function getScrollVerseAsset(uint256 tokenId) external view returns (ScrollVerseAsset memory) {
        require(_ownerOf(tokenId) != address(0), "Token does not exist");
        return scrollVerseAssets[tokenId];
    }
    
    /**
     * @dev Get total number of minted tokens
     * @notice Returns the count of tokens that have been minted.
     * This contract does not implement a burn function, so this
     * value represents both minted and currently existing tokens.
     */
    function totalSupply() external view returns (uint256) {
        return _tokenIdCounter;
    }
    
    /**
     * @dev Calculate time elapsed since ScrollVerse deployment
     */
    function getElapsedTime() external view returns (uint256) {
        return block.timestamp - scrollVerseDeploymentTimestamp;
    }
    
    /**
     * @dev Get treasury metrics
     */
    function getTreasuryMetrics() external view returns (
        uint256 totalRoyalties,
        uint256 lastUpdate,
        uint256 txCount
    ) {
        return (
            treasuryMetrics.totalRoyaltiesAccrued,
            treasuryMetrics.lastUpdateTimestamp,
            treasuryMetrics.transactionCount
        );
    }
    
    /**
     * @dev Compute real-time royalty for a sale
     * @param salePrice Sale price in wei
     * @return Royalty amount in wei (10% of sale price)
     */
    function computeRoyalty(uint256 salePrice) external pure returns (uint256) {
        return (salePrice * ROYALTY_BASIS_POINTS) / 10000;
    }
    
    /**
     * @dev Compute passive income for a token based on its geometry level
     * @param tokenId Token ID
     * @param baseValue Base value for computation (in wei)
     * @return Passive income amount in wei
     * @notice Calculation: (baseValue * passiveIncomeRate * level) / 10000
     * Solidity 0.8+ provides built-in overflow protection.
     */
    function computePassiveIncome(uint256 tokenId, uint256 baseValue) external view returns (uint256) {
        require(_ownerOf(tokenId) != address(0), "Token does not exist");
        uint8 level = geometryActivationLevel[tokenId];
        return (baseValue * passiveIncomeRate * level) / 10000;
    }
    
    /**
     * @dev Check if token exists
     * @param tokenId Token ID to check
     */
    function exists(uint256 tokenId) external view returns (bool) {
        return _ownerOf(tokenId) != address(0);
    }
    
    // Required overrides
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
        override(ERC721, ERC721URIStorage, ERC721Royalty)
        returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }
}
