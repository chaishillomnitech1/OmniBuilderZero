const hre = require("hardhat");

/**
 * Deploy ScrollVerseNFT to Scroll Sepolia
 * 
 * This script deploys the ScrollVerse NFT smart contract with treasury monitoring
 * and geometry activation capabilities to the Scroll Sepolia network.
 */
async function main() {
  console.log("✨ Initiating ScrollVerse NFT Deployment to Scroll Sepolia ✨");
  console.log("=".repeat(70));
  
  // Get deployer account
  const [deployer] = await hre.ethers.getSigners();
  console.log("📍 Deploying from account:", deployer.address);
  
  const balance = await hre.ethers.provider.getBalance(deployer.address);
  console.log("💰 Account balance:", hre.ethers.formatEther(balance), "ETH");
  console.log("");
  
  // Treasury address (update this with actual treasury address)
  const TREASURY_ADDRESS = process.env.SCROLLVERSE_TREASURY || deployer.address;
  console.log("🏦 Treasury Address:", TREASURY_ADDRESS);
  console.log("");
  
  // Deploy ScrollVerseNFT
  console.log("📜 Deploying ScrollVerseNFT Contract...");
  const ScrollVerseNFT = await hre.ethers.getContractFactory("ScrollVerseNFT");
  const scrollVerseNFT = await ScrollVerseNFT.deploy(TREASURY_ADDRESS);
  await scrollVerseNFT.waitForDeployment();
  
  const contractAddress = await scrollVerseNFT.getAddress();
  console.log("✅ ScrollVerseNFT deployed to:", contractAddress);
  
  // Get deployment timestamp
  const deploymentTimestamp = await scrollVerseNFT.scrollVerseDeploymentTimestamp();
  const deploymentDate = new Date(Number(deploymentTimestamp) * 1000);
  console.log("⏰ Deployment Timestamp:", deploymentTimestamp.toString());
  console.log("📅 Deployment Date:", deploymentDate.toISOString());
  console.log("");
  
  // Verify initial state
  console.log("🔍 Verifying Initial State...");
  const frequencyForgeActive = await scrollVerseNFT.frequencyForgeActive();
  const passiveIncomeRate = await scrollVerseNFT.passiveIncomeRate();
  const royaltyBasisPoints = await scrollVerseNFT.ROYALTY_BASIS_POINTS();
  
  console.log("  - Frequency Forge Active:", frequencyForgeActive);
  console.log("  - Passive Income Rate:", Number(passiveIncomeRate) / 100 + "%");
  console.log("  - Royalty Rate:", Number(royaltyBasisPoints) / 100 + "%");
  console.log("");
  
  // Display deployment summary
  console.log("=".repeat(70));
  console.log("🎉 SCROLLVERSE DEPLOYMENT COMPLETE 🎉");
  console.log("=".repeat(70));
  console.log("");
  console.log("📋 DEPLOYMENT SUMMARY:");
  console.log("─".repeat(70));
  console.log("Network:", hre.network.name);
  console.log("Chain ID: 534351 (Scroll Sepolia)");
  console.log("Deployer:", deployer.address);
  console.log("Treasury:", TREASURY_ADDRESS);
  console.log("");
  console.log("ScrollVerseNFT Contract:", contractAddress);
  console.log("  - Name: ScrollVerse Genesis Collection");
  console.log("  - Symbol: SVGC");
  console.log("  - Deployment Timestamp:", deploymentTimestamp.toString());
  console.log("  - Deployed:", deploymentDate.toISOString());
  console.log("");
  console.log("=".repeat(70));
  console.log("");
  
  // Save deployment info
  const deploymentInfo = {
    network: hre.network.name,
    chainId: 534351,
    deployer: deployer.address,
    treasury: TREASURY_ADDRESS,
    contract: {
      name: "ScrollVerseNFT",
      symbol: "SVGC",
      address: contractAddress,
      deploymentTimestamp: deploymentTimestamp.toString(),
      deploymentDate: deploymentDate.toISOString()
    },
    features: {
      frequencyForgeActive: frequencyForgeActive,
      passiveIncomeRate: Number(passiveIncomeRate) / 100 + "%",
      royaltyRate: Number(royaltyBasisPoints) / 100 + "%"
    },
    endpoints: {
      portal: "/portal/scrollverse_portal.html",
      dashboard: "/portal/sccc_dashboard.html",
      vibeCanvas: "/portal/vibe_canvas.html",
      certifier: "/portal/certifier_portal.html"
    },
    explorer: `https://sepolia.scrollscan.com/address/${contractAddress}`,
    timestamp: new Date().toISOString()
  };
  
  console.log("💾 Deployment Info:");
  console.log(JSON.stringify(deploymentInfo, null, 2));
  console.log("");
  
  // Verification instructions
  if (hre.network.name === "scrollSepolia") {
    console.log("📝 To verify contract on ScrollScan:");
    console.log("─".repeat(70));
    console.log(`npx hardhat verify --network scrollSepolia ${contractAddress} "${TREASURY_ADDRESS}"`);
    console.log("");
  }
  
  console.log("🔮 ScrollVerse systems are now ACTIVE on Scroll Sepolia.");
  console.log("✨ Frequency Forge is operational.");
  console.log("💎 Treasury monitoring is enabled.");
  console.log("🎨 Portal Interface ready for minting.");
  console.log("");
  console.log("🌟 ScrollVerse Genesis Collection - LIVE 🌟");
  
  return deploymentInfo;
}

// Execute deployment
main()
  .then((info) => {
    console.log("\n✅ Deployment successful!");
    process.exit(0);
  })
  .catch((error) => {
    console.error("❌ Deployment failed:", error);
    process.exit(1);
  });
