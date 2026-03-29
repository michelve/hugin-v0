# Registry Usage Guide

## Overview
DSAI components are installed as local source code via the `dsai add` CLI command. Components are NOT npm dependencies — they become part of your project source code that you own and can modify.

## Quick Start
```bash
# Install single component
dsai add button

# Install multiple components
dsai add button modal card tabs input select

# Install all components
dsai add --all

# Install all hooks
dsai add --type hook

# Preview without writing
dsai add --dry-run button modal
```

## Where Files Are Written
Based on dsai.config.mjs aliases:
```
Component → src/client/components/ui/<name>/
  ├── ComponentName.tsx
  ├── ComponentName.types.ts
  ├── ComponentName.fsm.ts (if interactive)
  ├── ComponentName.test.tsx
  ├── ComponentName.a11y.test.tsx
  └── index.ts

Hook → src/client/hooks/
  └── useHookName.ts

Utility → src/client/lib/utils/
  └── utilName.ts

Type → src/client/components/
  └── types/typeName.ts
```

## Import Transformation
Registry files use relative imports. During installation, these are transformed to use project aliases:

```
BEFORE (registry):  import { useHover } from '../../hooks/useHover';
AFTER (installed):  import { useHover } from '@/hooks/useHover';
```

This is controlled by `aliases.importAlias` in dsai.config.mjs (default: `@/`).

## Dependency Resolution
When you `dsai add modal`, the CLI:
1. Looks up modal.json in the registry
2. Finds dependencies: [button, spinner, useFocusTrap, useScrollLock, useKeyPress, cn]
3. BFS resolves transitive deps for each
4. Topological sort determines installation order
5. Installs all dependencies first, then modal

```
dsai add modal
  → button (dep of modal)
    → spinner (dep of button)
    → cn (dep of button)
  → useFocusTrap (dep of modal)
  → useScrollLock (dep of modal)
  → useKeyPress (dep of modal)
  → modal (target)
```

## File Behavior
- **Skip**: Existing files are NOT overwritten (safe to re-run)
- **Overwrite**: Use `--overwrite` flag to replace existing files
- **Dependencies**: Only missing deps are installed, existing ones skipped

## NPM Dependencies
The CLI also collects and installs required npm packages:
```bash
# After dsai add, you may see:
# Installing npm dependencies: bootstrap@^5.3.0, @popperjs/core@^2.11.0
```

## Registry Structure
Each registry entry is a JSON file like:
```json
{
  "name": "button",
  "type": "registry:ui",
  "dependencies": ["cn"],
  "registryDependencies": ["spinner"],
  "devDependencies": [],
  "files": [
    { "path": "Button.tsx", "type": "registry:ui" },
    { "path": "Button.types.ts", "type": "registry:ui" },
    { "path": "Button.fsm.ts", "type": "registry:ui" },
    { "path": "index.ts", "type": "registry:ui" }
  ]
}
```

## Common Workflows

### Starting a new project
```bash
dsai init
dsai add --all
dsai tokens build
```

### Adding a feature that needs new components
```bash
dsai add select searchselectfield
# Then import in your component:
# import { Select } from '@/components/ui/select';
```

### Customizing an installed component
Components are YOUR source code. Edit directly:
```bash
# Edit src/client/components/ui/button/Button.tsx
# Add custom variant, modify styling, etc.
```

### Updating after dsai package upgrade
```bash
npm update @dsai-io/tools
dsai add --overwrite button  # Get latest Button from registry
```
