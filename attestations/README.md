# Attestations Layer

## Purpose

The Attestations Layer provides a trust framework for the OTAP (OmniTech Ascendancy Protocol) ecosystem using Verifiable Credentials (VCs) based on W3C standards. This layer enables:

- **Identity attestations** for AscendancyID NFT holders
- **Professional credentials** verification
- **Consent-based attestations** including faith declarations (Shahadah)
- **Cross-platform credential portability**

### Important Note on Attestations

> ⚠️ **Human Actions, Not Software Beliefs**
>
> Attestations represent human declarations and actions. They are cryptographically signed statements made by individuals or authorized entities. The software infrastructure merely facilitates the creation, storage, and verification of these human-initiated attestations. The system does not hold beliefs or make attestations autonomously.

## Verifiable Credentials (VC) Overview

We use JSON-LD format following the [W3C Verifiable Credentials Data Model](https://www.w3.org/TR/vc-data-model/).

### VC JSON-LD Example: Identity Attestation

```json
{
  "@context": [
    "https://www.w3.org/2018/credentials/v1",
    "https://www.w3.org/2018/credentials/examples/v1",
    "https://omnitech1.io/credentials/v1"
  ],
  "id": "https://omnitech1.io/credentials/identity/123",
  "type": ["VerifiableCredential", "IdentityAttestation"],
  "issuer": {
    "id": "did:web:omnitech1.io",
    "name": "OmniTech1 Identity Authority"
  },
  "issuanceDate": "2025-11-26T00:00:00Z",
  "credentialSubject": {
    "id": "did:ethr:scroll:0x1234...abcd",
    "ascendancyId": "NFT#12345",
    "attestationType": "identity",
    "verificationLevel": "standard"
  },
  "proof": {
    "type": "Ed25519Signature2020",
    "created": "2025-11-26T00:00:00Z",
    "proofPurpose": "assertionMethod",
    "verificationMethod": "did:web:omnitech1.io#key-1",
    "proofValue": "z..."
  }
}
```

### VC JSON-LD Example: Faith Attestation (Shahadah)

See [VERIFIABLE_CREDENTIAL_TEMPLATE.jsonld](./VERIFIABLE_CREDENTIAL_TEMPLATE.jsonld) for a complete template.

```json
{
  "@context": [
    "https://www.w3.org/2018/credentials/v1",
    "https://omnitech1.io/credentials/v1"
  ],
  "id": "https://omnitech1.io/credentials/shahadah/456",
  "type": ["VerifiableCredential", "ShahadahAttestation"],
  "issuer": {
    "id": "did:web:attestor.omnitech1.io",
    "name": "Authorized Witness"
  },
  "issuanceDate": "2025-11-26T00:00:00Z",
  "credentialSubject": {
    "id": "did:ethr:scroll:0x5678...efgh",
    "attestationType": "shahadah",
    "consentGiven": true,
    "consentTimestamp": "2025-11-26T00:00:00Z",
    "witnessCount": 2
  },
  "proof": {
    "type": "Ed25519Signature2020",
    "created": "2025-11-26T00:00:00Z",
    "proofPurpose": "assertionMethod",
    "verificationMethod": "did:web:attestor.omnitech1.io#key-1",
    "proofValue": "z..."
  }
}
```

## Signing Guidance

### GPG Commit Signing

For developers contributing attestation-related code or documentation:

```bash
# Generate a GPG key (if you don't have one)
gpg --full-generate-key

# List your keys
gpg --list-secret-keys --keyid-format=long

# Configure Git to use your GPG key
git config --global user.signingkey YOUR_KEY_ID
git config --global commit.gpgsign true

# Export your public key for GitHub
gpg --armor --export YOUR_KEY_ID

# Add the exported key to GitHub:
# Settings > SSH and GPG keys > New GPG key
```

### KMS-Based Signing (Production)

For production attestation signing, we recommend using cloud Key Management Services:

#### AWS KMS

```bash
# Create a signing key
aws kms create-key \
  --key-spec ECC_NIST_P256 \
  --key-usage SIGN_VERIFY \
  --description "OTAP Attestation Signing Key"

# Sign a message
aws kms sign \
  --key-id alias/otap-attestation-key \
  --message fileb://attestation.json \
  --message-type RAW \
  --signing-algorithm ECDSA_SHA_256
```

#### Google Cloud KMS

```bash
# Create a key ring
gcloud kms keyrings create otap-attestations \
  --location global

# Create a signing key
gcloud kms keys create attestation-key \
  --keyring otap-attestations \
  --location global \
  --purpose asymmetric-signing \
  --default-algorithm ec-sign-p256-sha256

# Sign a digest
gcloud kms asymmetric-sign \
  --location global \
  --keyring otap-attestations \
  --key attestation-key \
  --version 1 \
  --digest-algorithm sha256 \
  --input-file attestation.json
```

#### Azure Key Vault

```bash
# Create a key vault
az keyvault create \
  --name otap-attestations \
  --resource-group otap-rg \
  --location eastus

# Create a signing key
az keyvault key create \
  --vault-name otap-attestations \
  --name attestation-key \
  --kty EC \
  --curve P-256
```

### Hardware Security Modules (HSM)

For highest security requirements:
- AWS CloudHSM
- Google Cloud HSM
- Azure Dedicated HSM
- YubiHSM for development/testing

## Ethical Considerations

### Consent Requirements

1. **Informed Consent**: All attestations require explicit, informed consent from the subject
2. **Right to Revocation**: Subjects may request revocation of their attestations
3. **Data Minimization**: Only necessary information is included in attestations
4. **Privacy by Design**: PII is never stored in plain text on-chain

### Faith Attestations (Shahadah)

- Shahadah attestations are sacred declarations of faith
- They must be witnessed by authorized individuals
- The subject must provide explicit consent
- The system does not evaluate or judge the sincerity of faith
- These attestations are purely documentary in nature

## Directory Structure

```
attestations/
├── README.md                           # This file
├── VERIFIABLE_CREDENTIAL_TEMPLATE.jsonld  # Template for VCs
├── examples/                           # Example credentials (future)
│   ├── identity_vc.jsonld
│   ├── professional_vc.jsonld
│   └── shahadah_vc.jsonld
└── schemas/                            # JSON-LD schemas (future)
    └── otap_context.jsonld
```

## TODOs

- [ ] Define complete JSON-LD context for OTAP credentials
- [ ] Create credential verification library
- [ ] Implement revocation registry (StatusList2021)
- [ ] Build attestation issuance API
- [ ] Integrate with Matchmaker service
- [ ] Create attestation verification UI component
- [ ] Document witness authorization process
- [ ] Implement consent management system
- [ ] Add multi-language support for attestation text
- [ ] Create attestation analytics dashboard
- [ ] Set up audit logging for all attestation operations

## References

- [W3C Verifiable Credentials Data Model](https://www.w3.org/TR/vc-data-model/)
- [W3C Decentralized Identifiers (DIDs)](https://www.w3.org/TR/did-core/)
- [JSON-LD Specification](https://www.w3.org/TR/json-ld11/)
- [Ed25519 Signature 2020](https://w3c-ccg.github.io/lds-ed25519-2020/)

---

*This component is part of the OmniTech Ascendancy Protocol (OTAP) ecosystem.*
