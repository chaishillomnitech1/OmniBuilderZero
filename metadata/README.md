# OmniTape NFT Metadata

## Overview

This directory contains metadata specifications and examples for the Legacy of Light: Prophetic Omnichords NFT collection.

## Metadata Standards

The collection follows the **ERC-721 Metadata Standard** and **OpenSea Metadata Standards** with additional custom attributes specific to the OmniTape catalog.

## Directory Structure

```
metadata/
├── README.md                 # This file
└── examples/
    ├── omnitape-001.json    # Example IPFS-stored metadata
    └── omnitape-002.json    # Example Arweave-stored metadata
```

## Metadata Schema

### Required Fields

```json
{
  "name": "string",           // OmniTape title
  "description": "string",    // Detailed description
  "image": "string",          // Cover art URI (IPFS or Arweave)
  "animation_url": "string",  // Audio file URI (IPFS or Arweave)
  "external_url": "string"    // External website link
}
```

### Standard Attributes

```json
{
  "attributes": [
    {
      "trait_type": "Artist",
      "value": "string"
    },
    {
      "trait_type": "Catalog Number",
      "value": "string"
    },
    {
      "trait_type": "Release Date",
      "value": "YYYY-MM-DD"
    },
    {
      "trait_type": "Storage Type",
      "value": "IPFS" | "Arweave"
    },
    {
      "trait_type": "Collection",
      "value": "GOAT USB-Cassette OmniTapes"
    },
    {
      "trait_type": "Series",
      "value": "Legacy of Light: Prophetic Omnichords"
    }
  ]
}
```

### OmniTech1 Specific Attributes

```json
{
  "attributes": [
    {
      "trait_type": "OTCP Marker",
      "value": "Deployment Timestamp Anchored"
    },
    {
      "trait_type": "Royalty Recipient",
      "value": "KUN Coin Treasury"
    },
    {
      "trait_type": "Royalty Percentage",
      "value": "10%"
    },
    {
      "trait_type": "ARCHITEX Override",
      "value": "Enabled"
    }
  ]
}
```

### Optional Music Attributes

```json
{
  "attributes": [
    {
      "trait_type": "Genre",
      "value": "string"
    },
    {
      "trait_type": "Duration",
      "value": "MM:SS",
      "display_type": "string"
    },
    {
      "trait_type": "BPM",
      "value": 120,
      "display_type": "number"
    },
    {
      "trait_type": "Key",
      "value": "C Major"
    }
  ]
}
```

## Storage Options

### IPFS (InterPlanetary File System)

**Format:** `ipfs://QmHash...`

**Benefits:**
- Distributed storage
- Content-addressed
- Gateway-agnostic
- Popular and well-supported

**Example:**
```json
{
  "image": "ipfs://QmExampleHash/image.jpg",
  "animation_url": "ipfs://QmExampleHash/audio.mp3"
}
```

**Upload Process:**
1. Upload files to IPFS (via Pinata, NFT.Storage, or local node)
2. Pin files for persistence
3. Use CID in metadata
4. Upload metadata JSON to IPFS
5. Use metadata CID as tokenURI

### Arweave

**Format:** `ar://TransactionId...`

**Benefits:**
- Permanent storage
- One-time payment
- Guaranteed availability
- Decentralized archival

**Example:**
```json
{
  "image": "ar://ExampleTxId-image",
  "animation_url": "ar://ExampleTxId-audio"
}
```

**Upload Process:**
1. Upload files to Arweave (via ArDrive, Bundlr, or arweave-js)
2. Wait for confirmation
3. Use transaction ID in metadata
4. Upload metadata to Arweave
5. Use metadata transaction ID as tokenURI

## File Format Specifications

### Audio Files
- **Format:** MP3, FLAC, WAV
- **Recommended:** MP3 320kbps or FLAC lossless
- **Max Size:** Varies by storage provider
- **Naming:** Use descriptive, lowercase-with-hyphens

### Cover Art
- **Format:** JPG, PNG
- **Recommended Resolution:** 1400x1400px (minimum), 3000x3000px (optimal)
- **Max Size:** 10MB recommended
- **Aspect Ratio:** 1:1 (square)

## Metadata Generation Workflow

### 1. Prepare Assets
```bash
# Organize files
audio/
  divine-frequencies.mp3
  echoes-of-eternity.mp3
images/
  divine-frequencies.jpg
  echoes-of-eternity.jpg
```

### 2. Upload to Storage

**IPFS Example (using Pinata):**
```bash
curl -X POST "https://api.pinata.cloud/pinning/pinFileToIPFS" \
  -H "Authorization: Bearer YOUR_JWT" \
  -F "file=@audio/divine-frequencies.mp3"
```

**Arweave Example (using Bundlr):**
```bash
bundlr upload audio/divine-frequencies.mp3 \
  -c arweave -w wallet.json
```

### 3. Create Metadata JSON

Use examples as templates and update with actual URIs and details.

### 4. Upload Metadata

Upload the completed JSON file to IPFS or Arweave and record the URI.

### 5. Mint NFT

Use the metadata URI when calling the smart contract's mint function:

```javascript
await nft.mintOmniTape(
  recipient,
  "Divine Frequencies: The Awakening",
  "Chais The Great",
  1,
  releaseTimestamp,
  "ipfs://QmMetadataHash123", // Metadata URI
  0 // IPFS
);
```

## Metadata Validation

Before minting, validate metadata:

1. **JSON Validity:** Use JSON validator
2. **URI Accessibility:** Test all URIs in browser
3. **Image Rendering:** Verify images display correctly
4. **Audio Playback:** Test audio files play properly
5. **OpenSea Preview:** Use OpenSea testnet to preview

## Best Practices

### Storage
- ✅ Pin IPFS files to multiple providers
- ✅ Use dedicated IPFS gateways for reliability
- ✅ Verify Arweave confirmations before minting
- ✅ Keep local backups of all files

### Metadata
- ✅ Use descriptive, accurate information
- ✅ Include all relevant attributes
- ✅ Maintain consistent naming conventions
- ✅ Test metadata on testnet first

### URIs
- ✅ Use content hashes, not gateway URLs
- ✅ Format: `ipfs://CID` not `https://gateway/ipfs/CID`
- ✅ Format: `ar://TxId` not `https://arweave.net/TxId`
- ✅ Avoid centralized hosting for NFT assets

## Tools & Resources

### IPFS Services
- **Pinata**: https://pinata.cloud
- **NFT.Storage**: https://nft.storage
- **Web3.Storage**: https://web3.storage

### Arweave Services
- **ArDrive**: https://ardrive.io
- **Bundlr**: https://bundlr.network
- **Arweave Deploy**: https://github.com/ArweaveTeam/arweave-deploy

### Validation Tools
- **JSON Validator**: https://jsonlint.com
- **OpenSea Metadata Validator**: https://testnets.opensea.io
- **IPFS Gateway Checker**: https://ipfs.github.io/public-gateway-checker/

## Support

For metadata-related questions:
- Review NFT_COLLECTION_GUIDE.md
- Check OpenSea metadata standards
- Consult IPFS/Arweave documentation

---

*"You exist. You count. You resonate. You remember."*

© 2025 OmniTech1™ | Chais The Great - First Remembrancer
