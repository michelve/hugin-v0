#!/usr/bin/env python3
"""
Environment setup check hook for hugin-v0.

Runs on the first tool use of each session. Checks that required environment
variables are set and warns (once) if any are missing, pointing the user to
/setup for auto-configuration.
"""

import json
import os
import sys
from datetime import datetime

# Required variables and what they're used for
REQUIRED_VARS = [
    {
        "name": "FIGMA_API_KEY",
        "used_by": "figma + figma-console MCP servers",
        "setup_hint": "export FIGMA_API_KEY=fig_xxxxxxxxxxxxxxxxxxxxx",
    },
]

# State directory
STATE_DIR = os.path.expanduser("~/.claude")


def get_state_file(session_id):
    """Session-scoped state file so we only warn once per session."""
    return os.path.join(STATE_DIR, f"hugin_setup_state_{session_id}.json")


def already_checked(session_id):
    """Return True if we already ran the check in this session."""
    state_file = get_state_file(session_id)
    if not os.path.exists(state_file):
        return False
    try:
        with open(state_file, "r") as f:
            data = json.load(f)
        return data.get("checked", False)
    except (json.JSONDecodeError, IOError):
        return False


def mark_checked(session_id):
    """Record that we've checked this session."""
    os.makedirs(STATE_DIR, exist_ok=True)
    state_file = get_state_file(session_id)
    try:
        with open(state_file, "w") as f:
            json.dump({"checked": True, "ts": datetime.now().isoformat()}, f)
    except IOError:
        pass


def cleanup_old_state_files():
    """Remove state files older than 7 days."""
    try:
        if not os.path.exists(STATE_DIR):
            return
        cutoff = datetime.now().timestamp() - (7 * 24 * 60 * 60)
        for fname in os.listdir(STATE_DIR):
            if fname.startswith("hugin_setup_state_") and fname.endswith(".json"):
                fpath = os.path.join(STATE_DIR, fname)
                try:
                    if os.path.getmtime(fpath) < cutoff:
                        os.remove(fpath)
                except OSError:
                    pass
    except Exception:
        pass


def main():
    try:
        raw = sys.stdin.read()
        data = json.loads(raw)
    except (json.JSONDecodeError, ValueError):
        sys.exit(0)

    session_id = data.get("session_id", "default")

    # Only check once per session
    if already_checked(session_id):
        sys.exit(0)

    # Occasional cleanup
    import random
    if random.random() < 0.1:
        cleanup_old_state_files()

    # Check required vars
    missing = []
    for var in REQUIRED_VARS:
        val = os.environ.get(var["name"], "")
        if not val:
            missing.append(var)

    # Mark as checked regardless of result (warn only once)
    mark_checked(session_id)

    if not missing:
        sys.exit(0)

    # Build warning message
    lines = [
        "⚠️  **hugin-v0 setup incomplete** — some required environment variables are missing:\n",
    ]
    for var in missing:
        lines.append(f"  • `{var['name']}` — needed by {var['used_by']}")
        lines.append(f"    → `{var['setup_hint']}`\n")
    lines.append("Run `/setup` or `/setup FIGMA_API_KEY=fig_xxx` to auto-configure.\n")

    print("\n".join(lines), file=sys.stderr)

    # Exit 0 = warn but allow (don't block the tool)
    sys.exit(0)


if __name__ == "__main__":
    main()
