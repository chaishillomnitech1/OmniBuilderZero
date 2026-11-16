# OmniBuilderZero Shared Build Orchestration Audit

**Date:** 2026-11-16  
**Scope:** GitHub Actions build, test, security, release, and deployment workflows  
**Base:** `main`  
**Status:** Evidence-backed assessment; no workflow behavior changed

## Executive finding

OmniBuilderZero has a strong candidate for a shared orchestration layer, but the right boundary is **shared preparation and verification primitives**, not one monolithic workflow.

The current workflows repeat Node.js setup, npm cache configuration, `npm ci`, and in several cases contract compilation and tests. At the same time, they have materially different triggers, permission scopes, environments, credentials, and side effects. Those differences are intentional control boundaries and should remain independent.

**Recommendation:** first introduce a small local composite action for Node/npm setup and frozen dependency installation. Evaluate a reusable verification workflow only after the CI, E2E, and release acceptance criteria are reconciled. Keep CodeQL, scheduled security scanning, release publication, GitHub Pages deployment, Vercel deployment, and smart-contract deployment as separately triggered and permission-scoped workflows.

## Evidence reviewed

The following files were read from the repository default branch on 2026-11-16:

| File | Observed responsibility | Repeated work / control boundary |
|---|---|---|
| `.github/workflows/ci.yml` | Push/PR CI; Node 18.x + 20.x matrix; compile, test, npm audit, contract-size check | Three jobs each repeat checkout, Node setup, npm cache, and `npm ci`; compile/test duties recur in other workflows |
| `.github/workflows/security.yml` | Push/PR plus weekly Sunday security scan; dependency audit, contract-security placeholder, CodeQL, basic secret-pattern scan | Repeats Node 20/npm install and npm audit; dedicated security schedule and CodeQL permissions are distinct |
| `.github/workflows/e2e.yml` | Main-branch push/PR E2E test and PR report comment | Repeats Node 20 setup, npm cache, `npm ci`, compile and tests; PR comment requires write access |
| `.github/workflows/release.yml` | Version-tag release; build, tests, changelog, GitHub Release | Repeats Node/npm install, compile and tests; `contents: write` is release-only |
| `.github/workflows/vercel-deploy.yml` | Main push/PR Vercel build/deploy | Repeats Node/npm install and compile; requires Vercel credentials and performs provider-specific deployment |
| `.github/workflows/deploy.yml` | Manual smart-contract deployment by selected network | Repeats Node/npm install and compile; environment protection and deployer/RPC secrets are high-impact controls |
| `.github/workflows/deploy-pages.yml` | Path-filtered Pages build and deploy; manual dispatch | Repeats Node/npm install; Pages permissions and deployment environment are distinct |
| `package.json` | Hardhat scripts and dependencies | `npm test` = `hardhat test`; `npm run compile` = `hardhat compile` |

Source file links:
- [CI](https://github.com/chaishillomnitech1/OmniBuilderZero/blob/main/.github/workflows/ci.yml)
- [Security](https://github.com/chaishillomnitech1/OmniBuilderZero/blob/main/.github/workflows/security.yml)
- [E2E](https://github.com/chaishillomnitech1/OmniBuilderZero/blob/main/.github/workflows/e2e.yml)
- [Release](https://github.com/chaishillomnitech1/OmniBuilderZero/blob/main/.github/workflows/release.yml)
- [Vercel deploy](https://github.com/chaishillomnitech1/OmniBuilderZero/blob/main/.github/workflows/vercel-deploy.yml)
- [Contract deploy](https://github.com/chaishillomnitech1/OmniBuilderZero/blob/main/.github/workflows/deploy.yml)
- [Pages deploy](https://github.com/chaishillomnitech1/OmniBuilderZero/blob/main/.github/workflows/deploy-pages.yml)
- [Package scripts](https://github.com/chaishillomnitech1/OmniBuilderZero/blob/main/package.json)

## Duplication map

### High-confidence shared primitives

1. Checkout action version and repository checkout.
2. Node.js version selection and npm cache setup.
3. `npm ci` dependency installation.
4. Hardhat compilation command.
5. Hardhat test command.

The setup/install sequence is the safest first consolidation target because it does not own release decisions or deployment credentials.

### Overlapping security duties that need policy clarification

- `ci.yml` includes a `security-audit` job running `npm audit` and a production audit.
- `security.yml` independently runs `npm audit`, creates a JSON report, and runs weekly.
- Both currently allow audit command failures to continue. The actual policy is therefore not a clearly enforced blocking gate in these workflow definitions.
- `security.yml` additionally owns CodeQL and a basic pattern-based secret scan. These must not be collapsed into a generic build job or lose their separate permissions and schedule.
- `ci.yml` has a separate contract-size check. It is not equivalent to CodeQL or dependency scanning.

Before changing audit behavior, the owner should decide which result is advisory, which is required for PR merge, and which is the scheduled evidence/reporting run. Do not silently convert a soft-fail into a blocking check or weaken a gate to make CI green.

### Release and deployment duties that must remain independent

- `release.yml` is tag-triggered and writes GitHub Releases (`contents: write`).
- `deploy.yml` is manually dispatched, selects a blockchain network, uses deployment secrets, and targets protected environments.
- `vercel-deploy.yml` has provider-specific preview/production behavior and Vercel credentials.
- `deploy-pages.yml` owns Pages permissions, Pages artifacts, and the Pages environment.
- Their triggers, permissions, credentials, environments, and side effects are not interchangeable.

A shared workflow may prepare and verify artifacts, but must not publish releases, deploy contracts, or deploy websites as an implicit side effect of a common build.

## Proposed orchestration boundary

### Phase 1 — local composite action (recommended first)

Create a repository-local action such as `.github/actions/setup-node-npm/action.yml` with explicit inputs:
- `node-version` (required)
- optional npm version only if a real requirement is identified

It should:
- set up the requested Node version;
- enable npm dependency caching using the repository lockfile;
- run `npm ci` exactly once per job.

Each caller keeps its own workflow name, trigger, job graph, matrix, permissions, conditions, environment, secrets, and deployment steps. The action must not receive deployment secrets or write tokens.

This is a low-risk reduction of repeated setup logic, not a claim of measured cost savings.

### Phase 2 — reusable verification workflow (conditional)

After checking the package lockfile, Hardhat configuration, test fixtures, Node 18 compatibility, and exact acceptance policies, consider a `workflow_call` workflow for a strictly shared compile/test gate.

Do not force every workflow onto one matrix:
- CI explicitly tests Node 18.x and 20.x.
- Other workflows currently use Node 20.
- E2E includes PR reporting behavior.
- Release requires tag-specific changelog and release publication steps.
- Deployments require independent protected environments and credentials.

The reusable workflow must return a clear pass/fail result and never perform deployment or release publication. Callers retain independent approvals and side effects.

### Phase 3 — security policy normalization (separate decision)

Document a clear split:
- PR merge gate: explicitly chosen blocking checks.
- Scheduled security evidence: periodic reports and CodeQL.
- Contract-specific security: real configured analyzers, not placeholder echo steps.
- Secret scanning: native GitHub secret scanning plus a clearly scoped repository check.

Keep security permissions minimal and distinct. Never pass `contents: write`, `security-events: write`, deploy secrets, or release tokens to generic build steps unless strictly required.

## Control invariants

1. No workflow is deleted or disabled as part of the first consolidation.
2. No release trigger, tag pattern, deploy trigger, protected environment, or approval is changed.
3. No deployment credentials are passed to shared setup or verification components.
4. No `secrets: inherit` shortcut; pass only explicitly required secrets to the workflow that owns the action.
5. Each independent workflow retains its own visible check/run and evidence trail.
6. Shared components are versioned and locally auditable.
7. No merge, production deployment, contract deployment, secret edit, DNS change, or infrastructure spend is part of this audit.

## Validation plan for an implementation PR

- Verify action metadata and YAML syntax.
- Confirm every caller retains its original trigger, matrix, permissions, conditions, and environment.
- Run CI on both Node 18.x and 20.x.
- Run E2E and release verification independently.
- Confirm CodeQL still produces a security result and the scheduled security trigger remains.
- Confirm Pages, Vercel, and contract deployment jobs still require their original independent triggers and credentials.
- Compare Actions minutes and job duration before/after only when run data is available; do not estimate savings from line counts.
- Review each changed workflow diff against this control-invariant list.

## Current conclusion

**Feasible:** yes, a common preparation layer is feasible and has a strong evidence basis.

**Safe first step:** a local composite Node/npm setup-and-install action.

**Not yet justified:** collapsing build, security, release, and deployment into one workflow; changing audit enforcement; replacing independent deployment workflows with a single orchestrator.

**Status:** investigation documented. No workflow source has been modified, no workflow has been run by this audit, and no deployment or release was triggered.
