#!/usr/bin/env python3
"""
audit-logging/verifier_pretooluse.py

preToolUse handler. Blocks delegation to a QE SPECIALIST (runSubagent with a
target in the specialist set) until the coordinator has posted its own audit
comment for this session. Delegations to built-in helpers (e.g. Explore) pass
freely. This enforces "the coordinator must comment before delegating".

PAYLOAD CONTRACT (VS Code Copilot agent mode = Claude-Code style):
  - stdin JSON snake_case: tool_name, tool_input, session_id
  - decision via hookSpecificOutput / permissionDecision
"""
import json
import sys
from pathlib import Path

AUDIT_FILE = Path(".audit/jira-comments.jsonl")

# QE specialists whose invocation is a coordinator-driven delegation.
GATED_SPECIALISTS = {"coder", "reviewer", "analyst", "healer", "regression"}


def _trace(event: str, raw: str, extra: str = "") -> None:
    """LOCAL TEST DIAGNOSTIC (remove before VDI)."""
    try:
        Path(".audit").mkdir(parents=True, exist_ok=True)
        with Path(".audit/hook-fired.log").open("a", encoding="utf-8") as f:
            f.write(f"{event} fired (stdin {len(raw)} bytes){extra}\n")
    except Exception:
        pass


def _is_delegation(tool_name: str) -> bool:
    name = (tool_name or "").lower()
    return "subagent" in name or name == "agent" or name.endswith("/agent")


def main() -> int:
    raw = sys.stdin.read()
    payload = json.loads(raw) if raw.strip() else {}
    tool_name = payload.get("tool_name", "")
    target = (payload.get("tool_input") or {}).get("agentName", "")
    _trace("preToolUse", raw,
           f" tool={tool_name!r} session={payload.get('session_id')!r} target={target!r}")

    # Only gate delegation to a QE specialist. Built-in sub-agents (Explore, etc.)
    # and all non-delegation tools pass straight through.
    if not _is_delegation(tool_name) or target.lower() not in GATED_SPECIALISTS:
        _emit_allow()
        return 0

    session_id = payload.get("session_id")
    if not session_id:
        _emit_allow()  # cannot enforce without a session id; fail open
        return 0

    # Delegating to a specialist is a coordinator action — require the
    # coordinator's own attestation for this session.
    if _has_entry_for(session_id, "coordinator"):
        _emit_allow()
        return 0

    _emit_deny(
        f"You cannot delegate to '{target}' yet: the coordinator has not posted its "
        "own audit comment for this ticket. FIRST post a JIRA comment "
        "(addCommentToJiraIssue) whose body has a ```yaml block with `agent: coordinator` "
        "and fields agent, phase, ticket, scope (list), action, artifacts, "
        "status (success|partial|blocked), timestamp. THEN delegate."
    )
    return 0


def _has_entry_for(session_id: str, agent: str) -> bool:
    if not AUDIT_FILE.exists():
        return False
    agent = agent.lower()
    with AUDIT_FILE.open(encoding="utf-8") as f:
        for line in f:
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue
            if entry.get("session_id") == session_id and \
               (entry.get("agent") or "").lower() == agent:
                return True
    return False


def _emit_allow() -> None:
    json.dump({"hookSpecificOutput": {
        "hookEventName": "PreToolUse", "permissionDecision": "allow"}}, sys.stdout)


def _emit_deny(reason: str) -> None:
    json.dump({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": reason}}, sys.stdout)


if __name__ == "__main__":
    sys.exit(main())
