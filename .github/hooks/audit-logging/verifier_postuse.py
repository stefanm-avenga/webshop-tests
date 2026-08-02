#!/usr/bin/env python3
"""
audit-logging/verifier_postuse.py

postToolUse handler. When an agent posts a JIRA comment (or writes the local
audit-file fallback), find the audit YAML block in the tool input, validate it
against the schema, and append an attestation entry to .audit/jira-comments.jsonl
keyed by session_id. Non-blocking: enforcement happens at preToolUse (delegation)
and Stop (turn-end).

PAYLOAD CONTRACT (VS Code Copilot agent mode = Claude-Code style):
  - stdin JSON uses snake_case: tool_name, tool_input, tool_response, session_id
  - the audit block may arrive as a fenced ```yaml block in a string, or as
    Atlassian ADF where the text is nested (no literal fence). Both are handled.
"""
import re
import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None  # fall back to _minimal_yaml_parse

AUDIT_FILE = Path(".audit/jira-comments.jsonl")

REQUIRED_FIELDS = (
    "agent", "phase", "ticket", "scope", "action",
    "artifacts", "status", "timestamp",
)
VALID_STATUSES = {"success", "partial", "blocked"}
# Lenient: any language tag (```yaml, ```yml, ```) or none.
AUDIT_BLOCK_RE = re.compile(r"```[a-zA-Z]*\s*\n(.*?)\n```", re.DOTALL)


def _trace(event: str, raw: str) -> None:
    """LOCAL TEST DIAGNOSTIC (remove before VDI): record that this hook fired."""
    try:
        Path(".audit").mkdir(parents=True, exist_ok=True)
        with Path(".audit/hook-fired.log").open("a", encoding="utf-8") as f:
            f.write(f"{event} fired (stdin {len(raw)} bytes)\n")
    except Exception:
        pass


def _is_delegation(tool_name: str) -> bool:
    name = (tool_name or "").lower()
    return "subagent" in name or name == "agent" or name.endswith("/agent")


def main() -> int:
    raw = sys.stdin.read()
    _trace("postToolUse", raw)
    payload = json.loads(raw) if raw.strip() else {}
    tool_name = payload.get("tool_name", "")

    # Skip delegation calls (the audit block could appear in a delegation prompt
    # and falsely attest). Any other tool's input is fair game.
    if not _is_delegation(tool_name):
        audit = _find_audit_block(payload.get("tool_input"))
        if audit is not None and _validate(audit):
            _write_attestation(audit, payload)

    _emit_noop()
    return 0


def _collect_strings(obj) -> list:
    """Recursively gather every string in a nested structure (handles ADF)."""
    out = []
    if isinstance(obj, str):
        out.append(obj)
    elif isinstance(obj, dict):
        for v in obj.values():
            out.extend(_collect_strings(v))
    elif isinstance(obj, list):
        for v in obj:
            out.extend(_collect_strings(v))
    return out


def _find_audit_block(tool_input) -> dict | None:
    """Look for a valid audit block: first as a fenced block in any string,
    then by parsing whole strings directly (ADF / fence-less)."""
    texts = _collect_strings(tool_input)
    if not texts:
        return None
    combined = "\n".join(texts)

    candidates = []
    for t in texts + [combined]:
        for m in AUDIT_BLOCK_RE.finditer(t):
            candidates.append(m.group(1))
    candidates.extend(texts)        # raw strings (ADF text nodes, fence-less)
    candidates.append(combined)

    for raw in candidates:
        audit = _parse_yaml(raw)
        if isinstance(audit, dict) and _validate(audit):
            return audit
    return None


def _write_attestation(audit: dict, payload: dict) -> None:
    entry = {
        "session_id": payload.get("session_id"),
        "timestamp_ms": payload.get("timestamp"),
        "tool_name": payload.get("tool_name"),
        "agent": audit.get("agent"),
        "ticket": audit.get("ticket"),
        "phase": audit.get("phase"),
        "action": audit.get("action"),
        "status": audit.get("status"),
        "comment_id": _extract_comment_id(json.dumps(payload.get("tool_response", ""))),
    }
    AUDIT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with AUDIT_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")


def _parse_yaml(raw: str) -> dict | None:
    if not raw or not raw.strip():
        return None
    if yaml:
        try:
            parsed = yaml.safe_load(raw)
            return parsed if isinstance(parsed, dict) else None
        except yaml.YAMLError:
            return None
    return _minimal_yaml_parse(raw)


def _minimal_yaml_parse(raw: str) -> dict | None:
    """Fallback parser supporting flat scalars, inline lists, AND block lists
    (a `key:` line followed by `- item` lines)."""
    result: dict = {}
    current_key = None
    for line in raw.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        # block-list item belonging to the most recent key
        if stripped.startswith("- ") and current_key is not None:
            if not isinstance(result.get(current_key), list):
                result[current_key] = []
            result[current_key].append(stripped[2:].strip().strip('"').strip("'"))
            continue
        if ":" not in stripped:
            continue
        key, _, value = stripped.partition(":")
        key = key.strip()
        value = value.strip()
        current_key = key
        if value == "":
            # empty for now; following `- item` lines may turn it into a list
            result[key] = ""
        elif value.startswith("[") and value.endswith("]"):
            items = value[1:-1].split(",")
            result[key] = [x.strip().strip('"').strip("'") for x in items if x.strip()]
        else:
            result[key] = value.strip('"').strip("'")
    return result if result else None


def _validate(audit: dict) -> bool:
    if not isinstance(audit, dict):
        return False
    if not all(field in audit for field in REQUIRED_FIELDS):
        return False
    if audit.get("status") not in VALID_STATUSES:
        return False
    if not isinstance(audit.get("scope"), list):
        return False
    return True


def _extract_comment_id(result_text: str) -> str | None:
    match = re.search(r"comment[ _]?id[\"':\s]+(\d+)", result_text, re.IGNORECASE)
    return match.group(1) if match else None


def _emit_noop() -> None:
    json.dump({"hookSpecificOutput": {"hookEventName": "PostToolUse"}}, sys.stdout)


if __name__ == "__main__":
    sys.exit(main())
