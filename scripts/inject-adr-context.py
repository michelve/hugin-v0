#!/usr/bin/env python3
"""Skill-scoped hook for adr-writer: injects next ADR number and template path.

This is a UserPromptSubmit hook that fires when the adr-writer skill is invoked.
It automatically determines the next ADR number and injects context so Claude
doesn't need to manually discover this information.

Usage in SKILL.md frontmatter (hypothesized syntax - needs Claude Code testing):
    hooks:
      UserPromptSubmit:
        - type: command
          command: "python3 ${CLAUDE_SKILL_DIR}/scripts/inject-adr-context.py"
"""
import os
import glob

decisions_dir = os.path.join(os.getcwd(), "docs", "decisions")

if not os.path.isdir(decisions_dir):
    print("[ADR Context] Warning: docs/decisions/ directory not found")
    exit(0)

existing = sorted(glob.glob(os.path.join(decisions_dir, "[0-9]*.md")))

if existing:
    last_file = os.path.basename(existing[-1])
    last_num = int(last_file.split("-")[0])
    next_num = last_num + 1
else:
    next_num = 1

next_padded = str(next_num).zfill(4)
template_path = os.path.join(decisions_dir, "_template.md")
template_exists = os.path.isfile(template_path)

print(f"[ADR Context] Next ADR number: {next_padded}")
print(f"[ADR Context] Template exists: {template_exists}")
print(f"[ADR Context] Existing ADRs: {len(existing)}")
if existing:
    print(f"[ADR Context] Last ADR: {os.path.basename(existing[-1])}")
