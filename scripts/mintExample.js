const hre = require("hardhat");

/**
 * Example script to mint OmniTapes from the catalog
 * 
 * This demonstrates minting individual and batch OmniTapes
 * from the GOAT USB-Cassette catalog
 */
async function main() {
  console.log("🎵 Minting GOAT USB-Cassette OmniTapes 🎵");
  console.log("=".repeat(70));
  
  // Configuration - Update these with your deployed contract addresses
  const NFT721_ADDRESS = process.env.NFT721_ADDRESS || "0x...";
  const NFT1155_ADDRESS = process.env.NFT1155_ADDRESS || "0x...";
  
  const [signer] = await hre.ethers.getSigners();
  console.log("Minting from account:", signer.address);
  console.log("");
  
  // Connect to deployed contracts
  const nft721 = await hre.ethers.getContractAt("LegacyOfLightNFT", NFT721_ADDRESS);
  const nft1155 = await hre.ethers.getContractAt("LegacyOfLightNFT1155", NFT1155_ADDRESS);
  
  // Example OmniTapes from the catalog
  const omniTapeCatalog = [
    {
      title: "Divine Frequencies: The Awakening",
      artist: "Chais The Great",
      catalogNumber: 1,
      releaseDate: 1640995200, // 2022-01-01
      storageURI: "ipfs://QmExampleHash1",
      storageType: 0, // IPFS
    },
    {
      title: "Echoes of Eternity",
      artist: "OmniTech Collective",
      catalogNumber: 2,
      releaseDate: 1672531200, // 2023-01-01
      storageURI: "ar://ExampleArweaveHash2",
      storageType: 1, // Arweave
    },
    {
      title: "Sacred Scroll Symphony",
      artist: "Prophetic Ensemble",
      catalogNumber: 3,
      releaseDate: 1704067200, // 2024-01-01
      storageURI: "ipfs://QmExampleHash3",
      storageType: 0, // IPFS
    },
  ];
  
  console.log("📜 Minting from ERC-721 Contract (Unique NFTs)");
  console.log("─".repeat(70));
  
  // Mint first OmniTape as unique NFT
  console.log(`\nMinting: "${omniTapeCatalog[0].title}"`);
  const tx1 = await nft721.mintOmniTape(
    signer.address,
    omniTapeCatalog[0].title,
    omniTapeCatalog[0].artist,
    omniTapeCatalog[0].catalogNumber,
    omniTapeCatalog[0].releaseDate,
    omniTapeCatalog[0].storageURI,
    omniTapeCatalog[0].storageType
  );
  await tx1.wait();
  console.log("✅ Minted Token ID: 0");
  console.log("   Transaction:", tx1.hash);
  
  // Get token details
  const totalSupply = await nft721.totalSupply();
  console.log("\n📊 ERC-721 Total Supply:", totalSupply.toString());
  
  console.log("\n" + "=".repeat(70));
  console.log("📚 Minting from ERC-1155 Contract (Multi-Edition)");
  console.log("─".repeat(70));
  
  // Create a multi-edition OmniTape
  console.log(`\nCreating multi-edition: "${omniTapeCatalog[1].title}"`);
  const createTx = await nft1155.createOmniTape(
    omniTapeCatalog[1].title,
    omniTapeCatalog[1].artist,
    omniTapeCatalog[1].catalogNumber,
    omniTapeCatalog[1].releaseDate,
    omniTapeCatalog[1].storageURI,
    omniTapeCatalog[1].storageType,
    100 // Max 100 editions
  );
  await createTx.wait();
  console.log("✅ Created Token Type ID: 0");
  console.log("   Max Supply: 100 editions");
  
  // Mint 10 editions
  console.log("\nMinting 10 editions...");
  const mintTx = await nft1155.mintOmniTape(0, signer.address, 10);
  await mintTx.wait();
  console.log("✅ Minted 10 editions to:", signer.address);
  
  // Check balance
  const balance = await nft1155.balanceOf(signer.address, 0);
  console.log("   Your balance:", balance.toString());
  
  const supply = await nft1155.totalSupply(0);
  console.log("   Total minted:", supply.toString(), "/ 100");
  
  console.log("\n" + "=".repeat(70));
  console.log("🎉 Batch Minting Example (ERC-721)");
  console.log("─".repeat(70));
  
  // Batch mint remaining catalog items
  console.log("\nBatch minting remaining catalog items...");
  const recipients = [signer.address];
  const titles = [omniTapeCatalog[2].title];
  const artists = [omniTapeCatalog[2].artist];
  const catalogNumbers = [omniTapeCatalog[2].catalogNumber];
  const releaseDates = [omniTapeCatalog[2].releaseDate];
  const storageURIs = [omniTapeCatalog[2].storageURI];
  const storageTypes = [omniTapeCatalog[2].storageType];
  
  const batchTx = await nft721.batchMintOmniTapes(
    recipients,
    titles,
    artists,
    catalogNumbers,
    releaseDates,
    storageURIs,
    storageTypes
  );
  await batchTx.wait();
  console.log("✅ Batch minted 1 OmniTape");
  console.log("   Transaction:", batchTx.hash);
  
  // Final stats
  const finalSupply = await nft721.totalSupply();
  console.log("\n📊 Final ERC-721 Total Supply:", finalSupply.toString());
  
  console.log("\n" + "=".repeat(70));
  console.log("✨ OTCP Divine Marker Status");
  console.log("─".repeat(70));
  
  const otcpTimestamp = await nft721.otcpDeploymentTimestamp();
  const otcpElapsed = await nft721.getOTCPElapsedTime();
  const otcpDate = new Date(Number(otcpTimestamp) * 1000);
  
  console.log("Deployment Timestamp:", otcpTimestamp.toString());
  console.log("Deployment Date:", otcpDate.toISOString());
  console.log("Time Elapsed:", otcpElapsed.toString(), "seconds");
  
  console.log("\n" + "=".repeat(70));
  console.log("🎉 Minting Complete!");
  console.log("🎵 The GOAT USB-Cassette OmniTapes are now tokenized!");
  console.log("💎 Connected to KUN Coin Treasury for royalties");
  console.log("∞ ARCHITEX OwnerOverride() functionality active");
  console.log("=".repeat(70));
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error("❌ Minting failed:", error);
    process.exit(1);
  });
