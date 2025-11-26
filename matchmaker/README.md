# Matchmaker Service

## Purpose

The Matchmaker Service is a core component of the OTAP (OmniTech Ascendancy Protocol) ecosystem. It facilitates intelligent matching and coordination between:

- **AscendancyID NFT holders** seeking services or partnerships
- **Service providers** within the ScrollVerse ecosystem
- **Cross-chain asset synchronization** via the Sync connectors
- **Attestation verification** workflows for trust-based interactions

The service acts as a decentralized coordination layer, enabling parties to discover, verify, and engage with each other based on on-chain credentials and verifiable attestations.

## Tech Choices

### Recommended Stack Options

#### Option A: Python (FastAPI)
```
- Python 3.11+
- FastAPI for REST API
- SQLAlchemy + PostgreSQL for persistence
- Redis for caching and pub/sub
- Web3.py for blockchain interactions
- Celery for background tasks
```

#### Option B: Node.js (Express/NestJS)
```
- Node.js 20 LTS
- NestJS or Express.js for REST API
- TypeORM + PostgreSQL for persistence
- Redis for caching and pub/sub
- ethers.js for blockchain interactions
- Bull for background job processing
```

### Infrastructure Requirements
- Docker/Kubernetes for containerization
- PostgreSQL 15+ for persistent storage
- Redis 7+ for caching and message queues
- RPC endpoints for Scroll, Ethereum, Polygon

## API Sketch

### Core Endpoints

```yaml
# Health & Status
GET  /health                    # Service health check
GET  /status                    # System status and metrics

# Match Discovery
POST /api/v1/matches/discover   # Find potential matches based on criteria
GET  /api/v1/matches/:id        # Get match details
POST /api/v1/matches/:id/accept # Accept a match proposal

# AscendancyID Integration
GET  /api/v1/identity/:tokenId  # Get AscendancyID holder info
POST /api/v1/identity/verify    # Verify identity attestations

# Attestation Verification
POST /api/v1/attestations/verify  # Verify a verifiable credential
GET  /api/v1/attestations/status  # Check attestation status

# Webhooks
POST /api/v1/webhooks/register    # Register webhook for events
DELETE /api/v1/webhooks/:id       # Unregister webhook
```

### Request/Response Examples

#### Discover Matches
```json
POST /api/v1/matches/discover
{
  "seeker": {
    "ascendancyId": "0x...",
    "requirements": ["attestation:kyc", "attestation:professional"],
    "preferences": {
      "region": "global",
      "serviceType": "consulting"
    }
  }
}

Response:
{
  "matches": [
    {
      "id": "match-uuid",
      "provider": { "ascendancyId": "0x...", "score": 0.95 },
      "attestations": ["verified"],
      "expiresAt": "2025-12-01T00:00:00Z"
    }
  ]
}
```

## Architecture Integration

The Matchmaker integrates with:
1. **AscendancyID NFT Contracts** - For identity verification
2. **Attestation Layer** - For credential verification
3. **Insights UI** - For dashboard and analytics
4. **Sync Connectors** - For cross-chain data synchronization

## Security Considerations

- All API endpoints require authentication via JWT or API keys
- Rate limiting enforced per client
- No PII stored on-chain; only attestation hashes
- All communications encrypted via TLS 1.3

## TODOs

- [ ] Define OpenAPI specification (swagger.yaml)
- [ ] Implement authentication middleware
- [ ] Create database schema migrations
- [ ] Build AscendancyID verification logic
- [ ] Integrate with attestation verification service
- [ ] Add webhook notification system
- [ ] Implement rate limiting and caching
- [ ] Create Docker configuration
- [ ] Write unit and integration tests
- [ ] Add observability (metrics, logging, tracing)
- [ ] Document deployment procedures
- [ ] Set up CI/CD pipeline integration

## Development Setup

```bash
# Clone and navigate
cd matchmaker

# Python setup (Option A)
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload

# Node.js setup (Option B)
npm install
npm run dev
```

## Environment Variables

```bash
# Required
DATABASE_URL=postgresql://user:pass@localhost:5432/matchmaker
REDIS_URL=redis://localhost:6379
RPC_URL_SCROLL=https://rpc.scroll.io
RPC_URL_ETHEREUM=https://eth-mainnet.g.alchemy.com/v2/...

# Optional
LOG_LEVEL=info
API_RATE_LIMIT=100
JWT_SECRET=<your-secret>  # Never commit actual secrets
```

---

*This component is part of the OmniTech Ascendancy Protocol (OTAP) ecosystem.*
