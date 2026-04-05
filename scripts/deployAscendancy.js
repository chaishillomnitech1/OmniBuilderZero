const { ethers } = require("hardhat");

async function main() {
  console.log("🚀 Deploying AscendancyID and ScrollCoinStaking contracts...\n");

  // Get deployer
  const [deployer] = await ethers.getSigners();
  console.log("📍 Deployer address:", deployer.address);

  const balance = await ethers.provider.getBalance(deployer.address);
  console.log("💰 Deployer balance:", ethers.formatEther(balance), "ETH\n");

  // Treasury address (use deployer for testing, update for production)
  const treasuryAddress = process.env.TREASURY_ADDRESS || deployer.address;
  console.log("🏦 Treasury address:", treasuryAddress);

  // For testing, we need a mock ScrollCoin token
  // In production, use the actual ScrollCoin address
  let scrollCoinAddress = process.env.SCROLLCOIN_ADDRESS;

  if (!scrollCoinAddress) {
    console.log("\n📝 No ScrollCoin address provided, deploying mock token...");
    
    // Deploy a simple ERC20 mock for testing
    const MockToken = await ethers.getContractFactory("MockScrollCoin");
    let mockToken;
    
    try {
      mockToken = await MockToken.deploy();
      await mockToken.waitForDeployment();
      scrollCoinAddress = await mockToken.getAddress();
      console.log("✅ Mock ScrollCoin deployed to:", scrollCoinAddress);
    } catch (e) {
      console.log("⚠️  MockScrollCoin not found. Using placeholder address.");
      console.log("   Create a mock token contract or provide SCROLLCOIN_ADDRESS");
      scrollCoinAddress = "0x0000000000000000000000000000000000000001";
    }
  }

  // Deploy AscendancyID
  console.log("\n📝 Deploying AscendancyID...");
  const AscendancyID = await ethers.getContractFactory("AscendancyID");
  const ascendancyId = await AscendancyID.deploy(treasuryAddress);
  await ascendancyId.waitForDeployment();
  const ascendancyIdAddress = await ascendancyId.getAddress();
  console.log("✅ AscendancyID deployed to:", ascendancyIdAddress);

  // Deploy ScrollCoinStaking
  console.log("\n📝 Deploying ScrollCoinStaking...");
  
  // Reward rate: approximately 0.0001 tokens per second per staked token
  // Using a smaller precision value for calculation accuracy
  const rewardRatePerSecond = ethers.parseUnits("0.0000001", 18);
  
  const ScrollCoinStaking = await ethers.getContractFactory("ScrollCoinStaking");
  const staking = await ScrollCoinStaking.deploy(
    scrollCoinAddress,
    treasuryAddress,
    rewardRatePerSecond
  );
  await staking.waitForDeployment();
  const stakingAddress = await staking.getAddress();
  console.log("✅ ScrollCoinStaking deployed to:", stakingAddress);

  // Link contracts
  console.log("\n🔗 Linking contracts...");
  
  // Set staking contract in AscendancyID
  const tx1 = await ascendancyId.setStakingContract(stakingAddress);
  await tx1.wait();
  console.log("✅ Staking contract set in AscendancyID");

  // Set AscendancyID in staking contract
  const tx2 = await staking.setAscendancyIdContract(ascendancyIdAddress);
  await tx2.wait();
  console.log("✅ AscendancyID contract set in ScrollCoinStaking");

  // Summary
  console.log("\n" + "=".repeat(60));
  console.log("📋 DEPLOYMENT SUMMARY");
  console.log("=".repeat(60));
  console.log("Network:", (await ethers.provider.getNetwork()).name);
  console.log("Chain ID:", (await ethers.provider.getNetwork()).chainId.toString());
  console.log("");
  console.log("Contracts Deployed:");
  console.log("  AscendancyID:", ascendancyIdAddress);
  console.log("  ScrollCoinStaking:", stakingAddress);
  console.log("");
  console.log("Configuration:");
  console.log("  Treasury:", treasuryAddress);
  console.log("  ScrollCoin:", scrollCoinAddress);
  console.log("  Reward Rate:", ethers.formatUnits(rewardRatePerSecond, 18), "per second");
  console.log("=".repeat(60));

  // Verification commands
  console.log("\n📝 Verification Commands:");
  console.log(`npx hardhat verify --network <network> ${ascendancyIdAddress} "${treasuryAddress}"`);
  console.log(`npx hardhat verify --network <network> ${stakingAddress} "${scrollCoinAddress}" "${treasuryAddress}" "${rewardRatePerSecond}"`);

  return {
    ascendancyId: ascendancyIdAddress,
    staking: stakingAddress,
    scrollCoin: scrollCoinAddress,
    treasury: treasuryAddress
  };
}

main()
  .then((addresses) => {
    console.log("\n✅ Deployment completed successfully!");
    process.exit(0);
  })
  .catch((error) => {
    console.error("\n❌ Deployment failed:", error);
    process.exit(1);
  });
