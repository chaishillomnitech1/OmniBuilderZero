const hre = require("hardhat");

/**
 * Deploy Legacy of Light: Prophetic Omnichords NFT Collection
 * 
 * This script deploys the Music NFT smart contract with OTCP divine marker
 * and connects it to the KUN Coin Treasury.
 */
async function main() {
  console.log("🌟 Initiating Legacy of Light: Prophetic Omnichords Deployment 🌟");
  console.log("=" .repeat(70));
  
  // Get deployer account
  const [deployer] = await hre.ethers.getSigners();
  console.log("📍 Deploying from account:", deployer.address);
  
  const balance = await hre.ethers.provider.getBalance(deployer.address);
  console.log("💰 Account balance:", hre.ethers.formatEther(balance), "ETH");
  console.log("");
  
  // KUN Coin Treasury address (update this with actual treasury address)
  const KUN_COIN_TREASURY = process.env.KUN_COIN_TREASURY || deployer.address;
  console.log("🏦 KUN Coin Treasury:", KUN_COIN_TREASURY);
  console.log("");
  
  // Deploy ERC-721 version
  console.log("📜 Deploying ERC-721 Contract: LegacyOfLightNFT...");
  const LegacyOfLightNFT = await hre.ethers.getContractFactory("LegacyOfLightNFT");
  const nft721 = await LegacyOfLightNFT.deploy(KUN_COIN_TREASURY);
  await nft721.waitForDeployment();
  
  const nft721Address = await nft721.getAddress();
  console.log("✅ LegacyOfLightNFT (ERC-721) deployed to:", nft721Address);
  
  // Get OTCP timestamp
  const otcpTimestamp = await nft721.otcpDeploymentTimestamp();
  const otcpDate = new Date(Number(otcpTimestamp) * 1000);
  console.log("⏰ OTCP Deployment Timestamp (Divine Marker):", otcpTimestamp.toString());
  console.log("📅 OTCP Date:", otcpDate.toISOString());
  console.log("");
  
  // Deploy ERC-1155 version
  console.log("📜 Deploying ERC-1155 Contract: LegacyOfLightNFT1155...");
  const baseURI = process.env.BASE_URI || "ipfs://";
  const LegacyOfLightNFT1155 = await hre.ethers.getContractFactory("LegacyOfLightNFT1155");
  const nft1155 = await LegacyOfLightNFT1155.deploy(KUN_COIN_TREASURY, baseURI);
  await nft1155.waitForDeployment();
  
  const nft1155Address = await nft1155.getAddress();
  console.log("✅ LegacyOfLightNFT1155 (ERC-1155) deployed to:", nft1155Address);
  
  // Get OTCP timestamp for 1155
  const otcpTimestamp1155 = await nft1155.otcpDeploymentTimestamp();
  const otcpDate1155 = new Date(Number(otcpTimestamp1155) * 1000);
  console.log("⏰ OTCP Deployment Timestamp (Divine Marker):", otcpTimestamp1155.toString());
  console.log("📅 OTCP Date:", otcpDate1155.toISOString());
  console.log("");
  
  // Display deployment summary
  console.log("=" .repeat(70));
  console.log("🎉 DEPLOYMENT COMPLETE - DIVINE MARKERS SET 🎉");
  console.log("=" .repeat(70));
  console.log("");
  console.log("📋 DEPLOYMENT SUMMARY:");
  console.log("─".repeat(70));
  console.log("Network:", hre.network.name);
  console.log("Deployer:", deployer.address);
  console.log("KUN Coin Treasury:", KUN_COIN_TREASURY);
  console.log("");
  console.log("ERC-721 Contract:", nft721Address);
  console.log("  - OTCP Timestamp:", otcpTimestamp.toString());
  console.log("  - Deployed:", otcpDate.toISOString());
  console.log("");
  console.log("ERC-1155 Contract:", nft1155Address);
  console.log("  - OTCP Timestamp:", otcpTimestamp1155.toString());
  console.log("  - Deployed:", otcpDate1155.toISOString());
  console.log("");
  console.log("=" .repeat(70));
  console.log("");
  
  // Save deployment info
  const deploymentInfo = {
    network: hre.network.name,
    deployer: deployer.address,
    kunCoinTreasury: KUN_COIN_TREASURY,
    contracts: {
      erc721: {
        address: nft721Address,
        otcpTimestamp: otcpTimestamp.toString(),
        deploymentDate: otcpDate.toISOString()
      },
      erc1155: {
        address: nft1155Address,
        otcpTimestamp: otcpTimestamp1155.toString(),
        deploymentDate: otcpDate1155.toISOString()
      }
    },
    timestamp: new Date().toISOString()
  };
  
  console.log("💾 Deployment Info:");
  console.log(JSON.stringify(deploymentInfo, null, 2));
  console.log("");
  
  // Verification instructions
  if (hre.network.name !== "hardhat" && hre.network.name !== "localhost") {
    console.log("📝 To verify contracts on Etherscan:");
    console.log("─".repeat(70));
    console.log(`npx hardhat verify --network ${hre.network.name} ${nft721Address} "${KUN_COIN_TREASURY}"`);
    console.log(`npx hardhat verify --network ${hre.network.name} ${nft1155Address} "${KUN_COIN_TREASURY}" "${baseURI}"`);
    console.log("");
  }
  
  console.log("🔮 The Omni-Temporal Coherence Protocol (OTCP) has been anchored.");
  console.log("🎵 The GOAT USB-Cassette OmniTapes catalog is ready for tokenization.");
  console.log("💎 KUN Coin Treasury royalty systems are active.");
  console.log("∞ ARCHITEX OwnerOverride() functionality is operational.");
  console.log("");
  console.log("🌟 Legacy of Light: Prophetic Omnichords - LIVE 🌟");
}

// Execute deployment
main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error("❌ Deployment failed:", error);
    process.exit(1);
  });
