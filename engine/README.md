# OMNITECH1 Autonomous Deployment Engine

A local-first, provider-independent deployment controller. This first implementation is a **local development engine**, not a production orchestrator.

## Operating model: IF / THEN / ELSE

- IF Docker is unavailable → stop and escalate; do not pretend deployment succeeded.
- IF the candidate image fails its health probe → remove only the candidate; preserve the active route.
- IF the candidate passes → switch Caddy to the candidate and verify through the visitor route.
- IF the active container becomes unhealthy → restart it once and verify.
- IF restart fails AND a known-good previous deployment exists → roll back and verify.
- ELSE → stop and emit an escalation event; never guess at destructive repairs.

## Components

- Git commit SHA → immutable image tag and provenance label.
- Docker Engine → isolated application containers.
- Caddy → local visitor routing on http://localhost:8080.
- SQLite → deployment state and append-only event history.
- Reconcile loop → health-driven IF/THEN/ELSE decisions.

## Windows quick start

From the repository root in PowerShell:

```powershell
python --version
docker version
docker compose version
python .\engine\engine.py doctor
```

Start the local router:

```powershell
docker compose -f .\engine\compose.yaml up -d
```

Deploy an application repository that has a Dockerfile and a /health endpoint:

```powershell
python .\engine\engine.py deploy --context C:\path\to\application --service scrollverse --container-port 3000
```

The source repository must be a clean Git checkout. The engine uses its full commit SHA as the image tag. It does not read, print, or configure API keys.

Monitor once:

```powershell
python .\engine\engine.py reconcile --service scrollverse
```

Continuously reconcile:

```powershell
python .\engine\engine.py reconcile --service scrollverse --watch --interval 15
```

Inspect state:

```powershell
python .\engine\engine.py status
```

## Boundaries in this milestone

- No Vercel dependency or Vercel API calls.
- No production DNS, cloud provisioning, secret changes, migrations, payments, wallets, or production deployment.
- The engine controls only containers it names with the `omnitech1-` prefix.
- Recovery is limited to one restart followed by a verified rollback to a recorded prior image.
- If neither path can be verified, the engine escalates and stops.
- This is not yet HA, multi-host, distributed monitoring, or an Agent 25 autonomous worker fleet.

## Evidence

Every deployment decision is written to SQLite with a timestamp, event type, service, and structured details. Health success is recorded only after an HTTP 200 response from the candidate and the Caddy visitor route.
