---
name: adr-writer
description: "Write, validate, and commit Architecture Decision Records in MADR 4.0.0 format. Use when user says 'write an ADR', 'create an ADR', 'document this decision', 'ADR for X', 'architecture decision record for X', 'record this decision', 'document the decision to use X', or wants to formally capture an architectural choice. Do NOT trigger on 'what ADR covers X?', 'show me the ADR for Y', 'does this violate an ADR?', or 'check ADR compliance' - those are lookup/audit tasks."
argument-hint: "supersedes: NNNN (optional, when replacing an existing ADR)"
user-invocable: true
context: fork
---

This skill uses extended thinking for complex architectural trade-off analysis. ultrathink

# ADR Writer

Writes complete, validated Architecture Decision Records in MADR 4.0.0 format and commits them to `docs/decisions/`. Follow `write-adr.prompt.md` for the full 10-step workflow.

## When to Activate

**Activate on:**

- "write an ADR for X"
- "create an ADR"
- "document this decision"
- "ADR for X"
- "architecture decision record for X"
- "record this decision"
- "document the decision to use X"
- "we decided to use X, write that up"
- Invoked from `check-adr-violations.prompt.md` with a `supersedes: NNNN` parameter

**Do NOT activate on:**

- "what ADR covers X?" → lookup task, read the index
- "show me the ADR for Y" → lookup task, read the file
- "does this violate an ADR?" → audit task, use `check-adr-violations.prompt.md`
- "check ADR compliance" → audit task, use `check-adr-violations.prompt.md`

## MADR 4.0.0 - Mandatory Sections

Every ADR must contain all five mandatory sections. Missing any one = invalid.

| Section                       | Required | Notes                                         |
| ----------------------------- | -------- | --------------------------------------------- |
| YAML frontmatter              | ✅       | `status` + `date` always present              |
| Context and Problem Statement | ✅       | 2–4 sentences, factual, project-specific      |
| Considered Options            | ✅       | 2–4 options, concise noun phrases             |
| Decision Outcome              | ✅       | Must start with `Chosen option: "X", because` |
| Consequences                  | ✅       | At least one Good + one Bad bullet            |

## Phrasing Rules (non-negotiable)

**Decision Outcome** - exact format:

```
Chosen option: "{option name}", because {justification}.
```

**Consequences** bullets - exact format:

```
- Good, because {positive consequence}.
- Bad, because {negative consequence}.
- Neutral, because {neutral consequence}.
```

## Numbering Convention

1. Read `docs/decisions/README.md` - find highest `NNNN`
2. Increment by 1
3. Filename: `NNNN-short-title.md` (lowercase kebab-case, max 5 words)
4. Always update the index table in `docs/decisions/README.md` after writing the file

## Status Values

| Status       | When to use                                                 |
| ------------ | ----------------------------------------------------------- |
| `accepted`   | Decision is made and implemented (most common)              |
| `proposed`   | Decision under discussion, not yet implemented              |
| `superseded` | Replaced by a newer ADR - add `superseded-by: NNNN - Title` |
| `deprecated` | No longer relevant, not replaced                            |

## Supersede Flow

When replacing an existing ADR (triggered by violation checker or user intent):

1. New ADR frontmatter gets `supersedes: "NNNN - Old Title"`
2. Old ADR frontmatter changes to `status: superseded` + `superseded-by: "NNNN - New Title"`
3. Old ADR row in `docs/decisions/README.md` status column → `superseded`
4. New ADR row added to index as `accepted`

## Optional: Web Research

If the user asks for external evidence or benchmarks to support the decision, invoke the `web-research-specialist` agent before finalizing. Use its findings in the Consequences section or a More Information section.

## Arguments

When invoked with the `supersedes: NNNN` argument (either by user or from `check-adr-violations.prompt.md`), the $ARGUMENTS variable contains the ADR number to supersede.

Example invocation: `/adr-writer supersedes: 0005`

The argument is parsed to:

- Mark the old ADR (0005) as `status: superseded`
- Add `supersedes: "0005 - Old Title"` to the new ADR frontmatter
- Update the index table in README.md to reflect the supersession

If no arguments are provided, this is a new ADR with no supersession relationship.

## Session Tracking

This skill logs the session ID using ${CLAUDE_SESSION_ID} for correlation:

```
ADR creation session: ${CLAUDE_SESSION_ID}
```

This allows tracking which ADRs were written in the same conversation and correlating with git commits when troubleshooting.

## Action

Invoke `.github/prompts/write-adr.prompt.md` and follow its steps in order. Do not shortcut or skip the validation step.
