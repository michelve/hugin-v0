---
description: Verify environment variables, MCP servers, and LSP are configured correctly
---

Run each of the following checks and report a summary table at the end.

## 1. Environment Variables

Check whether each variable is set (non-empty) in the current shell environment:

| Variable        | Required | Used by                          |
| --------------- | -------- | -------------------------------- |
| `FIGMA_API_KEY` | Yes      | figma, figma-console MCP servers |

For each variable, report ✅ Set or ❌ Missing.

If any required variable is missing, show the setup command for the user's OS:
- **macOS/Linux**: `export FIGMA_API_KEY=fig_xxxxxxxxxxxxxxxxxxxxx` (add to `~/.zshrc` or `~/.bashrc`)
- **Windows PowerShell**: `$env:FIGMA_API_KEY = "fig_xxxxxxxxxxxxxxxxxxxxx"` (add to `$PROFILE`)

## 2. TypeScript LSP

Check if `typescript-language-server` is available on `$PATH` by running:

```bash
which typescript-language-server || where typescript-language-server
```

Report ✅ Installed or ❌ Missing. If missing, show:

```bash
npm install -g typescript-language-server typescript
```

## 3. MCP Servers

List the MCP servers defined in this plugin's `.mcp.json` and check whether their commands (`npx` packages) can resolve. For URL-based servers (miro-mcp), just confirm the URL is configured.

Report each server as ✅ Configured or ⚠️ Needs attention.

## 4. Summary

Print a single summary table:

```
┌─────────────────────┬────────┐
│ Check               │ Status │
├─────────────────────┼────────┤
│ FIGMA_API_KEY       │ ✅/❌  │
│ TypeScript LSP      │ ✅/❌  │
│ context7 MCP        │ ✅/⚠️  │
│ playwright MCP      │ ✅/⚠️  │
│ figma MCP           │ ✅/⚠️  │
│ figma-console MCP   │ ✅/⚠️  │
│ sequential-thinking │ ✅/⚠️  │
│ miro-mcp            │ ✅/⚠️  │
│ shadcn MCP          │ ✅/⚠️  │
└─────────────────────┴────────┘
```

If everything passes, confirm the plugin is fully configured and ready to use.
If anything is missing, provide actionable next steps.
