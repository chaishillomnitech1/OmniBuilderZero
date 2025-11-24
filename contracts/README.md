# Legacy of Light: Prophetic Omnichords

## Music NFT Collection for GOAT USB-Cassette OmniTapes Catalog

### 🌟 Overview

The **Legacy of Light: Prophetic Omnichords** is a revolutionary music NFT collection that tokenizes the legendary GOAT USB-Cassette OmniTapes catalog. This smart contract system bridges divine artistry with blockchain technology, creating an eternal digital archive of sacred music.

### ✨ Key Features

#### 🎵 Dual Standard Support
- **ERC-721**: Unique 1-of-1 OmniTape NFTs for exclusive releases
- **ERC-1155**: Multi-edition support for limited releases and special editions

#### 📦 Decentralized Storage
- **IPFS Integration**: InterPlanetary File System for distributed metadata storage
- **Arweave Support**: Permanent storage solution for eternal preservation
- Flexible storage type selection per token

#### 💎 KUN Coin Treasury Integration
- Direct connection to Collector KUN Coin Treasury
- Automated 10% royalty system on all secondary sales
- Royalty payments flow directly to the treasury
- EIP-2981 compliant royalty standard

#### ∞ ARCHITEX OwnerOverride() Functionality
- Divine authority mechanism for special circumstances
- Multi-signature authorization system for ARCHITEX addresses
- Emergency override capability with full event logging
- Granular permission control

#### ⏰ Omni-Temporal Coherence Protocol (OTCP)
- Deployment timestamp acts as divine marker
- Immutable temporal anchor for the collection
- Track elapsed time since divine deployment
- Links contract to universal timeline

### 📋 Smart Contract Architecture

#### LegacyOfLightNFT.sol (ERC-721)
The primary contract for unique OmniTape tokens.

**Key Functions:**
- `mintOmniTape()`: Create new unique OmniTape NFTs
- `batchMintOmniTapes()`: Batch minting for multiple tokens
- `ownerOverride()`: ARCHITEX divine override capability
- `setArchitexAuthorization()`: Manage ARCHITEX permissions
- `updateKunCoinTreasury()`: Update treasury address
- `getOmniTape()`: Retrieve full metadata
- `getOTCPElapsedTime()`: Time since deployment

**OmniTape Structure:**
```solidity
struct OmniTape {
    string title;
    string artist;
    uint256 catalogNumber;
    uint256 releaseDate;
    string storageURI;
    StorageType storageType;
}
```

#### LegacyOfLightNFT1155.sol (ERC-1155)
Multi-edition contract for limited releases.

**Key Functions:**
- `createOmniTape()`: Define new OmniTape type
- `mintOmniTape()`: Mint editions of existing type
- `batchMintOmniTapes()`: Batch mint multiple editions
- `ownerOverride()`: ARCHITEX override for editions
- All treasury and authorization functions from ERC-721

**Additional Features:**
- Maximum supply constraints per token type
- Unlimited editions support (maxSupply = 0)
- Edition tracking and supply management

### 🚀 Deployment

#### Prerequisites
```bash
npm install
```

#### Configuration
1. Copy `.env.example` to `.env`
2. Configure your deployment parameters:
   - `PRIVATE_KEY`: Deployer wallet private key
   - `KUN_COIN_TREASURY`: Treasury address
   - `*_RPC_URL`: Network RPC endpoints
   - `*_API_KEY`: Block explorer API keys

#### Deploy to Networks
```bash
# Local Hardhat network (testing)
npm run deploy:local

# Ethereum Sepolia testnet
npm run deploy:sepolia

# Ethereum Mainnet
npm run deploy:mainnet

# Polygon Mainnet
npm run deploy:polygon
```

#### Verify Contracts
```bash
npx hardhat verify --network <network> <contract-address> "<constructor-args>"
```

### 🧪 Testing

Run the comprehensive test suite:
```bash
npm test
```

### 📖 Usage Examples

#### Minting a Single OmniTape (ERC-721)
```javascript
const tx = await nft721.mintOmniTape(
  recipientAddress,
  "Prophetic Vision #1",
  "Chais The Great",
  1,
  Date.now(),
  "ipfs://QmXxx...",
  0 // IPFS
);
```

#### Creating & Minting Multi-Edition (ERC-1155)
```javascript
// Create the OmniTape type
const tokenId = await nft1155.createOmniTape(
  "Sacred Harmonics Vol. 1",
  "OmniTech Collective",
  100,
  Date.now(),
  "ar://xxx...",
  1, // Arweave
  1000 // max supply
);

// Mint editions
await nft1155.mintOmniTape(tokenId, recipientAddress, 10);
```

#### ARCHITEX Override
```javascript
// Authorize ARCHITEX address
await nft721.setArchitexAuthorization(architexAddress, true);

// Execute override (from ARCHITEX account)
await nft721.connect(architexSigner).ownerOverride(tokenId, newOwnerAddress);
```

### 🔒 Security Features

1. **ReentrancyGuard**: Protection against reentrancy attacks
2. **Ownable**: Secure ownership management
3. **Access Control**: ARCHITEX authorization system
4. **Input Validation**: Comprehensive parameter checking
5. **Event Logging**: Full transparency of all operations

### 📊 Royalty System

- **Standard Rate**: 10% (1000 basis points)
- **Recipient**: KUN Coin Treasury
- **Standard**: EIP-2981 compliant
- **Flexibility**: Per-token and default royalty settings

### 🌐 Supported Networks

- Ethereum Mainnet
- Ethereum Sepolia (Testnet)
- Polygon Mainnet
- Polygon Mumbai (Testnet)
- Any EVM-compatible network

### 📜 License

MIT License - See LICENSE file for details

### 🤝 Contributing

This is a sacred project. Contributions aligned with the OmniTech1 vision are welcome.

### 📞 Support

For questions about the Legacy of Light collection:
- Review the main repository README
- Check the Phase 2 documentation
- Consult the NŪR Global Integration Protocol

### ⚡ Quick Reference

**Contract Names:**
- ERC-721: `LegacyOfLightNFT`
- ERC-1155: `LegacyOfLightNFT1155`

**Symbols:**
- ERC-721: `LLPO`
- ERC-1155: `LLPOME`

**Royalty Rate:** 10%

**Storage Options:**
- Type 0: IPFS
- Type 1: Arweave

---

🔥 **CHAIS THE GREAT ∞: THRONE SECURED. ALL SYSTEMS GREEN. ETERNITY BEGINS. 💎** 🔥

*"You exist. You count. You resonate. You remember."*

© 2025 OmniTech1™ | Architect of the Omni-Temporal Coherence Protocol
