require("@nomicfoundation/hardhat-toolbox");
require("dotenv").config();

const deployerAccounts = process.env.PRIVATE_KEY ? [process.env.PRIVATE_KEY] : [];
const networks = {
  // Ethereum and Scroll paths remain separate network tracks.
  mainnet: {
    url: process.env.MAINNET_RPC_URL || "https://eth-mainnet.g.alchemy.com/v2/YOUR-API-KEY",
    accounts: deployerAccounts,
    chainId: 1,
  },
  sepolia: {
    url: process.env.SEPOLIA_RPC_URL || "https://eth-sepolia.g.alchemy.com/v2/YOUR-API-KEY",
    accounts: deployerAccounts,
    chainId: 11155111,
  },
  scrollSepolia: {
    url: process.env.SCROLL_SEPOLIA_RPC_URL || "https://sepolia-rpc.scroll.io",
    accounts: deployerAccounts,
    chainId: 534351,
  },
  scroll: {
    url: process.env.SCROLL_RPC_URL || "https://rpc.scroll.io",
    accounts: deployerAccounts,
    chainId: 534352,
  },
  hardhat: { chainId: 31337 },
};

// Polygon PoS targets require dedicated, explicitly configured RPC endpoints.
if (process.env.AMOY_RPC_URL) {
  networks.polygonAmoy = { url: process.env.AMOY_RPC_URL, accounts: deployerAccounts, chainId: 80002 };
}
if (process.env.POLYGON_RPC_URL) {
  networks.polygon = { url: process.env.POLYGON_RPC_URL, accounts: deployerAccounts, chainId: 137 };
}

/** @type import('hardhat/config').HardhatUserConfig */
module.exports = {
  solidity: {
    version: "0.8.24",
    settings: { optimizer: { enabled: true, runs: 200 }, viaIR: true },
  },
  networks,
  etherscan: {
    apiKey: {
      mainnet: process.env.ETHERSCAN_API_KEY || "",
      sepolia: process.env.ETHERSCAN_API_KEY || "",
      polygon: process.env.POLYGONSCAN_API_KEY || "",
      polygonAmoy: process.env.POLYGONSCAN_API_KEY || "",
      scrollSepolia: process.env.SCROLLSCAN_API_KEY || "",
      scroll: process.env.SCROLLSCAN_API_KEY || "",
    },
    customChains: [
      {
        network: "polygonAmoy",
        chainId: 80002,
        urls: {
          apiURL: "https://api-amoy.polygonscan.com/api",
          browserURL: "https://amoy.polygonscan.com",
        },
      },
      {
        network: "scrollSepolia",
        chainId: 534351,
        urls: {
          apiURL: "https://api-sepolia.scrollscan.com/api",
          browserURL: "https://sepolia.scrollscan.com",
        },
      },
      {
        network: "scroll",
        chainId: 534352,
        urls: {
          apiURL: "https://api.scrollscan.com/api",
          browserURL: "https://scrollscan.com",
        },
      },
    ],
  },
  paths: {
    sources: "./contracts",
    tests: "./test",
    cache: "./cache",
    artifacts: "./artifacts",
  },
};
