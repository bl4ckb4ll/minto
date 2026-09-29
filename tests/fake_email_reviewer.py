#!/usr/bin/env python3
import json
import sys

request = json.load(sys.stdin)
draft = request["draft"]

good = "README says to contact" in draft or "README says to contact you" in draft

result = {
    "message_kind": "request",
    "purpose": "ask about additional checkpoints and useful pull requests",
    "purpose_in_opening": good,
    "support_before_purpose": not good,
    "opening_context_sufficient": True,
    "writer_centered_before_purpose": not good,
    "requested_action": "reply about checkpoints and useful pull requests",
    "requested_action_explicit": good,
}

json.dump(result, sys.stdout, sort_keys=True)
sys.stdout.write("\n")
