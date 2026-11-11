#!/usr/bin/env python3
"""Local-first OMNITECH1 deployment and recovery controller (stdlib only)."""
from __future__ import annotations

import argparse
import json
import os
import re
import sqlite3
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from policy import Action, decide

ROOT = Path(__file__).resolve().parent
DB_PATH = ROOT / "state" / "deployments.sqlite3"
CADDYFILE = ROOT / "Caddyfile"
COMPOSE = ROOT / "compose.yaml"
PORTS = (18081, 18082)


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def command(args: list[str], *, check: bool = True, cwd: str | None = None) -> str:
    result = subprocess.run(args, cwd=cwd, text=True, capture_output=True)
    if check and result.returncode:
        raise RuntimeError((result.stderr or result.stdout or "Command failed").strip())
    return result.stdout.strip()


def docker_available() -> bool:
    try:
        command(["docker", "info"])
        return True
    except Exception:
        return False


def connect_db() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB_PATH)
    con.execute("""CREATE TABLE IF NOT EXISTS deployments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        service TEXT NOT NULL, commit_sha TEXT NOT NULL, image TEXT NOT NULL,
        container TEXT NOT NULL, port INTEGER NOT NULL, container_port INTEGER NOT NULL,
        health_path TEXT NOT NULL, status TEXT NOT NULL, created_at TEXT NOT NULL
    )""")
    con.execute("""CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT, at TEXT NOT NULL,
        service TEXT NOT NULL, event TEXT NOT NULL, details TEXT NOT NULL
    )""")
    con.commit()
    return con


def record(service: str, event: str, **details: object) -> None:
    con = connect_db()
    con.execute("INSERT INTO events(at,service,event,details) VALUES(?,?,?,?)",
                (now(), service, event, json.dumps(details, sort_keys=True)))
    con.commit()
    con.close()


def active(service: str):
    con = connect_db()
    row = con.execute(
        "SELECT id,service,commit_sha,image,container,port,container_port,health_path,status,created_at "
        "FROM deployments WHERE service=? AND status='active' ORDER BY id DESC LIMIT 1",
        (service,),
    ).fetchone()
    con.close()
    return row


def previous(service: str):
    con = connect_db()
    row = con.execute(
        "SELECT id,service,commit_sha,image,container,port,container_port,health_path,status,created_at "
        "FROM deployments WHERE service=? AND status='previous' ORDER BY id DESC LIMIT 1",
        (service,),
    ).fetchone()
    con.close()
    return row


def container_exists(name: str) -> bool:
    return bool(command(["docker", "ps", "-aq", "--filter", f"name=^{name}$"], check=False))


def container_running(name: str) -> bool:
    return bool(command(["docker", "ps", "-q", "--filter", f"name=^{name}$", "--filter", "status=running"], check=False))


def wait_http(url: str, timeout: int = 35) -> bool:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            with urllib.request.urlopen(url, timeout=2) as response:
                if response.status == 200:
                    return True
        except (urllib.error.URLError, TimeoutError, OSError):
            time.sleep(1)
    return False


def route_config(port: int) -> str:
    return f":80 {{\n    reverse_proxy host.docker.internal:{port}\n}}\n"


def reload_caddy() -> None:
    command(["docker", "exec", "omnitech1-caddy", "caddy", "reload",
             "--config", "/etc/caddy/Caddyfile"])


def ensure_router() -> None:
    command(["docker", "compose", "-f", str(COMPOSE), "up", "-d", "caddy"])


def switch_route(port: int, health_path: str) -> bool:
    old = CADDYFILE.read_text(encoding="utf-8") if CADDYFILE.exists() else None
    CADDYFILE.write_text(route_config(port), encoding="utf-8")
    try:
        reload_caddy()
        if wait_http(f"http://127.0.0.1:8080{health_path}", timeout=15):
            return True
        raise RuntimeError("Visitor route did not return HTTP 200.")
    except Exception:
        if old is not None:
            CADDYFILE.write_text(old, encoding="utf-8")
            try:
                reload_caddy()
            except Exception:
                pass
        return False


def source_revision(context: Path) -> str:
    sha = command(["git", "rev-parse", "HEAD"], cwd=str(context))
    dirty = command(["git", "status", "--porcelain"], cwd=str(context))
    if dirty:
        raise RuntimeError("Source checkout is dirty. Commit the exact source before creating an immutable deployment.")
    return sha


def safe_service(value: str) -> str:
    value = re.sub(r"[^a-z0-9-]", "-", value.lower()).strip("-")
    if not value:
        raise ValueError("Service name must contain letters or digits.")
    return value[:40]


def start_image(service: str, image: str, container_port: int, health_path: str,
                port: int, commit_sha: str) -> str:
    name = f"omnitech1-{service}-{commit_sha[:12]}-{port}"
    if container_exists(name):
        command(["docker", "rm", "-f", name], check=False)
    command(["docker", "run", "-d", "--name", name, "--restart", "unless-stopped",
             "--label", "com.omnitech1.managed=true",
             "--label", f"org.opencontainers.image.revision={commit_sha}",
             "-p", f"127.0.0.1:{port}:{container_port}", image])
    if not wait_http(f"http://127.0.0.1:{port}{health_path}"):
        command(["docker", "rm", "-f", name], check=False)
        raise RuntimeError(f"Candidate failed health check at port {port}{health_path}.")
    return name


def persist_deployment(service: str, sha: str, image: str, name: str,
                       port: int, container_port: int, health_path: str) -> None:
    con = connect_db()
    con.execute("UPDATE deployments SET status='previous' WHERE service=? AND status='active'", (service,))
    con.execute(
        "INSERT INTO deployments(service,commit_sha,image,container,port,container_port,health_path,status,created_at) "
        "VALUES(?,?,?,?,?,?,?,'active',?)",
        (service, sha, image, name, port, container_port, health_path, now()),
    )
    con.commit()
    con.close()


def deploy(args) -> None:
    service = safe_service(args.service)
    context = Path(args.context).expanduser().resolve()
    if not context.is_dir():
        raise RuntimeError(f"Application context does not exist: {context}")
    if not docker_available():
        raise RuntimeError("Docker Engine unavailable; deployment stopped without changing the active route.")
    sha = source_revision(context)
    image = f"omnitech1/{service}:{sha}"
    current = active(service)
    port = PORTS[1] if current and current[5] == PORTS[0] else PORTS[0]
    dockerfile = str((context / args.dockerfile).resolve())
    if not Path(dockerfile).is_file():
        raise RuntimeError(f"Dockerfile not found: {dockerfile}")
    record(service, "build_started", commit=sha, image=image)
    command(["docker", "build", "--pull", "--label", f"org.opencontainers.image.revision={sha}",
             "-f", dockerfile, "-t", image, str(context)])
    record(service, "image_built", commit=sha, image=image)
    ensure_router()
    name = start_image(service, image, args.container_port, args.health_path, port, sha)
    if not switch_route(port, args.health_path):
        command(["docker", "rm", "-f", name], check=False)
        record(service, "candidate_rejected", commit=sha, reason="Caddy visitor route verification failed")
        raise RuntimeError("Candidate rejected; prior route preserved.")
    persist_deployment(service, sha, image, name, port, args.container_port, args.health_path)
    record(service, "deployment_verified", commit=sha, image=image, container=name,
           port=port, visitor_url=f"http://localhost:8080{args.health_path}")
    print(f"VERIFIED {service}: {sha} -> {image}; http://localhost:8080")


def rollback(service: str) -> bool:
    row = previous(service)
    if not row:
        record(service, "escalation", reason="No recorded previous deployment exists")
        print("ESCALATE: no known-good previous deployment.")
        return False
    _, _, sha, image, _, old_port, container_port, health_path, _, _ = row
    port = PORTS[1] if old_port == PORTS[0] else PORTS[0]
    if not docker_available():
        record(service, "escalation", reason="Docker unavailable during rollback")
        return False
    try:
        name = start_image(service, image, container_port, health_path, port, sha)
        if not switch_route(port, health_path):
            command(["docker", "rm", "-f", name], check=False)
            raise RuntimeError("Restored image did not pass visitor-route verification.")
        con = connect_db()
        con.execute("UPDATE deployments SET status='failed' WHERE service=? AND status='active'", (service,))
        con.execute("UPDATE deployments SET status='active' WHERE id=?", (row[0],))
        con.commit()
        con.close()
        record(service, "rollback_verified", commit=sha, image=image, container=name, port=port)
        print(f"ROLLBACK VERIFIED {service}: {sha}")
        return True
    except Exception as exc:
        record(service, "escalation", reason=str(exc), attempted_image=image)
        print(f"ESCALATE: rollback could not be verified: {exc}")
        return False


def reconcile(args) -> None:
    service = safe_service(args.service)

    def one_cycle():
        row = active(service)
        available = docker_available()
        exists = bool(row and container_exists(row[4]))
        healthy = bool(row and exists and container_running(row[4]) and
                       wait_http(f"http://127.0.0.1:{row[5]}{row[7]}", timeout=2))
        action = decide(docker_available=available, active_exists=exists,
                        active_healthy=healthy, restart_attempted=False,
                        previous_healthy=bool(previous(service)))
        record(service, "reconcile_decision", action=action.value,
               docker_available=available, active_exists=exists, active_healthy=healthy)
        if action == Action.HOLD:
            print(f"HEALTHY {service}")
            return
        if action == Action.ESCALATE:
            print(f"ESCALATE {service}: insufficient verified recovery path.")
            return
        if action == Action.ROLLBACK:
            rollback(service)
            return
        if action == Action.RESTART and row:
            print(f"RECOVERY: restarting {row[4]}")
            command(["docker", "restart", row[4]], check=False)
            if container_running(row[4]) and wait_http(f"http://127.0.0.1:{row[5]}{row[7]}", timeout=20):
                record(service, "restart_verified", container=row[4])
                print(f"RESTART VERIFIED {service}")
                return
            record(service, "restart_failed", container=row[4])
            if previous(service):
                rollback(service)
            else:
                record(service, "escalation", reason="Restart failed and no prior known-good deployment exists")
                print(f"ESCALATE {service}: restart failed; no known-good rollback.")
    if not args.watch:
        one_cycle()
        return
    while True:
        try:
            one_cycle()
        except KeyboardInterrupt:
            print("Reconcile loop stopped by operator.")
            return
        except Exception as exc:
            record(service, "controller_error", error=str(exc))
            print(f"CONTROLLER ERROR: {exc}")
        time.sleep(max(5, args.interval))


def doctor(_args) -> None:
    checks = {
        "docker_cli": subprocess.run(["docker", "--version"], text=True, capture_output=True).returncode == 0,
        "docker_engine": docker_available(),
        "compose": subprocess.run(["docker", "compose", "version"], text=True, capture_output=True).returncode == 0,
        "caddy_config": CADDYFILE.exists(),
    }
    print(json.dumps(checks, indent=2))
    if not all(checks[k] for k in ("docker_cli", "docker_engine", "compose")):
        sys.exit(1)


def status(_args) -> None:
    con = connect_db()
    rows = con.execute(
        "SELECT service,commit_sha,image,container,port,status,created_at FROM deployments ORDER BY id DESC LIMIT 30"
    ).fetchall()
    events = con.execute(
        "SELECT at,service,event,details FROM events ORDER BY id DESC LIMIT 20"
    ).fetchall()
    con.close()
    print(json.dumps({"deployments": rows, "recent_events": events}, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(description="OMNITECH1 local deployment/recovery engine")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("doctor")
    sub.add_parser("status")
    d = sub.add_parser("deploy")
    d.add_argument("--context", required=True)
    d.add_argument("--service", default="scrollverse")
    d.add_argument("--dockerfile", default="Dockerfile")
    d.add_argument("--container-port", type=int, default=3000)
    d.add_argument("--health-path", default="/health")
    r = sub.add_parser("reconcile")
    r.add_argument("--service", default="scrollverse")
    r.add_argument("--watch", action="store_true")
    r.add_argument("--interval", type=int, default=15)
    args = parser.parse_args()
    if args.command == "doctor":
        doctor(args)
    elif args.command == "status":
        status(args)
    elif args.command == "deploy":
        deploy(args)
    elif args.command == "reconcile":
        reconcile(args)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"STOPPED SAFELY: {exc}", file=sys.stderr)
        sys.exit(1)
