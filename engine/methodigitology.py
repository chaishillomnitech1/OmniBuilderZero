#!/usr/bin/env python3
"""Validate ScrollVerse Methodigitology intent records without executing them."""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

IMPACT = {"DRAFT", "PROPOSAL", "MERGE", "RUNTIME", "PRODUCTION"}
CONVICTION = {"LOW", "MEDIUM", "HIGH", "DECLARED"}
EXECUTION = {"RESEARCH", "BLUEPRINT", "VALIDATE", "EXECUTE"}
AUTHORIZATION = {"NONE", "GRANTED", "DENIED", "EXPIRED"}


def validate(record: object) -> list[str]:
    errors: list[str] = []
    if not isinstance(record, dict):
        return ["record must be a JSON object"]
    required = {"languageVersion", "source", "intention", "purpose", "conviction", "impact", "constraints", "execution"}
    missing = sorted(required - record.keys())
    if missing:
        errors.append("missing required fields: " + ", ".join(missing))
    if record.get("languageVersion") != "1.0.0-draft":
        errors.append("languageVersion must be 1.0.0-draft")
    source = record.get("source")
    if not isinstance(source, dict):
        errors.append("source must be an object")
    else:
        for key in ("expression", "origin"):
            if not isinstance(source.get(key), str) or not source[key].strip():
                errors.append(f"source.{key} must be a non-empty string")
        if source.get("preserveVerbatim") is not True:
            errors.append("source.preserveVerbatim must be true")
    if not isinstance(record.get("intention"), str) or not record["intention"].strip():
        errors.append("intention must be a non-empty string")
    purpose = record.get("purpose")
    if not isinstance(purpose, dict):
        errors.append("purpose must be an object")
    else:
        for key in ("statement", "beneficiary", "harmBoundary"):
            if not isinstance(purpose.get(key), str) or not purpose[key].strip():
                errors.append(f"purpose.{key} must be a non-empty string")
    conviction = record.get("conviction")
    if not isinstance(conviction, dict):
        errors.append("conviction must be an object")
    else:
        if conviction.get("level") not in CONVICTION:
            errors.append("conviction.level is not a supported value")
        if not isinstance(conviction.get("statement"), str) or not conviction["statement"].strip():
            errors.append("conviction.statement must be a non-empty string")
    impact = record.get("impact")
    if not isinstance(impact, dict):
        errors.append("impact must be an object")
    else:
        if impact.get("class") not in IMPACT:
            errors.append("impact.class is not a supported value")
        if not isinstance(impact.get("rationale"), str) or not impact["rationale"].strip():
            errors.append("impact.rationale must be a non-empty string")
    constraints = record.get("constraints")
    if not isinstance(constraints, list) or any(not isinstance(x, str) or not x.strip() for x in constraints):
        errors.append("constraints must be an array of non-empty strings")
    execution = record.get("execution")
    if not isinstance(execution, dict) or execution.get("mode") not in EXECUTION:
        errors.append("execution.mode must be RESEARCH, BLUEPRINT, VALIDATE, or EXECUTE")
    authorization = record.get("authorization")
    if authorization is not None:
        if not isinstance(authorization, dict):
            errors.append("authorization must be an object when supplied")
        else:
            if authorization.get("state") not in AUTHORIZATION:
                errors.append("authorization.state is not a supported value")
            for key in ("actor", "scope", "validUntil"):
                if not isinstance(authorization.get(key), str) or not authorization[key].strip():
                    errors.append(f"authorization.{key} must be a non-empty string")
            if not isinstance(authorization.get("actions"), list):
                errors.append("authorization.actions must be an array")
    if not errors and record["execution"]["mode"] == "EXECUTE":
        if not authorization or authorization.get("state") != "GRANTED":
            errors.append("EXECUTE requires a separate GRANTED authorization record")
    if not errors and record["impact"]["class"] == "PRODUCTION":
        if not authorization or authorization.get("state") != "GRANTED":
            errors.append("PRODUCTION impact requires a separate GRANTED authorization record")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a Methodigitology intent record; never execute it.")
    parser.add_argument("file", type=Path, help="JSON intent record")
    args = parser.parse_args()
    try:
        record = json.loads(args.file.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"INVALID: {exc}", file=sys.stderr)
        return 2
    errors = validate(record)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("VALID: Methodigitology intent record; validation only, no action executed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
