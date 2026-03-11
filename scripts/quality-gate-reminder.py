#!/usr/bin/env python3
"""
PostToolUse hook - quality-gate-reminder

After any .ts / .tsx file write, injects a reminder to run the quality
gates before committing. Eliminates the most common cause of push failures.

Triggers on: Write, Edit, MultiEdit tools targeting .ts or .tsx files
Does not trigger on: .md, .json, .css, .prisma, or any other file types
"""

import sys
import json

REMINDER = """\
📋 Quality gate reminder (auto-injected):
TypeScript file modified - run before committing:

    pnpm typecheck
    pnpm biome:check

Source: orchestrator.instructions.md § Quality Gates\
"""


def get_file_path(tool_name: str, tool_input: dict) -> str:
    return tool_input.get('file_path') or tool_input.get('path') or ''


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        sys.exit(0)

    if data.get('hook_event_name') != 'PostToolUse':
        sys.exit(0)

    tool_name = data.get('tool_name', '')
    if tool_name not in {'Write', 'Edit', 'MultiEdit'}:
        sys.exit(0)

    file_path = get_file_path(tool_name, data.get('tool_input', {}))
    if file_path.endswith('.ts') or file_path.endswith('.tsx'):
        print(REMINDER)

    sys.exit(0)


if __name__ == '__main__':
    main()
