---
name: setup
version: 1.0.0
description: "Verify environment variables, MCP servers, and LSP are configured correctly. Use when user says 'setup', 'check my setup', 'verify config', 'is everything configured', or wants to confirm their development environment is ready."
user-invocable: true
argument-hint: "Optional: FIGMA_API_KEY=fig_xxx to auto-configure Figma integration"
---

# Setup Verification

Run each of the following checks and report a summary table at the end.

## 0. Handle Arguments

If the user provided arguments (e.g. `/setup FIGMA_API_KEY=fig_xxx`), parse them first:

- **`FIGMA_API_KEY=<value>`**: Persist the key for the current and future sessions:
  1. Run `export FIGMA_API_KEY=<value>` in the current shell
  2. Check if `FIGMA_API_KEY` is already in `~/.zshrc` (or `~/.bashrc`):
     - If not present, append: `export FIGMA_API_KEY=<value>`
     - If present with a different value, ask before overwriting
  3. Mark the Figma environment check as ✅ for the rest of this run

If no arguments are provided, proceed normally and prompt for missing required values at the end.

## 1. Environment Variables

Check whether each variable is set (non-empty) in the current shell environment:

| Variable        | Required | Used by                          |
| --------------- | -------- | -------------------------------- |
| `FIGMA_API_KEY` | Yes      | figma, figma-console MCP servers |

For each variable, report ✅ Set or ❌ Missing.

If any required variable is missing, show the setup command for the user's OS:
- `export FIGMA_API_KEY=fig_xxxxxxxxxxxxxxxxxxxxx` (add to `~/.zshrc` or `~/.bashrc`)

## 2. TypeScript LSP

Check if `typescript-language-server` is available on `$PATH` by running:

```bash
which typescript-language-server
```

Report ✅ Installed or ❌ Missing. If missing, show:

```bash
npm install -g typescript-language-server typescript
```

## 3. Figma Console Log MCP

Check if the `figma-console-mcp` package is installed globally:

```bash
npm list -g figma-console-mcp 2>/dev/null
```

If not installed, install it:

```bash
npm install -g figma-console-mcp
```

Report ✅ Installed or ⚠️ Missing (and auto-install if missing).

## 4. MCP Servers

Read `.mcp.json` at the project root and verify each server:

| Server                  | Type        | Check                                                       |
| ----------------------- | ----------- | ----------------------------------------------------------- |
| **context7**            | npx         | `npx -y @upstash/context7-mcp --help` resolves              |
| **playwright**          | npx         | `npx -y @playwright/mcp --help` resolves                    |
| **figma**               | npx + env   | Package resolves AND `$FIGMA_API_KEY` is set                 |
| **figma-console**       | npx + env   | Package resolves AND `$FIGMA_API_KEY` is set                 |
| **sequential-thinking** | npx         | `npx -y @anthropic/sequential-thinking-mcp --help` resolves |
| **miro-mcp**            | URL (SSE)   | URL `https://mcp.miro.com/sse` is configured                |
| **shadcn**              | npx         | `npx -y shadcn@latest mcp --help` resolves                  |

For servers marked as needing env vars, cross-reference with section 1 results.

If any server is missing from `.mcp.json`, offer to add it.

Report each server as ✅ Configured or ⚠️ Needs attention.

## 5. Summary

Print a single summary table:

```
┌───────────────────────────┬────────┐
│ Check                     │ Status │
├───────────────────────────┼────────┤
│ FIGMA_API_KEY             │ ✅/❌  │
│ TypeScript LSP            │ ✅/❌  │
│ figma-console-mcp (npm)   │ ✅/⚠️  │
│ context7 MCP              │ ✅/⚠️  │
│ playwright MCP            │ ✅/⚠️  │
│ figma MCP                 │ ✅/⚠️  │
│ figma-console MCP         │ ✅/⚠️  │
│ sequential-thinking MCP   │ ✅/⚠️  │
│ miro-mcp MCP              │ ✅/⚠️  │
│ shadcn MCP                │ ✅/⚠️  │
└───────────────────────────┴────────┘
```

## 6. Auto-Fix Offer

If any checks failed, offer to fix them automatically:

- **Missing `FIGMA_API_KEY`**: Ask the user for their key, then set it (export + append to shell profile)
- **Missing TypeScript LSP**: Run `npm install -g typescript-language-server typescript`
- **Missing `figma-console-mcp`**: Run `npm install -g figma-console-mcp`
- **MCP server not resolving**: Suggest running `/setup` again after fixing network/npm issues

Only proceed with auto-fixes if the user confirms.
