# Changelog

All notable changes to hugin-v0 will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2026-03-11

### Added

- 4 custom output styles: `architecture-review`, `code-review`, `refactoring`, `documentation`
- Plugin marketplace file (`.claude-plugin/marketplace.json`)
- 5 new agents: `analyzer`, `comparator`, `grader`, `automatic-code-reviewer`, `task-check`
- 3 new hooks: `inject-adr-context` (UserPromptSubmit), `automatic-code-review` log (PostToolUse), `automatic-code-review` review (Stop)
- `commands/` directory with `check.md` command
- `outputStyles` field in plugin manifest
- Enhanced agent frontmatter: model, tools, skills, memory, maxTurns, disallowedTools, background

### Changed

- Default plugin agent set to `principal-engineer` in `settings.json`
- Migrated nested agents from skills to root `agents/` directory
- Migrated nested hooks from skills to root `hooks/hooks.json`
- Restructured `skills/shadcn/`: `resources/` → `references/`, `rules/` → `references/rules/`
- Restructured `skills/accessibility/`: merged duplicate `reference/` and `references/` directories
- Updated all SKILL.md links to match new directory paths

### Removed

- 7 `skill-rules-fragment.json` files (non-Claude format, from external tooling)
- OpenAI agent configuration files

## [1.1.0] - 2026-03-11

### Added

- TypeScript LSP server configuration (`.lsp.json`) — real-time diagnostics, go-to-definition, and type information for `.ts`, `.tsx`, `.js`, `.jsx` files
- `lsp` keyword in plugin manifest

## [1.0.0] - 2026-03-11

### Added

- 23 skills for full-stack development (React 19, TypeScript, Express, Prisma, Tailwind CSS v4, shadcn/ui, Figma, Playwright, and more)
- 8 specialized agents (auto-error-resolver, code-architecture-reviewer, code-refactor-master, documentation-architect, plan-reviewer, principal-engineer, refactor-planner, web-research-specialist)
- 5 event hooks (commitlint-enforcer, anti-pattern-guard, adr-gate, task-context-injector, quality-gate-reminder)
- 7 MCP server configurations (context7, playwright, figma, figma-console, sequential-thinking, miro-mcp, shadcn)
- Cross-platform hook runner (Windows + Unix) via run-hook.cjs
- Agent routing metadata (agent-rules JSON)
