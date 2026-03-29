# hugin-v0

A Claude Code plugin that helps **product designers and engineers ship design-to-production React 19 apps** — translating Figma mockups into accessible, production-ready components with automated code reviews, architecture guardrails, and quality gates baked into every workflow.

Packed with **27 skills**, **13 agents**, **8 event hooks**, **7 MCP servers**, **4 output styles**, and **1 LSP server** covering the full stack: React 19, TypeScript, Express, Prisma, DSAI Design System, and Bootstrap 5.

Built for and tested with [draft_v0](https://github.com/michelve/draft_v0) — a full-stack React 19 + Express + Prisma starter with opinionated architecture, ADR workflows, task management, Figma integration, and automated code quality gates.

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

### Skills (28)

| Skill                          | Description                                                              |           Invocable           |
| ------------------------------ | ------------------------------------------------------------------------ | :---------------------------: |
| **accessibility**              | WCAG 2.1 AA — keyboard nav, ARIA, focus management, color contrast       |       `/accessibility`        |
| **adr-writer**                 | Write Architecture Decision Records in MADR 4.0.0 format                 |         `/adr-writer`         |
| **automatic-code-review**      | Semantic code review on modified files (hook-driven)                     |             auto              |
| **figma-code-connect-components** | Connect Figma components to code via Code Connect                     | `/figma-code-connect-components` |
| **component-visualizer**       | Generate interactive HTML dependency graphs for React components         |    `/component-visualizer`    |
| **figma-create-design-system-rules** | Generate project-specific design system Figma-to-code rules         | `/figma-create-design-system-rules` |
| **figma-create-new-file**      | Create a new blank Figma design or FigJam file                           |   `/figma-create-new-file`    |
| **create-tasks**               | Break PRDs into well-formed, INVEST-compliant tasks                      |        `/create-tasks`        |
| **figma-generate-design**      | Build or update full-page screens in Figma from design system            |  `/figma-generate-design`     |
| **figma-generate-library**     | Build professional design systems in Figma from codebase                 |  `/figma-generate-library`    |
| **figma-implement-design**     | Translate Figma nodes into production-ready code                         |   `/figma-implement-design`   |
| **figma-use**                  | Mandatory prerequisite for every `use_figma` Plugin API call             |         `/figma-use`          |
| **miro-mcp**                   | Create diagrams, tables, docs on Miro boards via MCP                     |          `/miro-mcp`          |
| **nodejs**                     | Node.js backend patterns — async/await, middleware, layered architecture |           `/nodejs`           |
| **playwright-skill**           | Browser automation, e2e testing, UI validation                           |      `/playwright-skill`      |
| **prisma**                     | Prisma Client queries, schema, migrations, transactions                  |           `/prisma`           |
| **react**                      | React 19 hooks, Suspense, lazy loading, TypeScript patterns              |           `/react`            |
| **react-best-practices**       | Vercel Engineering performance optimization guidelines                   |    `/react-best-practices`    |
| **route-tester**               | HTTP API route testing, auth strategies, integration tests               |        `/route-tester`        |
| **dsai-components**            | DSAI component catalog, types, patterns, compound components, FSM        |     `/dsai-components`      |
| **skill-creator**              | Create new Claude Code skills and instruction files                      |       `/skill-creator`        |
| **skill-developer**            | Develop and iterate on existing skills                                   |      `/skill-developer`       |
| **dsai-styling**               | Bootstrap 5 + DSAI CSS custom properties, cn(), token pipeline           |       `/dsai-styling`        |
| **dsai-tools**                 | DSAI CLI tools — dsai add, tokens build, icons, framework mappers        |        `/dsai-tools`         |
| **dsai-figma**                 | DSAI Figma integration — token sync, FigmaClient, Code Connect           |        `/dsai-figma`         |
| **task-check**                 | Verify task completion against acceptance criteria                       |         `/task-check`         |
| **web-design-guidelines**      | UI accessibility and design review                                       |   `/web-design-guidelines`    |
| **writing-tests**              | Test naming, assertions, edge case coverage (BugMagnet-based)            |       `/writing-tests`        |

### Agents (13)

| Agent                          | Model   | Purpose                                                                  |
| ------------------------------ | ------- | ------------------------------------------------------------------------ |
| **principal-engineer**         | opus    | First-principles engineering analysis (default main agent)               |
| **code-architecture-reviewer** | opus    | Review code for best practices and architectural consistency             |
| **plan-reviewer**              | opus    | Review development plans before implementation                           |
| **auto-error-resolver**        | sonnet  | Fix TypeScript compilation and build errors systematically               |
| **code-refactor-master**       | sonnet  | Refactor code for better organization and maintainability                |
| **documentation-architect**    | sonnet  | Create, update, and enhance documentation                                |
| **refactor-planner**           | sonnet  | Analyze code structure and create refactoring plans with risk assessment |
| **analyzer**                   | sonnet  | Post-hoc analysis of blind comparison results                            |
| **comparator**                 | sonnet  | Blind comparison of two outputs for skill evaluation                     |
| **grader**                     | sonnet  | Evaluate expectations against execution transcripts                      |
| **automatic-code-reviewer**    | haiku   | Semantic code review using project-specific rules                        |
| **task-check**                 | haiku   | Verify task completion against acceptance criteria                        |
| **web-research-specialist**    | haiku   | Research debugging solutions, best practices, documentation              |

### Hooks (8 event hooks across 4 event types)

| Hook                           | Event            | Trigger                  | Purpose                                     |
| ------------------------------ | ---------------- | ------------------------ | ------------------------------------------- |
| **commitlint-enforcer**        | PreToolUse       | Before bash commands     | Enforce conventional commit messages        |
| **anti-pattern-guard**         | PreToolUse       | Before file writes       | Warn on React 19 anti-patterns              |
| **adr-gate**                   | UserPromptSubmit | Before prompt processing | Check for ADR-qualifying decisions          |
| **task-context-injector**      | UserPromptSubmit | Before prompt processing | Inject task context from `.tasks/`          |
| **inject-adr-context**         | UserPromptSubmit | Before prompt processing | Inject ADR context into prompts             |
| **quality-gate-reminder**      | PostToolUse      | After file edits         | Remind to run `typecheck` and `biome:check` |
| **automatic-code-review** (log)| PostToolUse      | After file edits         | Log modified files for review               |
| **automatic-code-review** (run)| Stop             | Before session ends      | Run semantic code review on all changes     |

### MCP Servers (7)

| Server                  | Package                              | Notes                              |
| ----------------------- | ------------------------------------ | ---------------------------------- |
| **context7**            | `@upstash/context7-mcp`              | Up-to-date library documentation   |
| **playwright**          | `@playwright/mcp`                    | Browser automation                 |
| **figma**               | `figma-developer-mcp`                | Requires `$FIGMA_API_KEY`          |
| **figma-console**       | `figma-console-mcp`                  | Requires `$FIGMA_API_KEY`          |
| **sequential-thinking** | `@anthropic/sequential-thinking-mcp` | Complex reasoning chains           |
| **miro-mcp**            | URL-based (`mcp.miro.com`)           | Board creation and data extraction |
| **dsai**                | `dsai@latest mcp`                    | DSAI component registry access     |

### Output Styles (4)

| Style                    | Description                                                                    |
| ------------------------ | ------------------------------------------------------------------------------ |
| **architecture-review**  | Structured architectural analysis with dependency mapping and component diagrams |
| **code-review**          | Inline findings with severity levels and diff-block fix suggestions             |
| **refactoring**          | Before/after comparisons with risk-tagged migration steps                       |
| **documentation**        | Technical documentation with API tables and progressive code examples           |

Switch styles with `/output-style architecture-review`, `/output-style code-review`, etc.

### LSP Servers (1)

| Server         | Binary                       | Install                                                | Languages                    |
| -------------- | ---------------------------- | ------------------------------------------------------ | ---------------------------- |
| **typescript** | `typescript-language-server` | `npm install -g typescript-language-server typescript` | `.ts`, `.tsx`, `.js`, `.jsx` |

The TypeScript LSP gives Claude real-time diagnostics, go-to-definition, find-references, and type information while editing. You must install the language server binary separately — the plugin configures the connection, not the server itself.

## Environment Variables

Some MCP servers and skills require API keys to function. Set them in your shell **before** launching Claude Code — the plugin reads from your environment at startup.

### Required keys

| Variable         | Used by                          | Get it from                                                        |
| ---------------- | -------------------------------- | ------------------------------------------------------------------ |
| `FIGMA_API_KEY`  | figma, figma-console MCP servers | [Figma → Settings → Personal access tokens](https://www.figma.com/developers/api#access-tokens) |

### Optional keys

| Variable         | Used by           | Notes                                                              |
| ---------------- | ----------------- | ------------------------------------------------------------------ |
| `MIRO_API_KEY`   | miro-mcp server   | Only needed if your Miro board requires auth beyond the web URL    |

### Setup by OS

**macOS / Linux** — add to your `~/.zshrc`, `~/.bashrc`, or `~/.profile`:

```bash
export FIGMA_API_KEY=fig_xxxxxxxxxxxxxxxxxxxxx
```

Then reload: `source ~/.zshrc`

**Windows (PowerShell)** — add to your `$PROFILE`:

```powershell
$env:FIGMA_API_KEY = "fig_xxxxxxxxxxxxxxxxxxxxx"
```

Then reload: `. $PROFILE`

**Windows (system-wide)** — or set it permanently:

```powershell
[Environment]::SetEnvironmentVariable("FIGMA_API_KEY", "fig_xxxxxxxxxxxxxxxxxxxxx", "User")
```

Restart your terminal after setting system-wide variables.

### Verify your setup

After setting your keys, run the `/setup` command inside Claude Code to verify everything is configured:

```text
/setup
```

This checks that required environment variables are set, MCP servers can initialize, and the TypeScript LSP binary is installed.

## Plugin Structure

```
hugin-v0/
├── .claude-plugin/
│   └── plugin.json           # Plugin manifest
├── skills/                   # 23 skills (SKILL.md + supporting files)
├── agents/                   # 13 specialized agents
├── agent-rules/              # Agent routing metadata (JSON)
├── commands/                 # Slash commands (check.md)
├── hooks/
│   └── hooks.json            # Hook event configuration (8 hooks)
├── scripts/                  # Hook scripts (Python + shell + cross-platform runners)
├── output-styles/            # 4 custom output styles
├── .mcp.json                 # MCP server configurations (7 servers)
├── .lsp.json                 # LSP server configurations
├── settings.json             # Default plugin settings (agent: principal-engineer)
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

### Local validation

The plugin ships a standalone validator that checks frontmatter, hooks, evals, and project structure — the same checks that run in CI.

```bash
# Full project scan
./scripts/validate-plugin.sh

# Validate a specific skill or agent
./scripts/validate-plugin.sh skills/react/SKILL.md

# Validate only git-staged files
./scripts/validate-plugin.sh --staged

# Auto-fix: generate missing evals/, trigger-evals.json, skills-rules.json
./scripts/validate-plugin.sh --fix

# Fix a specific skill
./scripts/validate-plugin.sh --fix skills/react/SKILL.md
```

Errors block with exit code 1. Warnings are shown but do not block.

### Pre-commit hook

Install the pre-commit hook to automatically validate plugin files before every commit:

```bash
ln -sf ../../scripts/pre-commit-validate.sh .git/hooks/pre-commit
```

The hook detects which staged files are plugin-relevant and runs targeted or full validation accordingly. Bypass once with `git commit --no-verify`.

### Hot reload (inside Claude Code)

```bash
/reload-plugins
```

## License

MIT — see [LICENSE](LICENSE)
