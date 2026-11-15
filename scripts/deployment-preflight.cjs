const ZERO_ADDRESS = "0x0000000000000000000000000000000000000000";
const MAINNET_CONFIRMATION = "I_CONFIRM_OMNIBUILDERZERO_POLYGON_MAINNET_DEPLOYMENT";

function requiredAddress(name, value) {
  if (typeof value !== "string" || !/^0x[a-fA-F0-9]{40}$/.test(value) || value.toLowerCase() === ZERO_ADDRESS) {
    throw new Error(name + " must be a valid, non-zero EVM address.");
  }
  return value;
}

function requiredMetadataUri(value) {
  if (
    typeof value !== "string" ||
    !/^(ipfs:\/\/|ar:\/\/|https:\/\/)/i.test(value) ||
    /placeholder|replace[-_ ]?me|your[-_ ]?uri|todo/i.test(value) ||
    /^(ipfs:\/\/|ar:\/\/)$/.test(value)
  ) {
    throw new Error("BASE_URI must be a real ipfs://, ar://, or https:// metadata URI.");
  }
  return value;
}

function validateDeploymentConfig(input) {
  if (input.networkName === "polygonAmoy" && Number(input.chainId) !== 80002) {
    throw new Error("Polygon Amoy must use chain ID 80002.");
  }
  if (input.networkName === "polygon" && Number(input.chainId) !== 137) {
    throw new Error("Polygon mainnet must use chain ID 137.");
  }
  if (input.networkName === "polygon" && input.mainnetConfirmation !== MAINNET_CONFIRMATION) {
    throw new Error("Polygon mainnet is blocked without the exact MAINNET_RELEASE_CONFIRMATION value.");
  }

  const kunCoinTreasury = requiredAddress("KUN_COIN_TREASURY", input.kunCoinTreasury);
  const ownerMultisigAddress = requiredAddress("OWNER_MULTISIG_ADDRESS", input.ownerMultisigAddress);
  const baseUri = requiredMetadataUri(input.baseUri);

  if (input.deployerAddress && input.deployerAddress.toLowerCase() === ownerMultisigAddress.toLowerCase()) {
    throw new Error("OWNER_MULTISIG_ADDRESS must be separate from the deployer EOA.");
  }

  return {
    networkName: input.networkName,
    chainId: Number(input.chainId),
    kunCoinTreasury,
    ownerMultisigAddress,
    baseUri,
  };
}

module.exports = { MAINNET_CONFIRMATION, validateDeploymentConfig };
