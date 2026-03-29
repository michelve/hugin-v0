---
name: dsai-styling
description: DSAI styling system reference, Bootstrap 5 utilities, CSS custom properties (design tokens), cn() utility, dark mode, and token pipeline. Replaces the old tailwindcss skill. Use this skill when generating or modifying styles, classNames, or theme configuration in DSAI consumer applications.
---

# DSAI Styling System

## Architecture

DSAI uses **Bootstrap 5** as the base CSS framework, with **design tokens** (CSS custom properties) providing the customization layer.

> **NO Tailwind CSS.** Never use Tailwind utility classes in DSAI projects.

---

## Token Pipeline

DTCG JSON tokens (`src/collections/`) are compiled via `dsai tokens build` into multiple output formats:

| Output File | Purpose |
|---|---|
| `src/generated/css/tokens.css` | Light theme tokens (`:root` selector, `--dsai-*` prefix) |
| `src/generated/css/tokens-dark.css` | Dark theme tokens (`[data-dsai-theme="dark"]` selector) |
| `src/generated/css/dsai-theme-bs.css` | Bootstrap compiled with DSAI token overrides |
| `src/generated/scss/_variables.scss` | Sass variables for build-time usage |
| `src/generated/js/tokens.js` | JavaScript token module |
| `src/generated/ts/tokens.d.ts` | TypeScript type declarations |
| `src/generated/json/tokens.json` | Raw JSON token map |

After editing any token JSON in `src/collections/`, run:

```bash
dsai tokens build
```

---

## CSS Import Order

**CRITICAL — imports in `main.tsx` must follow this exact order:**

```tsx
import '../generated/css/dsai-theme-bs.css';    // 1. Bootstrap + DSAI token overrides
import '../generated/css/tokens.css';            // 2. Light theme CSS custom properties
import '../generated/css/tokens-dark.css';       // 3. Dark theme CSS custom properties
import './index.css';                            // 4. App base styles
import './custom.css';                           // 5. App overrides
```

Changing this order will break theme resolution and specificity.

---

## CSS Custom Properties

All design tokens are exposed as CSS custom properties prefixed with `--dsai-`:

```css
var(--dsai-color-primary)
var(--dsai-spacing-3)
var(--dsai-font-size-base)
var(--dsai-shadow-lg)
var(--dsai-border-radius)
```

Use these for any value not covered by a Bootstrap utility class.

---

## Bootstrap 5 Utility Classes

Use Bootstrap utilities — **not** Tailwind classes.

### Layout

| Category | Classes |
|---|---|
| Display | `d-flex`, `d-grid`, `d-block`, `d-none`, `d-inline` |
| Flex direction | `flex-row`, `flex-column`, `flex-wrap` |
| Flex alignment | `justify-content-center`, `align-items-center` |
| Gap | `gap-1` through `gap-5` |
| Position | `position-relative`, `position-absolute`, `position-fixed`, `position-sticky` |

### Spacing

Margin: `m-0` through `m-5`, directional: `mt-`, `mb-`, `ms-`, `me-`, `mx-`, `my-`

Padding: `p-0` through `p-5`, directional: `pt-`, `pb-`, `ps-`, `pe-`, `px-`, `py-`

### Typography

| Category | Classes |
|---|---|
| Alignment | `text-center`, `text-start`, `text-end` |
| Color | `text-body-secondary`, `text-muted` |
| Weight | `fw-bold`, `fw-semibold` |
| Size | `fs-1` through `fs-6` |

### Sizing

`w-100`, `w-75`, `w-50`, `w-25`, `h-100`, `min-vh-100`

### Visibility & Overflow

`visually-hidden` (NOT `sr-only`), `overflow-hidden`

### Borders

`border`, `border-0`, `rounded`, `rounded-circle`

### Backgrounds

`bg-primary`, `bg-secondary`, `bg-body-secondary`, `bg-body-tertiary`

### Semantic Colors

`text-primary`, `text-secondary`, `text-success`, `text-danger`, `text-warning`, `text-info`

---

## cn() Utility

`cn()` is a simple filter-and-join helper. It is **not** `tailwind-merge` and **not** `clsx`.

```typescript
function cn(...classes: (string | boolean | undefined | null)[]): string {
  return classes.filter(Boolean).join(' ');
}
```

### Usage

```typescript
cn('btn', `btn-${variant}`, size === 'lg' && 'btn-lg', disabled && 'disabled', className)
```

**Important:** `cn()` performs no conflict resolution — it only concatenates truthy values. Class order matters for CSS specificity.

---

## Using Tokens in Components

Combine `cn()`, Bootstrap utilities, and `--dsai-*` tokens in component TSX:

```tsx
import { forwardRef } from 'react';
import { cn } from '@/utils/cn';
import type { AlertProps } from './Alert.types';

export const Alert = forwardRef<HTMLDivElement, AlertProps>(
  function Alert({ variant = 'info', dismissible, className, children, ...props }, ref) {
    return (
      <div
        ref={ref}
        className={cn(
          'alert',                          // Bootstrap base class
          `alert-${variant}`,               // Bootstrap variant
          dismissible && 'alert-dismissible fade show',
          className                         // Consumer overrides
        )}
        role="alert"
        style={{
          borderRadius: 'var(--dsai-border-radius)',       // DSAI token
          padding: 'var(--dsai-spacing-3) var(--dsai-spacing-4)',  // DSAI tokens
        }}
        {...props}
      >
        {children}
      </div>
    );
  }
);
Alert.displayName = 'Alert';
```

### When to Use What

| Need | Use | Example |
|---|---|---|
| Layout, spacing, display | Bootstrap utility classes | `d-flex gap-3 p-3` |
| Component variants | Bootstrap component classes via `cn()` | `cn('btn', \`btn-${variant}\`)` |
| Brand colors, custom sizes, shadows | `--dsai-*` CSS custom properties | `var(--dsai-color-primary)` |
| Conditional classes | `cn()` with boolean expressions | `cn('btn', loading && 'disabled')` |
| Theme-aware values | Tokens (auto-switch light/dark) | `var(--dsai-bg-surface)` |

**Rule of thumb:** Use Bootstrap utilities for standard layout. Use `--dsai-*` tokens for brand/theme values that Bootstrap doesn't cover.

---

## Dark Mode in Practice

### Toggle Theme

```tsx
import { useDarkMode } from '@/hooks/useDarkMode';

function ThemeToggle() {
  const { isDark, toggle } = useDarkMode();

  return (
    <Button
      variant={isDark ? 'light' : 'dark'}
      onClick={toggle}
      aria-label={`Switch to ${isDark ? 'light' : 'dark'} mode`}
    >
      {isDark ? 'light' : 'dark'}
    </Button>
  );
}
```

### Theme-Aware Component Styles

Tokens automatically resolve to the correct value based on the active theme:

```css
/* No conditional logic needed — tokens handle it */
.custom-card {
  background: var(--dsai-bg-surface);           /* white in light, dark gray in dark */
  color: var(--dsai-color-body);                /* dark text in light, light text in dark */
  border: 1px solid var(--dsai-border-color);   /* adapts per theme */
  box-shadow: var(--dsai-shadow-sm);            /* adapts per theme */
}
```

---

## Dark Mode

### Enabling Dark Mode

Both data attributes **must** be set on `<html>` for theming to work:

```tsx
document.documentElement.setAttribute('data-dsai-theme', 'dark');
document.documentElement.setAttribute('data-bs-theme', 'dark');
```

### CSS Selectors

| Theme | Selector |
|---|---|
| Light (default) | `:root` |
| Dark | `[data-dsai-theme="dark"]` |
| Auto-detect | `prefers-color-scheme: dark` media query |

### Postprocessing

The token build pipeline replaces `data-bs-theme` with `data-dsai-theme` in generated CSS files. DSAI controls theming independently while Bootstrap continues to work.

---

## Design Token Format (DTCG)

Token JSON files in `src/collections/` follow the Design Token Community Group format:

```json
{
  "color": {
    "blue": {
      "500": {
        "$value": "#0a58ca",
        "$type": "color",
        "$description": "Base primary brand color",
        "$extensions": {
          "platform": {
            "scssVariableName": "$color-blue-500",
            "bootstrapVersion": "5.3"
          }
        }
      }
    }
  }
}
```

### Token Collections

| Collection | Contents |
|---|---|
| `color/` | primitive, semantic, background, component, neutral, opacity (all with `-dark` variants) |
| `typography/` | sizes, weights, line heights, letter spacing, headings, display |
| `spacing/` | 0–11 scale: 0px, 4px, 8px, 16px, 24px, 48px, 64px, 80px, 96px, 128px, 160px |
| `border/` | width, radius |
| `shadow/` | sm, default, lg |
| `layout/` | container, grid breakpoints |

### Color Palettes

Primitive colors: **blue, indigo, purple, pink, red, orange, yellow, green, teal, cyan** — each with shades 50–950 (13 steps).

Semantic colors: **primary, secondary, success, danger, warning, info, light, dark**.

---

## Configuration — dsai.config.mjs

```javascript
import { defineConfig } from '@dsai-io/tools';

export default defineConfig({
  tokens: {
    source: 'theme',
    sourceDir: './src/figma-exports',
    collectionsDir: './src',
    outputDir: './src/generated',
    prefix: '--dsai-',
    formats: ['css', 'scss', 'js', 'ts', 'json'],
    scss: {
      themeEntry: 'src/scss/dsai-theme-bs.scss',
      framework: 'bootstrap',
    },
    themes: {
      enabled: true,
      default: 'light',
      definitions: {
        light: { isDefault: true, selector: ':root' },
        dark: {
          selector: '[data-dsai-theme="dark"]',
          mediaQuery: '(prefers-color-scheme: dark)',
        },
      },
    },
    aliases: {
      importAlias: '@/',
      ui: 'src/client/components/ui',
      hooks: 'src/client/hooks',
      utils: 'src/client/lib/utils',
    },
  },
});
```

---

## Critical Rules

1. **NEVER** use Tailwind utility classes (no `flex`, no Tailwind-style `gap-3`, no `bg-blue-500`).
2. **USE** Bootstrap utility classes (`d-flex`, `gap-3`, `bg-primary`, `text-body-secondary`).
3. **NEVER** hardcode colors — use `var(--dsai-*)` custom properties or Bootstrap semantic classes.
4. **NEVER** hardcode spacing — use Bootstrap spacing utilities or token values.
5. CSS import order in `main.tsx` **must** be maintained exactly as documented.
6. Both `data-dsai-theme` **and** `data-bs-theme` attributes are required for theme switching.
7. Token edits require `dsai tokens build` to regenerate outputs.
8. Use `visually-hidden` (Bootstrap), **not** `sr-only` (Tailwind).
9. `cn()` is simple — no conflict resolution, just concatenation. Class order matters for specificity.
