#!/usr/bin/env python3
"""
UserPromptSubmit hook - task-context-injector

Detects task number references in the user's message, reads the matching
task file from .tasks/, and injects the Deliverable + Acceptance Criteria
into Claude's context automatically.

Detection patterns:
  - Zero-padded 4-digit numbers: 0005, 0012
  - "task 5", "task #0005", "task5"
  - "#0005", "#12"

Search order: in-progress/ → backlog/ → done/
"""

import sys
import json
import re
import os
import glob

TASK_DIRS = [
    '.tasks/in-progress',
    '.tasks/backlog',
    '.tasks/done',
]

TASK_NUMBER_RE = re.compile(
    r'(?:'
    r'task\s*#?(\d{1,4})'   # "task 5", "task #0005", "task5"
    r'|#(\d{3,4})\b'         # "#0005", "#12"
    r'|\b(0\d{3})\b'         # bare "0005"
    r')',
    re.IGNORECASE,
)


def find_task_file(number: str) -> str | None:
    padded = number.zfill(4)
    for directory in TASK_DIRS:
        matches = glob.glob(os.path.join(directory, f'{padded}-*.md'))
        if matches:
            return matches[0]
    return None


def extract_sections(content: str, sections: list[str]) -> dict[str, str]:
    """Extract named ## sections from markdown content."""
    result: dict[str, str] = {}
    current_section: str | None = None
    current_lines: list[str] = []

    for line in content.splitlines():
        heading_match = re.match(r'^## (.+)', line)
        if heading_match:
            if current_section:
                result[current_section] = '\n'.join(current_lines).strip()
            current_section = heading_match.group(1).strip()
            current_lines = []
        elif current_section:
            current_lines.append(line)

    if current_section:
        result[current_section] = '\n'.join(current_lines).strip()

    return {k: v for k, v in result.items() if k in sections}


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        sys.exit(0)

    if data.get('hook_event_name') != 'UserPromptSubmit':
        sys.exit(0)

    prompt = data.get('prompt', '')
    match = TASK_NUMBER_RE.search(prompt)
    if not match:
        sys.exit(0)

    # Pick whichever capture group matched
    number = match.group(1) or match.group(2) or match.group(3)
    task_file = find_task_file(number)
    if not task_file:
        sys.exit(0)

    try:
        with open(task_file, encoding='utf-8') as f:
            content = f.read()
    except OSError:
        sys.exit(0)

    padded = number.zfill(4)
    sections = extract_sections(content, ['Deliverable', 'Acceptance Criteria'])

    if not sections:
        sys.exit(0)

    parts = [f'[Task {padded} context - auto-injected from {task_file}]']
    for section_name in ['Deliverable', 'Acceptance Criteria']:
        if section_name in sections and sections[section_name]:
            parts.append(f'\n### {section_name}\n{sections[section_name]}')

    if len(parts) > 1:
        parts.append(
            '\n⚙️  Task lifecycle reminder (auto-injected):\n'
            '   • START  : move task file to .tasks/in-progress/ and set status: in-progress\n'
            '   • FINISH : invoke task-check agent, then move to .tasks/done/ and set status: done'
        )
        print('\n'.join(parts))

    sys.exit(0)


if __name__ == '__main__':
    main()
