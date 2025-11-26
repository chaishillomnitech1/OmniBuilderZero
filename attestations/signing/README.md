# Signing Templates and Configuration Guide

This directory contains templates and guides for configuring various signing methods for ScrollVerse verifiable credentials.

## Available Signing Methods

### 1. GPG Signing (Development/Individual)

Best for: Individual contributors, development environments

**Setup:**
```bash
# Generate a new GPG key
gpg --full-generate-key

# Select: (1) RSA and RSA
# Key size: 4096
# Validity: 1y (or as needed)
# Enter your name and email

# List your keys
gpg --list-secret-keys --keyid-format=long

# Export private key for GitHub Secrets
gpg --armor --export-secret-keys YOUR_KEY_ID > private.key

# Export public key for verification
gpg --armor --export YOUR_KEY_ID > public.key
```

**GitHub Secrets Required:**
- `GPG_PRIVATE_KEY`: Content of `private.key`
- `GPG_PASSPHRASE`: Your key passphrase

### 2. AWS KMS Signing (Production)

Best for: Production environments, team signing

**Setup:**
1. Create KMS key in AWS Console:
   - Key type: Asymmetric
   - Key usage: Sign and verify
   - Key spec: ECC_NIST_P256 or RSA_2048

2. Create IAM policy:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "kms:Sign",
                "kms:GetPublicKey",
                "kms:DescribeKey"
            ],
            "Resource": "arn:aws:kms:REGION:ACCOUNT:key/KEY_ID"
        }
    ]
}
```

**GitHub Secrets Required:**
- `AWS_ACCESS_KEY_ID`: IAM access key
- `AWS_SECRET_ACCESS_KEY`: IAM secret key
- `AWS_KMS_KEY_ID`: KMS key ID or ARN
- `AWS_REGION`: AWS region (default: us-east-1)

### 3. Google Cloud KMS Signing (Production)

Best for: GCP-based infrastructure, enterprise signing

**Setup:**
1. Create keyring and key in GCP Console:
   - Algorithm: EC_SIGN_P256_SHA256
   - Protection level: Software or HSM

2. Create service account with `roles/cloudkms.signer`

3. Generate service account key JSON

**GitHub Secrets Required:**
- `GCP_SA_KEY`: Service account JSON key
- `GCP_KMS_KEY_PATH`: Full key path

**Key Path Format:**
```
projects/PROJECT_ID/locations/LOCATION/keyRings/KEYRING_NAME/cryptoKeys/KEY_NAME/cryptoKeyVersions/VERSION
```

### 4. Azure Key Vault Signing (Production)

Best for: Azure-based infrastructure, enterprise signing

**Setup:**
1. Create Key Vault in Azure Portal
2. Create key with EC or RSA algorithm
3. Create service principal with Key Vault Crypto User role

**GitHub Secrets Required:**
- `AZURE_CLIENT_ID`: Service principal app ID
- `AZURE_CLIENT_SECRET`: Service principal secret
- `AZURE_TENANT_ID`: Azure AD tenant ID
- `AZURE_KEY_VAULT_URL`: Key Vault URL
- `AZURE_KEY_NAME`: Key name in vault

## Verification

### GPG Signature Verification
```bash
gpg --verify credential.jsonld.asc credential.jsonld
```

### AWS KMS Verification
```bash
aws kms verify \
  --key-id KEY_ID \
  --message fileb://credential.jsonld \
  --message-type RAW \
  --signing-algorithm ECDSA_SHA_256 \
  --signature fileb://credential.jsonld.sig
```

### GCP KMS Verification
```bash
gcloud kms asymmetric-sign \
  --key KEY_PATH \
  --input-file credential.jsonld \
  --signature-file credential.jsonld.sig \
  --digest-algorithm sha256
```

## Security Best Practices

1. **Key Rotation**: Rotate signing keys at least annually
2. **Access Logging**: Enable CloudTrail/Cloud Audit Logs
3. **Least Privilege**: Grant minimal required permissions
4. **Key Backup**: Maintain secure backups of key material
5. **HSM Protection**: Use HSM-backed keys for production
