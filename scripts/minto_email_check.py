#!/usr/bin/env python3
import argparse
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

SCHEMA_VERSION = 1

BOOL_FIELDS = (
    "purpose_in_opening",
    "support_before_purpose",
    "opening_context_sufficient",
    "writer_centered_before_purpose",
    "requested_action_explicit",
)

MESSAGE_KINDS = {"request", "informational", "reply"}


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def canonical_json(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def load_bytes(path):
    return Path(path).read_bytes()


def validate_classification(obj):
    if not isinstance(obj, dict):
        raise ValueError("reviewer output must be one JSON object")

    expected = {
        "message_kind",
        "purpose",
        "purpose_in_opening",
        "support_before_purpose",
        "opening_context_sufficient",
        "writer_centered_before_purpose",
        "requested_action",
        "requested_action_explicit",
    }
    extra = set(obj) - expected
    missing = expected - set(obj)
    if missing:
        raise ValueError("missing reviewer fields: " + ", ".join(sorted(missing)))
    if extra:
        raise ValueError("unexpected reviewer fields: " + ", ".join(sorted(extra)))

    if obj["message_kind"] not in MESSAGE_KINDS:
        raise ValueError("invalid message_kind")
    if not isinstance(obj["purpose"], str) or not obj["purpose"].strip():
        raise ValueError("purpose must be a non-empty string")
    for field in BOOL_FIELDS:
        if not isinstance(obj[field], bool):
            raise ValueError(f"{field} must be boolean")

    action = obj["requested_action"]
    if action is not None and not isinstance(action, str):
        raise ValueError("requested_action must be a string or null")

    if obj["message_kind"] == "request" and (action is None or not action.strip()):
        raise ValueError("request messages must identify requested_action")

    return obj


def policy(classification):
    failures = []

    if not classification["purpose_in_opening"]:
        failures.append("purpose_not_in_opening")
    if classification["support_before_purpose"]:
        failures.append("support_before_purpose")
    if not classification["opening_context_sufficient"]:
        failures.append("opening_context_insufficient")
    if classification["writer_centered_before_purpose"]:
        failures.append("writer_centered_material_before_purpose")

    if classification["message_kind"] == "request":
        if not classification["requested_action_explicit"]:
            failures.append("requested_action_not_explicit")

    return {
        "passed": not failures,
        "failures": failures,
    }


def run_check(args):
    draft_bytes = load_bytes(args.draft)
    rubric_bytes = load_bytes(args.rubric)

    request = {
        "schema_version": SCHEMA_VERSION,
        "rubric": rubric_bytes.decode("utf-8"),
        "draft": draft_bytes.decode("utf-8"),
    }
    stdin_text = canonical_json(request) + "\n"

    proc = subprocess.run(
        args.reviewer,
        input=stdin_text,
        text=True,
        capture_output=True,
        check=False,
    )

    if proc.returncode != 0:
        sys.stderr.write(proc.stderr)
        raise SystemExit(f"reviewer exited {proc.returncode}")

    raw_stdout = proc.stdout
    try:
        classification = validate_classification(json.loads(raw_stdout))
    except (json.JSONDecodeError, ValueError) as exc:
        raise SystemExit(f"invalid reviewer output: {exc}")

    result = policy(classification)

    receipt = {
        "schema_version": SCHEMA_VERSION,
        "draft_sha256": sha256_bytes(draft_bytes),
        "rubric_sha256": sha256_bytes(rubric_bytes),
        "model_id": args.model_id,
        "model_revision": args.model_revision,
        "reviewer_argv": args.reviewer,
        "reviewer_stdout_sha256": sha256_bytes(raw_stdout.encode("utf-8")),
        "classification": classification,
        "policy": result,
        "ci": {
            "github_sha": os.environ.get("GITHUB_SHA"),
            "github_run_id": os.environ.get("GITHUB_RUN_ID"),
            "github_run_attempt": os.environ.get("GITHUB_RUN_ATTEMPT"),
        },
    }

    Path(args.receipt).write_text(
        json.dumps(receipt, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print(f"draft_sha256={receipt['draft_sha256']}")
    print(f"rubric_sha256={receipt['rubric_sha256']}")
    print(f"receipt={args.receipt}")
    print("passed=" + ("true" if result["passed"] else "false"))
    if result["failures"]:
        print("failures=" + ",".join(result["failures"]))

    return 0 if result["passed"] else 1


def run_verify(args):
    draft_bytes = load_bytes(args.draft)
    rubric_bytes = load_bytes(args.rubric)
    receipt = json.loads(Path(args.receipt).read_text(encoding="utf-8"))

    failures = []

    if receipt.get("schema_version") != SCHEMA_VERSION:
        failures.append("schema_version")
    if receipt.get("draft_sha256") != sha256_bytes(draft_bytes):
        failures.append("draft_hash")
    if receipt.get("rubric_sha256") != sha256_bytes(rubric_bytes):
        failures.append("rubric_hash")

    classification = receipt.get("classification")
    try:
        classification = validate_classification(classification)
        expected_policy = policy(classification)
    except ValueError:
        failures.append("classification")
        expected_policy = None

    if expected_policy is not None and receipt.get("policy") != expected_policy:
        failures.append("policy")

    if args.model_id is not None and receipt.get("model_id") != args.model_id:
        failures.append("model_id")
    if args.model_revision is not None and receipt.get("model_revision") != args.model_revision:
        failures.append("model_revision")

    if failures:
        print("verified=false")
        print("failures=" + ",".join(failures))
        return 1

    if not receipt["policy"]["passed"]:
        print("verified=true")
        print("passed=false")
        return 1

    print("verified=true")
    print("passed=true")
    print(f"draft_sha256={receipt['draft_sha256']}")
    return 0


def parser():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="command", required=True)

    check = sub.add_parser("check")
    check.add_argument("--draft", required=True)
    check.add_argument("--rubric", required=True)
    check.add_argument("--receipt", required=True)
    check.add_argument("--model-id", required=True)
    check.add_argument("--model-revision", required=True)
    check.add_argument(
        "--reviewer",
        nargs=argparse.REMAINDER,
        required=True,
        help="reviewer command; must be the final option",
    )
    check.set_defaults(func=run_check)

    verify = sub.add_parser("verify")
    verify.add_argument("--draft", required=True)
    verify.add_argument("--rubric", required=True)
    verify.add_argument("--receipt", required=True)
    verify.add_argument("--model-id")
    verify.add_argument("--model-revision")
    verify.set_defaults(func=run_verify)

    return p


def main():
    args = parser().parse_args()
    if args.command == "check" and not args.reviewer:
        raise SystemExit("--reviewer requires a command")
    raise SystemExit(args.func(args))


if __name__ == "__main__":
    main()
