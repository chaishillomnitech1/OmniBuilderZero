const { expect } = require("chai");
const { ethers } = require("hardhat");
const { time } = require("@nomicfoundation/hardhat-network-helpers");

describe("PreciousMetalBridge", function () {
  let bridge;
  let owner, treasury, certifier, vaultOperator, user1, user2;
  let deploymentTimestamp;

  // Test constants
  const GOLD = 0;
  const SILVER = 1;
  const PLATINUM = 2;
  const PALLADIUM = 3;

  const IPFS = 0;
  const ARWEAVE = 1;

  const ZURICH = 0;
  const SINGAPORE = 1;
  const DUBAI = 2;
  const LONDON = 3;
  const NEW_YORK = 4;
  const HONG_KONG = 5;

  const PENDING = 0;
  const CERTIFIED = 1;
  const SUSPENDED = 2;
  const REVOKED = 3;

  beforeEach(async function () {
    // Get signers
    [owner, treasury, certifier, vaultOperator, user1, user2] = await ethers.getSigners();

    // Deploy PreciousMetalBridge
    const PreciousMetalBridge = await ethers.getContractFactory("PreciousMetalBridge");
    bridge = await PreciousMetalBridge.deploy(treasury.address);
    await bridge.waitForDeployment();

    // Store deployment timestamp
    deploymentTimestamp = await bridge.bridgeDeploymentTimestamp();
  });

  describe("Deployment", function () {
    it("Should set the correct name and symbol", async function () {
      expect(await bridge.name()).to.equal("ScrollVerse Precious Metal Bridge");
      expect(await bridge.symbol()).to.equal("SPMB");
    });

    it("Should set the treasury address", async function () {
      expect(await bridge.treasuryAddress()).to.equal(treasury.address);
    });

    it("Should record bridge deployment timestamp", async function () {
      expect(deploymentTimestamp).to.be.gt(0);
    });

    it("Should authorize deployer as certifier", async function () {
      expect(await bridge.authorizedCertifiers(owner.address)).to.be.true;
    });

    it("Should authorize deployer as vault operator", async function () {
      expect(await bridge.authorizedVaultOperators(owner.address)).to.be.true;
    });

    it("Should revert with zero treasury address", async function () {
      const PreciousMetalBridge = await ethers.getContractFactory("PreciousMetalBridge");
      await expect(
        PreciousMetalBridge.deploy(ethers.ZeroAddress)
      ).to.be.revertedWith("Invalid treasury address");
    });
  });

  describe("Minting (PERMANENCE)", function () {
    const testAssetHash = ethers.keccak256(ethers.toUtf8Bytes("GOLD-BAR-001"));
    const testSerialHash = ethers.keccak256(ethers.toUtf8Bytes("SN-12345"));
    const testMetadataURI = "ipfs://QmTestGoldBar123";

    it("Should mint a new gold asset NFT", async function () {
      const tx = await bridge.mintPreciousMetal(
        user1.address,
        testAssetHash,
        testSerialHash,
        GOLD,
        1000000, // 1000 grams (1 kg)
        999, // 99.9% pure
        testMetadataURI,
        IPFS,
        ZURICH
      );

      await expect(tx)
        .to.emit(bridge, "PreciousMetalMinted")
        .withArgs(0, user1.address, GOLD, 1000000, 999, ZURICH);

      expect(await bridge.ownerOf(0)).to.equal(user1.address);
      expect(await bridge.totalSupply()).to.equal(1);
    });

    it("Should store asset data correctly", async function () {
      await bridge.mintPreciousMetal(
        user1.address,
        testAssetHash,
        testSerialHash,
        SILVER,
        5000000, // 5 kg
        995, // 99.5% pure
        "ar://ArweaveHash",
        ARWEAVE,
        LONDON
      );

      const asset = await bridge.getPreciousAsset(0);
      expect(asset.physicalAssetHash).to.equal(testAssetHash);
      expect(asset.serialNumberHash).to.equal(testSerialHash);
      expect(asset.metalType).to.equal(SILVER);
      expect(asset.weightInGrams).to.equal(5000000);
      expect(asset.purityInThousandths).to.equal(995);
      expect(asset.metadataURI).to.equal("ar://ArweaveHash");
      expect(asset.storageType).to.equal(ARWEAVE);
      expect(asset.vaultLocation).to.equal(LONDON);
      expect(asset.status).to.equal(PENDING);
    });

    it("Should prevent duplicate minting of same physical asset", async function () {
      await bridge.mintPreciousMetal(
        user1.address,
        testAssetHash,
        testSerialHash,
        GOLD,
        1000000,
        999,
        testMetadataURI,
        IPFS,
        ZURICH
      );

      await expect(
        bridge.mintPreciousMetal(
          user2.address,
          testAssetHash, // Same asset hash
          ethers.keccak256(ethers.toUtf8Bytes("SN-DIFFERENT")),
          GOLD,
          1000000,
          999,
          testMetadataURI,
          IPFS,
          ZURICH
        )
      ).to.be.revertedWith("Asset already tokenized");
    });

    it("Should record initial provenance on mint", async function () {
      await bridge.mintPreciousMetal(
        user1.address,
        testAssetHash,
        testSerialHash,
        GOLD,
        1000000,
        999,
        testMetadataURI,
        IPFS,
        ZURICH
      );

      const provenanceCount = await bridge.getProvenanceCount(0);
      expect(provenanceCount).to.equal(1);

      const history = await bridge.getProvenanceHistory(0);
      expect(history[0].actor).to.equal(owner.address);
      expect(history[0].description).to.equal("Asset minted and bridged to ScrollVerse");
    });

    it("Should only allow owner to mint", async function () {
      await expect(
        bridge.connect(user1).mintPreciousMetal(
          user1.address,
          testAssetHash,
          testSerialHash,
          GOLD,
          1000000,
          999,
          testMetadataURI,
          IPFS,
          ZURICH
        )
      ).to.be.reverted;
    });

    it("Should revert with zero weight", async function () {
      await expect(
        bridge.mintPreciousMetal(
          user1.address,
          testAssetHash,
          testSerialHash,
          GOLD,
          0, // Zero weight
          999,
          testMetadataURI,
          IPFS,
          ZURICH
        )
      ).to.be.revertedWith("Weight must be greater than zero");
    });

    it("Should revert with invalid purity", async function () {
      await expect(
        bridge.mintPreciousMetal(
          user1.address,
          testAssetHash,
          testSerialHash,
          GOLD,
          1000000,
          1001, // > 100%
          testMetadataURI,
          IPFS,
          ZURICH
        )
      ).to.be.revertedWith("Invalid purity");
    });
  });

  describe("Certification (DIVINITY)", function () {
    const testAssetHash = ethers.keccak256(ethers.toUtf8Bytes("GOLD-BAR-002"));
    const testSerialHash = ethers.keccak256(ethers.toUtf8Bytes("SN-67890"));
    const certificationProof = ethers.keccak256(ethers.toUtf8Bytes("CERT-PROOF-001"));

    beforeEach(async function () {
      // Mint a token for certification tests
      await bridge.mintPreciousMetal(
        user1.address,
        testAssetHash,
        testSerialHash,
        PLATINUM,
        500000,
        950,
        "ipfs://QmPlatinum",
        IPFS,
        DUBAI
      );

      // Authorize certifier
      await bridge.setCertifierAuthorization(certifier.address, true);
    });

    it("Should allow authorized certifier to certify asset", async function () {
      const tx = await bridge.connect(certifier).certifyAsset(0, certificationProof);

      await expect(tx)
        .to.emit(bridge, "AssetCertified")
        .withArgs(0, certifier.address, certificationProof, await time.latest());

      const asset = await bridge.getPreciousAsset(0);
      expect(asset.status).to.equal(CERTIFIED);
      expect(asset.certifier).to.equal(certifier.address);
      expect(asset.certificationProof).to.equal(certificationProof);
    });

    it("Should track certifier certification count", async function () {
      expect(await bridge.certifierCertificationCount(certifier.address)).to.equal(0);
      
      await bridge.connect(certifier).certifyAsset(0, certificationProof);
      
      expect(await bridge.certifierCertificationCount(certifier.address)).to.equal(1);
    });

    it("Should record certification in provenance", async function () {
      await bridge.connect(certifier).certifyAsset(0, certificationProof);

      const history = await bridge.getProvenanceHistory(0);
      expect(history.length).to.equal(2); // Mint + Certify
      expect(history[1].actor).to.equal(certifier.address);
      expect(history[1].description).to.equal("Asset certified by authorized certifier");
    });

    it("Should revert when unauthorized address tries to certify", async function () {
      await expect(
        bridge.connect(user2).certifyAsset(0, certificationProof)
      ).to.be.revertedWith("Not authorized certifier");
    });

    it("Should revert when certifying already certified asset", async function () {
      await bridge.connect(certifier).certifyAsset(0, certificationProof);

      await expect(
        bridge.connect(certifier).certifyAsset(0, certificationProof)
      ).to.be.revertedWith("Asset not pending certification");
    });

    it("Should allow certifier to update status to suspended", async function () {
      await bridge.connect(certifier).certifyAsset(0, certificationProof);
      
      await expect(
        bridge.connect(certifier).updateCertificationStatus(0, SUSPENDED)
      )
        .to.emit(bridge, "CertificationStatusChanged")
        .withArgs(0, CERTIFIED, SUSPENDED, certifier.address);

      const asset = await bridge.getPreciousAsset(0);
      expect(asset.status).to.equal(SUSPENDED);
    });

    it("Should not allow reverting to pending status", async function () {
      await bridge.connect(certifier).certifyAsset(0, certificationProof);

      await expect(
        bridge.connect(certifier).updateCertificationStatus(0, PENDING)
      ).to.be.revertedWith("Cannot revert to pending");
    });
  });

  describe("Valuation (WORTH)", function () {
    const testAssetHash = ethers.keccak256(ethers.toUtf8Bytes("GOLD-BAR-003"));
    const testSerialHash = ethers.keccak256(ethers.toUtf8Bytes("SN-11111"));
    const valuationInWei = ethers.parseEther("100"); // 100 ETH valuation

    beforeEach(async function () {
      // Mint a token
      await bridge.mintPreciousMetal(
        user1.address,
        testAssetHash,
        testSerialHash,
        GOLD,
        1000000,
        999,
        "ipfs://QmGold",
        IPFS,
        SINGAPORE
      );

      // Authorize vault operator
      await bridge.setVaultOperatorAuthorization(vaultOperator.address, true);
    });

    it("Should allow vault operator to update valuation", async function () {
      const tx = await bridge.connect(vaultOperator).updateValuation(0, valuationInWei);

      await expect(tx)
        .to.emit(bridge, "ValuationUpdated")
        .withArgs(0, 0, valuationInWei, await time.latest());

      const asset = await bridge.getPreciousAsset(0);
      expect(asset.valuationInWei).to.equal(valuationInWei);
      expect(asset.valuationTimestamp).to.be.gt(0);
    });

    it("Should record valuation update in provenance", async function () {
      await bridge.connect(vaultOperator).updateValuation(0, valuationInWei);

      const history = await bridge.getProvenanceHistory(0);
      expect(history.length).to.equal(2); // Mint + Valuation
      expect(history[1].actor).to.equal(vaultOperator.address);
      expect(history[1].description).to.equal("Asset valuation updated");
    });

    it("Should revert when unauthorized address tries to update valuation", async function () {
      await expect(
        bridge.connect(user2).updateValuation(0, valuationInWei)
      ).to.be.revertedWith("Not authorized vault operator");
    });

    it("Should compute pure metal weight correctly", async function () {
      // 1000g at 99.9% purity = 999g pure
      const pureWeight = await bridge.computePureMetalWeight(0);
      expect(pureWeight).to.equal(999000); // 1000000 * 999 / 1000
    });
  });

  describe("Provenance History (PERMANENCE)", function () {
    const testAssetHash = ethers.keccak256(ethers.toUtf8Bytes("GOLD-BAR-004"));
    const testSerialHash = ethers.keccak256(ethers.toUtf8Bytes("SN-22222"));
    const certificationProof = ethers.keccak256(ethers.toUtf8Bytes("CERT-PROOF-002"));

    beforeEach(async function () {
      await bridge.mintPreciousMetal(
        user1.address,
        testAssetHash,
        testSerialHash,
        PALLADIUM,
        250000,
        995,
        "ipfs://QmPalladium",
        IPFS,
        NEW_YORK
      );

      await bridge.setCertifierAuthorization(certifier.address, true);
      await bridge.setVaultOperatorAuthorization(vaultOperator.address, true);
    });

    it("Should build complete provenance chain", async function () {
      // Certify
      await bridge.connect(certifier).certifyAsset(0, certificationProof);

      // Update valuation
      await bridge.connect(vaultOperator).updateValuation(0, ethers.parseEther("50"));

      // Check provenance
      const history = await bridge.getProvenanceHistory(0);
      expect(history.length).to.equal(3);

      expect(history[0].description).to.equal("Asset minted and bridged to ScrollVerse");
      expect(history[1].description).to.equal("Asset certified by authorized certifier");
      expect(history[2].description).to.equal("Asset valuation updated");
    });

    it("Should track actors correctly in provenance", async function () {
      await bridge.connect(certifier).certifyAsset(0, certificationProof);

      const history = await bridge.getProvenanceHistory(0);
      expect(history[0].actor).to.equal(owner.address);
      expect(history[1].actor).to.equal(certifier.address);
    });
  });

  describe("Asset Lookup", function () {
    const testAssetHash = ethers.keccak256(ethers.toUtf8Bytes("GOLD-BAR-005"));
    const testSerialHash = ethers.keccak256(ethers.toUtf8Bytes("SN-33333"));

    it("Should track tokenized assets correctly", async function () {
      expect(await bridge.isAssetTokenized(testAssetHash)).to.be.false;

      await bridge.mintPreciousMetal(
        user1.address,
        testAssetHash,
        testSerialHash,
        GOLD,
        1000000,
        999,
        "ipfs://QmGold",
        IPFS,
        HONG_KONG
      );

      expect(await bridge.isAssetTokenized(testAssetHash)).to.be.true;
      expect(await bridge.getTokenIdByAssetHash(testAssetHash)).to.equal(0);
    });

    it("Should return max uint256 for non-existent asset hash", async function () {
      const nonExistentHash = ethers.keccak256(ethers.toUtf8Bytes("NON-EXISTENT"));
      const result = await bridge.getTokenIdByAssetHash(nonExistentHash);
      expect(result).to.equal(ethers.MaxUint256);
    });
  });

  describe("Admin Functions", function () {
    it("Should authorize and deauthorize certifiers", async function () {
      await expect(bridge.setCertifierAuthorization(certifier.address, true))
        .to.emit(bridge, "CertifierAuthorized")
        .withArgs(certifier.address, true);

      expect(await bridge.authorizedCertifiers(certifier.address)).to.be.true;

      await bridge.setCertifierAuthorization(certifier.address, false);
      expect(await bridge.authorizedCertifiers(certifier.address)).to.be.false;
    });

    it("Should authorize and deauthorize vault operators", async function () {
      await expect(bridge.setVaultOperatorAuthorization(vaultOperator.address, true))
        .to.emit(bridge, "VaultOperatorAuthorized")
        .withArgs(vaultOperator.address, true);

      expect(await bridge.authorizedVaultOperators(vaultOperator.address)).to.be.true;
    });

    it("Should update treasury address", async function () {
      const newTreasury = user1.address;
      await expect(bridge.updateTreasury(newTreasury))
        .to.emit(bridge, "TreasuryUpdated")
        .withArgs(treasury.address, newTreasury);

      expect(await bridge.treasuryAddress()).to.equal(newTreasury);
    });

    it("Should revert when updating treasury to zero address", async function () {
      await expect(
        bridge.updateTreasury(ethers.ZeroAddress)
      ).to.be.revertedWith("Invalid treasury address");
    });
  });

  describe("Royalties", function () {
    beforeEach(async function () {
      const testAssetHash = ethers.keccak256(ethers.toUtf8Bytes("GOLD-BAR-006"));
      const testSerialHash = ethers.keccak256(ethers.toUtf8Bytes("SN-44444"));

      await bridge.mintPreciousMetal(
        user1.address,
        testAssetHash,
        testSerialHash,
        GOLD,
        1000000,
        999,
        "ipfs://QmGold",
        IPFS,
        ZURICH
      );
    });

    it("Should return correct royalty info", async function () {
      const salePrice = ethers.parseEther("1");
      const royaltyInfo = await bridge.royaltyInfo(0, salePrice);

      expect(royaltyInfo[0]).to.equal(treasury.address);
      // 5% royalty = 0.05 ETH
      expect(royaltyInfo[1]).to.equal(ethers.parseEther("0.05"));
    });

    it("Should support ERC-2981 interface", async function () {
      // ERC-2981 interface ID: 0x2a55205a
      expect(await bridge.supportsInterface("0x2a55205a")).to.be.true;
    });
  });

  describe("Time Functions", function () {
    it("Should calculate elapsed time since deployment", async function () {
      // Advance time by 1 hour
      await time.increase(3600);

      const elapsed = await bridge.getElapsedTime();
      expect(elapsed).to.be.gte(3600);
    });

    it("Should have immutable deployment timestamp", async function () {
      const timestamp1 = await bridge.bridgeDeploymentTimestamp();

      await time.increase(100);

      const timestamp2 = await bridge.bridgeDeploymentTimestamp();
      expect(timestamp1).to.equal(timestamp2);
    });
  });

  describe("Token Existence", function () {
    it("Should return correct existence status", async function () {
      expect(await bridge.exists(0)).to.be.false;

      const testAssetHash = ethers.keccak256(ethers.toUtf8Bytes("GOLD-BAR-007"));
      await bridge.mintPreciousMetal(
        user1.address,
        testAssetHash,
        ethers.keccak256(ethers.toUtf8Bytes("SN-55555")),
        GOLD,
        1000000,
        999,
        "ipfs://QmGold",
        IPFS,
        ZURICH
      );

      expect(await bridge.exists(0)).to.be.true;
      expect(await bridge.exists(1)).to.be.false;
    });
  });
});
