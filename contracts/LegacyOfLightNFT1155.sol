// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC1155/ERC1155.sol";
import "@openzeppelin/contracts/token/ERC1155/extensions/ERC1155Supply.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/interfaces/IERC2981.sol";

/**
 * @title Legacy of Light: Prophetic Omnichords (ERC-1155 Multi-Edition)
 * @dev Music NFT Collection for GOAT USB-Cassette OmniTapes Catalog with multi-edition support
 * @notice ERC-1155 version allows multiple editions of the same OmniTape
 */
contract LegacyOfLightNFT1155 is ERC1155, ERC1155Supply, Ownable, ReentrancyGuard, IERC2981 {
    
    // Contract name and symbol
    string public name = "Legacy of Light: Prophetic Omnichords Multi-Edition";
    string public symbol = "LLPOME";
    
    // OTCP Deployment Timestamp - Divine Marker
    uint256 public immutable otcpDeploymentTimestamp;
    
    // KUN Coin Treasury address
    address public kunCoinTreasury;
    
    // Royalty percentage (in basis points, e.g., 1000 = 10%)
    uint96 public constant ROYALTY_BASIS_POINTS = 1000; // 10%
    
    // ARCHITEX ∞ Authorized addresses for OwnerOverride
    mapping(address => bool) public architexAuthorized;
    
    // Token ID counter for new OmniTapes
    uint256 private _currentTokenId;
    
    // Metadata storage type tracking
    enum StorageType { IPFS, Arweave }
    
    // OmniTapes catalog tracking
    struct OmniTape {
        string title;
        string artist;
        uint256 catalogNumber;
        uint256 releaseDate;
        string storageURI; // IPFS or Arweave URI
        StorageType storageType;
        uint256 maxSupply; // Maximum editions (0 = unlimited)
    }
    
    mapping(uint256 => OmniTape) public omniTapes;
    mapping(uint256 => string) private _tokenURIs;
    
    // Events
    event OmniTapeCreated(
        uint256 indexed tokenId,
        string title,
        uint256 catalogNumber,
        uint256 maxSupply,
        StorageType storageType
    );
    
    event OmniTapeMinted(
        uint256 indexed tokenId,
        address indexed recipient,
        uint256 amount
    );
    
    event ArchitexAuthorized(address indexed account, bool authorized);
    event KunCoinTreasuryUpdated(address indexed oldTreasury, address indexed newTreasury);
    event OwnerOverrideExecuted(address indexed architex, uint256 indexed tokenId, address indexed from, address to, uint256 amount);
    
    /**
     * @dev Constructor sets up the NFT collection with OTCP timestamp
     * @param _kunCoinTreasury Address of the KUN Coin Treasury
     * @param _baseURI Base URI for token metadata
     */
    constructor(address _kunCoinTreasury, string memory _baseURI) ERC1155(_baseURI) {
        require(_kunCoinTreasury != address(0), "Invalid treasury address");
        
        // Set OTCP Deployment Timestamp as divine marker
        otcpDeploymentTimestamp = block.timestamp;
        
        // Initialize KUN Coin Treasury
        kunCoinTreasury = _kunCoinTreasury;
        
        // Authorize contract deployer as first ARCHITEX
        architexAuthorized[msg.sender] = true;
        emit ArchitexAuthorized(msg.sender, true);
    }
    
    /**
     * @dev Creates a new OmniTape token type
     * @param title Title of the music piece
     * @param artist Artist name
     * @param catalogNumber Catalog number in OmniTapes collection
     * @param releaseDate Original release timestamp
     * @param storageURI IPFS or Arweave URI
     * @param storageType Type of decentralized storage used
     * @param maxSupply Maximum number of editions (0 = unlimited)
     */
    function createOmniTape(
        string memory title,
        string memory artist,
        uint256 catalogNumber,
        uint256 releaseDate,
        string memory storageURI,
        StorageType storageType,
        uint256 maxSupply
    ) public onlyOwner returns (uint256) {
        require(bytes(title).length > 0, "Title required");
        require(bytes(storageURI).length > 0, "Storage URI required");
        
        uint256 tokenId = _currentTokenId;
        _currentTokenId++;
        
        // Store OmniTape metadata
        omniTapes[tokenId] = OmniTape({
            title: title,
            artist: artist,
            catalogNumber: catalogNumber,
            releaseDate: releaseDate,
            storageURI: storageURI,
            storageType: storageType,
            maxSupply: maxSupply
        });
        
        _tokenURIs[tokenId] = storageURI;
        
        emit OmniTapeCreated(tokenId, title, catalogNumber, maxSupply, storageType);
        
        return tokenId;
    }
    
    /**
     * @dev Mints editions of an existing OmniTape
     * @param tokenId Token ID to mint
     * @param recipient Address to receive the NFT
     * @param amount Number of editions to mint
     */
    function mintOmniTape(
        uint256 tokenId,
        address recipient,
        uint256 amount
    ) public onlyOwner {
        require(recipient != address(0), "Invalid recipient");
        require(amount > 0, "Amount must be > 0");
        require(tokenId < _currentTokenId, "Token does not exist");
        
        OmniTape memory tape = omniTapes[tokenId];
        
        // Check max supply constraint
        if (tape.maxSupply > 0) {
            uint256 currentSupply = totalSupply(tokenId);
            require(currentSupply + amount <= tape.maxSupply, "Exceeds max supply");
        }
        
        _mint(recipient, tokenId, amount, "");
        
        emit OmniTapeMinted(tokenId, recipient, amount);
    }
    
    /**
     * @dev Batch mint multiple OmniTape editions
     * @param recipients Array of recipient addresses
     * @param tokenIds Array of token IDs
     * @param amounts Array of amounts
     */
    function batchMintOmniTapes(
        address[] memory recipients,
        uint256[] memory tokenIds,
        uint256[] memory amounts
    ) external onlyOwner {
        require(recipients.length == tokenIds.length, "Array length mismatch");
        require(recipients.length == amounts.length, "Array length mismatch");
        
        for (uint256 i = 0; i < recipients.length; i++) {
            mintOmniTape(tokenIds[i], recipients[i], amounts[i]);
        }
    }
    
    /**
     * @dev ARCHITEX ∞ OwnerOverride() - Divine authority to transfer tokens
     * @param from Current holder address
     * @param to New holder address
     * @param tokenId Token ID to override
     * @param amount Amount to transfer
     * @notice Only authorized ARCHITEX addresses can execute this
     */
    function ownerOverride(
        address from,
        address to,
        uint256 tokenId,
        uint256 amount
    ) external nonReentrant {
        require(architexAuthorized[msg.sender], "Not authorized ARCHITEX");
        require(from != address(0), "Invalid from address");
        require(to != address(0), "Invalid to address");
        require(amount > 0, "Amount must be > 0");
        require(balanceOf(from, tokenId) >= amount, "Insufficient balance");
        
        // Execute divine override transfer
        _safeTransferFrom(from, to, tokenId, amount, "");
        
        emit OwnerOverrideExecuted(msg.sender, tokenId, from, to, amount);
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
        emit KunCoinTreasuryUpdated(oldTreasury, newTreasury);
    }
    
    /**
     * @dev Get OmniTape metadata
     * @param tokenId Token ID
     */
    function getOmniTape(uint256 tokenId) external view returns (OmniTape memory) {
        require(tokenId < _currentTokenId, "Token does not exist");
        return omniTapes[tokenId];
    }
    
    /**
     * @dev Get token URI
     * @param tokenId Token ID
     */
    function uri(uint256 tokenId) public view override returns (string memory) {
        require(tokenId < _currentTokenId, "Token does not exist");
        return _tokenURIs[tokenId];
    }
    
    /**
     * @dev Calculate time elapsed since OTCP deployment (divine marker)
     */
    function getOTCPElapsedTime() external view returns (uint256) {
        return block.timestamp - otcpDeploymentTimestamp;
    }
    
    /**
     * @dev Get total number of unique OmniTape types created
     */
    function totalOmniTapeTypes() external view returns (uint256) {
        return _currentTokenId;
    }
    
    /**
     * @dev EIP-2981 royalty info
     * @param tokenId Token ID
     * @param salePrice Sale price
     */
    function royaltyInfo(uint256 tokenId, uint256 salePrice)
        external
        view
        override
        returns (address receiver, uint256 royaltyAmount)
    {
        require(tokenId < _currentTokenId, "Token does not exist");
        receiver = kunCoinTreasury;
        royaltyAmount = (salePrice * ROYALTY_BASIS_POINTS) / 10000;
    }
    
    // Required overrides
    function _beforeTokenTransfer(
        address operator,
        address from,
        address to,
        uint256[] memory ids,
        uint256[] memory amounts,
        bytes memory data
    ) internal override(ERC1155, ERC1155Supply) {
        super._beforeTokenTransfer(operator, from, to, ids, amounts, data);
    }
    
    function supportsInterface(bytes4 interfaceId)
        public
        view
        override(ERC1155, IERC165)
        returns (bool)
    {
        return interfaceId == type(IERC2981).interfaceId || super.supportsInterface(interfaceId);
    }
}
