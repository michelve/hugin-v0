---
name: automatic-code-review
description: "Automatic semantic code review triggered after file modifications. Hook-driven skill that logs file changes via PostToolUse and runs the automatic-code-reviewer agent on Stop. Not user-invocable — triggered automatically by lifecycle hooks."
user-invocable: false
disable-model-invocation: true
---

# Automatic Code Review

Hook-driven skill that performs semantic code review after Claude finishes modifying files.

## How It Works

1. **PostToolUse hook** — Logs every `Write`, `Edit`, or `MultiEdit` operation to `/tmp/event-log-{SESSION_ID}.jsonl`
2. **Stop hook** — Checks for new file modifications since the last review, then triggers the `automatic-code-reviewer` agent
3. **Agent** — Reads project-specific rules from the configured `rulesFile` and reviews only the changed files

## Configuration

Settings in `.claude/settings.json`:

```json
{
    "automaticCodeReview": {
        "enabled": true,
        "fileExtensions": ["ts", "tsx"],
        "rulesFile": ".claude/automatic-code-review/rules.md"
    }
}
```

Set `"enabled": false` to disable for a project.

## Components

- `../../agents/automatic-code-reviewer.md` — Review agent (model: haiku, tools: Read, Grep, Glob) — lives at plugin root `agents/`
- `../../hooks/hooks.json` — Hook manifest (PostToolUse + Stop) — merged into plugin root `hooks/`
- `../../scripts/automatic-code-review-plugin.sh` — Shell script for logging and review triggering — lives at plugin root `scripts/`
- `default-rules.md` — Default semantic review rules (stays with skill)
