#!/usr/bin/env python3
"""
UserPromptSubmit hook - adr-gate

Detects qualifying architectural decision keywords in the user's message and
injects an ADR violation check reminder before Claude processes the prompt.

Makes the orchestrator's ADR Auto-Gate mandatory rather than recall-dependent.

Trigger keywords (case-insensitive):
  install, add library/package/dependency, switch to, migrate to/from,
  replace...with, new pattern/layer/convention/architecture, deprecate,
  use X instead
"""

import sys
import json
import re

TRIGGER_PATTERNS = [
    r'\binstall\b',
    r'\badd\s+(?:a\s+)?(?:library|package|dependency|dep)\b',
    r'\bswitch\s+to\b',
    r'\bmigrate\s+(?:to|from)\b',
    r'\breplace\b.{0,40}\bwith\b',
    r'\bnew\s+(?:pattern|layer|convention|architecture)\b',
    r'\bdeprecate\b',
    r'\buse\s+\S+\s+instead\b',
]

ADR_REMINDER = """\
⚠️  ADR Gate (auto-injected by adr-gate hook):
This message may describe a qualifying architectural decision.

Before implementing, silently run these steps:
  1. Read all status:accepted ADRs from docs/decisions/README.md
  2. Compare the proposed approach against each ADR's Decision Outcome
  3. Conflict found  → stop; present Comply OR Supersede options to user
  4. No conflict     → proceed with implementation

Reference: orchestrator.instructions.md § ADR Auto-Gate\
"""


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        sys.exit(0)

    if data.get('hook_event_name') != 'UserPromptSubmit':
        sys.exit(0)

    prompt = data.get('prompt', '')

    for pattern in TRIGGER_PATTERNS:
        if re.search(pattern, prompt, re.IGNORECASE):
            print(ADR_REMINDER)
            sys.exit(0)

    sys.exit(0)


if __name__ == '__main__':
    main()
