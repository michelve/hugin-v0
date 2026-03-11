---
name: figma
description: Use the Figma MCP server to fetch design context, screenshots, variables, and assets from Figma, and to translate Figma nodes into production code. Trigger when a task involves Figma URLs, node IDs, design-to-code implementation, or Figma MCP setup and troubleshooting.
argument-hint: "Figma URL or node-id"
user-invocable: true
allowed-tools: figma__get_design_context, figma__get_screenshot, figma__get_assets, figma__get_variables, figma__get_code_connect_suggestions, figma__create_design_system_rules
---

# Figma MCP

Use the Figma MCP server for Figma-driven implementation. For setup and debugging details (env vars, config, verification), see `references/figma-mcp-config.md`.

## Figma MCP Integration Rules

These rules define how to translate Figma inputs into code for this project and must be followed for every Figma-driven change.

### Required flow (do not skip)

1. Run get_design_context first to fetch the structured representation for the exact node(s).
2. If the response is too large or truncated, run get_metadata to get the high-level node map and then re-fetch only the required node(s) with get_design_context.
3. Run get_screenshot for a visual reference of the node variant being implemented.
4. Only after you have both get_design_context and get_screenshot, download any assets needed and start implementation.
5. Translate the output (usually React + Tailwind) into this project's conventions, styles and framework. Reuse the project's color tokens, components, and typography wherever possible.
6. Validate against Figma for 1:1 look and behavior before marking complete.

### Implementation rules

- Treat the Figma MCP output (React + Tailwind) as a representation of design and behavior, not as final code style.
- Replace Tailwind utility classes with the project's preferred utilities/design-system tokens when applicable.
- Reuse existing components (e.g., buttons, inputs, typography, icon wrappers) instead of duplicating functionality.
- Use the project's color system, typography scale, and spacing tokens consistently.
- Respect existing routing, state management, and data-fetch patterns already adopted in the repo.
- Strive for 1:1 visual parity with the Figma design. When conflicts arise, prefer design-system tokens and adjust spacing or sizes minimally to match visuals.
- Validate the final UI against the Figma screenshot for both look and behavior.

### Asset handling

- The Figma MCP Server provides an assets endpoint which can serve image and SVG assets.
- IMPORTANT: If the Figma MCP Server returns a localhost source for an image or an SVG, use that image or SVG source directly.
- IMPORTANT: DO NOT import/add new icon packages, all the assets should be in the Figma payload.
- IMPORTANT: do NOT use or create placeholders if a localhost source is provided.

### Link-based prompting

- The server is link-based: copy the Figma frame/layer link and give that URL to the MCP client when asking for implementation help.
- The client cannot browse the URL but extracts the node ID from the link; always ensure the link points to the exact node/variant you want.

## Arguments

When invoking this skill with arguments:

- `$ARGUMENTS` - Flexible handling of Figma URLs or node IDs
    - Full URL: `https://figma.com/design/:fileKey/:fileName?node-id=1-2`
    - File key only: `abc123` (skill will extract design context for entire file)
    - Node ID: `10-25` (when file context is already established)
    - Example: `/figma https://figma.com/design/abc123/MyDesign?node-id=10-25`
    - Example: `/figma abc123`

The skill parses `$ARGUMENTS` to determine what Figma data to fetch (design context, screenshot, assets, or variables) based on the user's intent and the format provided.

## References

- `references/figma-mcp-config.md` - setup, verification, troubleshooting, and link-based usage reminders.
- `references/figma-tools-and-prompts.md` - tool catalog and prompt patterns for selecting frameworks/components and fetching metadata.
