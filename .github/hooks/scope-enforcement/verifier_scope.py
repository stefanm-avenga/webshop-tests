#!/usr/bin/env python3
"""
scope-enforcement/verifier_scope.py

PreToolUse handler, attached via AGENT-SCOPED HOOKS (a `hooks:` block in the
analyst/coder/reviewer .agent.md frontmatter; requires the VS Code setting
chat.useCustomAgentHooks). Every event reaching this script is a gated
specialist's tool call by construction — no agent identity check is needed
or possible (tool events carry no agent_type; only Stop events do).

Confines the specialist to the paths declared in .qe-active-scope.json,
which @coordinator writes at dispatch time. Context management as much as
safety: a UI ticket's agents never load database or API internals.

Fail-closed: no valid scope file -> deny file access. The coordinator
carries no scope hook, so triage (before the file exists) is unaffected.

PAYLOAD CONTRACT (spike-verified 2026-08-02): stdin snake_case JSON with
tool_name, tool_input. File paths arrive as ABSOLUTE Windows paths under
filePath keys, possibly NESTED (multi_replace_string_in_file uses
replacements[].filePath). Decision via hookSpecificOutput/permissionDecision.
"""
import json
import re
import sys
from pathlib import Path

SCOPE_FILE = Path(".qe-active-scope.json")

# Relative paths every specialist may always touch: the registry it may
# consult and the scope file itself. Membership is checked case-insensitively
# (Windows semantics) — see main().
BASELINE_ALLOWED = {".qe-projects.yaml", ".qe-active-scope.json"}

# A drive-relative path (e.g. "c:db\\inventory.py") names a location relative
# to the current directory ON that drive, not an absolute path — resolving it
# would silently depend on process state we can't verify. Deny by design.
_DRIVE_RELATIVE = re.compile(r"^[A-Za-z]:(?![/\\])")


def _is_path_key(key):
    """Key heuristic replacing the old closed PATH_KEYS set.

    Catches filePath, file_path, oldPath, newPath, notebookPath, dirPath,
    documentUri, uri, path, etc. Must not catch query, includePattern,
    command, cwd, explanation, agentName — none of those contain "path" or
    "uri" as a substring of the lowercased key.
    """
    lk = key.lower()
    return "path" in lk or "uri" in lk


def _extract_paths(node, out=None):
    """Collect path-like string values recursively from the tool input.

    A path-heuristic key may hold either a single string (filePath) or a
    list of strings (filePaths) — both are collected. Anything else under a
    matching key (or any value under a non-matching key) is still recursed
    into, so nested payloads keep working.
    """
    if out is None:
        out = []
    if isinstance(node, dict):
        for key, value in node.items():
            if _is_path_key(key) and isinstance(value, str) and value.strip():
                out.append(value)
            elif _is_path_key(key) and isinstance(value, list):
                for item in value:
                    if isinstance(item, str) and item.strip():
                        out.append(item)
                    else:
                        _extract_paths(item, out)
            else:
                _extract_paths(value, out)
    elif isinstance(node, list):
        for item in node:
            _extract_paths(item, out)
    return out


# Entries that would, after normalisation, refer to the repo root itself.
# ["."] as allowed_paths silently disables the hook (everything normalises
# under "."), so the scope-file validation rejects it as malformed.
_ROOT_EQUIVALENT = {"", ".", "/", "./"}


def _is_root_equivalent(entry):
    normalized = str(entry).strip().replace("\\", "/")
    return normalized in _ROOT_EQUIVALENT


def _repo_relative(path_str):
    """Normalise to a repo-relative POSIX path; None if it escapes the repo.

    Absolute paths are compared case-insensitively against the CWD (the
    repo root — hooks run with cwd '.'), matching Windows semantics.
    """
    raw = path_str.replace("\\", "/")
    if raw.startswith("//"):
        # UNC path (\\server\share\...). Never call resolve() on this: an
        # unreachable host/share can hang the process. Deny outright.
        return None
    if _DRIVE_RELATIVE.match(raw):
        return None
    if Path(raw).is_absolute():
        root = str(Path.cwd().resolve()).replace("\\", "/").rstrip("/")
        full = str(Path(raw).resolve()).replace("\\", "/")
        if not full.lower().startswith(root.lower() + "/"):
            return None
        raw = full[len(root) + 1:]
    parts = []
    for part in raw.split("/"):
        if part == "..":
            if not parts:
                return None
            parts.pop()
            continue
        if part in (".", ""):
            continue
        # Windows silently strips trailing dots/spaces from path segments
        # (e.g. "features." and "features" name the same directory) —
        # normalise the same way so scope checks aren't foolable by them.
        stripped = part.rstrip(". ")
        if stripped:
            parts.append(stripped)
    return "/".join(parts)


def _in_scope(rel, allowed):
    # No allow-all branch here by design: a root-equivalent entry is
    # rejected as malformed when the scope file is loaded (see
    # _is_root_equivalent), so every entry reaching this function should
    # already name a concrete subtree. A stray empty-after-normalisation
    # entry simply matches nothing, rather than granting blanket access.
    rel_l = rel.lower()
    for entry in allowed:
        entry = str(entry).strip().strip("/").replace("\\", "/").lower()
        if not entry:
            continue
        if rel_l == entry or rel_l.startswith(entry + "/"):
            return True
    return False


def main() -> int:
    raw = sys.stdin.read()
    if not raw.strip():
        # Empty stdin is a harness quirk we've observed, not a hostile or
        # malformed payload — fail open so it doesn't brick unrelated tool
        # calls that never carried a body to begin with.
        _emit_allow()
        return 0
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        # Non-empty but unparseable: unlike the empty-stdin case, this is
        # data we can't trust, so fail closed.
        _emit_deny(
            "scope-enforcement hook received an unreadable payload; denying "
            "by default. Retry the action; if this persists, report to "
            "@coordinator.")
        return 0

    tool_name = payload.get("tool_name") or ""
    if tool_name.startswith("mcp_"):
        # MCP tools are remote API calls, not filesystem access — their
        # path-shaped argument names (e.g. GitHub's `path`) name a location
        # on the remote service, not a local file, so scope doesn't apply.
        _emit_allow()
        return 0

    tool_input = payload.get("tool_input") or {}

    targets = _extract_paths(tool_input)
    if not targets:
        _emit_allow()  # search/terminal/delegation: nothing to judge
        return 0

    if not SCOPE_FILE.exists():
        _emit_deny(
            "No active scope declared. Specialist agents get file access only "
            "after @coordinator dispatches a ticket (it writes "
            ".qe-active-scope.json). Report this to @coordinator and stop.")
        return 0
    try:
        scope = json.loads(SCOPE_FILE.read_text(encoding="utf-8"))
        ticket = scope["ticket"]
        allowed = scope["allowed_paths"]
        if not isinstance(allowed, list) or not allowed:
            raise ValueError("allowed_paths must be a non-empty list")
        if any(_is_root_equivalent(entry) for entry in allowed):
            raise ValueError(
                "allowed_paths must not contain a root-equivalent entry")
    except Exception:
        _emit_deny(
            ".qe-active-scope.json exists but is malformed (need: ticket, "
            "allowed_paths list with no root-equivalent entries). "
            "@coordinator must rewrite it before specialist file access can "
            "proceed.")
        return 0

    baseline_lower = {b.lower() for b in BASELINE_ALLOWED}
    for target in targets:
        rel = _repo_relative(target)
        if rel is not None and rel.lower() in baseline_lower:
            continue
        if rel is None or not _in_scope(rel, allowed):
            _emit_deny(
                f"BLOCKED by scope-enforcement hook: '{target}' is outside "
                f"the active scope for ticket {ticket} (allowed: "
                f"{', '.join(str(a) for a in allowed)}). Do not retry or work "
                "around this — if you believe you need this file, report the "
                "path to @coordinator.")
            return 0
    _emit_allow()
    return 0


def _emit_allow():
    json.dump({"hookSpecificOutput": {
        "hookEventName": "PreToolUse", "permissionDecision": "allow"}}, sys.stdout)


def _emit_deny(reason):
    json.dump({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": reason}}, sys.stdout)


if __name__ == "__main__":
    sys.exit(main())
