---
name: dsai-tools
description: CLI reference and build system documentation for the @dsai-io/tools package. Covers the `dsai` command, component/hook/util installation from registry, design-token pipeline, icon generation, configuration schema, and framework mappers.
---

# @dsai-io/tools CLI & Build System

## Package Overview

- **Package:** `@dsai-io/tools` (v1.3.0)
- **CLI command:** `dsai`
- **Dependencies:** commander, cosmiconfig, deepmerge, fast-glob, ora, picocolors, svgo, zod
- **Config:** cosmiconfig (`dsai.config.mjs` / `.js` / `.ts`)

---

## CLI Commands

### `dsai init`

Initialize DSAI in a project.

- Creates `dsai.config.mjs` with sensible defaults
- Sets up directory structure (`collections/`, `generated/`, `scss/`)

### `dsai add <items...>`

Install components, hooks, or utilities from the registry.

```bash
dsai add button                    # Single component
dsai add button modal card         # Multiple components
dsai add --all                     # Everything
dsai add --type hook               # All hooks
dsai add --type util               # All utilities
dsai add --overwrite               # Overwrite existing files
dsai add --dry-run                 # Preview without writing
dsai add --registry ./path         # Custom registry path
```

#### How `dsai add` works internally

1. Parse items & validate
2. Load project config (`dsai.config.mjs`) for aliases + target dirs
3. Find registry at `node_modules/@dsai-io/tools/registry/`
4. Load `<item>.json` from `registry/{components,hooks,utils,types}/`
5. BFS dependency resolution (transitive dependencies)
6. Topological sort (Kahn's algorithm) — detects circular deps
7. Collect npm dependencies
8. Transform imports: relative (`../../hooks/`) → alias (`@/hooks/`)
9. Write files to target directories
10. Skip existing files unless `--overwrite`

#### Registry types

| Registry type        | Config key         | Target directory          |
|----------------------|--------------------|---------------------------|
| `registry:ui`        | `aliases.ui`       | `components/ui/<name>/`   |
| `registry:hook`      | `aliases.hooks`    | hooks directory            |
| `registry:util`      | `aliases.utils`    | utils directory            |
| `registry:lib`       | `aliases.lib`      | lib directory              |
| `registry:component` | `aliases.components` | components directory     |
| `registry:type`      | `aliases.components` | components directory     |
| `registry:style`     | `aliases.ui`       | UI directory               |

### `dsai tokens build`

Run the full token pipeline (12 steps). Pipeline is cached — only reruns changed steps.

| Step | Name | Description |
|------|------|-------------|
| 1 | `validate` | Check DTCG JSON structure (colors: HEX/RGB/HSL, dimensions: px/rem/em, references) |
| 2 | `snapshot` | Backup current tokens |
| 3 | `preprocess` | Extract Figma modes (light/dark) |
| 4 | `transform` | Figma exports → DTCG format |
| 5 | `style-dictionary` | Build CSS/JS/TS/SCSS/JSON outputs |
| 6 | `sync` | Create `tokens-flat.ts` |
| 7 | `sass-theme` | Compile Bootstrap SCSS theme (`dsai-theme-bs.scss` → `dsai-theme-bs.css`) |
| 8 | `sass-theme-minified` | Minified variant |
| 9 | `postprocess` | Replace `data-bs-theme` → `data-dsai-theme` in CSS |
| 10 | `sass-utilities` | Compile DSAI utilities SCSS |
| 11 | `sass-utilities-minified` | Minified utilities |
| 12 | `bundle` | Final tsup packaging |

### `dsai tokens validate`

Validate token structure only (no build).

### `dsai tokens transform`

Transform only (no build).

### `dsai icons`

Run the icon pipeline.

- Scan SVG files → Parse → Optimize (SVGO) → Generate React components + SVG sprites
- Tracks: `totalIcons`, `filesWritten`, `totalSizeReduction`

### `dsai info`

Display project info.

### `dsai config`

Manage configuration.

### `dsai registry`

Registry management (`build`, `list`).

---

## Configuration Schema

File: `dsai.config.mjs`

```javascript
import { defineConfig } from '@dsai-io/tools';
export default defineConfig({
  global: {
    debug: false,
    framework: 'react',       // 'react' | 'vue' | 'svelte'
  },
  tokens: {
    source: 'theme',
    sourceDir: './src/figma-exports',
    collectionsDir: './src',
    outputDir: './src/generated',
    outputDirs: {
      css: './src/generated/css',
      scss: './src/generated/scss',
      js: './src/generated/js',
      ts: './src/generated/ts',
      json: './src/generated/json',
    },
    prefix: '--dsai-',
    formats: ['css', 'scss', 'js', 'ts', 'json'],
    scss: {
      outputStyles: ['expanded', 'compressed'],
      themeEntry: 'src/scss/dsai-theme-bs.scss',
      cssOutputDir: 'src/generated/css',
      loadPaths: ['node_modules'],
      framework: 'bootstrap',     // 'bootstrap' | 'shadcn' | 'tailwind' | 'mui' | 'custom'
      variablesOutput: 'src/scss/_variables.scss',
    },
    postprocess: {
      enabled: true,
      cssDir: 'src/generated/css',
      files: ['dsai-theme-bs.css', 'dsai-theme-bs.min.css'],
      replacements: [{ from: /data-bs-theme/g, to: 'data-dsai-theme' }],
    },
    pipeline: {
      steps: [
        'validate', 'transform', 'multi-theme', 'sync',
        'sass-theme', 'sass-theme-minified', 'postprocess',
      ],
    },
    themes: {
      enabled: true,
      default: 'light',
      autoDetect: true,
      definitions: {
        light: {
          isDefault: true,
          selector: ':root',
          outputFiles: {
            css: 'tokens.css',
            scss: '_variables.scss',
            js: 'tokens.js',
            ts: 'tokens.d.ts',
            json: 'tokens.json',
          },
        },
        dark: {
          selector: '[data-dsai-theme="dark"]',
          mediaQuery: '(prefers-color-scheme: dark)',
          outputFiles: {
            css: 'tokens-dark.css',
            scss: '_variables-dark.scss',
          },
        },
      },
    },
    aliases: {
      importAlias: '@/',
      ui: 'src/client/components/ui',
      hooks: 'src/client/hooks',
      utils: 'src/client/lib/utils',
      components: 'src/client/components',
    },
    components: { enabled: true, tsx: true, overwrite: false },
  },
});
```

---

## Framework Mappers

### Bootstrap (default)

Maps DSAI tokens → Bootstrap SCSS variables.

| Category | DSAI Token | Bootstrap Variable |
|----------|------------|--------------------|
| Typography | `text-base` | `font-size-base` |
| Typography | `heading-h1` | `h1-font-size` |
| Typography | `display-d1` | `display1-size` |
| Font Weights | `thin` | `font-weight-lighter` |
| Font Weights | `semi-bold` | `font-weight-semibold` |
| Shadows | `shadow-default` | `box-shadow` |
| Shadows | `shadow-lg` | `box-shadow-lg` |
| Border Radius | `border-radius-default` | `border-radius` |

### Other Supported Frameworks

- **shadcn** — Pass-through (no mapping)
- **Tailwind** — Generates `config.js`
- **MUI** — Generates JS theme object
- **Custom** — User-defined mappings

---

## Output Formats

| Format | File | Content |
|--------|------|---------|
| CSS | `tokens.css` | `:root { --dsai-*: value; }` |
| CSS Dark | `tokens-dark.css` | `[data-dsai-theme="dark"] { --dsai-*: value; }` |
| SCSS | `_variables.scss` | `$token-name: value;` |
| Bootstrap | `dsai-theme-bs.css` | Compiled Bootstrap with token overrides |
| JS | `tokens.js` | `export const TokenName = "value";` |
| TS | `tokens.d.ts` | `export const TokenName: string;` |
| JSON | `tokens.json` | `{"TokenName": "value"}` |

---

## Typical Workflow

```bash
# Initial setup
dsai init
dsai add button modal card tabs input

# After editing token JSON
dsai tokens build

# After Figma sync
dsai figma sync
dsai tokens build

# Add more components later
dsai add select checkbox dropdown
```

---

## Default Configuration (No Config File)

Consumer projects can work **without** a `dsai.config.mjs` file. When no config file exists, `dsai` uses these defaults:

| Setting | Default Value |
|---|---|
| `aliases.importAlias` | `@/` |
| `aliases.ui` | `src/client/components/ui` |
| `aliases.hooks` | `src/client/hooks` |
| `aliases.utils` | `src/client/lib/utils` |
| `aliases.components` | `src/client/components` |
| `global.framework` | `react` |
| `components.tsx` | `true` |
| `components.overwrite` | `false` |

If these defaults match your project structure, `dsai add` works out of the box — no `dsai init` required.

> **Example:** `draft_v0` uses the default paths and has no `dsai.config.mjs` file. Running `dsai add button` writes to `src/client/components/ui/button/`.

Only create `dsai.config.mjs` when you need to override defaults (custom paths, different framework, or token pipeline settings).

---

## New Project Setup (End-to-End)

```bash
# 1. Install @dsai-io/tools as a dev dependency
npm install -D @dsai-io/tools

# 2. (Optional) Initialize config — skip if defaults match your project
dsai init

# 3. Add components you need
dsai add button modal card input select tabs

# 4. Verify files were written
ls src/client/components/ui/
#  → button/ card/ input/ modal/ select/ tabs/

# 5. Import and use in your app
```

```tsx
// src/client/App.tsx
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';

function App() {
  return (
    <Card variant="elevated">
      <Card.Body>
        <Button variant="primary">Hello DSAI</Button>
      </Card.Body>
    </Card>
  );
}
```

### Adding Token Pipeline (Optional)

If your project uses DSAI design tokens from Figma:

```bash
# 1. Install figma-tokens package
npm install -D @dsai-io/figma-tokens

# 2. Add scripts to package.json
# "figma:sync": "dsai figma sync"
# "tokens:build": "dsai tokens build"

# 3. Set Figma env vars
echo 'FIGMA_API_KEY=your-token' >> .env
echo 'FIGMA_FILE_ID=your-file-id' >> .env

# 4. Sync and build
dsai figma sync
dsai tokens build

# 5. Import generated CSS in main.tsx (order matters — see dsai-styling skill)
```

---

## Troubleshooting

### `dsai add` fails with "registry not found"

The CLI looks for registry files at `node_modules/@dsai-io/tools/registry/`. Ensure `@dsai-io/tools` is installed:

```bash
npm ls @dsai-io/tools
```

If missing, install it: `npm install -D @dsai-io/tools`

### Imports don't resolve after `dsai add`

Verify your `tsconfig.json` has the `@/` path alias:

```json
{
  "compilerOptions": {
    "paths": {
      "@/*": ["./src/client/*"]
    }
  }
}
```

Also check your bundler (Vite, webpack) has matching alias configuration.

### Components missing dependencies after `dsai add`

`dsai add` resolves transitive dependencies via BFS, but npm packages listed in each registry item's `dependencies` field must be installed separately:

```bash
# Check what a component needs
dsai add button --dry-run

# Install any missing npm packages
npm install <missing-package>
```

### `dsai tokens build` fails

- Verify token JSON files in `src/collections/` follow DTCG format (`$value`, `$type`)
- Check that Bootstrap SCSS entry file exists at the configured `scss.themeEntry` path
- Run `dsai tokens validate` first to isolate schema errors
