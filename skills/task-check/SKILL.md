---
name: task-check
description: "Verify task completion before finishing work. Agent-driven skill that checks acceptance criteria, catches incomplete work, bugs, and quality issues. Spawn with task ID, location, and work summary."
argument-hint: "<task-id> <task-location> [attempt]"
user-invocable: true
---

# Task Check

Verifies task completion before Claude finishes work. Catches incomplete work, bugs, and quality issues.

## Usage

Spawn the `task-check` agent with:

1. **Task ID** — From task file name, number, or issue reference
2. **Task location** — File path or CLI command to retrieve task details (default: `.tasks/in-progress/`)
3. **Work summary** — Files modified, changes made, decisions, what you skipped
4. **Attempt** — Which attempt (1, 2, or 3). Start with 1. Max 3 attempts.

## Components

- `agents/task-check.md` — Verification agent (tools: Read, color: yellow)
- `commands/check.md` — Manual trigger command with argument hints

## Protocol

1. Agent reads CLAUDE.md, PRD, task docs, and referenced documents
2. Compares work summary against task requirements and acceptance criteria
3. Returns structured verdict: PASS, FAIL, or NEED_INFO
4. On FAIL: follow the agent's report instructions and retry (up to 3 attempts)
