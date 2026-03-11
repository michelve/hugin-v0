---
name: code-connect-components
description: Connects Figma design components to code components using Code Connect. Use when user says "code connect", "connect this component to code", "connect Figma to code", "map this component", "link component to code", "create code connect mapping", "add code connect", "connect design to code", or wants to establish mappings between Figma designs and code implementations. Requires Figma MCP server connection.
argument-hint: "Figma URL + node-id (optional specific component)"
user-invocable: true
context: fork
allowed-tools: figma__get_code_connect_suggestions, figma__get_design_context
metadata:
    mcp-server: figma
---

# Code Connect Components

## Overview

This skill helps you connect Figma design components to their corresponding code implementations using Figma's Code Connect feature. It analyzes the Figma design structure, searches your codebase for matching components, and establishes mappings that maintain design-code consistency.

## Prerequisites

- Figma MCP server must be connected and accessible
    - Before proceeding, verify the Figma MCP server is connected by checking if Figma MCP tools (e.g., `get_code_connect_suggestions`) are available.
    - If the tools are not available, the Figma MCP server may not be enabled. Guide the user to enable the Figma MCP server that is included with the plugin. They may need to restart their MCP client afterward.
- User must provide a Figma URL with node ID: `https://figma.com/design/:fileKey/:fileName?node-id=1-2`
    - **IMPORTANT:** The Figma URL must include the `node-id` parameter. Code Connect mapping will fail without it.
- **IMPORTANT:** The Figma component must be published to a team library. Code Connect only works with published components or component sets.
- **IMPORTANT:** Code Connect is only available on Organization and Enterprise plans.
- Access to the project codebase for component scanning

## Required Workflow

**Follow these steps in order. Do not skip steps.**

### Step 1: Get Code Connect Suggestions

Call `get_code_connect_suggestions` to identify all unmapped components in a single operation. This tool automatically:

- Fetches component info from the Figma scenegraph
- Identifies published components in the selection
- Checks existing Code Connect mappings and filters out already-connected components
- Returns component names, properties, and thumbnail images for each unmapped component

Parse the URL to extract `fileKey` and `nodeId`, then call `get_code_connect_suggestions`.

**IMPORTANT:** When extracting the node ID from a Figma URL, convert the format:

- URL format uses hyphens: `node-id=1-2`
- Tool expects colons: `nodeId=1:2`

**Parse the Figma URL:**

- URL format: `https://figma.com/design/:fileKey/:fileName?node-id=1-2`
- Extract file key: `:fileKey` (segment after `/design/`)
- Extract node ID: `1-2` from URL, then convert to `1:2` for the tool

```
get_code_connect_suggestions(fileKey=":fileKey", nodeId="1:2")
```

**Handle the response:**

- If the tool returns **"No published components found in this selection"** → inform the user and stop. The components may need to be published to a team library first.
- If the tool returns **"All component instances in this selection are already connected to code via Code Connect"** → inform the user that everything is already mapped.
- Otherwise, the response contains a list of unmapped components, each with:
    - Component name
    - Node ID
    - Component properties (JSON with prop names and values)
    - A thumbnail image of the component (for visual inspection)

### Step 2: Scan Codebase for Matching Components

For each unmapped component returned by `get_code_connect_suggestions`, search the codebase for a matching code component.

**What to look for:**

- Component names that match or are similar to the Figma component name
- Component structure that aligns with the Figma hierarchy
- Props that correspond to Figma properties (variants, text, styles)
- Files in typical component directories (`src/components/`, `components/`, `ui/`, etc.)

**Search strategy:**

1. Search for component files with matching names
2. Read candidate files to check structure and props
3. Compare the code component's props with the Figma component properties returned in Step 1
4. Detect the programming language (TypeScript, JavaScript) and framework (React, Vue, etc.)
5. Identify the best match based on structural similarity, weighing:
    - Prop names and their correspondence to Figma properties
    - Default values that match Figma defaults
    - CSS classes or style objects
    - Descriptive comments that clarify intent
6. If multiple candidates are equally good, pick the one with the closest prop-interface match and document your reasoning in a 1-2 sentence comment before your tool call

**Example search patterns:**

- If Figma component is "PrimaryButton", search for `Button.tsx`, `PrimaryButton.tsx`, `Button.jsx`
- Check project component paths: `src/client/components/` (primary target; **do not** search `src/client/components/ui/` - those are immutable shadcn files)
- Look for variant props like `variant`, `size`, `color` that match Figma variants

### Step 3: Present Matches to User

Present your findings and let the user choose which mappings to create. The user can accept all, some, or none of the suggested mappings.

**Present matches in this format:**

```
The following components match the design:
- [ComponentName](path/to/component): DesignComponentName at nodeId [nodeId](figmaUrl?node-id=X-Y)
- [AnotherComponent](path/to/another): AnotherDesign at nodeId [nodeId2](figmaUrl?node-id=X-Y)

Would you like to connect these components? You can accept all, select specific ones, or skip.
```

**If no exact match is found for a component:**

- Show the 2 closest candidates
- Explain the differences
- Ask the user to confirm which component to use or provide the correct path

**If the user declines all mappings**, inform them and stop. No further tool calls are needed.

### Step 4: Create Code Connect Mappings

Once the user confirms their selections, call `send_code_connect_mappings` with only the accepted mappings. This tool handles batch creation of all mappings in a single call.

**Example:**

```
send_code_connect_mappings(
  fileKey=":fileKey",
  nodeId="1:2",
  mappings=[
    { nodeId: "1:2", componentName: "Button", source: "src/components/Button.tsx", label: "React" },
    { nodeId: "1:5", componentName: "Card", source: "src/components/Card.tsx", label: "React" }
  ]
)
```

**Key parameters for each mapping:**

- `nodeId`: The Figma node ID (with colon format: `1:2`)
- `componentName`: Name of the component to connect (e.g., "Button", "Card")
- `source`: Path to the code component file (relative to project root)
- `label`: The framework or language label for this Code Connect mapping. **For this project, always use `"React"`**. Valid values include:
    - Web: 'React', 'Web Components', 'Vue', 'Svelte', 'Storybook', 'Javascript'
    - iOS: 'Swift UIKit', 'Objective-C UIKit', 'SwiftUI'
    - Android: 'Compose', 'Java', 'Kotlin', 'Android XML Layout'
    - Cross-platform: 'Flutter'
    - Docs: 'Markdown'

**After the call:**

- On success: the tool confirms the mappings were created
- On error: the tool reports which specific mappings failed and why (e.g., "Component is already mapped to code", "Published component not found", "Insufficient permissions")

**Provide a summary** after processing:

```
Code Connect Summary:
- Successfully connected: 3
  - Button (1:2) → src/components/Button.tsx
  - Card (1:5) → src/components/Card.tsx
  - Input (1:8) → src/components/Input.tsx
- Could not connect: 1
  - CustomWidget (1:10) - No matching component found in codebase
```

## Examples

See [code-connect-scenarios.md](examples/code-connect-scenarios.md) for detailed scenarios including connecting a single button, handling multiple components with partial selection, and creating components that don't yet exist.

## Best Practices

### Proactive Component Discovery

Don't just ask the user for the file path - actively search their codebase to find matching components. This provides a better experience and catches potential mapping opportunities.

### Accurate Structure Matching

When comparing Figma components to code components, look beyond just names. Check that:

- Props align (variant types, size options, etc.)
- Component hierarchy matches (nested elements)
- The component serves the same purpose

### Clear Communication

When offering to create a mapping, clearly explain:

- What you found
- Why it's a good match
- What the mapping will do
- How props will be connected

### Handle Ambiguity

If multiple components could match, present options rather than guessing. Let the user make the final decision about which component to connect.

### Graceful Degradation

If you can't find an exact match, provide helpful next steps:

- Show close candidates
- Suggest component creation
- Ask for user guidance

## Common Issues and Solutions

See [troubleshooting.md](reference/troubleshooting.md) for solutions to common Code Connect problems including unpublished components, plan restrictions, missing components, permission issues, and URL format errors.

## Understanding Code Connect

Code Connect establishes a bidirectional link between design and code:

**For designers:** See which code component implements a Figma component
**For developers:** Navigate from Figma designs directly to the code that implements them
**For teams:** Maintain a single source of truth for component mappings

The mapping you create helps keep design and code in sync by making these connections explicit and discoverable.

## Arguments

When invoking this skill with arguments:

- `$0` or `$ARGUMENTS[0]` - Figma file key (extracted from URL: `https://figma.com/design/:fileKey/:fileName`)
    - The skill uses this to identify which Figma file contains the component
    - Example: `/code-connect-components abc123`
- `$1` or `$ARGUMENTS[1]` - Node ID of the specific Figma component to connect
    - Format: `1-2` (from `?node-id=1-2` in Figma URL)
    - Example: `/code-connect-components abc123 10-25`

If invoked without arguments, the skill will prompt for the full Figma URL and extract the file key and node ID automatically.

## Session Tracking

This skill uses `${CLAUDE_SESSION_ID}` to track Code Connect mapping sessions:

```typescript
// Each mapping is logged with session context
const sessionId = process.env.CLAUDE_SESSION_ID;
console.log(
    `[${sessionId}] Creating Code Connect mapping: ${fileKey}#${nodeId} → ${componentPath}`,
);
```

This allows correlation between:

- Code Connect file creation (`.figma.tsx`)
- The specific Figma component being mapped
- Git commits containing the mapping
- Future updates when the component or mapping changes

Use the session ID to maintain an audit trail of when components were connected and why.

## Additional Resources

For more information about Code Connect:

- [Code Connect Documentation](https://help.figma.com/hc/en-us/articles/23920389749655-Code-Connect)
- [Figma MCP Server Tools and Prompts](https://developers.figma.com/docs/figma-mcp-server/tools-and-prompts/)
