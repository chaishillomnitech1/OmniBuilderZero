# GitHub Labels Configuration for OmniBuilderZero
# This file documents the recommended labels for issues and pull requests
# Repository admins can create these labels via Settings -> Issues -> Labels

# Type Labels (what kind of change)
- name: "bug"
  color: "d73a4a"
  description: "Something isn't working"

- name: "feature"
  color: "a2eeef"
  description: "New feature or request"

- name: "enhancement"
  color: "a2eeef"
  description: "Improvement to existing feature"

- name: "documentation"
  color: "0075ca"
  description: "Improvements or additions to documentation"

- name: "security"
  color: "ee0701"
  description: "Security vulnerability or improvement"

- name: "performance"
  color: "f9d0c4"
  description: "Performance improvement"

- name: "refactor"
  color: "fbca04"
  description: "Code refactoring"

- name: "test"
  color: "1d76db"
  description: "Adding or improving tests"

# Priority Labels
- name: "priority: critical"
  color: "b60205"
  description: "Critical priority - immediate attention required"

- name: "priority: high"
  color: "d93f0b"
  description: "High priority"

- name: "priority: medium"
  color: "fbca04"
  description: "Medium priority"

- name: "priority: low"
  color: "0e8a16"
  description: "Low priority"

# Status Labels
- name: "status: needs review"
  color: "ededed"
  description: "Waiting for review"

- name: "status: in progress"
  color: "c5def5"
  description: "Currently being worked on"

- name: "status: blocked"
  color: "d93f0b"
  description: "Blocked by another issue or dependency"

- name: "status: on hold"
  color: "fef2c0"
  description: "Work has been paused"

# Area Labels (component affected)
- name: "area: contracts"
  color: "bfdadc"
  description: "Smart contracts"

- name: "area: tests"
  color: "bfdadc"
  description: "Test infrastructure"

- name: "area: deployment"
  color: "bfdadc"
  description: "Deployment scripts and processes"

- name: "area: ci/cd"
  color: "bfdadc"
  description: "CI/CD workflows and automation"

- name: "area: phase2"
  color: "bfdadc"
  description: "Phase 2 automation and partnerships"

- name: "area: flame-academy"
  color: "bfdadc"
  description: "FlameAcademy educational content"

- name: "area: dao"
  color: "bfdadc"
  description: "DAO governance and automation"

# Difficulty Labels (for contributors)
- name: "good first issue"
  color: "7057ff"
  description: "Good for newcomers"

- name: "help wanted"
  color: "008672"
  description: "Extra attention is needed"

- name: "difficulty: easy"
  color: "c2e0c6"
  description: "Easy difficulty"

- name: "difficulty: medium"
  color: "fbca04"
  description: "Medium difficulty"

- name: "difficulty: hard"
  color: "d93f0b"
  description: "Hard difficulty"

# Process Labels
- name: "dependencies"
  color: "0366d6"
  description: "Dependency updates"

- name: "automated"
  color: "ededed"
  description: "Automated process (e.g., Dependabot)"

- name: "dao-governance"
  color: "5319e7"
  description: "DAO governance decision required"

- name: "community-approved"
  color: "0e8a16"
  description: "Approved by community/DAO vote"

- name: "needs-discussion"
  color: "d4c5f9"
  description: "Needs further discussion"

- name: "breaking-change"
  color: "b60205"
  description: "Breaking change requiring major version bump"

# Network Labels
- name: "network: mainnet"
  color: "1d76db"
  description: "Related to mainnet deployment"

- name: "network: testnet"
  color: "c5def5"
  description: "Related to testnet deployment"

- name: "network: scroll"
  color: "ff6b6b"
  description: "Scroll blockchain specific"

- name: "network: polygon"
  color: "8b5cf6"
  description: "Polygon blockchain specific"

# Special Labels
- name: "duplicate"
  color: "cfd3d7"
  description: "This issue or pull request already exists"

- name: "invalid"
  color: "e4e669"
  description: "This doesn't seem right"

- name: "wontfix"
  color: "ffffff"
  description: "This will not be worked on"

- name: "question"
  color: "d876e3"
  description: "Further information is requested"

- name: "quantum-security"
  color: "5319e7"
  description: "Related to quantum-resistant features"

- name: "scrollverse"
  color: "ffd700"
  description: "ScrollVerse ecosystem related"

# INSTRUCTIONS FOR REPOSITORY ADMINS:
# To create these labels, you can:
# 1. Manually create via GitHub UI: Settings -> Issues -> Labels -> New label
# 2. Use GitHub CLI: gh label create "label-name" --color "hex-color" --description "description"
# 3. Use a label sync tool like: https://github.com/Financial-Times/github-label-sync
