---
name: component-visualizer
description: >-
    Generate interactive HTML dependency graphs for React components.
    Use when asked to "visualize components", "show component dependencies",
    "dependency graph", "component map", or "what depends on what".
user-invocable: true
---

# Component Visualizer

Generate an interactive force-directed dependency graph of React components
as a standalone HTML file. Scans `src/client/components/` and `src/client/routes/`
for import relationships and produces a browser-ready visualization.

## When to Use

- Understanding component relationships before refactoring
- Identifying tightly coupled or orphaned components
- Onboarding to understand component architecture
- Reviewing impact of changes across the component tree

## Quick Start

Run the visualization script from the project root:

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/visualize-components.py"
```

This outputs `component-graph.html` in the project root. Open it in a browser.

To specify a custom output path:

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/visualize-components.py" /tmp/graph.html
```

## Graph Features

- **Force-directed layout** — nodes self-organize by dependency proximity
- **Color-coded categories**:
    - Blue: Route files (`src/client/routes/`)
    - Green: Feature components (`src/client/components/`)
    - Purple: UI components (`src/client/components/ui/` — shadcn)
    - Gray: Other files
- **Interactive** — drag nodes, scroll to zoom, click for file details
- **Filterable** — toggle category visibility with checkboxes
- **Hover highlighting** — shows direct dependency edges for any node
- **Zero dependencies** — standalone HTML with embedded CSS/JS, no CDN

## What It Scans

| Directory                   | Category    | Purpose                     |
| --------------------------- | ----------- | --------------------------- |
| `src/client/components/ui/` | UI (shadcn) | Installed shadcn primitives |
| `src/client/components/`    | Component   | Project feature components  |
| `src/client/routes/`        | Route       | TanStack Router page files  |

## Import Resolution

The script resolves these import patterns:

- `@/components/ui/button` → `src/client/components/ui/button.tsx`
- `@/components/app-sidebar` → `src/client/components/app-sidebar.tsx`
- `../components/header` → relative path resolution
- `./sub-component` → same-directory resolution

Node module imports (e.g., `react`, `@tanstack/router`) are excluded.

## Interpreting the Graph

**Healthy patterns:**

- Routes (blue) connect to components (green), which compose UI (purple)
- Clusters indicate feature groupings
- UI nodes have many incoming edges (high reuse)

**Warning signs:**

- Components with no incoming edges may be dead code
- Circular dependency clusters (tight bidirectional edges)
- Routes importing directly from `ui/` (skipping abstraction layer)
- Single components with excessive outgoing edges (doing too much)

## Limitations

- Static analysis only — does not resolve dynamic imports or `React.lazy()` paths
- Does not parse re-exports from barrel files (`index.ts`)
- TypeScript path aliases other than `@/` are not resolved
- File must exist on disk (does not resolve virtual modules)
