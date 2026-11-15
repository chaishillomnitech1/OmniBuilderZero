const { expect } = require("chai");
const { MAINNET_CONFIRMATION, validateDeploymentConfig } = require("../scripts/deployment-preflight.cjs");

const validAmoy = {
  networkName: "polygonAmoy",
  chainId: 80002,
  deployerAddress: "0x1111111111111111111111111111111111111111",
  kunCoinTreasury: "0x2222222222222222222222222222222222222222",
  ownerMultisigAddress: "0x3333333333333333333333333333333333333333",
  baseUri: "ipfs://bafybeigdyrzt5sfp7udm7hu76uh7y26nf4k4j6j3s6h7s7y2x5q6p7r8",
};

describe("OmniBuilderZero Polygon deployment preflight", function () {
  it("accepts a fully specified Amoy configuration", function () {
    expect(validateDeploymentConfig(validAmoy).chainId).to.equal(80002);
  });

  it("rejects a wrong Amoy chain ID", function () {
    expect(() => validateDeploymentConfig({ ...validAmoy, chainId: 137 })).to.throw(/chain ID 80002/i);
  });

  it("rejects missing and zero treasury or multisig addresses", function () {
    expect(() => validateDeploymentConfig({ ...validAmoy, kunCoinTreasury: "" })).to.throw(/KUN_COIN_TREASURY/i);
    expect(() => validateDeploymentConfig({ ...validAmoy, ownerMultisigAddress: "0x0000000000000000000000000000000000000000" })).to.throw(/OWNER_MULTISIG_ADDRESS/i);
  });

  it("requires a separate multisig from the deployer", function () {
    expect(() => validateDeploymentConfig({ ...validAmoy, ownerMultisigAddress: validAmoy.deployerAddress })).to.throw(/separate from the deployer/i);
  });

  it("rejects placeholder metadata", function () {
    expect(() => validateDeploymentConfig({ ...validAmoy, baseUri: "ipfs://" })).to.throw(/real .* metadata URI/i);
    expect(() => validateDeploymentConfig({ ...validAmoy, baseUri: "ipfs://QmPlaceholder/" })).to.throw(/real .* metadata URI/i);
  });

  it("blocks Polygon mainnet without the explicit release confirmation", function () {
    const mainnet = { ...validAmoy, networkName: "polygon", chainId: 137 };
    expect(() => validateDeploymentConfig(mainnet)).to.throw(/MAINNET_RELEASE_CONFIRMATION/i);
    expect(validateDeploymentConfig({ ...mainnet, mainnetConfirmation: MAINNET_CONFIRMATION }).chainId).to.equal(137);
  });
});
