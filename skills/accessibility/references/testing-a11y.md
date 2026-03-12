# Testing Accessibility

## Browser DevTools (zero setup)

- **Chrome DevTools** → Elements panel → Accessibility tab: inspect the a11y tree, roles, and properties for any element
- **axe DevTools** browser extension (free tier): full page audit with issue explanations
- **WAVE** browser extension: visual overlay of a11y issues

## Playwright + @axe-core/playwright (e2e - recommended)

Playwright is already configured in this project. Add `@axe-core/playwright` as an optional dev dependency for automated audits:

```bash
npm install -D @axe-core/playwright
```

```ts
// e2e/a11y.spec.ts
import { test, expect } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";

test("home page has no accessibility violations", async ({ page }) => {
    await page.goto("/");
    const results = await new AxeBuilder({ page }).analyze();
    expect(results.violations).toEqual([]);
});

// Scope to a specific component
test("modal is accessible", async ({ page }) => {
    await page.goto("/");
    await page.getByRole("button", { name: "Open" }).click();
    const results = await new AxeBuilder({ page }).include('[role="dialog"]').analyze();
    expect(results.violations).toEqual([]);
});
```

## Vitest + vitest-axe (unit tests - optional)

For component-level a11y checks, install `vitest-axe` if needed:

```bash
npm install -D vitest-axe
```

```ts
import { test, expect } from 'vitest';
import { render } from '@testing-library/react';
import { axe } from 'vitest-axe';

test('component has no accessibility violations', async () => {
  const { container } = render(<MyComponent />);
  expect(await axe(container)).toHaveNoViolations();
});
```

---

## Screen Reader Quick Reference

For the full 5-browser × 10-scenario test matrix, see
[`enterprise-audit.md`](./enterprise-audit.md#screen-reader-test-matrix).

### Essential Shortcuts

| Screen Reader | OS | Navigation keys |
| ------------- | -- | --------------- |
| **NVDA** | Windows | `Insert+F7` element list · `H` headings · `D` landmarks · `B` buttons · `F` form fields · `T` tables |
| **JAWS** | Windows | `Insert+F6` headings list · `Insert+F3` links list · `R` rows in table · `F` forms mode |
| **VoiceOver** | macOS/iOS | `VO+U` rotor · `VO+Cmd+H` heading · `VO+Cmd+L` links · `VO+Space` activate |
| **TalkBack** | Android | Swipe left/right navigate · Double-tap activate · Swipe up then right for Reading Controls |
| **Narrator** | Windows | `Caps+F6` headings · `Caps+F7` links · `Caps+Enter` activate · `Caps+Space` action |

### Priority Test Scenarios

For each screen reader, verify at minimum:

1. Skip link works and moves focus to `#main-content`
2. Page title announced on load/route change
3. All images have meaningful alternative text
4. Form fields announced with label + error
5. Dialogs trap focus and announce `role="dialog"` + accessible name
6. Live regions (role="status" / role="alert") announced without focus move
7. Custom widgets (combobox, tree, carousel) follow APG key model

---

## CI/CD Automated Accessibility Checks

For the complete GitHub Actions YAML with multi-page testing, see
[`enterprise-audit.md`](./enterprise-audit.md#automated-cicd--github-actions).

**Minimal single-file snippet:**

```yaml
# .github/workflows/accessibility.yml
name: Accessibility
on: [push, pull_request]

jobs:
  axe:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: npm
      - run: npm ci
      - run: npx playwright install --with-deps chromium
      - run: npm run build
      - run: npx serve dist &
      - run: npx playwright test e2e/a11y.spec.ts
```

**Tag axe tests so they run independently:**

```ts
test("home page passes axe audit @a11y", async ({ page }) => { … });
```

```bash
# Run only a11y tests locally
npx playwright test --grep @a11y
```

---

## Axe Rule Customization

Disable specific rules only when you have a documented justification:

```ts
const results = await new AxeBuilder({ page })
  .withRules(["color-contrast", "keyboard-navigation"]) // test only these
  .analyze();

// OR disable a rule with documented reason
const results = await new AxeBuilder({ page })
  .disableRules(["color-contrast"]) // ⚠️ document why in a comment
  .analyze();
```

**Useful axe rule tags:**

| Tag | Covers |
| --- | ------- |
| `wcag2a` | WCAG 2.1 Level A |
| `wcag2aa` | WCAG 2.1 Level AA |
| `wcag22aa` | WCAG 2.2 Level AA (new criteria) |
| `best-practice` | Non-normative best practices |
| `experimental` | Rules under development |

```ts
// Test only WCAG 2.2 AA rules
const results = await new AxeBuilder({ page })
  .withTags(["wcag2a", "wcag2aa", "wcag22aa"])
  .analyze();
```

---

## Manual Testing Checklist (Abbreviated)

For the full POUR-organized checklist with ~30 checkboxes, see
[`enterprise-audit.md`](./enterprise-audit.md#manual-test-checklist-pour-framework).

**Quick smoke test (5 minutes per page):**

- [ ] Tab through the page — no keyboard traps, logical order
- [ ] All interactive elements reachable by keyboard and have visible focus
- [ ] Skip link present and functional
- [ ] No content only distinguishable by color
- [ ] All images have alt text (inspect with DevTools or WAVE)
- [ ] Zoom to 400% at 1280px — no horizontal scroll, no content loss
- [ ] Test with screen reader: announce headings, form labels, errors

---

## Audit Cadence

For a full schedule with owners and tooling, see
[`enterprise-audit.md`](./enterprise-audit.md#audit-cadence).

| Frequency | Activity |
| --------- | -------- |
| Every PR | Axe CI check (automated) |
| Weekly | Dev self-test with keyboard + WAVE |
| Monthly | Screen reader test (NVDA + VoiceOver) |
| Quarterly | Full POUR manual audit + VPAT update |

---

## VPAT & Accessibility Statement

A Voluntary Product Accessibility Template (VPAT) documents how a product
conforms to accessibility standards. Required for enterprise customers and
government procurement.

See [`enterprise-audit.md`](./enterprise-audit.md#vpat-voluntary-product-accessibility-template)
for the full template, conformance levels, and section structure.

**Quick facts:**

- Use **VPAT 2.5 WCAG Edition** for web products
- Conformance levels: Supports / Partially Supports / Does Not Support / Not Applicable
- Update the VPAT after each major release or quarterly audit
- Public accessibility statement required for WCAG self-declaration

---

## Testing Pyramid

```text
         /‾‾‾‾‾‾‾‾‾‾‾‾‾‾\
        /  Manual + SR    \   ← Quarterly full audit + VPAT
       /‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾\
      /  e2e axe (Playwright) \  ← Every PR via CI
     /‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾\
    /  Unit vitest-axe (Vitest)  \  ← During development
   /________________________________\
  /  Static: TypeScript + ESLint a11y \  ← Continuous (editor)
 /______________________________________\
```

Install `eslint-plugin-jsx-a11y` for continuous static analysis in the editor:

```bash
npm install -D eslint-plugin-jsx-a11y
```

```js
// eslint.config.js
import jsxA11y from "eslint-plugin-jsx-a11y";

export default [
  jsxA11y.flatConfigs.recommended,
  // … rest of your config
];
```
