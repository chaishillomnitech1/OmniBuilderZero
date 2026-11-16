const hre = require("hardhat");
const fs = require("node:fs");
const path = require("node:path");
const { validateDeploymentConfig } = require("./deployment-preflight.cjs");

async function main() {
  const [deployer] = await hre.ethers.getSigners();
  if (!deployer) {
    throw new Error("No deployer signer configured. Set PRIVATE_KEY in the secure runtime.");
  }

  const network = await hre.ethers.provider.getNetwork();
  const config = validateDeploymentConfig({
    networkName: hre.network.name,
    chainId: network.chainId.toString(),
    deployerAddress: deployer.address,
    kunCoinTreasury: process.env.KUN_COIN_TREASURY,
    ownerMultisigAddress: process.env.OWNER_MULTISIG_ADDRESS,
    baseUri: process.env.BASE_URI,
    mainnetConfirmation: process.env.MAINNET_RELEASE_CONFIRMATION,
  });

  const multisigCode = await hre.ethers.provider.getCode(config.ownerMultisigAddress);
  if (!multisigCode || multisigCode === "0x") {
    throw new Error("OWNER_MULTISIG_ADDRESS has no deployed contract code on the selected network.");
  }

  if (["polygonAmoy", "polygon"].includes(hre.network.name) &&
      (!process.env.POLYGONSCAN_API_KEY || process.env.POLYGONSCAN_API_KEY.trim() === "")) {
    throw new Error("POLYGONSCAN_API_KEY is required for Polygon source verification.");
  }

  const outputPath = path.resolve(__dirname, "../deployments", hre.network.name + ".json");
  fs.mkdirSync(path.dirname(outputPath), { recursive: true });
  const deployment = {
    schemaVersion: 1,
    status: "DEPLOYMENT_IN_PROGRESS",
    network: hre.network.name,
    chainId: network.chainId.toString(),
    timestamp: new Date().toISOString(),
    deployer: deployer.address,
    ownerMultisig: config.ownerMultisigAddress,
    kunCoinTreasury: config.kunCoinTreasury,
    baseUri: config.baseUri,
    contracts: {},
    deploymentTransactions: {},
    setupTransactions: {},
    verification: "PENDING",
  };
  const persist = () => fs.writeFileSync(outputPath, JSON.stringify(deployment, null, 2) + "\n", { mode: 0o600 });
  persist();

  console.log("ScrollVerse Legacy of Light controlled deployment");
  console.log("Network:", hre.network.name, "Chain ID:", network.chainId.toString());
  console.log("Deployer:", deployer.address);
  console.log("Treasury:", config.kunCoinTreasury);
  console.log("Owner multisig:", config.ownerMultisigAddress);

  const LegacyOfLightNFT = await hre.ethers.getContractFactory("LegacyOfLightNFT");
  const nft721 = await LegacyOfLightNFT.deploy(config.kunCoinTreasury);
  await nft721.waitForDeployment();
  deployment.contracts.erc721 = await nft721.getAddress();
  deployment.deploymentTransactions.erc721 = nft721.deploymentTransaction()?.hash || null;
  persist();

  const LegacyOfLightNFT1155 = await hre.ethers.getContractFactory("LegacyOfLightNFT1155");
  const nft1155 = await LegacyOfLightNFT1155.deploy(config.kunCoinTreasury, config.baseUri);
  await nft1155.waitForDeployment();
  deployment.contracts.erc1155 = await nft1155.getAddress();
  deployment.deploymentTransactions.erc1155 = nft1155.deploymentTransaction()?.hash || null;
  persist();

  // The deployer is the temporary Ownable owner during setup. Transfer the
  // ARCHITEX privilege to the multisig and revoke the deployer's special role.
  for (const [label, contract] of [["erc721", nft721], ["erc1155", nft1155]]) {
    const revokeDeployer = await contract.setArchitexAuthorization(deployer.address, false);
    await revokeDeployer.wait();
    deployment.setupTransactions[label + "RevokeDeployerArchitex"] = revokeDeployer.hash;
    persist();

    const authorizeMultisig = await contract.setArchitexAuthorization(config.ownerMultisigAddress, true);
    await authorizeMultisig.wait();
    deployment.setupTransactions[label + "AuthorizeMultisigArchitex"] = authorizeMultisig.hash;
    persist();

    const transferOwner = await contract.transferOwnership(config.ownerMultisigAddress);
    await transferOwner.wait();
    deployment.setupTransactions[label + "TransferOwnership"] = transferOwner.hash;
    persist();
  }

  const [owner721, owner1155, treasury721, treasury1155, deployerRole721, deployerRole1155, multisigRole721, multisigRole1155] = await Promise.all([
    nft721.owner(),
    nft1155.owner(),
    nft721.kunCoinTreasury(),
    nft1155.kunCoinTreasury(),
    nft721.architexAuthorized(deployer.address),
    nft1155.architexAuthorized(deployer.address),
    nft721.architexAuthorized(config.ownerMultisigAddress),
    nft1155.architexAuthorized(config.ownerMultisigAddress),
  ]);

  const same = (a, b) => a.toLowerCase() === b.toLowerCase();
  if (!same(owner721, config.ownerMultisigAddress) || !same(owner1155, config.ownerMultisigAddress)) {
    throw new Error("Final Ownable verification failed: both contracts must be owned by the configured multisig.");
  }
  if (!same(treasury721, config.kunCoinTreasury) || !same(treasury1155, config.kunCoinTreasury)) {
    throw new Error("Treasury readback failed for one or both NFT contracts.");
  }
  if (deployerRole721 || deployerRole1155 || !multisigRole721 || !multisigRole1155) {
    throw new Error("ARCHITEX role verification failed: deployer must be revoked and multisig authorized.");
  }

  deployment.ownershipVerification = {
    erc721Owner: owner721,
    erc1155Owner: owner1155,
    deployerArchitexRevoked: !deployerRole721 && !deployerRole1155,
    multisigArchitexAuthorized: multisigRole721 && multisigRole1155,
    treasury721,
    treasury1155,
  };
  deployment.status = "DEPLOYED_PENDING_EXTERNAL_VERIFICATION";
  persist();

  console.log("Deployment record:", outputPath);
  console.log("ERC-721:", deployment.contracts.erc721);
  console.log("ERC-1155:", deployment.contracts.erc1155);
  console.log("Ownership and ARCHITEX roles verified against multisig.");
  console.log("Source verification and independent review remain pending.");
}

main().catch((error) => {
  console.error("Deployment stopped:", error.message);
  process.exitCode = 1;
});
