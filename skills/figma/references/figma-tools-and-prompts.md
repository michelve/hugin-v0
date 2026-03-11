# Figma MCP tools and prompt patterns

Quick reference for the Figma MCP toolset, when to use each tool, and prompt examples to steer output toward your stack.

Source: https://developers.figma.com/docs/figma-mcp-server/tools-and-prompts/

## Core tools

- `generate_figma_design` (remote only; VS Code, Claude Code, Codex): Captures live UI from your web app and sends it as design layers to a new Figma file, an existing file, or your clipboard. Exempt from standard rate limits. Start a local server, then prompt the agent to capture. Use the in-browser toolbar to capture entire screen or specific elements.
- `get_design_context` (Figma Design, Figma Make): Primary tool. Returns structured design data and default React + Tailwind code. Selection-based prompting works on desktop; the remote server uses a frame/layer link to extract the node ID. Use the `clientFrameworks` parameter to control which Code Connect mappings are returned (e.g., `React`, `SwiftUI`).
- `get_variable_defs` (Figma Design): Lists variables/styles (colors, spacing, typography) used in the selection. Useful to align with tokens.
- `get_metadata` (Figma Design): Sparse XML outline of layer IDs/names/types/positions/sizes. Use before re-calling `get_design_context` on large nodes to avoid truncation. Also works with multiple selections or the whole page if nothing is selected.
- `get_screenshot` (Figma Design, FigJam): Screenshot of the selection for visual fidelity checks. Recommended to keep on (only turn off if concerned about token limits).
- `get_figjam` (FigJam): XML + screenshots for FigJam diagrams (architecture, flows).
- `generate_diagram` (no file context): Generates a FigJam diagram from Mermaid syntax. Supports flowcharts, Gantt charts, state diagrams, and sequence diagrams. You can describe diagrams in natural language - the agent generates the Mermaid syntax automatically.
- `create_design_system_rules` (no file context): Generates a rule file with design-to-code guidance for your stack. Save it to the `rules/` or `instructions/` path so the agent can access it during code generation.
- `get_code_connect_map` (Figma Design): Returns mapping of Figma node IDs to code components (`codeConnectSrc`, `codeConnectName`). Use to reuse existing components.
- `add_code_connect_map` (Figma Design): Adds/updates a mapping between a Figma node and a code component to improve design-to-code output quality.
- `get_code_connect_suggestions` (Figma Design): Figma-prompted tool to detect and suggest mappings of Figma components to code components in your codebase using Code Connect.
- `send_code_connect_mappings` (Figma Design): Figma-prompted tool to confirm the Code Connect mappings after calling `get_code_connect_suggestions`.
- `whoami` (remote only): Returns the authenticated Figma user identity (email, plans, seat types).

## Prompt patterns (generate design)

- To a new file: "Start a local server for my app and capture the UI in a new Figma file."
- To an existing file: "Start a local server for my app and capture the UI in `<Figma file URL>`."
- To clipboard: "Start a local server for my app and use the Figma MCP server to capture the UI to my clipboard."
- Subsequent captures: "Also capture the account screen" (agent infers the same file).

## Prompt patterns (design context)

- Change framework: "generate my Figma selection in Vue" or "in plain HTML + CSS" or "for iOS".
- Use my components: "generate my Figma selection using components from `src/components/ui`".
- Combine: "generate my Figma selection using components from `src/ui` and style with Tailwind".
- Tip: Set up Code Connect for best code reuse results. The Desktop MCP server uses the Code Connect mapping selected in Dev Mode. For the Remote MCP Server, set the `clientFrameworks` tool call parameter to the exact Code Connect label (e.g., `React`, `SwiftUI`).
- Note: Selection-based prompting only works with the desktop MCP server. The remote server requires a link to a frame or layer to extract context.

## Prompt patterns (variables/styles)

- "get the variables used in my Figma selection"
- "what color and spacing variables are used in my Figma selection?"
- "list the variable names and their values used in my Figma selection"

## Prompt patterns (diagrams)

- "create a flowchart for the user authentication flow using the Figma MCP generate_diagram tool"
- "generate a gantt chart for the project timeline using the Figma MCP generate_diagram tool"
- "generate a sequence diagram for the payment processing system using the Figma MCP generate_diagram tool"
- "create a diagram from this mermaid syntax: ..."

## Prompt patterns (code connect)

- "show the code connect map for this selection"
- "map this node to `src/components/ui/Button.tsx` with name `Button`"

## Best-practice flow reminder

Use `get_design_context` → (optionally `get_metadata` for large nodes) → `get_screenshot`, and keep project rules from `SKILL.md` in mind when applying the generated output.
