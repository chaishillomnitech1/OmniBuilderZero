# Polygon Amoy Migration and Mainnet Deployment Controls

**Updated:** 2026-11-15  
**Status:** Configuration and deployment controls under review; no release approval.

## Network targets

| Target | Chain ID | Hardhat alias | Provider variable |
|---|---:|---|---|
| Polygon Amoy testnet | 80002 | `polygonAmoy` | `AMOY_RPC_URL` |
| Polygon PoS mainnet | 137 | `polygon` | `POLYGON_RPC_URL` |

Polygon Mumbai (80001) is retired. Do not use Mumbai RPC endpoints, explorer URLs, or network aliases.

## Amoy rehearsal

1. Configure a maintained provider URL in the secure runtime as `AMOY_RPC_URL`.
2. Use a dedicated testnet deployer key with no production funds.
3. Set explicit non-zero `KUN_COIN_TREASURY` and `OWNER_MULTISIG_ADDRESS`.
4. Set `BASE_URI` to a real IPFS, Arweave, or HTTPS metadata URI; the preflight rejects placeholder values.
5. Ensure the multisig contract is deployed on Amoy and verify its owners and threshold.
6. Run tests and compile before deploying.
7. Execute `npm run deploy:polygon-amoy` only after the exact source and constructor arguments have been reviewed.
8. Retain the deployment manifest, transaction hashes, chain ID, contract addresses, owner readbacks, and explorer verification records.

## Deployment safety implemented in this workstream

The deployment preflight requires explicit treasury, multisig, and metadata values. It rejects zero addresses and placeholder URIs. The deployment script requires multisig bytecode on the selected network, transfers the ARCHITEX privilege to the multisig, revokes the deployer's ARCHITEX privilege, transfers Ownable ownership to the multisig, and reads back owners, treasury values, and ARCHITEX roles. Deployment output remains pending external source verification.

The contract constructors explicitly initialize OpenZeppelin Ownable v5 with the deployer as the temporary owner. The deployment script transfers control to the multisig before reporting successful custody verification.

## Polygon mainnet gate

The `polygon` network (chain ID 137) additionally requires the exact `MAINNET_RELEASE_CONFIRMATION` value enforced by the preflight. This is a technical guard, not a substitute for human release approval.

Before mainnet:
- Independent security audit of exact source commit and dependency lockfile.
- Passing unit, integration, invariant, fuzz, and deployment-preflight tests.
- Reproducible compiler settings and verified explorer source.
- Multisig owners/threshold and all contract owner roles reviewed.
- Explicit treasury and metadata values verified.
- NFT owner and ARCHITEX permissions read back from chain.
- Emergency controls, admin powers, royalty logic, and recovery procedures reviewed.
- Release manifest binds source commit, audit, tests, chain ID, deployment transactions, contract addresses, and multisig approvals.
- Human approval for the exact release.

## Contributor reward workflow

The current GitHub contributor reward workflow calculates and comments on points only. It does not connect to a chain, call a rewards contract, mint tokens, or transfer funds. Do not describe simulated points as CHX paid or tokens distributed. The workflow's no-transfer statement is part of the evidence record.

## Preservation

Historical Mumbai screenshots, docs, and deployment notes remain preserved. Mark superseded instructions as historical; do not delete or rewrite archival evidence.
