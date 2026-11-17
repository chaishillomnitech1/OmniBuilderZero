# Methodigitology ↔ Agent 25 ↔ OMNITECH1 bridge (v1.0-draft)

## Status

- Grammar, ontology, lexicon, JSON Schema, and a Python validation-only reference implementation are proposed in this branch.
- The bridge contract is documented here; it does not grant Agent 25 production execution rights.
- OMNITECH1 PR #46 remains a local-first deployment/recovery engine. This addition validates intent records; it does not invoke Docker, change routes, deploy, or reconcile services.

## Contract flow

1. Agent 25 receives or constructs a Methodigitology record while preserving the exact source expression.
2. The four semantic fields remain separate: intention, purpose, conviction, and impact.
3. Agent 25 emits a typed record conforming to methodigitology/intent.schema.json.
4. OMNITECH1's validation-only adapter checks structure and authorization separation.
5. A validated record may be converted into a proposed work package. It is not an execution command.
6. Any consequential operation must pass the existing engine policy and a separate scoped authorization gate.
7. Evidence receipts link source expression → semantic record → code artifact → test/runtime evidence.

## Agent 25 integration boundary

The existing Agent 25 25-role registry remains authoritative for specialist selection. Methodigitology is a shared message/intent envelope, not a replacement for role identity. Public visitor chat remains informational and read-only. A visitor-provided EXECUTE mode or PRODUCTION impact label is data only and cannot authorize action.

## OMNITECH1 integration boundary

Invoke the validator with: python engine/methodigitology.py path/to/intent.json

It returns a validation result and never executes the described action. PR #46 deployment/recovery behavior is unchanged.

## Acceptance gates

- JSON Schema parses as JSON and uses a declared JSON Schema dialect.
- EBNF defines the canonical record grammar.
- Lexicon terms preserve canonical wording.
- Validator rejects missing fields, false verbatim-preservation flags, and execution/production records without separate authorization.
- Unit tests pass.
- No production deployment, secret changes, database migration, DNS change, or runtime activation occurs in this milestone.
