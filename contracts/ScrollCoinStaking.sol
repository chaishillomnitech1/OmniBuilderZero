// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";
import "@openzeppelin/contracts/utils/Pausable.sol";

/**
 * @title ScrollCoinStaking
 * @dev Staking contract for ScrollCoin with time-lock privilege escalation
 * @notice Enables ScrollCoin holders to stake tokens and unlock AscendancyID privileges
 */
contract ScrollCoinStaking is Ownable, ReentrancyGuard, Pausable {
    using SafeERC20 for IERC20;

    // ScrollCoin token interface
    IERC20 public immutable scrollCoin;

    // Staking position structure
    struct StakingPosition {
        uint256 amount;           // Amount of SCROLL staked
        uint256 startTime;        // Timestamp when stake began
        uint256 lockDuration;     // Lock duration in seconds
        uint256 endTime;          // Unlock timestamp
        uint8 tierAtStake;        // Tier achieved with this stake
        uint256 rewardDebt;       // Reward debt for calculation
        bool active;              // Whether position is active
    }

    // User staking data
    mapping(address => StakingPosition) public stakingPositions;

    // Privilege tier thresholds (in base units, 18 decimals)
    uint256 public constant TIER_BRONZE_THRESHOLD = 1_000 * 1e18;
    uint256 public constant TIER_SILVER_THRESHOLD = 10_000 * 1e18;
    uint256 public constant TIER_GOLD_THRESHOLD = 50_000 * 1e18;
    uint256 public constant TIER_PLATINUM_THRESHOLD = 100_000 * 1e18;
    uint256 public constant TIER_DIAMOND_THRESHOLD = 500_000 * 1e18;

    // Lock duration requirements (in seconds)
    uint256 public constant LOCK_BRONZE = 30 days;
    uint256 public constant LOCK_SILVER = 90 days;
    uint256 public constant LOCK_GOLD = 180 days;
    uint256 public constant LOCK_PLATINUM = 365 days;
    uint256 public constant LOCK_DIAMOND = 730 days;

    // Reward parameters
    uint256 public rewardRatePerSecond;      // Base reward rate per second per token
    uint256 public accRewardPerShare;        // Accumulated rewards per share
    uint256 public lastRewardTime;           // Last reward update timestamp
    uint256 public totalStaked;              // Total tokens staked

    // Early withdrawal penalty (basis points, 2000 = 20%)
    uint256 public constant EARLY_WITHDRAWAL_PENALTY = 2000;
    uint256 public constant BASIS_POINTS = 10000;

    // Treasury for penalties
    address public treasury;

    // AscendancyID integration
    address public ascendancyIdContract;

    // Events
    event Staked(
        address indexed user,
        uint256 amount,
        uint256 duration,
        uint256 unlockTime,
        uint8 tier
    );
    event Unstaked(
        address indexed user,
        uint256 amount,
        uint256 penalty,
        bool early
    );
    event RewardsClaimed(address indexed user, uint256 amount);
    event TierUpgraded(address indexed user, uint8 oldTier, uint8 newTier);
    event RewardRateUpdated(uint256 oldRate, uint256 newRate);
    event TreasuryUpdated(address oldTreasury, address newTreasury);
    event AscendancyIdContractUpdated(address oldContract, address newContract);

    /**
     * @dev Constructor
     * @param _scrollCoin Address of the ScrollCoin token
     * @param _treasury Address of the treasury for penalty collection
     * @param _rewardRatePerSecond Initial reward rate per second per token
     */
    constructor(
        address _scrollCoin,
        address _treasury,
        uint256 _rewardRatePerSecond
    ) Ownable(msg.sender) {
        require(_scrollCoin != address(0), "Invalid token address");
        require(_treasury != address(0), "Invalid treasury address");

        scrollCoin = IERC20(_scrollCoin);
        treasury = _treasury;
        rewardRatePerSecond = _rewardRatePerSecond;
        lastRewardTime = block.timestamp;
    }

    /**
     * @dev Update accumulated rewards
     */
    function updateRewards() public {
        if (block.timestamp <= lastRewardTime || totalStaked == 0) {
            lastRewardTime = block.timestamp;
            return;
        }

        uint256 timeElapsed = block.timestamp - lastRewardTime;
        uint256 rewards = timeElapsed * rewardRatePerSecond;
        accRewardPerShare += (rewards * 1e12) / totalStaked;
        lastRewardTime = block.timestamp;
    }

    /**
     * @dev Stake ScrollCoin tokens
     * @param amount Amount of tokens to stake
     * @param lockDuration Duration to lock tokens (in seconds)
     */
    function stake(
        uint256 amount,
        uint256 lockDuration
    ) external nonReentrant whenNotPaused {
        require(amount > 0, "Cannot stake 0");
        require(!stakingPositions[msg.sender].active, "Already staking");
        require(
            lockDuration >= LOCK_BRONZE,
            "Lock duration too short"
        );

        updateRewards();

        // Calculate tier based on amount and duration
        uint8 tier = calculateTier(amount, lockDuration);

        // Transfer tokens from user
        scrollCoin.safeTransferFrom(msg.sender, address(this), amount);

        // Create staking position
        stakingPositions[msg.sender] = StakingPosition({
            amount: amount,
            startTime: block.timestamp,
            lockDuration: lockDuration,
            endTime: block.timestamp + lockDuration,
            tierAtStake: tier,
            rewardDebt: (amount * accRewardPerShare) / 1e12,
            active: true
        });

        totalStaked += amount;

        // Notify AscendancyID contract if set
        if (ascendancyIdContract != address(0)) {
            _notifyPrivilegeChange(msg.sender, tier);
        }

        emit Staked(msg.sender, amount, lockDuration, block.timestamp + lockDuration, tier);
    }

    /**
     * @dev Add more tokens to existing stake
     * @param additionalAmount Amount of additional tokens to stake
     */
    function addToStake(uint256 additionalAmount) external nonReentrant whenNotPaused {
        require(additionalAmount > 0, "Cannot add 0");
        require(stakingPositions[msg.sender].active, "No active stake");

        updateRewards();
        
        StakingPosition storage position = stakingPositions[msg.sender];
        
        // Claim pending rewards first
        uint256 pending = pendingRewards(msg.sender);
        if (pending > 0) {
            _safeRewardTransfer(msg.sender, pending);
            emit RewardsClaimed(msg.sender, pending);
        }

        // Transfer additional tokens
        scrollCoin.safeTransferFrom(msg.sender, address(this), additionalAmount);

        // Update position
        uint256 newAmount = position.amount + additionalAmount;
        uint8 oldTier = position.tierAtStake;
        uint8 newTier = calculateTier(newAmount, position.lockDuration);

        position.amount = newAmount;
        position.tierAtStake = newTier;
        position.rewardDebt = (newAmount * accRewardPerShare) / 1e12;

        totalStaked += additionalAmount;

        // Notify tier upgrade if changed
        if (newTier > oldTier && ascendancyIdContract != address(0)) {
            _notifyPrivilegeChange(msg.sender, newTier);
            emit TierUpgraded(msg.sender, oldTier, newTier);
        }
    }

    /**
     * @dev Extend lock duration
     * @param additionalDuration Additional time to add to lock (in seconds)
     */
    function extendLock(uint256 additionalDuration) external nonReentrant {
        require(stakingPositions[msg.sender].active, "No active stake");
        require(additionalDuration > 0, "Invalid duration");

        StakingPosition storage position = stakingPositions[msg.sender];
        
        uint256 newDuration = position.lockDuration + additionalDuration;
        uint8 oldTier = position.tierAtStake;
        uint8 newTier = calculateTier(position.amount, newDuration);

        position.lockDuration = newDuration;
        position.endTime = position.startTime + newDuration;
        position.tierAtStake = newTier;

        // Notify tier upgrade if changed
        if (newTier > oldTier && ascendancyIdContract != address(0)) {
            _notifyPrivilegeChange(msg.sender, newTier);
            emit TierUpgraded(msg.sender, oldTier, newTier);
        }
    }

    /**
     * @dev Unstake tokens
     * @notice Early withdrawal incurs a 20% penalty
     */
    function unstake() external nonReentrant {
        StakingPosition storage position = stakingPositions[msg.sender];
        require(position.active, "No active stake");

        updateRewards();

        uint256 amount = position.amount;
        uint256 penalty = 0;
        bool isEarly = block.timestamp < position.endTime;

        // Claim pending rewards
        uint256 pending = pendingRewards(msg.sender);
        if (pending > 0) {
            _safeRewardTransfer(msg.sender, pending);
            emit RewardsClaimed(msg.sender, pending);
        }

        // Calculate penalty for early withdrawal
        if (isEarly) {
            penalty = (amount * EARLY_WITHDRAWAL_PENALTY) / BASIS_POINTS;
            // Send penalty to treasury
            scrollCoin.safeTransfer(treasury, penalty);
        }

        // Transfer remaining tokens to user
        uint256 withdrawAmount = amount - penalty;
        scrollCoin.safeTransfer(msg.sender, withdrawAmount);

        // Clear staking position
        totalStaked -= amount;
        delete stakingPositions[msg.sender];

        // Notify AscendancyID contract of privilege loss
        if (ascendancyIdContract != address(0)) {
            _notifyPrivilegeChange(msg.sender, 0);
        }

        emit Unstaked(msg.sender, withdrawAmount, penalty, isEarly);
    }

    /**
     * @dev Claim pending rewards without unstaking
     */
    function claimRewards() external nonReentrant {
        updateRewards();

        uint256 pending = pendingRewards(msg.sender);
        require(pending > 0, "No rewards to claim");

        StakingPosition storage position = stakingPositions[msg.sender];
        position.rewardDebt = (position.amount * accRewardPerShare) / 1e12;

        _safeRewardTransfer(msg.sender, pending);

        emit RewardsClaimed(msg.sender, pending);
    }

    /**
     * @dev Calculate pending rewards for a user
     * @param user Address to check rewards for
     * @return Pending reward amount
     */
    function pendingRewards(address user) public view returns (uint256) {
        StakingPosition storage position = stakingPositions[user];
        if (!position.active) {
            return 0;
        }

        uint256 currentAccRewardPerShare = accRewardPerShare;
        
        if (block.timestamp > lastRewardTime && totalStaked > 0) {
            uint256 timeElapsed = block.timestamp - lastRewardTime;
            uint256 rewards = timeElapsed * rewardRatePerSecond;
            currentAccRewardPerShare += (rewards * 1e12) / totalStaked;
        }

        return (position.amount * currentAccRewardPerShare) / 1e12 - position.rewardDebt;
    }

    /**
     * @dev Calculate privilege tier based on amount and duration
     * @param amount Amount of tokens staked
     * @param duration Lock duration in seconds
     * @return tier Privilege tier (0-5)
     */
    function calculateTier(
        uint256 amount,
        uint256 duration
    ) public pure returns (uint8) {
        if (amount >= TIER_DIAMOND_THRESHOLD && duration >= LOCK_DIAMOND) {
            return 5; // Diamond
        }
        if (amount >= TIER_PLATINUM_THRESHOLD && duration >= LOCK_PLATINUM) {
            return 4; // Platinum
        }
        if (amount >= TIER_GOLD_THRESHOLD && duration >= LOCK_GOLD) {
            return 3; // Gold
        }
        if (amount >= TIER_SILVER_THRESHOLD && duration >= LOCK_SILVER) {
            return 2; // Silver
        }
        if (amount >= TIER_BRONZE_THRESHOLD && duration >= LOCK_BRONZE) {
            return 1; // Bronze
        }
        return 0; // Initiate (no privileges)
    }

    /**
     * @dev Get staked amount for a user
     * @param user Address to check
     * @return Staked amount
     */
    function getStakedAmount(address user) external view returns (uint256) {
        return stakingPositions[user].amount;
    }

    /**
     * @dev Get unlock time for a user
     * @param user Address to check
     * @return Unlock timestamp
     */
    function getUnlockTime(address user) external view returns (uint256) {
        return stakingPositions[user].endTime;
    }

    /**
     * @dev Get current tier for a user
     * @param user Address to check
     * @return Current privilege tier
     */
    function getCurrentTier(address user) external view returns (uint8) {
        return stakingPositions[user].tierAtStake;
    }

    /**
     * @dev Check if user can unstake without penalty
     * @param user Address to check
     * @return Whether unlock time has passed
     */
    function canUnstakeWithoutPenalty(address user) external view returns (bool) {
        StakingPosition storage position = stakingPositions[user];
        return position.active && block.timestamp >= position.endTime;
    }

    /**
     * @dev Internal function to transfer rewards safely
     * @param to Address to transfer rewards to
     * @param amount Amount to transfer
     */
    function _safeRewardTransfer(address to, uint256 amount) internal {
        uint256 balance = scrollCoin.balanceOf(address(this)) - totalStaked;
        if (amount > balance) {
            scrollCoin.safeTransfer(to, balance);
        } else {
            scrollCoin.safeTransfer(to, amount);
        }
    }

    /**
     * @dev Internal function to notify AscendancyID contract of privilege changes
     * @param user Address whose privileges changed
     * @param newTier New privilege tier
     */
    function _notifyPrivilegeChange(address user, uint8 newTier) internal {
        // This will call the AscendancyID contract when integrated
        // For now, emit an event that can be listened to
        emit TierUpgraded(user, stakingPositions[user].tierAtStake, newTier);
    }

    // Admin functions

    /**
     * @dev Update reward rate
     * @param newRate New reward rate per second per token
     */
    function setRewardRate(uint256 newRate) external onlyOwner {
        updateRewards();
        uint256 oldRate = rewardRatePerSecond;
        rewardRatePerSecond = newRate;
        emit RewardRateUpdated(oldRate, newRate);
    }

    /**
     * @dev Update treasury address
     * @param newTreasury New treasury address
     */
    function setTreasury(address newTreasury) external onlyOwner {
        require(newTreasury != address(0), "Invalid treasury");
        address oldTreasury = treasury;
        treasury = newTreasury;
        emit TreasuryUpdated(oldTreasury, newTreasury);
    }

    /**
     * @dev Set AscendancyID contract address
     * @param newContract New AscendancyID contract address
     */
    function setAscendancyIdContract(address newContract) external onlyOwner {
        address oldContract = ascendancyIdContract;
        ascendancyIdContract = newContract;
        emit AscendancyIdContractUpdated(oldContract, newContract);
    }

    /**
     * @dev Pause staking
     */
    function pause() external onlyOwner {
        _pause();
    }

    /**
     * @dev Unpause staking
     */
    function unpause() external onlyOwner {
        _unpause();
    }

    /**
     * @dev Deposit reward tokens
     * @param amount Amount of reward tokens to deposit
     */
    function depositRewardTokens(uint256 amount) external onlyOwner {
        scrollCoin.safeTransferFrom(msg.sender, address(this), amount);
    }

    /**
     * @dev Emergency withdraw (owner only, for stuck tokens)
     * @param token Address of token to withdraw
     * @param amount Amount to withdraw
     */
    function emergencyWithdraw(address token, uint256 amount) external onlyOwner {
        require(token != address(scrollCoin) || amount <= scrollCoin.balanceOf(address(this)) - totalStaked, "Cannot withdraw staked tokens");
        IERC20(token).safeTransfer(owner(), amount);
    }
}
