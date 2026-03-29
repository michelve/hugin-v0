---
name: dsai-figma
description: Reference for the @dsai-io/figma-tokens package and Figma integration workflow. Covers Figma Variables API sync, token pipeline, rate limiting, description parsing, Code Connect, and the complete Figma-to-production-CSS flow.
---

# @dsai-io/figma-tokens — Figma Integration

## Package: @dsai-io/figma-tokens (v1.1.0)

Purpose: Pull design tokens from Figma Variables API into DTCG format for the DSAI token pipeline.

## Getting Started

### 1. Create a Figma Personal Access Token

1. Open Figma → Settings → Account → Personal access tokens
2. Create a new token with **File content: Read-only** and **Variables: Read** scopes
3. Copy the token

### 2. Set Environment Variables

Add to your project's `.env` file (never commit this):

```env
FIGMA_API_KEY=figd_xxxxxxxxxxxxxxxxxxxx
FIGMA_FILE_ID=AbCdEfGhIjKlMnOpQrStUv
```

`FIGMA_FILE_ID` is the string after `/design/` in your Figma file URL:
`figma.com/design/AbCdEfGhIjKlMnOpQrStUv/My-Design` → `AbCdEfGhIjKlMnOpQrStUv`

### 3. Verify Connection

```bash
dsai figma sync --dry-run
```

If successful, you'll see the list of variable collections found in the file.

### 4. Run First Sync

```bash
dsai figma sync          # Pull tokens from Figma
dsai tokens build        # Build CSS/SCSS/JS/TS outputs
```

---

## Architecture

Three components:

1. **FigmaClient** — REST API wrapper for Figma Variables API
2. **RateLimiter** — Automatic request throttling based on `X-RateLimit-*` headers
3. **DescriptionParser** — Extracts structured metadata from Figma variable descriptions

The package re-exports all token operations from `@dsai-io/tools`, so consumers get both Figma sync AND token building from one import.

## FigmaClient Configuration

```typescript
const client = new FigmaClient({
  accessToken: process.env.FIGMA_API_KEY,  // Required
  baseUrl: 'https://api.figma.com',         // Default
  timeout: 30000,                           // 30 seconds
  retries: 3,                               // Auto-retry on failure
  cache: true,                              // Cache responses
});
```

## Rate Limiting

Proactive throttling based on remaining API quota:

- At 20% remaining (`throttleThreshold: 0.2`) → 2 second delay between requests
- At 10% remaining (`criticalThreshold: 0.1`) → 5 second delay
- Parses `X-RateLimit-Remaining` and `X-RateLimit-Limit` headers automatically

## Font Detection Patterns

Identifies font properties by Figma variable name:

| Property       | Pattern                                        |
| -------------- | ---------------------------------------------- |
| Weight         | `/weight/i`                                    |
| Family         | `/family/i`                                    |
| Size           | `/size\|fontSize/i`                            |
| LineHeight     | `/lineHeight\|line-height/i`                   |
| LetterSpacing  | `/letterSpacing\|letter-spacing\|tracking/i`   |

## Description Parser

Extracts structured metadata from Figma variable descriptions:

```
Input:  "Main description text. Docs.Reference: https://example.com • Platform.Variable: $color-primary"
Output: {
  description: "Main description text",
  metadata: {
    docs: { reference: "https://example.com" },
    platform: { variable: "$color-primary" }
  }
}
```

## Complete Workflow: Figma → Production CSS

```
1. Design tokens defined in Figma Variables
   ↓
2. dsai figma sync (or pnpm figma:sync)
   - Uses FIGMA_API_KEY and FIGMA_FILE_ID env vars
   - Pulls variables via Figma REST API
   - Rate-limited automatically
   - Outputs to src/figma-exports/
   ↓
3. Token files land in src/figma-exports/ (raw Figma format)
   ↓
4. dsai tokens build
   - Step 1: validate (DTCG schema check)
   - Step 3: preprocess (extract light/dark modes)
   - Step 4: transform (Figma → DTCG format in src/collections/)
   - Steps 5-12: Build CSS/SCSS/JS/TS outputs
   ↓
5. Generated files in src/generated/
   - tokens.css (:root { --dsai-*: value; })
   - tokens-dark.css ([data-dsai-theme="dark"] { ... })
   - dsai-theme-bs.css (Bootstrap compiled with token overrides)
   ↓
6. Imported in main.tsx, components use CSS custom properties
```

## Figma Code Connect

Separate from tokens — maps Figma component instances to code.

### Setup

```bash
# Install Code Connect
npm install -D @figma/code-connect

# Initialize (creates figma.config.json)
pnpm figma:connect
```

### Creating a Code Connect Mapping

Code Connect files are colocated with their component. For example, `Button.figma.tsx` sits next to `Button.tsx`:

```tsx
// src/client/components/ui/button/Button.figma.tsx
import figma from '@figma/code-connect';
import { Button } from './Button';

figma.connect(Button, 'https://figma.com/design/FILE_KEY/..?node-id=NODE_ID', {
  props: {
    label: figma.string('Label'),
    variant: figma.enum('Variant', {
      Primary: 'primary',
      Secondary: 'secondary',
      Danger: 'danger',
      Ghost: 'ghost',
    }),
    size: figma.enum('Size', {
      Small: 'sm',
      Medium: 'md',
      Large: 'lg',
    }),
    disabled: figma.boolean('Disabled'),
    loading: figma.boolean('Loading'),
  },
  example: ({ label, variant, size, disabled, loading }) => (
    <Button variant={variant} size={size} disabled={disabled} loading={loading}>
      {label}
    </Button>
  ),
});
```

### Publishing Mappings

```bash
pnpm figma:publish          # Publish to Figma
pnpm figma:publish:dry      # Preview without publishing
```

After publishing, Figma's Dev Mode shows the DSAI React code snippet for each mapped component.

---

## Environment Variables

```env
FIGMA_API_KEY=""        # Figma personal access token (required for sync)
FIGMA_FILE_ID=""        # Figma file containing design tokens
FIGMA_PROJECT_ID=""     # Optional: specific Figma project
```

## Token Sync Scripts (in consumer project package.json)

```json
{
  "figma:sync": "dsai figma sync",
  "tokens:build": "dsai tokens build",
  "tokens:validate": "dsai tokens validate",
  "tokens:watch": "dsai tokens watch"
}
```

## Critical Rules

1. **NEVER** manually edit files in `src/generated/` — they are auto-generated by the pipeline.
2. Edit tokens in `src/collections/*.json`, then run `dsai tokens build`.
3. For Figma-sourced tokens, edit in Figma first, then `dsai figma sync` + `dsai tokens build`.
4. `FIGMA_API_KEY` should be in `.env` (never committed to git).
5. Rate limiter is automatic — no manual throttling needed.
6. Token edits in `collections/` follow DTCG format (`$value`, `$type`, `$description`).

---

## Troubleshooting

### "Unauthorized" or "Invalid token" on `dsai figma sync`

- Verify `FIGMA_API_KEY` is set in `.env` and the app has loaded it
- Check that the token has **File content: Read-only** and **Variables: Read** scopes
- Regenerate the token if it was revoked or expired

### Rate limit errors

The `RateLimiter` handles most cases automatically. If you still hit limits:

- Reduce the number of files being synced in parallel
- Wait a few minutes and retry — Figma rate limits reset over time
- Check the `X-RateLimit-Remaining` header in debug output

### Sync runs but no tokens appear

- Ensure the Figma file has **Variables** defined (not just Styles)
- Verify `FIGMA_FILE_ID` matches the file containing the variables
- Check `src/figma-exports/` for raw output — if empty, the API returned no variables

### `dsai tokens build` fails after sync

- Run `dsai tokens validate` to check for DTCG format errors
- Figma exports may need the `transform` step to convert to DTCG format — ensure the pipeline includes both `preprocess` and `transform` steps
