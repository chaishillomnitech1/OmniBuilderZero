const hre = require("hardhat");

/**
 * Deploy PreciousMetalBridge Contract
 * 
 * ScrollVerse Precious Metal Bridge - Physical to Digital Asset Bridge
 * Aligned with PERMANENCE, DIVINITY, and WORTH values
 */
async function main() {
  console.log("\n═══════════════════════════════════════════════════════════");
  console.log("   ScrollVerse Precious Metal Bridge Deployment");
  console.log("   Physical-to-Digital Asset Bridge Protocol");
  console.log("═══════════════════════════════════════════════════════════\n");

  // Get deployer account
  const [deployer] = await hre.ethers.getSigners();
  console.log("📜 Deployer Address:", deployer.address);
  
  // Check balance
  const balance = await hre.ethers.provider.getBalance(deployer.address);
  console.log("💰 Deployer Balance:", hre.ethers.formatEther(balance), "ETH\n");

  // Treasury address - use deployer for testing, replace with actual treasury for production
  const treasuryAddress = process.env.TREASURY_ADDRESS || deployer.address;
  console.log("🏛️  Treasury Address:", treasuryAddress);

  // Deploy PreciousMetalBridge
  console.log("\n🔧 Deploying PreciousMetalBridge...");
  
  const PreciousMetalBridge = await hre.ethers.getContractFactory("PreciousMetalBridge");
  const bridge = await PreciousMetalBridge.deploy(treasuryAddress);
  await bridge.waitForDeployment();

  const bridgeAddress = await bridge.getAddress();
  console.log("✅ PreciousMetalBridge deployed to:", bridgeAddress);

  // Get deployment timestamp
  const deploymentTimestamp = await bridge.bridgeDeploymentTimestamp();
  console.log("⏰ Bridge Deployment Timestamp:", new Date(Number(deploymentTimestamp) * 1000).toISOString());

  // Verify initial state
  console.log("\n📊 Verifying Initial State...");
  console.log("   - Name:", await bridge.name());
  console.log("   - Symbol:", await bridge.symbol());
  console.log("   - Treasury:", await bridge.treasuryAddress());
  console.log("   - Deployer is Certifier:", await bridge.authorizedCertifiers(deployer.address));
  console.log("   - Deployer is Vault Operator:", await bridge.authorizedVaultOperators(deployer.address));

  // Network-specific information
  const network = await hre.ethers.provider.getNetwork();
  console.log("\n🌐 Network Information:");
  console.log("   - Chain ID:", network.chainId.toString());
  console.log("   - Network Name:", network.name);

  // Verification instructions for Scroll networks
  if (network.chainId === 534351n || network.chainId === 534352n) {
    console.log("\n📝 Contract Verification Command:");
    console.log(`   npx hardhat verify --network ${network.chainId === 534351n ? 'scrollSepolia' : 'scroll'} ${bridgeAddress} ${treasuryAddress}`);
  }

  console.log("\n═══════════════════════════════════════════════════════════");
  console.log("   Deployment Complete - PERMANENCE • DIVINITY • WORTH");
  console.log("═══════════════════════════════════════════════════════════\n");

  return {
    bridgeAddress,
    treasuryAddress,
    deploymentTimestamp: Number(deploymentTimestamp)
  };
}

// Execute deployment
main()
  .then((result) => {
    console.log("📦 Deployment Result:", JSON.stringify(result, null, 2));
    process.exit(0);
  })
  .catch((error) => {
    console.error("❌ Deployment Error:", error);
    process.exit(1);
  });
