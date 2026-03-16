---
name: sync-schemas
description: "Re-analyze the official anthropics/claude-plugins-official marketplace and update local JSON Schemas. Use when user says 'sync schemas', 'update schemas', or 'refresh schemas'."
user-invocable: true
---

# Sync Schemas

Re-analyze the official `anthropics/claude-plugins-official` marketplace.json to keep our local schemas accurate.

## Why This Exists

The canonical `$schema` URL (`https://anthropic.com/claude-code/marketplace.schema.json`) returns **404** — confirmed since October 2025 ([GitHub Issue #9686](https://github.com/anthropics/claude-code/issues/9686)). We maintain inferred schemas locally at:

- `schemas/marketplace.schema.json` — validates marketplace.json catalog files
- `schemas/plugin.schema.json` — validates .claude-plugin/plugin.json manifests

## Steps

### 1. Fetch the Official Marketplace

Fetch the raw official marketplace.json:

```
https://raw.githubusercontent.com/anthropics/claude-plugins-official/main/.claude-plugin/marketplace.json
```

### 2. Extract All Plugin Entry Fields

Scan every plugin entry in the `plugins` array and collect:

- **All top-level keys** used across entries (name, description, source, category, version, author, homepage, strict, lspServers, tags, etc.)
- **Source format variants**: relative path string, `{ source: "url" }`, `{ source: "git-subdir" }`
- **Category values**: collect every unique `category` string
- **lspServer shape**: command, args, extensionToLanguage, startupTimeout
- **Tag values**: collect every unique tag string
- **Author shape**: name (required), email (optional)

### 3. Fetch Sample plugin.json Files

Fetch 3–5 official plugin.json files from different plugin types:

- One LSP plugin (e.g. `plugins/typescript-lsp`)
- One workflow plugin (e.g. `plugins/commit-commands`)
- One hook plugin (e.g. `plugins/security-guidance`)

Collect all top-level keys used across plugin.json manifests.

### 4. Diff Against Local Schemas

Compare findings against the current local schemas:

- `schemas/marketplace.schema.json`
- `schemas/plugin.schema.json`

Report any differences:
- New fields found in official that are missing from local schemas
- Category values that need to be added to the enum
- Source format changes
- Fields in local schemas that no longer appear in official

### 5. Update Local Schemas

Apply any necessary changes to keep schemas in sync. For each update:

1. Add new fields/values discovered
2. Remove fields/values no longer used
3. Update descriptions if semantics changed
4. Preserve the `$id`, `title`, and `description` metadata

### 6. Validate Our Own Files

After updating schemas, validate:

- `schemas/marketplace.schema.json` — valid JSON Schema
- `schemas/plugin.schema.json` — valid JSON Schema
- `.claude-plugin/plugin.json` — conforms to plugin.schema.json

Report results as a summary table:

| File | Status | Notes |
|------|--------|-------|
| marketplace.schema.json | ✅ Updated | Added 2 new categories |
| plugin.schema.json | ✅ No changes | — |
| plugin.json | ✅ Valid | — |

### 7. Report

Print a changelog of what was updated (or confirm schemas are already current).
