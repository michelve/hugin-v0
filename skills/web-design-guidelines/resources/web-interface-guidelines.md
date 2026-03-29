# Web Interface Guidelines

Review these files for compliance: $ARGUMENTS

Read files, check against rules below. Output concise but comprehensive—sacrifice grammar for brevity. High signal-to-noise.

> **Stack context:** React 19 · shadcn/ui (Radix primitives) · Tailwind CSS v4 (CSS-first, `@theme inline`) · Vite SPA (no RSC, no `"use client"`)

## Rules

### Accessibility (WCAG 2.2 AA)

- Icon-only buttons need `aria-label`
- Form controls need `<label>` (via `FieldLabel`) or `aria-label`
- Interactive elements need keyboard handlers (`onKeyDown`/`onKeyUp`) — unless using Radix primitives (they handle this)
- `<button>` for actions, `<a>`/`<Link>` for navigation (not `<div onClick>`)
- Images need `alt` (or `alt=""` if decorative)
- Decorative icons need `aria-hidden="true"`
- Async updates (toasts via `sonner`, validation) need `aria-live="polite"`
- Use semantic HTML (`<button>`, `<a>`, `<label>`, `<table>`) before ARIA
- Headings hierarchical `<h1>`–`<h6>`; include skip link for `#main-content`
- `scroll-margin-top` on heading anchors (Focus Not Obscured — SC 2.4.11 AA)
- Interactive targets ≥ 24×24 CSS px (`min-h-6 min-w-6`) — Target Size SC 2.5.8 AA
- Drag actions need single-pointer alternative — Dragging Movements SC 2.5.7 AA
- Auth flows: no cognitive puzzle required — Accessible Auth SC 3.3.8 AA
- `Dialog`/`Sheet`/`Drawer` always need a `Title` — use `className="sr-only"` if visually hidden

### Focus States

- Interactive elements need visible focus: `focus-visible:ring-[3px] focus-visible:ring-ring/50`
- Never `outline-none` / `outline: none` without `focus-visible:` replacement
- Use `focus-visible:` over `focus:` (avoid focus ring on click)
- Group focus with `focus-within:` for compound controls
- Focus Not Obscured: `focus-visible:scroll-mt-20` for content behind sticky headers

### shadcn/ui Components

- **Use existing shadcn components before custom markup.** Check registry first (`npx shadcn@latest search`)
- **Callouts → `Alert`**, not custom styled divs
- **Empty states → `Empty`**, not custom markup
- **Toast → `sonner`** (`toast()` function), not custom toast divs
- **Separators → `Separator`**, not `<hr>` or `border-t` divs
- **Loading → `Skeleton`**, not custom `animate-pulse` divs
- **Status labels → `Badge`**, not custom styled spans
- **Items always inside their Group:** `SelectItem` → `SelectGroup`, `CommandItem` → `CommandGroup`
- **`TabsTrigger` must be inside `TabsList`** — never render triggers directly in `Tabs`
- **`Avatar` always needs `AvatarFallback`** for when image fails to load
- **Button has no `isPending`/`isLoading`** — compose with `Spinner` + `data-icon` + `disabled`

### Forms (shadcn patterns)

- **Forms use `FieldGroup` + `Field`** — never raw `div` with `space-y-*` for form layout
- **`InputGroup` uses `InputGroupInput`/`InputGroupTextarea`** — never raw `Input`/`Textarea` inside
- **Buttons inside inputs use `InputGroup` + `InputGroupAddon`**
- **Option sets (2–7 choices) use `ToggleGroup`** — don't loop `Button` with manual active state
- **`FieldSet` + `FieldLegend`** for grouping related checkboxes/radios
- **Validation: `data-invalid` on `Field`, `aria-invalid` on the control**
- Inputs need `autocomplete` and meaningful `name`
- Use correct `type` (`email`, `tel`, `url`, `number`) and `inputmode`
- Never block paste (`onPaste` + `preventDefault`)
- Labels clickable (`htmlFor` or wrapping control)
- Disable spellcheck on emails, codes, usernames (`spellCheck={false}`)
- Submit button stays enabled until request starts; spinner during request
- Errors inline next to fields; focus first error on submit
- Placeholders end with `…` and show example pattern
- Warn before navigation with unsaved changes (`beforeunload` or router guard)

### Icons (shadcn patterns)

- **Icons in `Button` use `data-icon`** — `data-icon="inline-start"` or `data-icon="inline-end"`
- **No sizing classes on icons inside components** — components handle icon sizing via CSS, no `size-4` or `w-4 h-4`
- **Pass icons as objects, not string keys** — `icon={CheckIcon}`, not a string lookup
- Import from `lucide-react`

### Tailwind CSS v4

- **Semantic color tokens only:** `bg-background`, `bg-primary`, `text-foreground`, `text-muted-foreground` — never raw values like `bg-blue-500`
- **No manual `dark:` color overrides** — use semantic tokens that adapt automatically
- **`gap-*` not `space-x-*`/`space-y-*`** — use `flex` with `gap-*`; vertical stacks → `flex flex-col gap-*`
- **`size-*` when width = height** — `size-10` not `w-10 h-10`
- **`truncate` shorthand** — not `overflow-hidden text-ellipsis whitespace-nowrap`
- **`cn()` for conditional classes** — don't write manual template literal ternaries
- **`className` for layout, not styling** — never override component colors/typography
- **No manual `z-index` on overlay components** — Dialog, Sheet, Popover handle their own stacking
- **`motion-reduce:transition-none`** for `prefers-reduced-motion` — use Tailwind variant, not media query
- **`aria-invalid:border-destructive`** — style elements based on ARIA state via Tailwind variant
- CSS-first config: theme defined via `@theme inline` in `src/client/index.css`, no `tailwind.config.js`
- Colors use `oklch` values via CSS variables

### Animation

- Honor `prefers-reduced-motion` — use `motion-reduce:transition-none` Tailwind variant
- Animate `transform`/`opacity` only (compositor-friendly)
- Never `transition: all` or `transition-all`—list properties explicitly
- Set correct `transform-origin`
- SVG: transforms on `<g>` wrapper with `transform-box: fill-box; transform-origin: center`
- Animations interruptible—respond to user input mid-animation

### Typography

- `…` not `...`
- Curly quotes `"` `"` not straight `"`
- Non-breaking spaces: `10&nbsp;MB`, `⌘&nbsp;K`, brand names
- Loading states end with `…`: `"Loading…"`, `"Saving…"`
- `font-variant-numeric: tabular-nums` for number columns/comparisons
- Use `text-wrap: balance` or `text-pretty` on headings (prevents widows)

### Content Handling

- Text containers handle long content: `truncate`, `line-clamp-*`, or `break-words`
- Flex children need `min-w-0` to allow text truncation
- Handle empty states—don't render broken UI for empty strings/arrays
- User-generated content: anticipate short, average, and very long inputs

### Images

- `<img>` needs explicit `width` and `height` (prevents CLS)
- Below-fold images: `loading="lazy"`
- Above-fold critical images: `priority` or `fetchpriority="high"`

### Performance

- Large lists (>50 items): virtualize (`virtua`, `content-visibility: auto`)
- No layout reads in render (`getBoundingClientRect`, `offsetHeight`, `offsetWidth`, `scrollTop`)
- Batch DOM reads/writes; avoid interleaving
- Prefer uncontrolled inputs; controlled inputs must be cheap per keystroke
- Add `<link rel="preconnect">` for CDN/asset domains
- Critical fonts: `<link rel="preload" as="font">` with `font-display: swap`

### Navigation & State

- URL reflects state—filters, tabs, pagination, expanded panels in query params
- Links use `<a>`/`<Link>` (Cmd/Ctrl+click, middle-click support)
- Deep-link all stateful UI (if uses `useState`, consider URL sync via nuqs or similar)
- Destructive actions need confirmation modal or undo window—never immediate

### Touch & Interaction

- `touch-action: manipulation` (prevents double-tap zoom delay)
- `-webkit-tap-highlight-color` set intentionally
- `overscroll-behavior: contain` in modals/drawers/sheets
- During drag: disable text selection, `inert` on dragged elements
- `autoFocus` sparingly—desktop only, single primary input; avoid on mobile

### Safe Areas & Layout

- Full-bleed layouts need `env(safe-area-inset-*)` for notches
- Avoid unwanted scrollbars: `overflow-x-hidden` on containers, fix content overflow
- Flex/grid over JS measurement for layout

### Dark Mode & Theming

- `color-scheme: dark` on `<html>` for dark themes (fixes scrollbar, inputs)
- `<meta name="theme-color">` matches page background
- Native `<select>`: explicit `background-color` and `color` (Windows dark mode)
- Use class-based dark mode: `@custom-variant dark (&:is(.dark *))` — not `prefers-color-scheme`
- Colors via CSS variables using `oklch` values — never hardcode hex/rgb
- Use semantic tokens (`bg-background`, `text-foreground`) — they adapt to theme automatically

### Locale & i18n

- Dates/times: use `Intl.DateTimeFormat` not hardcoded formats
- Numbers/currency: use `Intl.NumberFormat` not hardcoded formats
- Detect language via `Accept-Language` / `navigator.languages`, not IP

### Hydration Safety

- Inputs with `value` need `onChange` (or use `defaultValue` for uncontrolled)
- Date/time rendering: guard against hydration mismatch (server vs client)
- `suppressHydrationWarning` only where truly needed

### Hover & Interactive States

- Buttons/links need `hover:` state (visual feedback)
- Interactive states increase contrast: hover/active/focus more prominent than rest

### Content & Copy

- Active voice: "Install the CLI" not "The CLI will be installed"
- Title Case for headings/buttons (Chicago style)
- Numerals for counts: "8 deployments" not "eight"
- Specific button labels: "Save API Key" not "Continue"
- Error messages include fix/next step, not just problem
- Second person; avoid first person
- `&` over "and" where space-constrained

### Anti-patterns (flag these)

- `user-scalable=no` or `maximum-scale=1` disabling zoom
- `onPaste` with `preventDefault`
- `transition: all` or `transition-all`
- `outline-none` without `focus-visible:` replacement
- Inline `onClick` navigation without `<a>`
- `<div>` or `<span>` with click handlers (should be `<button>`)
- Images without dimensions
- Large arrays `.map()` without virtualization
- Form inputs without labels
- Icon buttons without `aria-label`
- Hardcoded date/number formats (use `Intl.*`)
- `autoFocus` without clear justification
- `space-y-*` / `space-x-*` (use `gap-*` instead)
- `w-* h-*` when equal (use `size-*`)
- Raw color values (`bg-blue-500`, `text-red-600`) instead of semantic tokens
- Manual `dark:` overrides instead of semantic tokens
- Custom styled divs when a shadcn component exists (`Alert`, `Badge`, `Skeleton`, `Separator`)
- Raw `Input`/`Textarea` inside `InputGroup` (use `InputGroupInput`/`InputGroupTextarea`)
- `div` + `space-y-*` for form layout (use `FieldGroup` + `Field`)
- Sizing classes on icons inside shadcn components (`size-4`, `w-4 h-4`)
- Manual `z-index` on overlay components (Dialog, Sheet, Popover)
- `"use client"` directive (this is a Vite SPA, not RSC)
- `overflow-hidden text-ellipsis whitespace-nowrap` instead of `truncate`
- Template literal ternaries for class names instead of `cn()`
- Interactive targets < 24×24 CSS px (SC 2.5.8 AA)
- Dialog/Sheet/Drawer without a Title component

## Output Format

Group by file. Use `file:line` format (VS Code clickable). Terse findings.

```text
## src/Button.tsx

src/Button.tsx:42 - icon button missing aria-label
src/Button.tsx:18 - form field missing FieldLabel
src/Button.tsx:55 - animation missing motion-reduce: variant
src/Button.tsx:67 - transition-all → list properties explicitly

## src/Modal.tsx

src/Modal.tsx:12 - missing overscroll-behavior: contain
src/Modal.tsx:23 - Dialog missing DialogTitle (a11y)
src/Modal.tsx:34 - "..." → "…"

## src/Card.tsx

src/Card.tsx:8 - space-y-4 → flex flex-col gap-4
src/Card.tsx:15 - bg-blue-500 → use semantic token (bg-primary)
src/Card.tsx:22 - w-10 h-10 → size-10

## src/Form.tsx

✓ pass
```

State issue + location. Skip explanation unless fix non-obvious. No preamble.
