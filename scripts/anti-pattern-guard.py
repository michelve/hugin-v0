#!/usr/bin/env python3
"""
PreToolUse hook - anti-pattern-guard

Warns (does not block) when React/TypeScript anti-patterns from
orchestrator.instructions.md are detected in .ts / .tsx file writes.
Catches drift at write-time rather than in code review.

Covered patterns:
  - React.FC           (removed in React 19)
  - forwardRef(        (removed in React 19)
  - .propTypes =       (removed in React 19)
  - export default function in .tsx  (banned - named exports only)
"""

import sys
import json

ANTI_PATTERNS = [
    {
        'pattern': 'React.FC',
        'rule': 'React.FC was removed in React 19.',
        'fix': 'function MyComponent(props: Props) { ... }',
    },
    {
        'pattern': 'forwardRef(',
        'rule': 'forwardRef was removed in React 19 - pass ref as a regular prop.',
        'fix': 'function MyComponent({ ref, ...props }: Props & { ref?: React.Ref<T> }) { ... }',
    },
    {
        'pattern': '.propTypes =',
        'rule': 'propTypes were removed in React 19 - use TypeScript interface instead.',
        'fix': 'interface Props { name: string; }',
    },
    {
        'pattern': 'export default function',
        'rule': 'Default exports are banned - named exports only.',
        'fix': 'export function MyComponent() { ... }',
        'tsx_only': True,
    },
]


def get_file_path(tool_name: str, tool_input: dict) -> str:
    return tool_input.get('file_path') or tool_input.get('path') or ''


def get_content(tool_name: str, tool_input: dict) -> str:
    if tool_name == 'Write':
        return tool_input.get('content', '')
    if tool_name == 'Edit':
        return tool_input.get('new_string', '')
    if tool_name == 'MultiEdit':
        edits = tool_input.get('edits', [])
        return '\n'.join(e.get('new_string', '') for e in edits)
    return ''


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        sys.exit(0)

    tool_name = data.get('tool_name', '')
    if tool_name not in {'Write', 'Edit', 'MultiEdit'}:
        sys.exit(0)

    tool_input = data.get('tool_input', {})
    file_path = get_file_path(tool_name, tool_input)

    is_ts = file_path.endswith('.ts')
    is_tsx = file_path.endswith('.tsx')
    if not (is_ts or is_tsx):
        sys.exit(0)

    content = get_content(tool_name, tool_input)
    if not content:
        sys.exit(0)

    hits = []
    for ap in ANTI_PATTERNS:
        if ap.get('tsx_only') and not is_tsx:
            continue
        if ap['pattern'] in content:
            hits.append(ap)

    if hits:
        lines = [f'⚠️  Anti-pattern guard - {file_path}:']
        for h in hits:
            lines.append(f'\n   ✗ Pattern : {h["pattern"]}')
            lines.append(f'     Rule    : {h["rule"]}')
            lines.append(f'     Fix     : {h["fix"]}')
        lines.append('\n   Source: orchestrator.instructions.md § Anti-Patterns')
        print('\n'.join(lines))

    sys.exit(0)  # Warn only - do not block


if __name__ == '__main__':
    main()
