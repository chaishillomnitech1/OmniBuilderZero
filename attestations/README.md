# Attestations Framework

The Attestations module provides a verifiable credentials framework for the ScrollVerse ecosystem, enabling signed, provenance-tracked attestations for identities, achievements, and partnerships.

## Purpose

- **Verifiable Credentials**: Issue W3C-compliant JSON-LD credentials
- **PR-Based Attestations**: Automated attestation workflows via GitHub Actions
- **KMS Integration**: Secure signing using GPG or cloud-based Key Management Services
- **Provenance Tracking**: Immutable record of credential issuance and verification

## Directory Structure

```
attestations/
├── README.md                    # This file
├── templates/                   # Credential templates
│   └── scrollverse-credential.jsonld  # JSON-LD verifiable credential template
├── workflows/                   # Attestation workflow documentation
│   └── pr-attestation-guide.md  # PR-based attestation instructions
├── signing/                     # Signing guides and templates
└── schemas/                     # Credential schemas
```

## Credential Types

### Opt-In Verifiable Credentials
- **FlameDNA Holder Attestation**: Proves ownership of FlameDNA NFTs
- **Partnership Credential**: Validates partnership agreements
- **Achievement Badge**: Records accomplishments within ScrollVerse
- **Identity Attestation**: Self-sovereign identity verification

## Signing Methods

### GPG Signing
Local signing using GPG keys for individual contributors.

### Cloud KMS Signing
Production-grade signing using:
- **AWS KMS**: Amazon Web Services Key Management Service
- **Google Cloud KMS**: Google Cloud Platform key management
- **Azure Key Vault**: Microsoft Azure key management

## Status

🚧 **Under Development** - This component is part of the OTAP scaffold phase.

## Related Documentation

- [ARCHITECTURE.md](../ARCHITECTURE.md) - System architecture overview
- [Matchmaker](../matchmaker/README.md) - Entity matching component
- [PR Attestation Guide](./workflows/pr-attestation-guide.md) - Workflow instructions
