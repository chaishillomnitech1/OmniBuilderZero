// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Royalty.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";

/**
 * @title PreciousMetalBridge
 * @dev NFT contract for bridging physical precious metals (gold, silver, platinum) to digital assets
 * @notice Aligned with ScrollVerse values of PERMANENCE, DIVINITY, and WORTH
 * 
 * PERMANENCE: Immutable on-chain provenance tracking for eternal record
 * DIVINITY: Sacred certification protocols with multi-authority verification
 * WORTH: Real-world asset backing with transparent valuation
 */
contract PreciousMetalBridge is ERC721, ERC721URIStorage, ERC721Royalty, Ownable, ReentrancyGuard {
    
    // ============ CONSTANTS ============
    
    /// @notice Royalty basis points (1000 = 10%)
    uint96 public constant ROYALTY_BASIS_POINTS = 500; // 5% royalty for physical asset bridge
    
    // ============ STATE VARIABLES ============
    
    /// @notice Token ID counter
    uint256 private _tokenIdCounter;
    
    /// @notice Bridge deployment timestamp - Divine Marker
    uint256 public immutable bridgeDeploymentTimestamp;
    
    /// @notice Treasury address for royalty collection
    address public treasuryAddress;
    
    /// @notice Metal types supported
    enum MetalType { GOLD, SILVER, PLATINUM, PALLADIUM }
    
    /// @notice Purity grades (in parts per thousand)
    /// 999 = 99.9% pure, 995 = 99.5% pure, etc.
    
    /// @notice Certification status
    enum CertificationStatus { PENDING, CERTIFIED, SUSPENDED, REVOKED }
    
    /// @notice Asset storage type for metadata
    enum StorageType { IPFS, ARWEAVE }
    
    /// @notice Physical asset vault locations
    enum VaultLocation { 
        ZURICH,      // Switzerland - traditional gold hub
        SINGAPORE,   // Asia Pacific hub
        DUBAI,       // Middle East hub
        LONDON,      // Traditional bullion market
        NEW_YORK,    // Americas hub
        HONG_KONG    // East Asia hub
    }
    
    /**
     * @notice Encrypted asset data structure
     * @dev Core structure for physical-to-digital bridge with ScrollVerse values
     */
    struct PreciousMetalAsset {
        // === PERMANENCE: Immutable identifiers ===
        bytes32 physicalAssetHash;      // Cryptographic hash of physical asset ID
        bytes32 serialNumberHash;       // Encrypted serial number
        uint256 mintTimestamp;          // Eternal record of creation
        
        // === DIVINITY: Sacred certification ===
        address certifier;              // Authorized certifier address
        CertificationStatus status;     // Current certification status
        uint256 certificationTimestamp; // When certification was granted
        bytes32 certificationProof;     // Cryptographic proof of certification
        
        // === WORTH: Real value backing ===
        MetalType metalType;            // Type of precious metal
        uint256 weightInGrams;          // Weight in grams (precision: 3 decimals via 1000x)
        uint256 purityInThousandths;    // Purity in parts per thousand (e.g., 999 = 99.9%)
        uint256 valuationTimestamp;     // Last valuation timestamp
        uint256 valuationInWei;         // Last valuation in Wei
        
        // === METADATA ===
        string metadataURI;             // IPFS/Arweave URI for extended metadata
        StorageType storageType;        // Type of decentralized storage
        VaultLocation vaultLocation;    // Physical storage location
    }
    
    /**
     * @notice Provenance record for tracking asset history
     */
    struct ProvenanceRecord {
        uint256 timestamp;
        address actor;
        bytes32 actionHash;
        string description;
    }
    
    // ============ MAPPINGS ============
    
    /// @notice Token ID to asset data
    mapping(uint256 => PreciousMetalAsset) public preciousAssets;
    
    /// @notice Token ID to provenance history
    mapping(uint256 => ProvenanceRecord[]) private provenanceHistory;
    
    /// @notice Authorized certifiers
    mapping(address => bool) public authorizedCertifiers;
    
    /// @notice Authorized vault operators
    mapping(address => bool) public authorizedVaultOperators;
    
    /// @notice Physical asset hash to token ID (prevents duplicate minting)
    mapping(bytes32 => uint256) public assetHashToTokenId;
    
    /// @notice Certifier to certification count (for reputation tracking)
    mapping(address => uint256) public certifierCertificationCount;
    
    // ============ EVENTS ============
    
    event PreciousMetalMinted(
        uint256 indexed tokenId,
        address indexed recipient,
        MetalType metalType,
        uint256 weightInGrams,
        uint256 purityInThousandths,
        VaultLocation vaultLocation
    );
    
    event AssetCertified(
        uint256 indexed tokenId,
        address indexed certifier,
        bytes32 certificationProof,
        uint256 timestamp
    );
    
    event CertificationStatusChanged(
        uint256 indexed tokenId,
        CertificationStatus oldStatus,
        CertificationStatus newStatus,
        address indexed changedBy
    );
    
    event ValuationUpdated(
        uint256 indexed tokenId,
        uint256 oldValuation,
        uint256 newValuation,
        uint256 timestamp
    );
    
    event ProvenanceRecorded(
        uint256 indexed tokenId,
        address indexed actor,
        bytes32 actionHash,
        uint256 timestamp
    );
    
    event CertifierAuthorized(address indexed account, bool authorized);
    event VaultOperatorAuthorized(address indexed account, bool authorized);
    event TreasuryUpdated(address indexed oldTreasury, address indexed newTreasury);
    
    // ============ MODIFIERS ============
    
    modifier onlyCertifier() {
        require(authorizedCertifiers[msg.sender], "Not authorized certifier");
        _;
    }
    
    modifier onlyVaultOperator() {
        require(authorizedVaultOperators[msg.sender], "Not authorized vault operator");
        _;
    }
    
    modifier tokenExists(uint256 tokenId) {
        require(_ownerOf(tokenId) != address(0), "Token does not exist");
        _;
    }
    
    // ============ CONSTRUCTOR ============
    
    /**
     * @notice Deploy the Precious Metal Bridge contract
     * @param _treasuryAddress Address for royalty collection
     */
    constructor(address _treasuryAddress) 
        ERC721("ScrollVerse Precious Metal Bridge", "SPMB") 
        Ownable(msg.sender) 
    {
        require(_treasuryAddress != address(0), "Invalid treasury address");
        
        // Set deployment timestamp as divine marker
        bridgeDeploymentTimestamp = block.timestamp;
        
        // Initialize treasury
        treasuryAddress = _treasuryAddress;
        
        // Set default royalty
        _setDefaultRoyalty(_treasuryAddress, ROYALTY_BASIS_POINTS);
        
        // Authorize deployer as initial certifier and vault operator
        authorizedCertifiers[msg.sender] = true;
        authorizedVaultOperators[msg.sender] = true;
        
        emit CertifierAuthorized(msg.sender, true);
        emit VaultOperatorAuthorized(msg.sender, true);
    }
    
    // ============ CORE MINTING FUNCTIONS ============
    
    /**
     * @notice Mint a new precious metal NFT
     * @dev Creates an encrypted bridge between physical metal and digital token
     * @param recipient Address to receive the NFT
     * @param physicalAssetHash Cryptographic hash of physical asset identifier
     * @param serialNumberHash Encrypted serial number hash
     * @param metalType Type of precious metal
     * @param weightInGrams Weight in grams (use 1000x for 3 decimal precision)
     * @param purityInThousandths Purity in parts per thousand
     * @param metadataURI IPFS/Arweave URI for extended metadata
     * @param storageType Type of decentralized storage
     * @param vaultLocation Physical storage location
     */
    function mintPreciousMetal(
        address recipient,
        bytes32 physicalAssetHash,
        bytes32 serialNumberHash,
        MetalType metalType,
        uint256 weightInGrams,
        uint256 purityInThousandths,
        string memory metadataURI,
        StorageType storageType,
        VaultLocation vaultLocation
    ) public onlyOwner returns (uint256) {
        require(recipient != address(0), "Invalid recipient");
        require(physicalAssetHash != bytes32(0), "Physical asset hash required");
        require(assetHashToTokenId[physicalAssetHash] == 0 || assetHashToTokenId[physicalAssetHash] == type(uint256).max, 
            "Asset already tokenized");
        require(weightInGrams > 0, "Weight must be greater than zero");
        require(purityInThousandths > 0 && purityInThousandths <= 1000, "Invalid purity");
        require(bytes(metadataURI).length > 0, "Metadata URI required");
        
        uint256 tokenId = _tokenIdCounter;
        _tokenIdCounter++;
        
        // Mint the NFT
        _safeMint(recipient, tokenId);
        
        // Set token URI
        _setTokenURI(tokenId, metadataURI);
        
        // Store asset data with ScrollVerse values
        preciousAssets[tokenId] = PreciousMetalAsset({
            // PERMANENCE
            physicalAssetHash: physicalAssetHash,
            serialNumberHash: serialNumberHash,
            mintTimestamp: block.timestamp,
            // DIVINITY
            certifier: address(0),
            status: CertificationStatus.PENDING,
            certificationTimestamp: 0,
            certificationProof: bytes32(0),
            // WORTH
            metalType: metalType,
            weightInGrams: weightInGrams,
            purityInThousandths: purityInThousandths,
            valuationTimestamp: 0,
            valuationInWei: 0,
            // METADATA
            metadataURI: metadataURI,
            storageType: storageType,
            vaultLocation: vaultLocation
        });
        
        // Map asset hash to token ID (prevent duplicate minting)
        assetHashToTokenId[physicalAssetHash] = tokenId + 1; // +1 to distinguish from default 0
        
        // Set royalty for this token
        _setTokenRoyalty(tokenId, treasuryAddress, ROYALTY_BASIS_POINTS);
        
        // Record initial provenance
        _recordProvenance(
            tokenId,
            msg.sender,
            keccak256(abi.encodePacked("MINT", block.timestamp)),
            "Asset minted and bridged to ScrollVerse"
        );
        
        emit PreciousMetalMinted(
            tokenId,
            recipient,
            metalType,
            weightInGrams,
            purityInThousandths,
            vaultLocation
        );
        
        return tokenId;
    }
    
    // ============ CERTIFICATION FUNCTIONS (DIVINITY) ============
    
    /**
     * @notice Certify a precious metal asset
     * @dev Authorized certifier validates the physical-to-digital bridge
     * @param tokenId Token ID to certify
     * @param certificationProof Cryptographic proof of physical asset verification
     */
    function certifyAsset(uint256 tokenId, bytes32 certificationProof) 
        external 
        onlyCertifier 
        tokenExists(tokenId) 
        nonReentrant 
    {
        PreciousMetalAsset storage asset = preciousAssets[tokenId];
        require(asset.status == CertificationStatus.PENDING, "Asset not pending certification");
        require(certificationProof != bytes32(0), "Certification proof required");
        
        CertificationStatus oldStatus = asset.status;
        
        asset.certifier = msg.sender;
        asset.status = CertificationStatus.CERTIFIED;
        asset.certificationTimestamp = block.timestamp;
        asset.certificationProof = certificationProof;
        
        certifierCertificationCount[msg.sender]++;
        
        // Record provenance
        _recordProvenance(
            tokenId,
            msg.sender,
            keccak256(abi.encodePacked("CERTIFY", certificationProof)),
            "Asset certified by authorized certifier"
        );
        
        emit AssetCertified(tokenId, msg.sender, certificationProof, block.timestamp);
        emit CertificationStatusChanged(tokenId, oldStatus, CertificationStatus.CERTIFIED, msg.sender);
    }
    
    /**
     * @notice Update certification status
     * @dev Used to suspend or revoke certifications
     * @param tokenId Token ID
     * @param newStatus New certification status
     */
    function updateCertificationStatus(uint256 tokenId, CertificationStatus newStatus) 
        external 
        onlyCertifier 
        tokenExists(tokenId) 
    {
        PreciousMetalAsset storage asset = preciousAssets[tokenId];
        require(newStatus != CertificationStatus.PENDING, "Cannot revert to pending");
        
        CertificationStatus oldStatus = asset.status;
        asset.status = newStatus;
        
        // Record provenance
        _recordProvenance(
            tokenId,
            msg.sender,
            keccak256(abi.encodePacked("STATUS_CHANGE", uint8(oldStatus), uint8(newStatus))),
            "Certification status updated"
        );
        
        emit CertificationStatusChanged(tokenId, oldStatus, newStatus, msg.sender);
    }
    
    // ============ VALUATION FUNCTIONS (WORTH) ============
    
    /**
     * @notice Update asset valuation
     * @dev Vault operators update the valuation based on market prices
     * @param tokenId Token ID
     * @param newValuationInWei New valuation in Wei
     */
    function updateValuation(uint256 tokenId, uint256 newValuationInWei) 
        external 
        onlyVaultOperator 
        tokenExists(tokenId) 
    {
        PreciousMetalAsset storage asset = preciousAssets[tokenId];
        uint256 oldValuation = asset.valuationInWei;
        
        asset.valuationInWei = newValuationInWei;
        asset.valuationTimestamp = block.timestamp;
        
        // Record provenance
        _recordProvenance(
            tokenId,
            msg.sender,
            keccak256(abi.encodePacked("VALUATION", oldValuation, newValuationInWei)),
            "Asset valuation updated"
        );
        
        emit ValuationUpdated(tokenId, oldValuation, newValuationInWei, block.timestamp);
    }
    
    // ============ PROVENANCE FUNCTIONS (PERMANENCE) ============
    
    /**
     * @notice Internal function to record provenance
     */
    function _recordProvenance(
        uint256 tokenId,
        address actor,
        bytes32 actionHash,
        string memory description
    ) internal {
        provenanceHistory[tokenId].push(ProvenanceRecord({
            timestamp: block.timestamp,
            actor: actor,
            actionHash: actionHash,
            description: description
        }));
        
        emit ProvenanceRecorded(tokenId, actor, actionHash, block.timestamp);
    }
    
    /**
     * @notice Get provenance history for a token
     * @param tokenId Token ID
     * @return Array of provenance records
     */
    function getProvenanceHistory(uint256 tokenId) 
        external 
        view 
        tokenExists(tokenId) 
        returns (ProvenanceRecord[] memory) 
    {
        return provenanceHistory[tokenId];
    }
    
    /**
     * @notice Get provenance count for a token
     * @param tokenId Token ID
     * @return Number of provenance records
     */
    function getProvenanceCount(uint256 tokenId) 
        external 
        view 
        tokenExists(tokenId) 
        returns (uint256) 
    {
        return provenanceHistory[tokenId].length;
    }
    
    // ============ ADMIN FUNCTIONS ============
    
    /**
     * @notice Authorize or deauthorize a certifier
     * @param account Address to modify
     * @param authorized Authorization status
     */
    function setCertifierAuthorization(address account, bool authorized) external onlyOwner {
        require(account != address(0), "Invalid address");
        authorizedCertifiers[account] = authorized;
        emit CertifierAuthorized(account, authorized);
    }
    
    /**
     * @notice Authorize or deauthorize a vault operator
     * @param account Address to modify
     * @param authorized Authorization status
     */
    function setVaultOperatorAuthorization(address account, bool authorized) external onlyOwner {
        require(account != address(0), "Invalid address");
        authorizedVaultOperators[account] = authorized;
        emit VaultOperatorAuthorized(account, authorized);
    }
    
    /**
     * @notice Update treasury address
     * @param newTreasury New treasury address
     */
    function updateTreasury(address newTreasury) external onlyOwner {
        require(newTreasury != address(0), "Invalid treasury address");
        address oldTreasury = treasuryAddress;
        treasuryAddress = newTreasury;
        _setDefaultRoyalty(newTreasury, ROYALTY_BASIS_POINTS);
        emit TreasuryUpdated(oldTreasury, newTreasury);
    }
    
    // ============ VIEW FUNCTIONS ============
    
    /**
     * @notice Get precious metal asset details
     * @param tokenId Token ID
     * @return Asset data structure
     */
    function getPreciousAsset(uint256 tokenId) 
        external 
        view 
        tokenExists(tokenId) 
        returns (PreciousMetalAsset memory) 
    {
        return preciousAssets[tokenId];
    }
    
    /**
     * @notice Get total number of minted tokens
     */
    function totalSupply() external view returns (uint256) {
        return _tokenIdCounter;
    }
    
    /**
     * @notice Calculate time elapsed since bridge deployment
     */
    function getElapsedTime() external view returns (uint256) {
        return block.timestamp - bridgeDeploymentTimestamp;
    }
    
    /**
     * @notice Check if a physical asset has been tokenized
     * @param physicalAssetHash Hash of the physical asset
     * @return Boolean indicating if asset is tokenized
     */
    function isAssetTokenized(bytes32 physicalAssetHash) external view returns (bool) {
        return assetHashToTokenId[physicalAssetHash] != 0;
    }
    
    /**
     * @notice Get token ID for a physical asset hash
     * @param physicalAssetHash Hash of the physical asset
     * @return Token ID (returns max uint256 if not found)
     */
    function getTokenIdByAssetHash(bytes32 physicalAssetHash) external view returns (uint256) {
        uint256 storedValue = assetHashToTokenId[physicalAssetHash];
        if (storedValue == 0) {
            return type(uint256).max; // Not found
        }
        return storedValue - 1; // Subtract 1 to get actual token ID
    }
    
    /**
     * @notice Compute the pure metal content in grams
     * @param tokenId Token ID
     * @return Pure metal weight in grams
     */
    function computePureMetalWeight(uint256 tokenId) 
        external 
        view 
        tokenExists(tokenId) 
        returns (uint256) 
    {
        PreciousMetalAsset memory asset = preciousAssets[tokenId];
        return (asset.weightInGrams * asset.purityInThousandths) / 1000;
    }
    
    /**
     * @notice Check if token exists
     * @param tokenId Token ID to check
     */
    function exists(uint256 tokenId) external view returns (bool) {
        return _ownerOf(tokenId) != address(0);
    }
    
    // ============ REQUIRED OVERRIDES ============
    
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
