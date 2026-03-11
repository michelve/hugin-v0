---
name: accessibility
description: Implements WCAG 2.1 AA accessibility for draft_v0 components. Use when ensuring keyboard navigation, screen reader support, focus management, ARIA attributes, or color contrast compliance in React 19 components built with shadcn/ui and Tailwind CSS v4.
user-invocable: true
---

# Accessibility

Implement WCAG 2.1 AA compliant accessibility in React 19 components using the draft_v0 stack (shadcn/ui, Tailwind CSS v4, `radix-ui` flat package).

## When to Use

- Building interactive components
- Implementing keyboard navigation
- Adding ARIA attributes
- Managing focus states
- Ensuring color contrast compliance
- Supporting screen readers

## Accessibility Utilities in This Project

| Tool / Pattern   | How to Use                                                              | Notes                                                                   |
| ---------------- | ----------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| `FocusScope`     | `import { FocusScope } from 'radix-ui'`                                 | Focus trapping for modals/dialogs. `radix-ui` v1.4.3 already installed. |
| `sr-only`        | Tailwind built-in class: `className="sr-only"`                          | Visually hidden, screen-reader visible text.                            |
| `focus-visible:` | Tailwind variant: `focus-visible:ring-[3px] focus-visible:ring-ring/50` | Focus ring on keyboard interaction only.                                |
| `motion-reduce:` | Tailwind variant: `motion-reduce:transition-none`                       | Respects user's reduced-motion preference.                              |
| `aria-*:`        | Tailwind variant: `aria-invalid:border-destructive`                     | Style elements based on ARIA state.                                     |
| Custom hooks     | `src/client/hooks/` (`@/hooks`)                                         | Project-specific hooks (e.g., `useKeyPress`, `useReducedMotion`).       |

## shadcn/Radix Built-in Accessibility

**shadcn/ui components are accessible by default** - they are built on Radix UI primitives that handle ARIA roles, keyboard navigation, and focus management automatically. Do not re-implement what these components already provide:

| Component      | What Radix handles                                                                                 |
| -------------- | -------------------------------------------------------------------------------------------------- |
| `Dialog`       | `role="dialog"`, `aria-modal`, focus trap (`FocusScope`), `Escape` to close, return focus on close |
| `DropdownMenu` | `role="menu"` / `menuitem`, roving tabindex, `Arrow` keys, `Escape` to close                       |
| `Select`       | `role="listbox"` / `option`, `Arrow` keys, type-ahead search                                       |
| `Tabs`         | `role="tablist"` / `tab` / `tabpanel`, `Arrow Left/Right` navigation                               |
| `Checkbox`     | `role="checkbox"`, `Space` to toggle, `aria-checked`                                               |
| `AlertDialog`  | `role="alertdialog"`, focus trap, prevents accidental close                                        |

Install via: `npx shadcn@latest add dialog dropdown-menu select tabs` - components appear in `src/client/components/ui/` and must never be modified directly.

## Keyboard Navigation

See [keyboard-navigation.md](reference/keyboard-navigation.md) for required keys by component type, useKeyPress hook, and inline arrow key navigation patterns.

---

## ARIA Attributes

See [aria-attributes.md](reference/aria-attributes.md) for interactive elements, form elements, and live region ARIA patterns.

---

## Focus Management

See [focus-management.md](reference/focus-management.md) for FocusScope (Radix UI), focus trapping, and return focus patterns.

---

## Screen Reader Announcements

### Live Regions in JSX

Place live region containers in your layout so they persist between renders:

```tsx
// Polite announcements - screen reader finishes current sentence first
<div aria-live="polite" aria-atomic="true">
  {statusMessage}
</div>

// Urgent announcements - interrupts screen reader immediately
<div role="alert" aria-live="assertive">
  {errorMessage}
</div>
```

> **Key rule:** The live region element must exist in the DOM _before_ the message
> is injected. Mounting and populating it at the same time often silences it.

---

## Reduced Motion

See [reduced-motion.md](reference/reduced-motion.md) for useReducedMotion hook, Tailwind motion-reduce variant, and CSS alternatives.

---

## Color Contrast

### Minimum Ratios (WCAG AA)

| Content            | Ratio |
| ------------------ | ----- |
| Normal text        | 4.5:1 |
| Large text (18pt+) | 3:1   |
| UI components      | 3:1   |

### Compliant Combinations (Project Design System)

Use Tailwind semantic class pairs that map to the oklch tokens in `src/client/index.css`:

```tsx
// Body text on page background (−16:1 contrast) ✔
<p className="text-foreground bg-background">...</p>

// Primary action buttons (verified against --primary oklch(0.205 0 0)) ✔
<Button className="bg-primary text-primary-foreground">Action</Button>

// Destructive / error state ✔
<span className="bg-destructive text-destructive-foreground">Error</span>

// Secondary / muted surfaces ✔
<div className="bg-secondary text-secondary-foreground">...</div>

// Avoid - muted-foreground on white is borderline and fails for small text
<span className="text-muted-foreground">Caption</span> {/* verify at your font size */}
```

> Use the [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/) to
> verify oklch values from `src/client/index.css` when adding new color combinations.

## Visible Focus

This project uses Tailwind's `focus-visible:` variant. The pattern is already established
in `src/client/components/ui/button.tsx` - follow it:

```tsx
// ✔ Correct - Tailwind focus-visible utilities (matches project button pattern)
<button className="focus-visible:border-ring focus-visible:ring-ring/50 focus-visible:ring-[3px]">
    Click me
</button>;

// For custom interactive elements, add focus-visible: classes via cn()
import { cn } from "@/lib/utils";

<div
    role="button"
    tabIndex={0}
    className={cn(
        "rounded-md px-4 py-2",
        "focus-visible:ring-ring/50 focus-visible:ring-[3px] focus-visible:outline-none",
    )}
/>;
```

> Never use `focus:` alone for ring styles - `focus-visible:` only shows the ring
> on keyboard interaction, not on mouse click (better UX).
> Never override with raw CSS - always use Tailwind utilities so the `--ring` token
> from the design system applies consistently.

## Screen Reader Only Text

Tailwind provides a built-in `sr-only` utility - no custom CSS required:

```tsx
<button>
  <Icon name="close" />
  <span className="sr-only">Close modal</span>
</button>

// To reverse sr-only (make visible again):
<span className="not-sr-only">Visible text</span>
```

The `sr-only` class hides content visually while keeping it accessible to screen readers.
Use it for icon-only buttons, decorative separators with labels, and skip links.

---

## Testing Accessibility

See [testing-a11y.md](reference/testing-a11y.md) for browser DevTools, Playwright + axe-core, and Vitest + vitest-axe testing approaches.

---

## Checklist

- [ ] All interactive elements keyboard accessible
- [ ] Focus visible on all focusable elements
- [ ] ARIA roles and attributes correct
- [ ] Color contrast meets 4.5:1 for text
- [ ] Form inputs have associated labels
- [ ] Error messages announced to screen readers
- [ ] Modal traps focus and returns on close
- [ ] No content relies on color alone
