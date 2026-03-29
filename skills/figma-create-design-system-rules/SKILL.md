---
name: figma-create-design-system-rules
version: 1.0.0
description: "Generates custom design system rules for the user's codebase. Use when user says \"create design system rules\", \"generate rules for my project\", \"set up design rules\", \"customize design system guidelines\", or wants to establish project-specific conventions for Figma-to-code workflows. Requires Figma MCP server connection."
argument-hint: "output path (optional, defaults to project rules location)"
user-invocable: true
disable-model-invocation: false
compatibility: "Requires Figma MCP server and FIGMA_API_KEY environment variable"
metadata:
    mcp-server: figma
---

This skill uses extended thinking for system-wide design pattern analysis. ultrathink

# Create Design System Rules

## Overview

This skill helps you generate custom design system rules tailored to your project's specific needs. These rules guide AI coding agents to produce consistent, high-quality code when implementing Figma designs, ensuring that your team's conventions, component patterns, and architectural decisions are followed automatically.

### Supported Rule Files

| Agent          | Rule File                                                  |
| -------------- | ---------------------------------------------------------- |
| Claude Code    | `CLAUDE.md`                                                |
| Codex CLI      | `AGENTS.md`                                                |
| Cursor         | `.cursor/rules/figma-design-system.mdc`                    |
| GitHub Copilot | `.github/instructions/figma-design-system.instructions.md` |

## What Are Design System Rules?

Design system rules are project-level instructions that encode the "unwritten knowledge" of your codebase - the kind of expertise that experienced developers know and would pass on to new team members:

- Which layout primitives and components to use
- Where component files should be located
- How components should be named and structured
- What should never be hardcoded
- How to handle design tokens and styling
- Project-specific architectural patterns

Once defined, these rules dramatically reduce repetitive prompting and ensure consistent output across all Figma implementation tasks.

## Prerequisites

- Figma MCP server must be connected and accessible
    - Before proceeding, verify the Figma MCP server is connected by checking if Figma MCP tools (e.g., `create_design_system_rules`) are available.
    - If the tools are not available, the Figma MCP server may not be enabled. Guide the user to enable the Figma MCP server that is included with the plugin. They may need to restart their MCP client afterward.
- Access to the project codebase for analysis
- Understanding of your team's component conventions (or willingness to establish them)

## When to Use This Skill

Use this skill when:

- Starting a new project that will use Figma designs
- Onboarding an AI coding agent to an existing project with established patterns
- Standardizing Figma-to-code workflows across your team
- Updating or refining existing design system conventions
- Users explicitly request: "create design system rules", "set up Figma guidelines", "customize rules for my project"

## Required Workflow

**Follow these steps in order. Do not skip steps.**

### Step 1: Run the Create Design System Rules Tool

Call the Figma MCP server's `create_design_system_rules` tool to get the foundational prompt and template.

**Parameters:**

- `clientLanguages`: Comma-separated list of languages used in the project (e.g., "typescript,javascript", "python", "javascript")
- `clientFrameworks`: Framework being used (e.g., "react", "vue", "svelte", "angular", "unknown")

This tool returns guidance and a template for creating design system rules.

Structure your design system rules following the template format provided in the tool's response.

### Step 2: Analyze the Codebase

Before finalizing rules, analyze the project to understand existing patterns:

**Component Organization:**

- Where are UI components located? (e.g., `src/components/`, `app/ui/`, `lib/components/`)
- Is there a dedicated design system directory?
- How are components organized? (by feature, by type, flat structure)

**Styling Approach:**

- DSAI uses Bootstrap 5 as the CSS framework with CSS custom properties (`--dsai-*` prefix)
- Design tokens defined in `src/collections/*.json` (DTCG format), generated to `src/generated/css/`
- Color tokens: `var(--dsai-color-primary)`, typography: `var(--dsai-font-size-base)`, spacing: Bootstrap utilities
- Token pipeline: `dsai tokens build` transforms DTCG JSON → CSS/SCSS/JS/TS outputs

**Component Patterns:**

- What naming conventions are used? (PascalCase, kebab-case, prefixes)
- How are component props typically structured?
- Are there common composition patterns?

**Architecture Decisions:**

- How is state management handled?
- What routing system is used?
- Are there specific import patterns or path aliases?

### Step 3: Generate Project-Specific Rules

Based on your codebase analysis, create a comprehensive set of rules. Include:

#### General Component Rules

```markdown
- IMPORTANT: Always use DSAI components from `@/components/ui/` when possible
- Install missing components via `dsai add <name>` before creating custom ones
- Place app-specific components in `src/client/components/`
- All components use `memo(forwardRef(function Name(props, ref)))` + `displayName`
- Props defined in separate `*.types.ts` files
```

#### Styling Rules

```markdown
- Use Bootstrap 5 utility classes for styling (d-flex, gap-3, m-3, p-2, text-center)
- Design tokens are CSS custom properties with --dsai-* prefix: `var(--dsai-color-primary)`
- IMPORTANT: Never hardcode colors — use DSAI tokens or Bootstrap semantic classes
- Spacing values use Bootstrap utilities (m-0 through m-5, p-0 through p-5)
- Typography follows DSAI token scale: `var(--dsai-font-size-base)`, `var(--dsai-font-weight-semibold)`
- Use `cn()` from `@/lib/utils` for class composition (simple filter+join, NOT tailwind-merge)
```

#### Figma MCP Integration Rules

```markdown
## Figma MCP Integration Rules

These rules define how to translate Figma inputs into code for this project and must be followed for every Figma-driven change.

### Required Flow (do not skip)

1. Run get_design_context first to fetch the structured representation for the exact node(s)
2. If the response is too large or truncated, run get_metadata to get the high-level node map, then re-fetch only the required node(s) with get_design_context
3. Run get_screenshot for a visual reference of the node variant being implemented
4. Only after you have both get_design_context and get_screenshot, download any assets needed and start implementation
5. Translate the output (usually React + Tailwind) into this project's DSAI conventions — Bootstrap 5, CSS custom properties, DSAI components
6. Validate against Figma for 1:1 look and behavior before marking complete

> **CRITICAL: NEVER output Tailwind CSS in generated rules or code.** Figma MCP output is React + Tailwind by default. All rules MUST enforce conversion to Bootstrap 5 + DSAI tokens.

#### Required Conversion Rule Template

When generating design system rules that reference Figma output, always include this conversion rule:

```markdown
## Figma-to-DSAI Conversion (Required)

All Figma MCP output must be converted before use:
- `flex` → `d-flex`, `flex-col` → `flex-column`
- `items-center` → `align-items-center`, `justify-between` → `justify-content-between`
- `gap-N` / `p-N` / `m-N` → Bootstrap spacing scale (`gap-3`, `p-3`, `m-2`)
- `rounded-*` → `rounded` or `var(--dsai-border-radius)`
- `shadow-*` → `var(--dsai-shadow-sm)` / `var(--dsai-shadow-default)` / `var(--dsai-shadow-lg)`
- `text-gray-*` → `text-body-secondary` or `var(--dsai-color-neutral-*)`
- `bg-white` → `bg-body` or `var(--dsai-bg-surface)`
- `sr-only` → `visually-hidden`
- `hover:*` → FSM state + conditional `cn()` class
- Color utilities → DSAI semantic tokens: `var(--dsai-color-primary)`, `var(--dsai-color-danger)`
```

### Implementation Rules

- Treat the Figma MCP output (React + Tailwind) as a reference for design intent, not as final code
- Replace Tailwind utility classes with Bootstrap 5 utilities and DSAI CSS custom properties
- Reuse DSAI components from `@/components/ui/` — install missing ones with `dsai add`
- Use DSAI token system: colors via `var(--dsai-color-*)`, spacing via Bootstrap utilities
- Respect existing routing, state management, and data-fetch patterns
- Strive for 1:1 visual parity with the Figma design
- Validate the final UI against the Figma screenshot for both look and behavior
```

#### Asset Handling Rules

```markdown
## Asset Handling

- The Figma MCP server provides an assets endpoint which can serve image and SVG assets
- IMPORTANT: If the Figma MCP server returns a localhost source for an image or SVG, use that source directly
- IMPORTANT: DO NOT import/add new icon packages - all assets should be in the Figma payload
- IMPORTANT: DO NOT use or create placeholders if a localhost source is provided
- Store downloaded assets in `[ASSET_DIRECTORY]`
```

#### Project-Specific Conventions

```markdown
## Project-Specific Conventions

- [Add any unique architectural patterns]
- [Add any special import requirements]
- [Add any testing requirements]
- [Add any accessibility standards]
- [Add any performance considerations]
```

### Step 4: Save Rules to the Appropriate Rule File

Detect which AI coding agent the user is working with and save the generated rules to the corresponding file:

| Agent          | Rule File                                                  | Notes                                                                                          |
| -------------- | ---------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| Claude Code    | `CLAUDE.md` in project root                                | Markdown format. Can also use `.claude/rules/figma-design-system.md` for modular organization. |
| Codex CLI      | `AGENTS.md` in project root                                | Markdown format. Append as a new section if file already exists. 32 KiB combined size limit.   |
| Cursor         | `.cursor/rules/figma-design-system.mdc`                    | Markdown with YAML frontmatter (`description`, `globs`, `alwaysApply`).                        |
| GitHub Copilot | `.github/instructions/figma-design-system.instructions.md` | Markdown with YAML frontmatter (`applyTo` glob, optional `description`).                       |

If unsure which agent the user is working with, check for existing rule files in the project or ask the user.

For Cursor, wrap the rules with YAML frontmatter:

```markdown
---
description: Rules for implementing Figma designs using the Figma MCP server. Covers component organization, styling conventions, design tokens, asset handling, and the required Figma-to-code workflow.
globs: "src/components/**"
alwaysApply: false
---

[Generated rules here]
```

Customize the `globs` pattern to match the directories where Figma-derived code will live in the project (e.g., `"src/**/*.tsx"` or `["src/components/**", "src/pages/**"]`).

For GitHub Copilot, wrap the rules with YAML frontmatter:

```markdown
---
applyTo: "src/client/components/**"
description: Rules for implementing Figma designs into this project. Covers component organization, styling conventions, design tokens, and the required Figma-to-code workflow.
---

[Generated rules here]
```

Customize the `applyTo` pattern to match the component directories in the project. For this project use `src/client/components/**`.

After saving, the rules will be automatically loaded by the agent and applied to all Figma implementation tasks.

### Step 5: Validate and Iterate

After creating rules:

1. Test with a simple Figma component implementation
2. Verify the agent follows the rules correctly
3. Refine any rules that aren't working as expected
4. Share with team members for feedback
5. Update rules as the project evolves

## Rule Categories and Examples

See [reference/rule-categories.md](reference/rule-categories.md) for essential, recommended, and optional rule templates with code examples.

## Examples

See [examples/framework-examples.md](examples/framework-examples.md) for complete walkthroughs (React+Bootstrap/DSAI, Vue+CSS, Design System Team).

## Best Practices and Troubleshooting

See [reference/best-practices-and-issues.md](reference/best-practices-and-issues.md) for best practices, common issues, and understanding design system rules.

## Arguments

When invoking this skill with arguments:

- `$0` or `$ARGUMENTS[0]` - Optional output path for the generated rules file
    - Defaults to `.claude/rules/design-system.md` if not specified
    - Example: `/create-design-system-rules docs/figma-rules.md`

If invoked without arguments, the skill will save rules to the default location and prompt for any configuration decisions during execution.

## Session Tracking

This skill uses `${CLAUDE_SESSION_ID}` to track design system rule generation sessions:

```typescript
// Each rule generation is logged with session context
const sessionId = process.env.CLAUDE_SESSION_ID;
console.log(`[${sessionId}] Generating design system rules from Figma file: ${fileKey}`);
```

This allows correlation between:

- The Figma file analyzed
- The rules file created/updated
- Git commits containing the new rules
- Subsequent design implementations that follow these rules

Use the session ID to understand which design system setup led to specific project conventions.

## Additional Resources

- [Figma MCP Server Documentation](https://developers.figma.com/docs/figma-mcp-server/)
- [Figma Variables and Design Tokens](https://help.figma.com/hc/en-us/articles/15339657135383-Guide-to-variables-in-Figma)
