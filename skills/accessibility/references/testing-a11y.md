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
