// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Royalty.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";

/**
 * @title Legacy of Light: Prophetic Omnichords
 * @dev Music NFT Collection for GOAT USB-Cassette OmniTapes Catalog
 * @notice This contract tokenizes the OmniTapes catalog with KUN Coin Treasury integration
 * and ARCHITEX ∞ OwnerOverride() functionality
 */
contract LegacyOfLightNFT is ERC721, ERC721URIStorage, ERC721Royalty, Ownable, ReentrancyGuard {
    // Token ID counter
    uint256 private _tokenIdCounter;
    
    // OTCP Deployment Timestamp - Divine Marker
    uint256 public immutable otcpDeploymentTimestamp;
    
    // KUN Coin Treasury address
    address public kunCoinTreasury;
    
    // Royalty percentage (in basis points, e.g., 1000 = 10%)
    uint96 public constant ROYALTY_BASIS_POINTS = 1000; // 10%
    
    // ARCHITEX ∞ Authorized addresses for OwnerOverride
    mapping(address => bool) public architexAuthorized;
    
    // Metadata storage type tracking
    enum StorageType { IPFS, Arweave }
    mapping(uint256 => StorageType) public tokenStorageType;
    
    // OmniTapes catalog tracking
    struct OmniTape {
        string title;
        string artist;
        uint256 catalogNumber;
        uint256 releaseDate;
        string storageURI; // IPFS or Arweave URI
        StorageType storageType;
    }
    
    mapping(uint256 => OmniTape) public omniTapes;
    
    // Events
    event OmniTapeMinted(
        uint256 indexed tokenId,
        address indexed recipient,
        string title,
        uint256 catalogNumber,
        StorageType storageType
    );
    
    event ArchitexAuthorized(address indexed account, bool authorized);
    event KunCoinTreasuryUpdated(address indexed oldTreasury, address indexed newTreasury);
    event OwnerOverrideExecuted(address indexed architex, uint256 indexed tokenId, address indexed newOwner);
    
    /**
     * @dev Constructor sets up the NFT collection with OTCP timestamp
     * @param _kunCoinTreasury Address of the KUN Coin Treasury
     */
    constructor(address _kunCoinTreasury) ERC721("Legacy of Light: Prophetic Omnichords", "LLPO") {
        require(_kunCoinTreasury != address(0), "Invalid treasury address");
        
        // Set OTCP Deployment Timestamp as divine marker
        otcpDeploymentTimestamp = block.timestamp;
        
        // Initialize KUN Coin Treasury
        kunCoinTreasury = _kunCoinTreasury;
        
        // Set default royalty to treasury
        _setDefaultRoyalty(_kunCoinTreasury, ROYALTY_BASIS_POINTS);
        
        // Authorize contract deployer as first ARCHITEX
        architexAuthorized[msg.sender] = true;
        emit ArchitexAuthorized(msg.sender, true);
    }
    
    /**
     * @dev Mints a new OmniTape NFT
     * @param recipient Address to receive the NFT
     * @param title Title of the music piece
     * @param artist Artist name
     * @param catalogNumber Catalog number in OmniTapes collection
     * @param releaseDate Original release timestamp
     * @param storageURI IPFS or Arweave URI
     * @param storageType Type of decentralized storage used
     */
    function mintOmniTape(
        address recipient,
        string memory title,
        string memory artist,
        uint256 catalogNumber,
        uint256 releaseDate,
        string memory storageURI,
        StorageType storageType
    ) public onlyOwner returns (uint256) {
        require(recipient != address(0), "Invalid recipient");
        require(bytes(title).length > 0, "Title required");
        require(bytes(storageURI).length > 0, "Storage URI required");
        
        uint256 tokenId = _tokenIdCounter;
        _tokenIdCounter++;
        
        // Mint the NFT
        _safeMint(recipient, tokenId);
        
        // Set token URI
        _setTokenURI(tokenId, storageURI);
        
        // Store OmniTape metadata
        omniTapes[tokenId] = OmniTape({
            title: title,
            artist: artist,
            catalogNumber: catalogNumber,
            releaseDate: releaseDate,
            storageURI: storageURI,
            storageType: storageType
        });
        
        // Track storage type
        tokenStorageType[tokenId] = storageType;
        
        // Set royalty for this token
        _setTokenRoyalty(tokenId, kunCoinTreasury, ROYALTY_BASIS_POINTS);
        
        emit OmniTapeMinted(tokenId, recipient, title, catalogNumber, storageType);
        
        return tokenId;
    }
    
    /**
     * @dev Batch mint multiple OmniTapes
     * @param recipients Array of recipient addresses
     * @param titles Array of titles
     * @param artists Array of artists
     * @param catalogNumbers Array of catalog numbers
     * @param releaseDates Array of release dates
     * @param storageURIs Array of storage URIs
     * @param storageTypes Array of storage types
     */
    function batchMintOmniTapes(
        address[] memory recipients,
        string[] memory titles,
        string[] memory artists,
        uint256[] memory catalogNumbers,
        uint256[] memory releaseDates,
        string[] memory storageURIs,
        StorageType[] memory storageTypes
    ) external onlyOwner returns (uint256[] memory) {
        require(recipients.length == titles.length, "Array length mismatch");
        require(recipients.length == artists.length, "Array length mismatch");
        require(recipients.length == catalogNumbers.length, "Array length mismatch");
        require(recipients.length == releaseDates.length, "Array length mismatch");
        require(recipients.length == storageURIs.length, "Array length mismatch");
        require(recipients.length == storageTypes.length, "Array length mismatch");
        
        uint256[] memory tokenIds = new uint256[](recipients.length);
        
        for (uint256 i = 0; i < recipients.length; i++) {
            tokenIds[i] = mintOmniTape(
                recipients[i],
                titles[i],
                artists[i],
                catalogNumbers[i],
                releaseDates[i],
                storageURIs[i],
                storageTypes[i]
            );
        }
        
        return tokenIds;
    }
    
    /**
     * @dev ARCHITEX ∞ OwnerOverride() - Divine authority to transfer tokens
     * @param tokenId Token ID to override
     * @param newOwner New owner address
     * @notice Only authorized ARCHITEX addresses can execute this
     */
    function ownerOverride(uint256 tokenId, address newOwner) external nonReentrant {
        require(architexAuthorized[msg.sender], "Not authorized ARCHITEX");
        require(_exists(tokenId), "Token does not exist");
        require(newOwner != address(0), "Invalid new owner");
        
        address currentOwner = ownerOf(tokenId);
        require(currentOwner != newOwner, "Already the owner");
        
        // Execute divine override transfer
        _transfer(currentOwner, newOwner, tokenId);
        
        emit OwnerOverrideExecuted(msg.sender, tokenId, newOwner);
    }
    
    /**
     * @dev Authorize or deauthorize an ARCHITEX address
     * @param account Address to modify authorization
     * @param authorized Authorization status
     */
    function setArchitexAuthorization(address account, bool authorized) external onlyOwner {
        require(account != address(0), "Invalid address");
        architexAuthorized[account] = authorized;
        emit ArchitexAuthorized(account, authorized);
    }
    
    /**
     * @dev Update KUN Coin Treasury address
     * @param newTreasury New treasury address
     */
    function updateKunCoinTreasury(address newTreasury) external onlyOwner {
        require(newTreasury != address(0), "Invalid treasury address");
        address oldTreasury = kunCoinTreasury;
        kunCoinTreasury = newTreasury;
        
        // Update default royalty recipient
        _setDefaultRoyalty(newTreasury, ROYALTY_BASIS_POINTS);
        
        emit KunCoinTreasuryUpdated(oldTreasury, newTreasury);
    }
    
    /**
     * @dev Get OmniTape metadata
     * @param tokenId Token ID
     */
    function getOmniTape(uint256 tokenId) external view returns (OmniTape memory) {
        require(_exists(tokenId), "Token does not exist");
        return omniTapes[tokenId];
    }
    
    /**
     * @dev Get total number of minted tokens
     */
    function totalSupply() external view returns (uint256) {
        return _tokenIdCounter;
    }
    
    /**
     * @dev Calculate time elapsed since OTCP deployment (divine marker)
     */
    function getOTCPElapsedTime() external view returns (uint256) {
        return block.timestamp - otcpDeploymentTimestamp;
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
    
    function _burn(uint256 tokenId) 
        internal 
        override(ERC721, ERC721URIStorage, ERC721Royalty) 
    {
        super._burn(tokenId);
    }
}
