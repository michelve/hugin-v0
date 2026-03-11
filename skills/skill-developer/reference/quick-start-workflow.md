# Quick Start: Creating a New Skill

## Step 1: Create Skill File

**Location:** `.github/skills/{skill-name}/SKILL.md`

**Template:**

```markdown
---
name: my-new-skill
description: Brief description including keywords that trigger this skill. Mention topics, file types, and use cases. Be explicit about trigger terms.
---

# My New Skill

## Purpose

What this skill helps with

## When to Use

Specific scenarios and conditions

## Key Information

The actual guidance, documentation, patterns, examples
```

**Best Practices:**

- ✅ **Name**: Lowercase, hyphens, gerund form (verb + -ing) preferred
- ✅ **Description**: Include ALL trigger keywords/phrases (max 1024 chars)
- ✅ **Content**: Under 500 lines - use reference files for details
- ✅ **Examples**: Real code examples
- ✅ **Structure**: Clear headings, lists, code blocks

## Step 2: Add to skill-rules.json

See [SKILL_RULES_REFERENCE.md](../resources/SKILL_RULES_REFERENCE.md) for complete schema.

**Basic Template:**

```json
{
    "my-new-skill": {
        "type": "domain",
        "enforcement": "suggest",
        "priority": "medium",
        "promptTriggers": {
            "keywords": ["keyword1", "keyword2"],
            "intentPatterns": ["(create|add).*?something"]
        }
    }
}
```

## Step 3: Test Triggers

**Test UserPromptSubmit:**

```bash
echo '{"session_id":"test","prompt":"your test prompt"}' | \
  npx tsx .claude/hooks/skill-activation-prompt.ts
```

**Test PreToolUse:**

```bash
cat <<'EOF' | npx tsx .claude/hooks/skill-verification-guard.ts
{"session_id":"test","tool_name":"Edit","tool_input":{"file_path":"test.ts"}}
EOF
```

## Step 4: Refine Patterns

Based on testing:

- Add missing keywords
- Refine intent patterns to reduce false positives
- Adjust file path patterns
- Test content patterns against actual files

## Step 5: Follow Anthropic Best Practices

✅ Keep SKILL.md under 500 lines
✅ Use progressive disclosure with reference files
✅ Add table of contents to reference files > 100 lines
✅ Write detailed description with trigger keywords
✅ Test with 3+ real scenarios before documenting
✅ Iterate based on actual usage
