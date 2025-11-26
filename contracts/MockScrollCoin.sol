// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

/**
 * @title MockScrollCoin
 * @dev Mock ERC20 token for testing ScrollCoinStaking
 * @notice This contract is for testing purposes only
 */
contract MockScrollCoin is ERC20, Ownable {
    uint256 public constant INITIAL_SUPPLY = 10_000_000_000 * 1e18; // 10 billion tokens

    constructor() ERC20("ScrollCoin", "SCROLL") Ownable(msg.sender) {
        _mint(msg.sender, INITIAL_SUPPLY);
    }

    /**
     * @dev Mint tokens (for testing)
     * @param to Address to mint to
     * @param amount Amount to mint
     */
    function mint(address to, uint256 amount) external onlyOwner {
        _mint(to, amount);
    }

    /**
     * @dev Faucet function for testing
     * @param amount Amount to receive (max 100,000 SCROLL)
     */
    function faucet(uint256 amount) external {
        require(amount <= 100_000 * 1e18, "Max 100,000 SCROLL per request");
        _mint(msg.sender, amount);
    }
}
