# PR-Based Attestation Workflow Guide

This guide explains how to request and issue verifiable credentials through GitHub Pull Requests using automated workflows with KMS-based signing.

## Overview

The ScrollVerse attestation system enables:
- **Opt-in attestations**: Contributors can request credentials via PR
- **Automated validation**: GitHub Actions verify eligibility
- **KMS signing**: Credentials are signed using cloud KMS or GPG
- **Provenance tracking**: All attestations are recorded on-chain

## Requesting an Attestation

### Step 1: Create Attestation Request

Create a new file in the `attestations/requests/` directory:

```bash
attestations/requests/YOUR_REQUEST_ID.json
```

Use the following template:

```json
{
  "requestId": "YOUR_REQUEST_ID",
  "requestType": "FlameDNA_Holder|Partnership|Achievement",
  "subjectAddress": "0x...",
  "evidence": {
    "description": "Reason for attestation request",
    "links": [
      "https://scrollscan.io/tx/0x..."
    ]
  },
  "preferences": {
    "soulbound": true,
    "expirationDays": 365
  }
}
```

### Step 2: Submit Pull Request

1. Fork the repository (if external contributor)
2. Create a branch: `attestation/YOUR_REQUEST_ID`
3. Add your attestation request file
4. Submit PR with title: `[ATTESTATION] YOUR_REQUEST_ID`

### Step 3: Automated Validation

The GitHub Actions workflow will:
1. Parse and validate the request JSON
2. Verify on-chain eligibility (FlameDNA ownership, etc.)
3. Check for duplicate requests
4. Label the PR appropriately

### Step 4: Review and Approval

**Who Can Approve:**
- Repository maintainers with `write` access or higher
- Members of the `@chaishillomnitech1/attestation-reviewers` team (if configured)

**Approval Process:**
1. A ScrollVerse maintainer reviews the request for validity
2. The maintainer verifies the evidence provided
3. If approved, the maintainer applies the `attestation-approved` label to the PR
4. The PR is then merged by a maintainer
5. Upon merge with the `attestation-approved` label, the signing workflow triggers automatically
6. The credential is signed and added to the `attestations/issued/` directory

**Note:** Only users with repository write access can apply labels. The `attestation-approved` label should be protected and only applied after thorough review.

### Step 5: Receive Credential

Once merged:
- The signed credential is available in `attestations/issued/YOUR_REQUEST_ID.jsonld`
- On-chain record is created (if applicable)
- Notification is sent to the subject address

## Signing Configuration

### GPG Signing (Individual Contributors)

1. Generate a GPG key pair:
   ```bash
   gpg --full-generate-key
   ```

2. Export your public key:
   ```bash
   gpg --armor --export YOUR_KEY_ID > public.key
   ```

3. Add to GitHub Secrets:
   - `GPG_PRIVATE_KEY`: Your ASCII-armored private key
   - `GPG_PASSPHRASE`: Your key passphrase

### AWS KMS Signing

1. Create a KMS key in AWS Console
2. Configure IAM permissions for GitHub Actions
3. Add secrets:
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`
   - `AWS_KMS_KEY_ID`

### Google Cloud KMS Signing

1. Create a keyring and key in GCP Console
2. Create a service account with `cloudkms.signer` role
3. Add secrets:
   - `GCP_SA_KEY`: Service account JSON key
   - `GCP_KMS_KEY_PATH`: `projects/PROJECT/locations/LOCATION/keyRings/KEYRING/cryptoKeys/KEY/cryptoKeyVersions/VERSION`

### Azure Key Vault Signing

1. Create a Key Vault and key in Azure Portal
2. Create a service principal with Key Vault Crypto User role
3. Add secrets:
   - `AZURE_CLIENT_ID`
   - `AZURE_CLIENT_SECRET`
   - `AZURE_TENANT_ID`
   - `AZURE_KEY_VAULT_URL`
   - `AZURE_KEY_NAME`

## Workflow File Reference

The attestation workflow is defined in `.github/workflows/attestation-signing.yml`.

Key features:
- Triggers on PR merge with `attestation-approved` label
- Validates request JSON schema
- Signs credential using configured KMS
- Commits signed credential to repository
- Creates on-chain record (optional)

## Security Considerations

1. **Key Rotation**: Rotate signing keys periodically
2. **Access Control**: Limit who can approve attestation PRs
3. **Audit Trail**: All attestations are logged in git history
4. **Revocation**: Credentials can be revoked by updating status endpoint

## Troubleshooting

### Common Issues

**Issue**: Workflow fails with "Invalid request format"
**Solution**: Ensure JSON is valid and all required fields are present

**Issue**: "Subject not eligible"
**Solution**: Verify on-chain ownership or partnership status

**Issue**: "KMS signing failed"
**Solution**: Check KMS credentials and permissions in GitHub Secrets

## Related Documentation

- [Attestations README](../README.md)
- [Credential Template](../templates/scrollverse-credential.jsonld)
- [ARCHITECTURE.md](../../ARCHITECTURE.md)
