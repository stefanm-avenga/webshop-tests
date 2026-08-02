#!/usr/bin/env python3
"""
audit-logging/verifier_stop.py

Turn-end handler (registered on agentStop + subagentStop). Blocks an agent from
finishing unless IT has posted its own audit comment for this session.

Per-agent attribution: the SubagentStop payload carries `agent_type` (e.g.
"coder"). The root agent's Stop has no agent_type → treated as "coordinator".
Built-in sub-agents (e.g. Explore) are not gated.

PAYLOAD CONTRACT (VS Code Copilot agent mode = Claude-Code style):
  - stdin JSON snake_case: session_id, hook_event_name, agent_type (subagentStop)
  - to BLOCK: hookSpecificOutput.decision = "block" (+ reason)
"""
import json
import sys
from pathlib import Path

AUDIT_FILE = Path(".audit/jira-comments.jsonl")

# Agents that must each leave their own audit comment before finishing.
GATED_AGENTS = {"coordinator", "coder", "reviewer", "analyst", "healer", "regression"}


def _trace(event: str, raw: str, extra: str = "") -> None:
    """LOCAL TEST DIAGNOSTIC (remove before VDI)."""
    try:
        Path(".audit").mkdir(parents=True, exist_ok=True)
        with Path(".audit/hook-fired.log").open("a", encoding="utf-8") as f:
            f.write(f"{event} fired (stdin {len(raw)} bytes){extra}\n")
    except Exception:
        pass


def main() -> int:
    raw = sys.stdin.read()
    payload = json.loads(raw) if raw.strip() else {}

    # Root agent (Stop) has no agent_type → it's the coordinator.
    agent = (payload.get("agent_type") or "coordinator").lower()
    session_id = payload.get("session_id")
    _trace("turn-end", raw,
           f" event={payload.get('hook_event_name')!r} agent={agent!r} session={session_id!r}")

    # Built-in / non-QE sub-agents (Explore, etc.) are not gated.
    if agent not in GATED_AGENTS:
        _emit_allow()
        return 0

    if not session_id:
        _emit_allow()  # cannot enforce without a session id; fail open
        return 0

    if _has_entry_for(session_id, agent):
        _emit_allow()
        return 0

    _emit_block(
        f"Agent '{agent}' cannot finish: it has not posted its own audit comment "
        f"for this ticket. Post a JIRA comment (addCommentToJiraIssue) whose body "
        f"has a ```yaml block with `agent: {agent}` and fields agent, phase, ticket, "
        f"scope (list), action, artifacts, status (success|partial|blocked), "
        f"timestamp. Then finish."
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
    json.dump({"hookSpecificOutput": {"hookEventName": "Stop"}}, sys.stdout)


def _emit_block(reason: str) -> None:
    json.dump({"hookSpecificOutput": {
        "hookEventName": "Stop", "decision": "block", "reason": reason}}, sys.stdout)


if __name__ == "__main__":
    sys.exit(main())
