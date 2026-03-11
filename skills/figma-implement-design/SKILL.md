---
name: "figma-implement-design"
description: "Translate Figma nodes into production-ready code with 1:1 visual fidelity using the Figma MCP workflow (design context, screenshots, assets, and project-convention translation). Trigger when the user provides Figma URLs or node IDs, or asks to implement designs or components that must match Figma specs. Requires a working Figma MCP server connection."
argument-hint: "Figma URL (https://figma.com/design/:fileKey/:fileName?node-id=1-2)"
user-invocable: true
context: fork
allowed-tools: figma__get_design_context, figma__get_screenshot, figma__get_assets, figma__get_variables
---

This skill uses extended thinking for complex design-to-code translation. ultrathink

## Current Repository State

```
!`git status --short 2>/dev/null || echo 'Not a git repository'`
```

```
!`git log --oneline -5 2>/dev/null || echo 'No git history available'`
```

# Implement Design

## Overview

This skill provides a structured workflow for translating Figma designs into production-ready code with pixel-perfect accuracy. It ensures consistent integration with the Figma MCP server, proper use of design tokens, and 1:1 visual parity with designs.

## Prerequisites

- Figma MCP server must be connected and accessible
    - Before proceeding, verify the Figma MCP server is connected by checking if Figma MCP tools (e.g., `get_design_context`) are available.
    - If the tools are not available, the Figma MCP server may not be enabled. Guide the user to enable the Figma MCP server that is included with the plugin. They may need to restart their MCP client afterward.
- User must provide a Figma URL in the format: `https://figma.com/design/:fileKey/:fileName?node-id=1-2`
    - `:fileKey` is the file key
    - `1-2` is the node ID (the specific component or frame to implement)
- **OR** when using `figma-desktop` MCP: User can select a node directly in the Figma desktop app (no URL required)
- Project should have an established design system or component library (preferred)

## Required Workflow

**Follow these steps in order. Do not skip steps.**

### Step 0: Set up Figma MCP (if not already configured)

**VS Code + GitHub Copilot users:** Figma MCP is pre-configured in `.vscode/mcp.json` - skip to Step 1. If tools are still unavailable, reload the VS Code window and check the MCP panel.

**Claude Code / Codex CLI users:** If any MCP call fails because Figma MCP is not connected, pause and set it up:

1. Add the Figma MCP:
    - `codex mcp add figma --url https://mcp.figma.com/mcp`
2. Enable remote MCP client:
    - Set `[features].rmcp_client = true` in `config.toml` **or** run `codex --enable rmcp_client`
3. Log in with OAuth:
    - `codex mcp login figma`

After successful login, the user will have to restart codex. You should finish your answer and tell them so when they try again they can continue with Step 1.

### Step 1: Get Node ID

#### Option A: Parse from Figma URL

When the user provides a Figma URL, extract the file key and node ID to pass as arguments to MCP tools.

**URL format:** `https://figma.com/design/:fileKey/:fileName?node-id=1-2`

**Extract:**

- **File key:** `:fileKey` (the segment after `/design/`)
- **Node ID:** `1-2` (the value of the `node-id` query parameter)

**Note:** When using the local desktop MCP (`figma-desktop`), `fileKey` is not passed as a parameter to tool calls. The server automatically uses the currently open file, so only `nodeId` is needed.

**Example:**

- URL: `https://figma.com/design/kL9xQn2VwM8pYrTb4ZcHjF/DesignSystem?node-id=42-15`
- File key: `kL9xQn2VwM8pYrTb4ZcHjF`
- Node ID: `42-15`

#### Option B: Use Current Selection from Figma Desktop App (figma-desktop MCP only)

When using the `figma-desktop` MCP and the user has NOT provided a URL, the tools automatically use the currently selected node from the open Figma file in the desktop app.

**Note:** Selection-based prompting only works with the `figma-desktop` MCP server. The remote server requires a link to a frame or layer to extract context. The user must have the Figma desktop app open with a node selected.

### Step 2: Fetch Design Context

Run `get_design_context` with the extracted file key and node ID.

```
get_design_context(fileKey=":fileKey", nodeId="1-2")
```

This provides the structured data including:

- Layout properties (Auto Layout, constraints, sizing)
- Typography specifications
- Color values and design tokens
- Component structure and variants
- Spacing and padding values

**If the response is too large or truncated:**

1. Run `get_metadata(fileKey=":fileKey", nodeId="1-2")` to get the high-level node map
2. Identify the specific child nodes needed from the metadata
3. Fetch individual child nodes with `get_design_context(fileKey=":fileKey", nodeId=":childNodeId")`

### Step 3: Capture Visual Reference

Run `get_screenshot` with the same file key and node ID for a visual reference.

```
get_screenshot(fileKey=":fileKey", nodeId="1-2")
```

This screenshot serves as the source of truth for visual validation. Keep it accessible throughout implementation.

### Step 4: Download Required Assets

Download any assets (images, icons, SVGs) returned by the Figma MCP server.

**IMPORTANT:** Follow these asset rules:

- If the Figma MCP server returns a `localhost` source for an image or SVG, use that source directly
- DO NOT import or add new icon packages - all assets should come from the Figma payload
- DO NOT use or create placeholders if a `localhost` source is provided
- Assets are served through the Figma MCP server's built-in assets endpoint

**Project asset and style file locations:**

| Type                                            | Location                                                  |
| ----------------------------------------------- | --------------------------------------------------------- |
| Images / icons (Vite-processed, imported in TS) | `src/client/assets/images/` or `src/client/assets/icons/` |
| Static fonts referenced by URL in CSS           | `public/fonts/`                                           |
| Tailwind theme tokens (colors, spacing, radii)  | `src/client/index.css` - `@theme inline` block            |
| Custom CSS (keyframes, @font-face, overrides)   | `src/client/custom.css`                                   |

### Step 5: Translate to Project Conventions

Translate the Figma output into this project's framework, styles, and conventions.

**Key principles:**

- Treat the Figma MCP output (typically React + Tailwind) as a representation of design and behavior, not as final code style
- Replace Tailwind utility classes with the project's preferred utilities or design system tokens
- Reuse existing components (buttons, inputs, typography, icon wrappers) instead of duplicating functionality
- Use the project's color system, typography scale, and spacing tokens consistently
- Respect existing routing, state management, and data-fetch patterns

### Step 6: Achieve 1:1 Visual Parity

Strive for pixel-perfect visual parity with the Figma design.

**Guidelines:**

- Prioritize Figma fidelity to match designs exactly
- Avoid hardcoded values - use design tokens from Figma where available
- When conflicts arise between design system tokens and Figma specs, prefer design system tokens but adjust spacing or sizes minimally to match visuals
- Follow WCAG requirements for accessibility
- Add component documentation as needed

### Step 7: Validate Against Figma

Before marking complete, validate the final UI against the Figma screenshot.

**Validation checklist:**

- [ ] Layout matches (spacing, alignment, sizing)
- [ ] Typography matches (font, size, weight, line height)
- [ ] Colors match exactly
- [ ] Interactive states work as designed (hover, active, disabled)
- [ ] Responsive behavior follows Figma constraints
- [ ] Assets render correctly
- [ ] Accessibility standards met

## Implementation Rules

### Component Organization

- Place new UI components in `src/client/components/` (never in `src/client/components/ui/` - those are shadcn files and must not be modified)
- To extend a shadcn/ui component, create a wrapper in `src/client/components/` that imports from `@/components/ui/`
- Use **named exports only** - no default exports
- Component names must be PascalCase; file names must match the component name
- Never use inline `style={}` when an equivalent Tailwind utility class exists
- Use `cn()` from `@/lib/utils` for conditional class merging

### Design System Integration

- ALWAYS check `src/client/components/` for an existing component before creating a new one
- Map Figma design tokens to project tokens: colors from `@theme inline` in `src/client/index.css`, typography from the theme block, spacing via Tailwind scale
- When a matching component exists, extend it (create a wrapper) rather than duplicating
- Use `cn()` from `@/lib/utils` for all conditional class merging

### Code Quality

- Avoid hardcoded values - extract to constants or design tokens
- Keep components composable and reusable
- Add TypeScript types for component props

## Examples

See [design-implementation-scenarios.md](examples/design-implementation-scenarios.md) for detailed scenarios including implementing a button component and building a complete dashboard layout from Figma designs.

## Best Practices

### Always Start with Context

Never implement based on assumptions. Always fetch `get_design_context` and `get_screenshot` first.

### Incremental Validation

Validate frequently during implementation, not just at the end. This catches issues early.

### Document Deviations

If you must deviate from the Figma design (e.g., for accessibility or technical constraints), document why in code comments.

### Reuse Over Recreation

Always check for existing components before creating new ones. Consistency across the codebase is more important than exact Figma replication.

### Design System First

When in doubt, prefer the project's design system patterns over literal Figma translation.

## Common Issues and Solutions

See [troubleshooting.md](reference/troubleshooting.md) for solutions to common issues including truncated Figma output, design mismatches, asset loading problems, and design token discrepancies.

## Understanding Design Implementation

The Figma implementation workflow establishes a reliable process for translating designs to code:

**For designers:** Confidence that implementations will match their designs with pixel-perfect accuracy.
**For developers:** A structured approach that eliminates guesswork and reduces back-and-forth revisions.
**For teams:** Consistent, high-quality implementations that maintain design system integrity.

By following this workflow, you ensure that every Figma design is implemented with the same level of care and attention to detail.

## Arguments

When invoking this skill with arguments:

- `$0` or `$ARGUMENTS[0]` - Figma URL in format `https://figma.com/design/:fileKey/:fileName?node-id=1-2`
    - The skill extracts `:fileKey` (file identifier) and `1-2` (node ID) from the URL
    - Example: `/figma-implement-design https://figma.com/design/abc123/MyDesign?node-id=10-25`
- `$1` or `$ARGUMENTS[1]` - Optional explicit node-id override
    - Use when targeting a specific variant or nested component
    - Example: `/figma-implement-design https://figma.com/design/abc123/MyDesign 10-25`

If invoked without arguments, the skill will prompt for the Figma URL during execution.

## Session Tracking

This skill uses `${CLAUDE_SESSION_ID}` to track design implementation sessions:

```typescript
// Each implementation is logged with session context
const sessionId = process.env.CLAUDE_SESSION_ID;
console.log(`[${sessionId}] Implementing Figma design: ${fileKey}, node: ${nodeId}`);
```

This allows correlation between:

- Design implementation start/completion
- MCP tool invocations (get_design_context, get_screenshot, get_assets)
- Git commits containing the implementation code
- Code review feedback and iterations

Use the session ID to trace the full lifecycle of a design implementation from Figma link to production code.

## Additional Resources

- [Figma MCP Server Documentation](https://developers.figma.com/docs/figma-mcp-server/)
- [Figma MCP Server Tools and Prompts](https://developers.figma.com/docs/figma-mcp-server/tools-and-prompts/)
- [Figma Variables and Design Tokens](https://help.figma.com/hc/en-us/articles/15339657135383-Guide-to-variables-in-Figma)
