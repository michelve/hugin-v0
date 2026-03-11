---
name: skill-developer
description: Create and manage Claude Code skills following Anthropic best practices. Use when creating new skills, modifying skill-rules.json, understanding trigger patterns, working with hooks, debugging skill activation, or implementing progressive disclosure. Covers skill structure, YAML frontmatter, trigger types (keywords, intent patterns, file paths, content patterns), enforcement levels (block, suggest, warn), hook mechanisms (UserPromptSubmit, PreToolUse), session tracking, and the 500-line rule.
user-invocable: true
disable-model-invocation: true
---

# Skill Developer Guide

## Purpose

Comprehensive guide for creating and managing skills in Claude Code with auto-activation system, following Anthropic's official best practices including the 500-line rule and progressive disclosure pattern.

## When to Use This Skill

Automatically activates when you mention:

- Creating or adding skills
- Modifying skill triggers or rules
- Understanding how skill activation works
- Debugging skill activation issues
- Working with skill-rules.json
- Hook system mechanics
- Claude Code best practices
- Progressive disclosure
- YAML frontmatter
- 500-line rule

---

## System Overview

See [hook-architecture.md](reference/hook-architecture.md) for the two-hook architecture (UserPromptSubmit + Stop Hook) and configuration file details.

---

## Skill Types

See [skill-types.md](reference/skill-types.md) for guardrail skills (block enforcement) and domain skills (suggest enforcement) with examples.

---

## Quick Start: Creating a New Skill

See [quick-start-workflow.md](reference/quick-start-workflow.md) for the 5-step workflow: create skill file, add to skill-rules.json, test triggers, refine patterns, follow best practices.

---

## Enforcement Levels

### BLOCK (Critical Guardrails)

- Physically prevents Edit/Write tool execution
- Exit code 2 from hook, stderr → Claude
- Claude sees message and must use skill to proceed
- **Use For**: Critical mistakes, data integrity, security issues

**Example:** Database column name verification

### SUGGEST (Recommended)

- Reminder injected before Claude sees prompt
- Claude is aware of relevant skills
- Not enforced, just advisory
- **Use For**: Domain guidance, best practices, how-to guides

**Example:** Frontend development guidelines

### WARN (Optional)

- Low priority suggestions
- Advisory only, minimal enforcement
- **Use For**: Nice-to-have suggestions, informational reminders

**Rarely used** - most skills are either BLOCK or SUGGEST.

---

## Skip Conditions & User Control

See [enforcement-skip.md](reference/enforcement-skip.md) for session tracking, file markers, and environment variable overrides.

---

## Testing Checklist

When creating a new skill, verify:

- [ ] Skill file created in `.github/skills/{name}/SKILL.md`
- [ ] Proper frontmatter with name and description
- [ ] Entry added to `skill-rules.json`
- [ ] Keywords tested with real prompts
- [ ] Intent patterns tested with variations
- [ ] File path patterns tested with actual files
- [ ] Content patterns tested against file contents
- [ ] Block message is clear and actionable (if guardrail)
- [ ] Skip conditions configured appropriately
- [ ] Priority level matches importance
- [ ] No false positives in testing
- [ ] No false negatives in testing
- [ ] Performance is acceptable (<100ms or <200ms)
- [ ] JSON syntax validated: `jq . skill-rules.json`
- [ ] **SKILL.md under 500 lines** ⭐
- [ ] Reference files created if needed
- [ ] Table of contents added to files > 100 lines

---

## Advanced Patterns

See [advanced-patterns.md](reference/advanced-patterns.md) for comprehensive documentation on:

1. **Ultrathink keyword** — Force extended reasoning for complex analysis
2. **Dynamic context injection** — `` `!`command`` `` syntax for live codebase data
3. **Supporting files structure** — Directory conventions and extraction guidelines
4. **Skill-scoped hooks** — Lifecycle hooks scoped to individual skills (deferred — needs CLI testing)
5. **Model field** — Per-skill model selection (not recommended for current skills)
6. **Agent field optimization** — Choosing between `default`, `Explore`, and `Plan` agents
7. **Visual output pattern** — Bundled scripts generating interactive HTML visualizations

---

## YAML Frontmatter Reference

All 13 official fields for `SKILL.md` frontmatter:

### Core Fields

| Field         | Type   | Default    | Purpose                                                          |
| ------------- | ------ | ---------- | ---------------------------------------------------------------- |
| `name`        | string | dir name   | Skill identifier (lowercase, hyphens, max 64 chars)              |
| `description` | string | first para | Trigger matching — use phrasing users would say (max 1024 chars) |
| `version`     | string | -          | Semantic version (e.g., `1.0.0`)                                 |
| `license`     | string | -          | License identifier (e.g., `MIT`)                                 |

### Discoverability Fields

| Field            | Type    | Default | Purpose                                            |
| ---------------- | ------- | ------- | -------------------------------------------------- |
| `user-invocable` | boolean | `true`  | Show in `/` menu. `false` for background knowledge |
| `argument-hint`  | string  | -       | Autocomplete UI hint: `[issue-number]`, `[url]`    |

### Execution Control Fields

| Field                      | Type    | Default | Purpose                                                |
| -------------------------- | ------- | ------- | ------------------------------------------------------ |
| `disable-model-invocation` | boolean | `false` | Prevent auto-triggering. Manual-only workflows         |
| `context`                  | string  | -       | `fork` to run in isolated subagent                     |
| `agent`                    | string  | -       | Subagent type: `default`, `Explore`, `Plan`, custom    |
| `model`                    | string  | -       | Claude model override (e.g., `claude-opus-4-20250514`) |

### MCP Integration Fields

| Field                    | Type   | Default | Purpose                                        |
| ------------------------ | ------ | ------- | ---------------------------------------------- |
| `metadata.allowed-tools` | array  | -       | Whitelist MCP tools (nested under `metadata:`) |
| `metadata.mcp-server`    | string | -       | MCP server name (documentation only)           |

### Advanced Fields

| Field   | Type   | Default | Purpose                                                                        |
| ------- | ------ | ------- | ------------------------------------------------------------------------------ |
| `hooks` | object | -       | Skill-scoped lifecycle hooks (`UserPromptSubmit`, `PreToolUse`, `PostToolUse`) |

### Example

```yaml
---
name: "my-skill"
description: "Short description with trigger keywords users would say."
user-invocable: true
argument-hint: "[url] [options]"
context: fork
agent: default
metadata:
    allowed-tools:
        - tool_name_1
        - tool_name_2
    mcp-server: server-name
---
```

---

## Reference Files

For detailed information on specific topics, see:

### [TRIGGER_TYPES.md](resources/TRIGGER_TYPES.md)

Complete guide to all trigger types:

- Keyword triggers (explicit topic matching)
- Intent patterns (implicit action detection)
- File path triggers (glob patterns)
- Content patterns (regex in files)
- Best practices and examples for each
- Common pitfalls and testing strategies

### [SKILL_RULES_REFERENCE.md](resources/SKILL_RULES_REFERENCE.md)

Complete skill-rules.json schema:

- Full TypeScript interface definitions
- Field-by-field explanations
- Complete guardrail skill example
- Complete domain skill example
- Validation guide and common errors

### [HOOK_MECHANISMS.md](resources/HOOK_MECHANISMS.md)

Deep dive into hook internals:

- UserPromptSubmit flow (detailed)
- PreToolUse flow (detailed)
- Exit code behavior table (CRITICAL)
- Session state management
- Performance considerations

### [TROUBLESHOOTING.md](resources/TROUBLESHOOTING.md)

Comprehensive debugging guide:

- Skill not triggering (UserPromptSubmit)
- PreToolUse not blocking
- False positives (too many triggers)
- Hook not executing at all
- Performance issues

### [PATTERNS_LIBRARY.md](resources/PATTERNS_LIBRARY.md)

Ready-to-use pattern collection:

- Intent pattern library (regex)
- File path pattern library (glob)
- Content pattern library (regex)
- Organized by use case
- Copy-paste ready

### [ADVANCED.md](resources/ADVANCED.md)

Future enhancements and ideas:

- Dynamic rule updates
- Skill dependencies
- Conditional enforcement
- Skill analytics
- Skill versioning

---

## Quick Reference Summary

### Create New Skill (5 Steps)

1. Create `.github/skills/{name}/SKILL.md` with frontmatter
2. Add entry to `.github/skills/skill-rules.json`
3. Test with `npx tsx` commands
4. Refine patterns based on testing
5. Keep SKILL.md under 500 lines

### Trigger Types

- **Keywords**: Explicit topic mentions
- **Intent**: Implicit action detection
- **File Paths**: Location-based activation
- **Content**: Technology-specific detection

See [TRIGGER_TYPES.md](resources/TRIGGER_TYPES.md) for complete details.

### Enforcement

- **BLOCK**: Exit code 2, critical only
- **SUGGEST**: Inject context, most common
- **WARN**: Advisory, rarely used

### Skip Conditions

- **Session tracking**: Automatic (prevents repeated nags)
- **File markers**: `// @skip-validation` (permanent skip)
- **Env vars**: `SKIP_SKILL_GUARDRAILS` (emergency disable)

### Anthropic Best Practices

✅ **500-line rule**: Keep SKILL.md under 500 lines
✅ **Progressive disclosure**: Use reference files for details
✅ **Table of contents**: Add to reference files > 100 lines
✅ **One level deep**: Don't nest references deeply
✅ **Rich descriptions**: Include all trigger keywords (max 1024 chars)
✅ **Test first**: Build 3+ evaluations before extensive documentation
✅ **Gerund naming**: Prefer verb + -ing (e.g., "processing-pdfs")

### Troubleshoot

Test hooks manually:

```bash
# UserPromptSubmit
echo '{"prompt":"test"}' | npx tsx .claude/hooks/skill-activation-prompt.ts

# PreToolUse
cat <<'EOF' | npx tsx .claude/hooks/skill-verification-guard.ts
{"tool_name":"Edit","tool_input":{"file_path":"test.ts"}}
EOF
```

See [TROUBLESHOOTING.md](resources/TROUBLESHOOTING.md) for complete debugging guide.

---

## Related Files

**Configuration:**

- `.github/skills/skill-rules.json` - Master configuration
- `.claude/hooks/state/` - Session tracking
- `.claude/settings.json` - Hook registration

**Hooks:**

- `.claude/hooks/skill-activation-prompt.ts` - UserPromptSubmit
- `.claude/hooks/error-handling-reminder.ts` - Stop event (gentle reminders)

**All Skills:**

- `.github/skills/*/SKILL.md` - Skill content files

---

**Skill Status**: COMPLETE - Restructured following Anthropic best practices ✅
**Line Count**: < 500 (following 500-line rule) ✅
**Progressive Disclosure**: Reference files for detailed information ✅

**Next**: Create more skills, refine patterns based on usage
