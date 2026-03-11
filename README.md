# hugin-v0

A Claude Code plugin with **23 skills**, **8 agents**, **5 event hooks**, and **7 MCP servers** for full-stack development with React 19, TypeScript, Express, Prisma, Tailwind CSS v4, and shadcn/ui.

Built and tested in [draft_v0](https://github.com/michelve/draft_v0) — a full-stack React 19 + Express + Prisma starter with opinionated architecture, ADR workflows, task management, Figma integration, and automated code quality gates.

## Requirements

- [Claude Code](https://code.claude.com) v1.0.33+

## Installation

### From a marketplace (recommended)

```bash
/plugin marketplace add michelve/hugin-v0
/plugin install hugin-v0@michelve
```

### Local testing

```bash
claude --plugin-dir ./path/to/hugin-v0
```

Or from within Claude Code:

```bash
/plugin marketplace add ./path/to/hugin-v0
/plugin install hugin-v0
```

## What's included

### Skills (23)

| Skill                          | Description                                                              |           Invocable           |
| ------------------------------ | ------------------------------------------------------------------------ | :---------------------------: |
| **accessibility**              | WCAG 2.1 AA — keyboard nav, ARIA, focus management, color contrast       |       `/accessibility`        |
| **adr-writer**                 | Write Architecture Decision Records in MADR 4.0.0 format                 |         `/adr-writer`         |
| **automatic-code-review**      | Semantic code review on modified files (hook-driven)                     |             auto              |
| **code-connect-components**    | Connect Figma components to code via Code Connect                        |  `/code-connect-components`   |
| **component-visualizer**       | Generate interactive HTML dependency graphs for React components         |    `/component-visualizer`    |
| **create-design-system-rules** | Generate project-specific design system Figma-to-code rules              | `/create-design-system-rules` |
| **create-tasks**               | Break PRDs into well-formed, INVEST-compliant tasks                      |        `/create-tasks`        |
| **figma**                      | Fetch design context, screenshots, variables from Figma MCP              |           `/figma`            |
| **figma-implement-design**     | Translate Figma nodes into production-ready code                         |   `/figma-implement-design`   |
| **miro-mcp**                   | Create diagrams, tables, docs on Miro boards via MCP                     |          `/miro-mcp`          |
| **nodejs**                     | Node.js backend patterns — async/await, middleware, layered architecture |           `/nodejs`           |
| **playwright-skill**           | Browser automation, e2e testing, UI validation                           |      `/playwright-skill`      |
| **prisma**                     | Prisma Client queries, schema, migrations, transactions                  |           `/prisma`           |
| **react**                      | React 19 hooks, Suspense, lazy loading, TypeScript patterns              |           `/react`            |
| **react-best-practices**       | Vercel Engineering performance optimization guidelines                   |    `/react-best-practices`    |
| **route-tester**               | HTTP API route testing, auth strategies, integration tests               |        `/route-tester`        |
| **shadcn**                     | shadcn/ui component management — add, search, fix, compose               |           `/shadcn`           |
| **skill-creator**              | Create new Claude Code skills and instruction files                      |       `/skill-creator`        |
| **skill-developer**            | Develop and iterate on existing skills                                   |      `/skill-developer`       |
| **tailwindcss**                | Tailwind CSS v4 utility-first styling, responsive, dark mode             |        `/tailwindcss`         |
| **task-check**                 | Verify task completion against acceptance criteria                       |         `/task-check`         |
| **web-design-guidelines**      | UI accessibility and design review                                       |   `/web-design-guidelines`    |
| **writing-tests**              | Test naming, assertions, edge case coverage (BugMagnet-based)            |       `/writing-tests`        |

### Agents (8)

| Agent                          | Purpose                                                                  |
| ------------------------------ | ------------------------------------------------------------------------ |
| **auto-error-resolver**        | Fix TypeScript compilation and build errors systematically               |
| **code-architecture-reviewer** | Review code for best practices and architectural consistency             |
| **code-refactor-master**       | Refactor code for better organization and maintainability                |
| **documentation-architect**    | Create, update, and enhance documentation                                |
| **plan-reviewer**              | Review development plans before implementation                           |
| **principal-engineer**         | First-principles engineering analysis (Carmack-style thinking)           |
| **refactor-planner**           | Analyze code structure and create refactoring plans with risk assessment |
| **web-research-specialist**    | Research debugging solutions, best practices, documentation              |

### Hooks (5 event hooks)

| Hook                      | Event            | Trigger                  | Purpose                                     |
| ------------------------- | ---------------- | ------------------------ | ------------------------------------------- |
| **commitlint-enforcer**   | PreToolUse       | Before bash commands     | Enforce conventional commit messages        |
| **anti-pattern-guard**    | PreToolUse       | Before file writes       | Warn on React 19 anti-patterns              |
| **adr-gate**              | UserPromptSubmit | Before prompt processing | Check for ADR-qualifying decisions          |
| **task-context-injector** | UserPromptSubmit | Before prompt processing | Inject task context from `.tasks/`          |
| **quality-gate-reminder** | PostToolUse      | After file edits         | Remind to run `typecheck` and `biome:check` |

### MCP Servers (7)

| Server                  | Package                              | Notes                              |
| ----------------------- | ------------------------------------ | ---------------------------------- |
| **context7**            | `@upstash/context7-mcp`              | Up-to-date library documentation   |
| **playwright**          | `@playwright/mcp`                    | Browser automation                 |
| **figma**               | `figma-developer-mcp`                | Requires `$FIGMA_API_KEY`          |
| **figma-console**       | `figma-console-mcp`                  | Requires `$FIGMA_API_KEY`          |
| **sequential-thinking** | `@anthropic/sequential-thinking-mcp` | Complex reasoning chains           |
| **miro-mcp**            | URL-based (`mcp.miro.com`)           | Board creation and data extraction |
| **shadcn**              | `shadcn@latest mcp`                  | Component registry access          |

### LSP Servers (1)

| Server         | Binary                         | Install                                               | Languages                                |
| -------------- | ------------------------------ | ----------------------------------------------------- | ---------------------------------------- |
| **typescript** | `typescript-language-server`   | `npm install -g typescript-language-server typescript` | `.ts`, `.tsx`, `.js`, `.jsx`             |

The TypeScript LSP gives Claude real-time diagnostics, go-to-definition, find-references, and type information while editing. You must install the language server binary separately — the plugin configures the connection, not the server itself.

## Environment Variables

Some MCP servers require API keys. Set them in your environment:

```bash
export FIGMA_API_KEY=your-figma-api-key
```

## Plugin Structure

```
hugin-v0/
├── .claude-plugin/
│   └── plugin.json           # Plugin manifest
├── skills/                   # 23 skills (SKILL.md + supporting files)
├── agents/                   # 8 specialized agents
├── agent-rules/              # Agent routing metadata (JSON)
├── hooks/
│   └── hooks.json            # Hook event configuration
├── scripts/                  # Hook scripts (Python + cross-platform runners)
│   ├── run-hook.cjs          # Cross-platform Python runner (Windows/Unix)
│   ├── commitlint-enforcer.py
│   ├── anti-pattern-guard.py
│   ├── adr-gate.py
│   ├── task-context-injector.py
│   └── quality-gate-reminder.py
├── .mcp.json                 # MCP server configurations
├── .lsp.json                 # LSP server configurations
├── settings.json             # Default plugin settings
├── LICENSE
├── CHANGELOG.md
└── README.md
```

## Development

### Test locally

```bash
claude --plugin-dir ./hugin-v0
```

### Validate

```bash
claude plugin validate ./hugin-v0
```

### Hot reload (inside Claude Code)

```bash
/reload-plugins
```

## License

MIT — see [LICENSE](LICENSE)

## Origin

This plugin was extracted from [draft_v0](https://github.com/michelve/draft_v0), where all skills, agents, and hooks were developed and refined in a production full-stack codebase. Contributions and issues should be filed in this repo.

## Author

[michelve](https://github.com/michelve)
