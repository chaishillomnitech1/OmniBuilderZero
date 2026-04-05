const { expect } = require("chai");
const { ethers } = require("hardhat");
const { time } = require("@nomicfoundation/hardhat-network-helpers");

describe("Legacy of Light NFT Collection", function () {
  let nft721, nft1155;
  let owner, treasury, user1, user2, architex;
  let deploymentTimestamp;

  beforeEach(async function () {
    // Get signers
    [owner, treasury, user1, user2, architex] = await ethers.getSigners();

    // Deploy ERC-721 contract
    const LegacyOfLightNFT = await ethers.getContractFactory("LegacyOfLightNFT");
    nft721 = await LegacyOfLightNFT.deploy(treasury.address);
    await nft721.waitForDeployment();

    // Deploy ERC-1155 contract
    const LegacyOfLightNFT1155 = await ethers.getContractFactory("LegacyOfLightNFT1155");
    nft1155 = await LegacyOfLightNFT1155.deploy(treasury.address, "ipfs://base/");
    await nft1155.waitForDeployment();

    // Store deployment timestamp
    deploymentTimestamp = await nft721.otcpDeploymentTimestamp();
  });

  describe("ERC-721 Contract", function () {
    describe("Deployment", function () {
      it("Should set the correct name and symbol", async function () {
        expect(await nft721.name()).to.equal("Legacy of Light: Prophetic Omnichords");
        expect(await nft721.symbol()).to.equal("LLPO");
      });

      it("Should set the KUN Coin Treasury", async function () {
        expect(await nft721.kunCoinTreasury()).to.equal(treasury.address);
      });

      it("Should record OTCP deployment timestamp", async function () {
        expect(deploymentTimestamp).to.be.gt(0);
      });

      it("Should authorize deployer as ARCHITEX", async function () {
        expect(await nft721.architexAuthorized(owner.address)).to.be.true;
      });
    });

    describe("Minting", function () {
      it("Should mint a new OmniTape", async function () {
        const releaseDate = 1640995200; // Fixed timestamp: 2022-01-01
        const tx = await nft721.mintOmniTape(
          user1.address,
          "Prophetic Vision #1",
          "Chais The Great",
          1,
          releaseDate,
          "ipfs://QmTest123",
          0 // IPFS
        );

        await expect(tx)
          .to.emit(nft721, "OmniTapeMinted")
          .withArgs(0, user1.address, "Prophetic Vision #1", 1, 0);

        expect(await nft721.ownerOf(0)).to.equal(user1.address);
        expect(await nft721.totalSupply()).to.equal(1);
      });

      it("Should store OmniTape metadata correctly", async function () {
        const releaseDate = 1672531200; // Fixed timestamp: 2023-01-01
        await nft721.mintOmniTape(
          user1.address,
          "Sacred Harmonics",
          "OmniTech Collective",
          42,
          releaseDate,
          "ar://ArweaveHash",
          1 // Arweave
        );

        const tape = await nft721.getOmniTape(0);
        expect(tape.title).to.equal("Sacred Harmonics");
        expect(tape.artist).to.equal("OmniTech Collective");
        expect(tape.catalogNumber).to.equal(42);
        expect(tape.releaseDate).to.equal(releaseDate);
        expect(tape.storageURI).to.equal("ar://ArweaveHash");
        expect(tape.storageType).to.equal(1);
      });

      it("Should batch mint multiple OmniTapes", async function () {
        const recipients = [user1.address, user1.address, user2.address];
        const titles = ["Song 1", "Song 2", "Song 3"];
        const artists = ["Artist 1", "Artist 2", "Artist 3"];
        const catalogNumbers = [1, 2, 3];
        const releaseDates = [1000, 2000, 3000];
        const storageURIs = ["ipfs://1", "ipfs://2", "ipfs://3"];
        const storageTypes = [0, 0, 1];

        await nft721.batchMintOmniTapes(
          recipients,
          titles,
          artists,
          catalogNumbers,
          releaseDates,
          storageURIs,
          storageTypes
        );

        expect(await nft721.totalSupply()).to.equal(3);
        expect(await nft721.ownerOf(0)).to.equal(user1.address);
        expect(await nft721.ownerOf(2)).to.equal(user2.address);
      });

      it("Should revert when minting to zero address", async function () {
        await expect(
          nft721.mintOmniTape(
            ethers.ZeroAddress,
            "Test",
            "Artist",
            1,
            1000,
            "ipfs://test",
            0
          )
        ).to.be.revertedWith("Invalid recipient");
      });

      it("Should only allow owner to mint", async function () {
        await expect(
          nft721.connect(user1).mintOmniTape(
            user1.address,
            "Test",
            "Artist",
            1,
            1000,
            "ipfs://test",
            0
          )
        ).to.be.reverted;
      });
    });

    describe("ARCHITEX OwnerOverride", function () {
      beforeEach(async function () {
        // Mint a token to user1
        await nft721.mintOmniTape(
          user1.address,
          "Test Song",
          "Test Artist",
          1,
          1000,
          "ipfs://test",
          0
        );
      });

      it("Should allow authorized ARCHITEX to override ownership", async function () {
        // Authorize architex
        await nft721.setArchitexAuthorization(architex.address, true);

        // Execute override
        await expect(
          nft721.connect(architex).ownerOverride(0, user2.address)
        )
          .to.emit(nft721, "OwnerOverrideExecuted")
          .withArgs(architex.address, 0, user2.address);

        expect(await nft721.ownerOf(0)).to.equal(user2.address);
      });

      it("Should revert when unauthorized address attempts override", async function () {
        await expect(
          nft721.connect(user1).ownerOverride(0, user2.address)
        ).to.be.revertedWith("Not authorized ARCHITEX");
      });

      it("Should allow owner to authorize/deauthorize ARCHITEX", async function () {
        await expect(nft721.setArchitexAuthorization(architex.address, true))
          .to.emit(nft721, "ArchitexAuthorized")
          .withArgs(architex.address, true);

        expect(await nft721.architexAuthorized(architex.address)).to.be.true;

        await nft721.setArchitexAuthorization(architex.address, false);
        expect(await nft721.architexAuthorized(architex.address)).to.be.false;
      });
    });

    describe("KUN Coin Treasury", function () {
      it("Should update treasury address", async function () {
        const newTreasury = user1.address;
        await expect(nft721.updateKunCoinTreasury(newTreasury))
          .to.emit(nft721, "KunCoinTreasuryUpdated")
          .withArgs(treasury.address, newTreasury);

        expect(await nft721.kunCoinTreasury()).to.equal(newTreasury);
      });

      it("Should revert when updating to zero address", async function () {
        await expect(
          nft721.updateKunCoinTreasury(ethers.ZeroAddress)
        ).to.be.revertedWith("Invalid treasury address");
      });
    });

    describe("Royalties", function () {
      beforeEach(async function () {
        await nft721.mintOmniTape(
          user1.address,
          "Test",
          "Artist",
          1,
          1000,
          "ipfs://test",
          0
        );
      });

      it("Should return correct royalty info", async function () {
        const salePrice = ethers.parseEther("1");
        const royaltyInfo = await nft721.royaltyInfo(0, salePrice);

        expect(royaltyInfo[0]).to.equal(treasury.address);
        // 10% royalty = 0.1 ETH
        expect(royaltyInfo[1]).to.equal(ethers.parseEther("0.1"));
      });
    });

    describe("OTCP Functions", function () {
      it("Should calculate elapsed time since deployment", async function () {
        // Advance time by 1 hour
        await time.increase(3600);

        const elapsed = await nft721.getOTCPElapsedTime();
        expect(elapsed).to.be.gte(3600);
      });

      it("Should have immutable deployment timestamp", async function () {
        const timestamp1 = await nft721.otcpDeploymentTimestamp();
        
        // Mine some blocks
        await time.increase(100);
        
        const timestamp2 = await nft721.otcpDeploymentTimestamp();
        expect(timestamp1).to.equal(timestamp2);
      });
    });
  });

  describe("ERC-1155 Contract", function () {
    describe("Deployment", function () {
      it("Should set the correct name and symbol", async function () {
        expect(await nft1155.name()).to.equal("Legacy of Light: Prophetic Omnichords Multi-Edition");
        expect(await nft1155.symbol()).to.equal("LLPOME");
      });

      it("Should set the KUN Coin Treasury", async function () {
        expect(await nft1155.kunCoinTreasury()).to.equal(treasury.address);
      });

      it("Should record OTCP deployment timestamp", async function () {
        const timestamp = await nft1155.otcpDeploymentTimestamp();
        expect(timestamp).to.be.gt(0);
      });
    });

    describe("Creating and Minting", function () {
      it("Should create a new OmniTape type", async function () {
        const tx = await nft1155.createOmniTape(
          "Multi-Edition Song",
          "Artist",
          1,
          1000,
          "ipfs://test",
          0,
          100 // max supply
        );

        await expect(tx)
          .to.emit(nft1155, "OmniTapeCreated")
          .withArgs(0, "Multi-Edition Song", 1, 100, 0);

        expect(await nft1155.totalOmniTapeTypes()).to.equal(1);
      });

      it("Should mint editions of an OmniTape", async function () {
        await nft1155.createOmniTape(
          "Song",
          "Artist",
          1,
          1000,
          "ipfs://test",
          0,
          100
        );

        await expect(nft1155.mintOmniTape(0, user1.address, 10))
          .to.emit(nft1155, "OmniTapeMinted")
          .withArgs(0, user1.address, 10);

        expect(await nft1155.balanceOf(user1.address, 0)).to.equal(10);
        expect(await nft1155.totalSupply(0)).to.equal(10);
      });

      it("Should enforce max supply", async function () {
        await nft1155.createOmniTape(
          "Limited",
          "Artist",
          1,
          1000,
          "ipfs://test",
          0,
          5 // max 5 editions
        );

        await nft1155.mintOmniTape(0, user1.address, 5);

        await expect(
          nft1155.mintOmniTape(0, user1.address, 1)
        ).to.be.revertedWith("Exceeds max supply");
      });

      it("Should allow unlimited supply when maxSupply is 0", async function () {
        await nft1155.createOmniTape(
          "Unlimited",
          "Artist",
          1,
          1000,
          "ipfs://test",
          0,
          0 // unlimited
        );

        await nft1155.mintOmniTape(0, user1.address, 1000);
        await nft1155.mintOmniTape(0, user2.address, 1000);

        expect(await nft1155.totalSupply(0)).to.equal(2000);
      });
    });

    describe("ARCHITEX OwnerOverride (1155)", function () {
      beforeEach(async function () {
        await nft1155.createOmniTape("Song", "Artist", 1, 1000, "ipfs://test", 0, 100);
        await nft1155.mintOmniTape(0, user1.address, 50);
        await nft1155.setArchitexAuthorization(architex.address, true);
      });

      it("Should allow ARCHITEX to override transfer", async function () {
        await expect(
          nft1155.connect(architex).ownerOverride(user1.address, user2.address, 0, 10)
        )
          .to.emit(nft1155, "OwnerOverrideExecuted")
          .withArgs(architex.address, 0, user1.address, user2.address, 10);

        expect(await nft1155.balanceOf(user1.address, 0)).to.equal(40);
        expect(await nft1155.balanceOf(user2.address, 0)).to.equal(10);
      });

      it("Should revert when unauthorized", async function () {
        await expect(
          nft1155.connect(user1).ownerOverride(user1.address, user2.address, 0, 10)
        ).to.be.revertedWith("Not authorized ARCHITEX");
      });
    });

    describe("Royalties (1155)", function () {
      beforeEach(async function () {
        await nft1155.createOmniTape("Song", "Artist", 1, 1000, "ipfs://test", 0, 100);
      });

      it("Should return correct royalty info", async function () {
        const salePrice = ethers.parseEther("1");
        const royaltyInfo = await nft1155.royaltyInfo(0, salePrice);

        expect(royaltyInfo[0]).to.equal(treasury.address);
        expect(royaltyInfo[1]).to.equal(ethers.parseEther("0.1")); // 10%
      });
    });
  });
});
