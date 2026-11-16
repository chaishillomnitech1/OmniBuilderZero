# Reusable Compile/Test Workflow — Design Record

**Status:** Proposed reusable workflow, isolated draft; no existing caller workflow is rewired by this change.  
**Baseline commit:** `0dd2251b9503075fa9e04b9d4535cc872a35f1c5` (PR #52 merge commit).  
**Purpose:** Standardize compile/test mechanics without taking ownership of security, release, or deployment decisions.

## PR #52 closure and review

PR #52 is merged:
- PR: https://github.com/chaishillomnitech1/OmniBuilderZero/pull/52
- Merge commit: `0dd2251b9503075fa9e04b9d4535cc872a35f1c5`
- Source commit: `c740d052860b91f6c45254240b49ac537da9890c`
- Merged at: 2026-11-16 13:34:31 UTC.

Review of the merged patch found one repository-local composite action:
`.github/actions/setup-node-npm/action.yml`, with required `node-version`, `actions/setup-node@v4`, npm cache, and `npm ci`. Ten call sites were updated across seven workflows. No dependency manifests, triggers, release actions, deploy commands, secret mappings, environment approvals, or job permission blocks were intentionally changed.

## Runtime compatibility evidence

The merged PR's CI run `43876517470` completed successfully:
- Node 18.x: setup, lint, compile, and tests all succeeded.
- Node 20.x: setup, lint, compile, tests, and coverage artifact step all succeeded.
- Security Audit and Contract Size Check jobs succeeded.

E2E run `43876518191` also succeeded, including compile, Hardhat tests, report generation, artifact upload, and PR-comment step. This is direct runtime evidence for Node 18 and 20 in the CI matrix and Node 20 in E2E.

The Vercel PR workflow `43876517598` failed at **Pull Vercel Environment Information** after the shared preparation and compile steps succeeded; subsequent Vercel build/deploy/comment steps were skipped. This is a missing/unavailable Vercel environment/credential path, not evidence of a Node compatibility failure. No production deploy was completed by that PR run.

Post-merge push runs on `0dd2251b9503075fa9e04b9d4535cc872a35f1c5`:
- CI: `43877092095` — success, including Node 18 and 20.
- E2E: `43877092201` — success.
- Vercel: `43877092092` — failed at Vercel environment pull.
- GitHub Pages: `43877092360` — failed; investigate independently before any Pages workflow changes.

## Reusable workflow contract

Workflow file: `.github/workflows/reusable-compile-test.yml`.

Dedicated caller-only validation file: `.github/workflows/test-reusable-compile-test.yml`. It invokes the reusable workflow as a Node `18.x` / `20.x` matrix, runs the repository's actual `npm run compile` and `npm test` scripts, and uploads the generated Hardhat `artifacts/` directory under a version-specific artifact name. The reusable workflow publishes the requested Node version, compile/test outcomes, overall result, and artifact URL in the job summary; it also exposes these as reusable-workflow outputs.

### Inputs

| Input | Type | Default | Purpose |
|---|---|---|---|
| `node-version` | string | `20.x` | Caller-selected Node runtime; caller matrix can pass 18.x and 20.x |
| `run-compile` | boolean | `true` | Enable/skip compile step |
| `compile-command` | string | `npm run compile` | Compile command |
| `run-tests` | boolean | `true` | Enable/skip test step |
| `test-command` | string | `npm test` | Test command |
| `upload-artifacts` | boolean | `false` | Opt-in artifact upload |
| `artifact-path` | string | coverage and test-results paths | Newline-separated upload paths |
| `artifact-name` | string | `compile-test-results` | Artifact name |
| `artifact-retention-days` | number | `14` | Artifact retention |
| `test-private-key` | optional secret | unset | Test-only secret, mapped only to the test step; never a deployer key |

### Outputs

| Output | Meaning |
|---|---|
| `node-version` | Requested Node version |
| `compile-result` | Compile step outcome: success, failure, or skipped |
| `test-result` | Test step outcome: success, failure, or skipped |
| `verification-result` | Overall compile/test result (`success`, `failure`, or `cancelled`) |
| `artifact-url` | Uploaded artifact URL; empty when upload is disabled or no artifact is produced |

### Security and ownership boundary

- Read-only repository permission (`contents: read`).
- No release token, deployment token, cloud credentials, RPC secrets, or deployment private key input.
- No release creation, tagging, Vercel deployment, Pages deployment, contract deployment, DNS, or environment approval.
- Test-only secret is optional and only available to the test command.
- Caller retains triggers, job permissions, environments, concurrency, artifact/report/comment behavior, and downstream decisions.
- Security scans, CodeQL, secret scanning, and audit policy remain independent.

## Adoption sequence

1. The dedicated caller-only test workflow is now committed on the same isolated PR branch; it targets Node 18.x and 20.x and does not replace any existing workflow.
2. Await and inspect both matrix jobs, their compile/test outcomes, generated artifacts, and artifact URLs before treating the reusable workflow as validated.
3. Confirm E2E reporting/comment behavior remains in the E2E caller (the reusable workflow does not own PR comments).
4. Only after the caller run proves equivalence, propose one caller migration at a time. Do not migrate security, release, Pages, Vercel, or contract-deploy workflows as a bundle.
5. Retain independent security and release/deployment gates.

## Measured timing — preliminary, not a savings claim

One pre-change baseline and one post-merge run were inspected from GitHub job timestamps:

| Workflow/job | Before (s) | After (s) | Difference |
|---|---:|---:|---:|
| CI Node 18 job | 36 | 38 | +2 |
| CI Node 20 job | 30 | 32 | +2 |
| CI Security Audit | 15 | 18 | +3 |
| CI Contract Size Check | 25 | 30 | +5 |
| E2E job | 35 | 39 | +4 |

Baseline CI run: `43805232290`; baseline E2E run: `43805232313`.  
Post-merge CI run: `43877092095`; post-merge E2E run: `43877092201`.

The observed jobs were 2–5 seconds slower in the single post-merge sample. This is not a controlled benchmark: runner variance, cache state, and concurrent load may differ. The reusable preparation component reduces duplicated workflow code; it has **not** demonstrated lower elapsed time or lower Actions usage in this sample.

The repository-level Actions billing/usage endpoint was not available through the connected GitHub read path. These job durations are not billable-minute totals. A meaningful efficiency claim requires multiple matched runs, runner labels, job-duration sums, cache hit/miss observations, and authoritative Actions usage data.

## Explicitly unchanged workflows

- `.github/workflows/security.yml`: dependency audit, contract security, CodeQL, and secret scan remain independently triggered and permissioned.
- `.github/workflows/release.yml`: tag-triggered release and `contents: write` remain independent.
- `.github/workflows/vercel-deploy.yml`: Vercel preview/production behavior and its credentials remain independent.
- `.github/workflows/deploy.yml`: manually selected contract network, protected environment, and deployer secrets remain independent.
- `.github/workflows/deploy-pages.yml`: Pages permissions, triggers, concurrency, and publication remain independent.
- `.github/workflows/e2e.yml`: report generation, artifact upload, and PR comment remain caller-owned.

**Decision:** Treat this workflow as a reusable compile/test building block only. Do not centralize the system's security, release, or deployment control planes.
