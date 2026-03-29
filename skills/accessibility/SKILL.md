---
name: accessibility
version: 1.0.0
description: "Use this skill for any accessibility concern: WCAG compliance (any success criterion including SC 1.3.5 autocomplete, SC 2.4.11 focus obscured), ARIA roles/attributes, screen reader behavior, axe-core or WAVE audit failures, color/non-text contrast, keyboard navigation, focus trapping/management, skip links, touch targets, VPAT reports, or accessible form patterns. Also trigger when a user asks whether a UI library (DSAI) handles keyboard interactions — but only if the question is specifically about accessibility behavior, not general usage. Do NOT trigger for general component usage questions where keyboard behavior is incidental (e.g., \"does DSAI Tooltip show on hover and focus?\" without an accessibility problem to solve)."
user-invocable: true
argument-hint: "Describe the accessibility problem, WCAG criterion (e.g. SC 1.3.5), component to audit, or topic (aria, keyboard nav, contrast, screen reader, VPAT)"
---

# Accessibility

> **Standard:** WCAG 2.2 AA required · AAA aspirational
> **Stack:** React 19 · DSAI Design System · Bootstrap 5 · CSS Custom Properties (--dsai-* tokens)
> **POUR Principles:** Perceivable · Operable · Understandable · Robust

Implement WCAG 2.2 AA compliant accessibility in React 19 components using the draft_v0 stack. Items marked **(AAA)** exceed the required AA level and are aspirational best practices to pursue where feasible.

---

## POUR Reference Map

| Principle | Key Topics | Reference Files |
|-----------|-----------|-----------------|
| **Perceivable** | Alt text, landmarks, headings, data tables, color contrast, non-text contrast, text spacing, reflow | [semantic-html.md](references/semantic-html.md), [mobile-touch.md](references/mobile-touch.md) |
| **Operable** | Keyboard, focus management, focus not obscured, skip links, page titles, target size, dragging, pointer gestures | [keyboard-navigation.md](references/keyboard-navigation.md), [focus-management.md](references/focus-management.md), [mobile-touch.md](references/mobile-touch.md), [wcag22-new-criteria.md](references/wcag22-new-criteria.md) |
| **Understandable** | ARIA, forms, error handling, auth, redundant entry, consistent help, live regions | [aria-attributes.md](references/aria-attributes.md), [forms-a11y.md](references/forms-a11y.md) |
| **Robust** | Screen reader support, status messages, automated + manual testing, VPAT, CI/CD | [testing-a11y.md](references/testing-a11y.md) |

---

## WCAG 2.2 New Criteria — Enterprise Baseline

WCAG 2.2 added 9 success criteria not present in WCAG 2.1. All **AA** items are **required**; **AAA** items are aspirational.

| SC | Title | Level | Requirement in One Line |
|----|-------|-------|-------------------------|
| 2.4.11 | Focus Not Obscured (Minimum) | **AA** | Focused element not fully hidden behind sticky/fixed UI chrome |
| 2.4.12 | Focus Not Obscured (Enhanced) | AAA | Focused element not obscured at all — not even partially |
| 2.4.13 | Focus Appearance | AAA | Focus indicator ≥ 2px perimeter, 3:1 contrast ratio |
| 2.5.7 | Dragging Movements | **AA** | Every drag action has a single-pointer (click/tap) alternative |
| 2.5.8 | Target Size (Minimum) | **AA** | Interactive targets ≥ 24×24 CSS pixels |
| 3.2.6 | Consistent Help | **A** | Help mechanisms in same relative position across pages |
| 3.3.7 | Redundant Entry | **A** | Previously entered data auto-populated or selectable |
| 3.3.8 | Accessible Authentication (Minimum) | **AA** | No cognitive puzzle required in auth unless alternative exists |
| 3.3.9 | Accessible Authentication (Enhanced) | AAA | No cognitive test in any auth step, no exceptions |

See [wcag22-new-criteria.md](references/wcag22-new-criteria.md) for detailed implementation guidance, code examples, common failures, and test procedures for each criterion.

---

## Accessibility Utilities in This Project

| Tool / Pattern | How to Use | Notes |
|----------------|-----------|-------|
| `useFocusTrap` | `import { useFocusTrap } from '@/hooks'` | DSAI hook for focus trapping in modals/dialogs. |
| `useRovingFocus` | `import { useRovingFocus } from '@/hooks'` | Arrow key navigation within tab lists, menus. |
| `useReducedMotion` | `import { useReducedMotion } from '@/hooks'` | Respects `prefers-reduced-motion` OS preference. |
| `visually-hidden` | `className="visually-hidden"` | Bootstrap class — visually hidden, screen-reader visible text. |
| `useKeyPress` | `import { useKeyPress } from '@/hooks'` | Keyboard event handling hook. |
| `useScrollLock` | `import { useScrollLock } from '@/hooks'` | Prevents body scroll when modal/sheet is open. |
| `SafeHTMLAttributes` | `import type { SafeHTMLAttributes } from '@/types'` | Whitelisted HTML attributes — blocks event handlers in spread. |
| `announceToScreenReader` | `import { announceToScreenReader } from '@/utils'` | DSAI utility for live region announcements. |
| Custom hooks | `src/client/hooks/` (`@/hooks`) | `useFocusTrap`, `useKeyPress`, `useReducedMotion`, `useRovingFocus`, `useScrollLock`, `useHover`. |

---

## DSAI Built-in Accessibility

**DSAI components implement accessibility patterns directly** — using SafeHTMLAttributes, ARIA props, keyboard hooks, and focus management. Components handle ARIA roles, keyboard navigation, and focus management through the DSAI hook system.

| Component | What DSAI Handles |
|-----------|-------------------|
| `Modal` | Focus trap (`useFocusTrap`), scroll lock (`useScrollLock`), `Escape` to close, return focus on close, `aria-modal` |
| `Dropdown` | `role="menu"` / `menuitem`, roving focus (`useRovingFocus`), Arrow keys, `Escape` to close |
| `Select` | `role="listbox"` / `option`, Arrow keys, type-ahead search |
| `Tabs` | `role="tablist"` / `tab` / `tabpanel`, Arrow Left/Right (`useRovingFocus`), activation modes |
| `Checkbox` | `role="checkbox"`, `Space` to toggle, `aria-checked` |
| `Tooltip` | `role="tooltip"`, hoverable, dismissible with `Escape`, persistent |
| `Popover` | Focus-managed popup, `Escape` to close, returns focus to trigger |
| `Accordion` | `aria-expanded`, Arrow keys for panel navigation |
| `Switch` | `role="switch"`, `aria-checked`, `Space`/`Enter` to toggle |
| `Button` | FSM-based states (loading, error, disabled), `announceText` for screen readers |

Install via: `dsai add modal tabs select` — components appear in `src/client/components/ui/` as local source code you own and can customize.

---

## Landmark Regions

Use native HTML5 elements — they carry implicit ARIA roles and need no `role` attribute.

| Landmark | Element | `aria-label` needed? | Notes |
|----------|---------|----------------------|-------|
| Banner | `<header>` | No | Top-level only; one per page |
| Navigation | `<nav>` | Yes (if multiple exist) | Label each distinctly |
| Main | `<main>` | No | One per page; add `id="main-content" tabIndex={-1}` |
| Complementary | `<aside>` | Yes | Describe the supporting content |
| Contentinfo | `<footer>` | No | Top-level only; one per page |
| Search | `<search>` | No | Preferred over `role="search"` |

**Rules:** one `<main>` per page · label every `<nav>` when multiple exist · never nest `<main>` inside another landmark · give `<main>` `id="main-content" tabIndex={-1}` for skip-link targeting.

See [semantic-html.md](references/semantic-html.md) for the full `AppLayout` implementation.

---

## Skip Links

Skip links bypass repeated navigation — required by WCAG 2.4.1 (Level A). Place `<SkipLink />` as the **first** element in `<App />`. It uses `visually-hidden` (shown on focus via CSS) so it appears only on keyboard Tab.

**Requirements:**

- First focusable element in DOM order
- Href target (`#main-content`) must have `tabIndex={-1}` to receive programmatic focus
- For multi-section pages add more: "Skip to search", "Skip to filters"

See [focus-management.md](references/focus-management.md) for the `SkipLink` component and `App.tsx` placement.

---

## Page Title Management

WCAG 2.4.2 (Level A): every page needs a unique, descriptive `document.title` that updates on route change.

- Call `useDocumentTitle(pageTitle)` in every route component. Format: `"Page Name — Site Name"`.
- Add `<RouteAnnouncer />` once in `<App />` — announces the new title to screen readers on navigation without moving focus.

See [focus-management.md](references/focus-management.md) for both implementations.

---

## Keyboard Navigation

See [keyboard-navigation.md](references/keyboard-navigation.md) for:
- Required keys by component type (button, link, menu, tabs, modal, combobox, tree, data grid, carousel, toolbar)
- `useKeyPress` hook
- Roving tabindex pattern
- Data grid two-dimensional navigation model (`Arrow` + `Home`/`End`/`Ctrl+Home`/`Ctrl+End`)
- Tree view expand/collapse key model
- Carousel `Previous`/`Next`/`Pause` patterns
- Pointer cancellation (WCAG 2.5.2 AA)

---

## ARIA Attributes

See [aria-attributes.md](references/aria-attributes.md) for:
- Button, input, checkbox, radio group, switch/toggle patterns
- Dialog/modal, alert, menu patterns
- Combobox (autocomplete input + listbox), data grid, tree view, carousel patterns
- Tooltip, breadcrumb, pagination, loading/spinner patterns
- Live region and status message patterns

---

## Focus Management

See [focus-management.md](references/focus-management.md) for:
- `useFocusTrap` (DSAI) — focus trapping for modals
- Return focus pattern — restore trigger element focus on close
- **Focus Not Obscured (WCAG 2.4.11 AA)** — `scroll-margin-top` fix for sticky headers
- Skip link focus target setup
- Focus management on SPA route change

---

## Screen Reader Announcements

### Live Regions in JSX

Place live region containers in your layout so they persist between renders — **the container must exist in the DOM before content is injected:**

```tsx
// Polite — screen reader finishes current speech before announcing
<div aria-live="polite" aria-atomic="true">
  {statusMessage}
</div>

// Assertive — interrupts screen reader immediately (use sparingly)
<div role="alert" aria-live="assertive">
  {errorMessage}
</div>

// Status updates (WCAG 4.1.3 A) — equivalent to aria-live="polite" + aria-atomic
<div role="status">
  {`${resultCount} results found`}
</div>
```

### Reusable Announcement Hook

For imperative announcements (filter applied, item saved, search complete) without moving focus, use the `useAnnounce` hook from `@/hooks/useAnnounce`.

See [aria-attributes.md](references/aria-attributes.md) for the implementation.

---

## Reduced Motion

See [reduced-motion.md](references/reduced-motion.md) for:
- `useReducedMotion` hook
- CSS `@media (prefers-reduced-motion: reduce)` (preferred approach)
- Framer Motion `useReducedMotion` integration
- CSS `@media (prefers-reduced-motion: reduce)` global overrides
- WCAG 2.3.3 Animation from Interactions (AAA)

---

## Color Contrast

### Minimum Ratios (WCAG 2.2 AA)

| Content | Required Ratio |
|---------|---------------|
| Normal text (< 18pt / < 14pt bold) | **4.5:1** |
| Large text (≥ 18pt or ≥ 14pt bold) | **3:1** |
| UI components & graphical objects (borders, icons, chart lines) | **3:1** (SC 1.4.11) |
| Inactive/disabled UI, pure decoration | No requirement |

> **(AAA)** Enhanced contrast (SC 1.4.6): Normal text 7:1 · Large text 4.5:1

### Compliant Combinations (Project Design System)

Use DSAI semantic color tokens — they map to CSS custom properties via the token pipeline:

| Pair | Token / Classes | Notes |
|------|----------------|-------|
| Body text | `text-body` / `bg-body` | Uses `var(--dsai-color-body)` — passes ✔ |
| Primary action | `bg-primary text-white` | Uses `var(--dsai-color-primary)` — passes ✔ |
| Danger / error | `bg-danger text-white` | Uses `var(--dsai-color-danger)` — passes ✔ |
| Secondary surface | `bg-secondary text-white` | Uses `var(--dsai-color-secondary)` — passes ✔ |
| Muted text | `text-body-secondary` | ⚠ Verify at your font size |

> Use [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/) or [APCA Calculator](https://apcacontrast.com/) to verify contrast for custom color combinations. DSAI tokens are pre-validated for AA compliance.

### Non-text Contrast (WCAG 1.4.11 AA)

Input borders, button outlines, checkbox frames, focus rings, and icon-only controls must have **3:1 contrast** against adjacent colors. Use DSAI tokens `var(--dsai-border-color)` / `var(--dsai-color-primary)` and verify in the contrast checker when customizing.

---

## Visible Focus

Use CSS `:focus-visible` pseudo-class (keyboard only — does not appear on mouse click). DSAI provides focus styles via CSS custom properties:

```css
:focus-visible {
  outline: 3px solid var(--dsai-color-primary);
  outline-offset: 2px;
}
```

Add `scroll-margin-top` to prevent the focused element hiding behind a sticky header (WCAG 2.4.11 AA).

- Never use `:focus` alone for ring styles — it triggers on mouse too
- Use DSAI token `var(--dsai-color-primary)` for focus ring color (consistent across themes)
- **(AAA) 2.4.13** — focus indicator must encircle with ≥ 2px perimeter and ≥ 3:1 contrast between focused/unfocused states

See [focus-management.md](references/focus-management.md) for the sticky-header fix.

---

## Screen Reader Only Text

```tsx
// Icon-only button — always provide visually-hidden label
<button aria-label="Close modal">
  <XIcon aria-hidden="true" />
</button>

// Or use visually-hidden span (Bootstrap class, either approach is valid)
<button>
  <XIcon aria-hidden="true" />
  <span className="visually-hidden">Close modal</span>
</button>
```

---

## Forms & Input

See [forms-a11y.md](references/forms-a11y.md) for:
- `autocomplete` attributes and WCAG 1.3.5 Identify Input Purpose (AA)
- Redundant Entry — WCAG 3.3.7 (A): auto-populate previously entered data in multi-step flows
- Accessible Authentication — WCAG 3.3.8 (AA) / 3.3.9 (AAA): no cognitive tests in auth flows; password manager and paste must work
- `fieldset`/`legend` for grouped inputs (radio groups, checkboxes, date parts)
- Multi-step form state management and progress communication
- Comprehensive error identification, description, and suggestion patterns

---

## Semantic HTML

See [semantic-html.md](references/semantic-html.md) for:
- `img` alt text decision tree (informative vs decorative vs functional)
- Decorative images: `alt=""` + `aria-hidden="true"`
- SVG accessibility: `role="img"`, `<title>`, `<desc>`, `aria-labelledby`
- Landmark regions in depth (header, nav, main, aside, footer)
- Heading hierarchy rules (h1–h6, one h1 per page, no skipping levels)
- Data tables: `<caption>`, `scope`, `headers` attribute for complex tables
- Ordered vs. unordered lists — when to use each

---

## Mobile & Touch

See [mobile-touch.md](references/mobile-touch.md) for:
- **Target Size (AA):** 24×24 CSS px minimum — WCAG 2.5.8
- **Target Size (AAA):** 44×44 CSS px recommended — WCAG 2.5.5
- **Pointer Gestures (AA):** multi-touch gesture alternatives — WCAG 2.5.1
- **Pointer Cancellation (AA):** activate on `pointerup`, not `pointerdown` — WCAG 2.5.2
- **Orientation (AA):** support portrait and landscape — WCAG 1.3.4
- **Motion Actuation (AA):** device-motion (shake/tilt) alternatives — WCAG 2.5.4
- **Dragging Movements (AA):** single-pointer alternative for all drag UIs — WCAG 2.5.7
- **Content on Hover/Focus (AA):** tooltips/popovers must be dismissible, hoverable, persistent — WCAG 1.4.13
- **Reflow (AA):** no horizontal scrolling at 320px CSS width — WCAG 1.4.10
- **Text Spacing (AA):** layout survives user text-spacing overrides — WCAG 1.4.12

---

## Testing Accessibility

See [testing-a11y.md](references/testing-a11y.md) for:
- Browser DevTools accessibility tree inspection (zero setup)
- Playwright + `@axe-core/playwright` automated audits (recommended for CI)
- Vitest + `vitest-axe` component-level unit tests
- **Screen reader test matrix** — NVDA · JAWS · VoiceOver · TalkBack · Narrator with browser pairings
- **CI/CD GitHub Actions** — automated axe scan on every PR
- **VPAT / accessibility statement** guidance for enterprise reporting
- Manual test checklist organized by POUR principle

---

## WCAG 2.2 AA Compliance Checklist

Use this checklist for every new component or page before merge. Each item maps to a WCAG 2.2 success criterion.

### Perceivable

- [ ] **1.1.1 A** — Every `<img>` has meaningful `alt`; decorative images use `alt=""` and `aria-hidden="true"`
- [ ] **1.3.1 A** — Semantic HTML used for structure (headings, lists, tables); data relationships programmatically defined
- [ ] **1.3.2 A** — DOM reading order matches visual presentation order
- [ ] **1.3.3 A** — Instructions don't rely solely on shape, color, size, or spatial position
- [ ] **1.3.4 AA** — Content works in both portrait and landscape orientation
- [ ] **1.3.5 AA** — User data input fields have correct `autocomplete` attribute values
- [ ] **1.4.1 A** — Color is not the only means of conveying information, indicating an action, or distinguishing an element
- [ ] **1.4.3 AA** — Text and images of text meet 4.5:1 contrast ratio (3:1 for large text)
- [ ] **1.4.4 AA** — Text resizes to 200% without loss of content or functionality
- [ ] **1.4.5 AA** — Images of text not used where styled text could achieve the same visual effect (except logos)
- [ ] **1.4.10 AA** — Content reflows at 320px CSS width without requiring horizontal scrolling
- [ ] **1.4.11 AA** — UI component boundaries (input borders, button outlines, focus indicators) meet 3:1 non-text contrast
- [ ] **1.4.12 AA** — Layout and content survive user text-spacing overrides (line-height 1.5×, letter-spacing 0.12em, word-spacing 0.16em)
- [ ] **1.4.13 AA** — Hover/focus-triggered popovers and tooltips are dismissible (Escape), hoverable (pointer can move over them), and persistent until explicitly dismissed

### Operable

- [ ] **2.1.1 A** — All functionality is operable by keyboard; no functionality requires specific timing or a path-dependent gesture
- [ ] **2.1.2 A** — No keyboard trap — user can always Tab away from any focused component
- [ ] **2.4.1 A** — A skip link is provided to bypass repeated navigation blocks
- [ ] **2.4.2 A** — Every page/view has a unique, descriptive `document.title` that updates on route change
- [ ] **2.4.3 A** — Focus order follows a logical sequence that matches reading order
- [ ] **2.4.4 A** — Link text (or link + context) describes the link's purpose clearly
- [ ] **2.4.6 AA** — Headings and labels describe their topic or purpose
- [ ] **2.4.7 AA** — A visible keyboard focus indicator is present on all keyboard-operable elements
- [ ] **2.4.11 AA** — When a component receives focus, it is not entirely hidden behind sticky/fixed UI (cookie banners, sticky headers, toolbars)
- [ ] **2.5.1 AA** — Multi-touch gestures (pinch, swipe) have a single-pointer alternative (tap, button)
- [ ] **2.5.2 AA** — Click/tap functionality activates on pointer-up, not pointer-down; or up-event abort is available
- [ ] **2.5.3 AA** — The accessible name of interactive elements contains the visible label text
- [ ] **2.5.7 AA** — Drag interactions have a single-pointer (click/tap) alternative mechanism
- [ ] **2.5.8 AA** — Interactive targets are at least 24×24 CSS pixels (with spacing exceptions for inline text)

### Understandable

- [ ] **3.1.1 A** — Page language declared: `<html lang="en">` (or appropriate BCP-47 language code)
- [ ] **3.2.1 A** — Receiving focus does not trigger unexpected context changes (form submit, page navigation)
- [ ] **3.2.2 A** — Changing an input setting does not auto-submit or change context without prior user notice
- [ ] **3.2.3 AA** — Navigation components (nav bars, breadcrumbs, sidebars) are consistent across pages
- [ ] **3.2.4 AA** — Components with the same function are labeled consistently across the site
- [ ] **3.2.6 A** — Help mechanisms (contact link, chat, FAQ) appear in the same relative position across pages
- [ ] **3.3.1 A** — Errors are automatically detected, the erroneous item identified, and the error described in text
- [ ] **3.3.2 A** — Labels or instructions are provided for all form inputs before or alongside them
- [ ] **3.3.3 AA** — Error correction suggestions are provided when an input error is detected and suggestions are known
- [ ] **3.3.4 AA** — Legal, financial, or data-destructive submissions are reversible, checkable, or confirmable
- [ ] **3.3.7 A** — Previously entered information is auto-populated or selectable in the same process/session
- [ ] **3.3.8 AA** — Authentication does not require solving a puzzle, transcribing characters, or memorization unless a supported alternative or assistance mechanism exists (paste and password managers must work)

### Robust

- [ ] **4.1.2 A** — Every UI component has a programmatically determinable name, role, and value; states and properties are settable; changes are notified to assistive technologies
- [ ] **4.1.3 A** — Status messages (save confirmations, error counts, progress updates, loading complete) are conveyed to screen readers via live regions or `role="status"` without moving focus

---

## AAA Aspirational

These exceed the required AA level. Implement where feasible to provide a superior experience.

| SC | Title | Implementation Guidance |
|----|-------|------------------------|
| **1.4.6** | Contrast Enhanced | Normal text 7:1 · Large text 4.5:1 |
| **2.3.3** | Animation from Interactions | Motion triggered by interaction can be disabled by the user — see [reduced-motion.md](references/reduced-motion.md) |
| **2.4.12** | Focus Not Obscured (Enhanced) | Focused element not obscured at all — increase `scroll-margin-top` to fully clear sticky UI |
| **2.4.13** | Focus Appearance | Focus indicator ≥ 2px perimeter, 3:1 contrast between focused and unfocused states |
| **2.5.5** | Target Size Enhanced | Interactive targets ≥ 44×44 CSS pixels — use `min-h-[44px] min-w-[44px]` |
| **2.5.6** | Concurrent Input Mechanisms | Do not restrict the user to a single input modality (e.g., do not disable mouse when touch is detected) |
| **3.1.5** | Reading Level | If content exceeds lower secondary school reading level, provide supplemental simpler version |
| **3.3.9** | Accessible Auth Enhanced | No cognitive function test (including CAPTCHA with alternatives) in any auth step |

---

## Platform Notes

| Platform | Metadata | Shell commands | Packaging |
|----------|----------|----------------|-----------|
| **Claude Code** | YAML frontmatter in `SKILL.md` | ✅ Full `!`command`` support | n/a |
| **Cowork** | `skills-rules.json` (see `skills-rules.json` in this skill) | ✅ | `.skill` file via `python -m scripts.package_skill skills/accessibility`; use `present_files` to deliver packaged results |
| **Claude.ai** | Paste `SKILL.md` body into Project instructions; attach reference files as knowledge | ❌ No shell commands | n/a |

See [skill-creator/reference/platform-specific.md](../skill-creator/reference/platform-specific.md) for the full platform compatibility guide.

---

## Resources

| Resource | URL |
|----------|-----|
| WCAG 2.2 Specification | https://www.w3.org/TR/WCAG22/ |
| WCAG 2.2 Quick Reference | https://www.w3.org/WAI/WCAG22/quickref/ |
| Understanding WCAG 2.2 | https://www.w3.org/WAI/WCAG22/Understanding/ |
| What's New in WCAG 2.2 | https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/ |
| ARIA Authoring Practices Guide (APG) | https://www.w3.org/WAI/ARIA/apg/ |
| WebAIM Contrast Checker | https://webaim.org/resources/contrastchecker/ |
| APCA Contrast Calculator | https://apcacontrast.com/ |
| axe DevTools Browser Extension | https://www.deque.com/axe/browser-extensions/ |
| WAVE Evaluation Tool | https://wave.webaim.org/ |
| NVDA Screen Reader (free, Windows) | https://www.nvaccess.org/ |
| Deque University — free courses | https://dequeuniversity.com/ |
| Inclusive Components — patterns | https://inclusive-components.design/ |
