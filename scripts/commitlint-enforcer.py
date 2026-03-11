#!/usr/bin/env python3
"""
PreToolUse hook - commitlint-enforcer

Intercepts `git commit -m` commands and blocks them if the commit message
violates project commitlint rules. Runs before git and lint-staged.

Rules (from copilot-instructions.md):
  - type prefix from: feat | fix | refactor | docs | chore | test | style
  - subject must be lowercase
  - header must be ≤ 100 characters
  - no trailing dot
"""

import sys
import json
import re

VALID_TYPES = {"feat", "fix", "refactor", "docs", "chore", "test", "style"}

# Matches: git commit [-flags] -m "msg" or -m 'msg'
COMMIT_RE = re.compile(
    r'\bgit\s+commit\b.*?\s-m\s+(?:"((?:[^"\\]|\\.)*)"|\'((?:[^\'\\]|\\.)*)\')',
    re.DOTALL,
)

# Matches valid commit structure: type(optional-scope)?: subject
STRUCTURE_RE = re.compile(r'^([a-z][a-z0-9_-]*)(?:\([^)]+\))?!?:\s+(.+)$')


def validate(msg: str) -> list[str]:
    m = STRUCTURE_RE.match(msg)
    if not m:
        return [
            f'missing or malformed type prefix in: "{msg}"',
            f'expected format: <type>: <lowercase subject>',
            f'valid types: {", ".join(sorted(VALID_TYPES))}',
        ]

    commit_type, subject = m.group(1), m.group(2)
    errors = []

    if commit_type not in VALID_TYPES:
        errors.append(
            f'unknown type "{commit_type}" - valid: {", ".join(sorted(VALID_TYPES))}'
        )
    if msg != msg.lower():
        errors.append('subject must be lowercase')
    if msg.rstrip().endswith('.'):
        errors.append('must not end with a dot')
    if len(msg) > 100:
        errors.append(f'header too long ({len(msg)} chars, max 100)')

    return errors


def suggest(msg: str) -> str:
    m = STRUCTURE_RE.match(msg)
    if m:
        t, s = m.group(1), m.group(2)
        return f'{t}: {s.lower().rstrip(".")}'[:100]
    return 'feat: <describe your change>'


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        sys.exit(0)

    if data.get('tool_name') != 'Bash':
        sys.exit(0)

    command = data.get('tool_input', {}).get('command', '')
    match = COMMIT_RE.search(command)
    if not match:
        sys.exit(0)  # No -m flag or not a commit command - allow

    msg = (match.group(1) or match.group(2) or '').strip()
    errors = validate(msg)

    if errors:
        print(
            '❌ Commit blocked - commitlint violation(s):\n'
            + '\n'.join(f'   • {e}' for e in errors)
            + f'\n\n   Suggested: {suggest(msg)}'
        )
        sys.exit(2)

    sys.exit(0)


if __name__ == '__main__':
    main()
