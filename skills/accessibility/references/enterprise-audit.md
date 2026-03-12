# Enterprise Accessibility Audit — Reference

This reference provides enterprise-level tooling, processes, and delivery artefacts for maintaining WCAG 2.2 AA compliance at scale.

## Contents

- [Screen Reader Test Matrix](#screen-reader-test-matrix)
- [Manual Test Checklist (POUR Framework)](#manual-test-checklist-pour-framework)
- [Automated CI/CD — GitHub Actions](#automated-cicd--github-actions)
- [Tools Reference](#tools-reference)
- [VPAT (Voluntary Product Accessibility Template)](#vpat-voluntary-product-accessibility-template)
- [Accessibility Statement](#accessibility-statement)
- [Audit Cadence](#audit-cadence)
- [Escalation & Remediation Process](#escalation--remediation-process)
- [Accessibility Champions Program](#accessibility-champions-program)

---

## Screen Reader Test Matrix

Test all new features across this 5 × browser matrix **before every release**. Assign pairs to team members for dedicated SR testing.

| Screen Reader | OS | Primary Browser | Secondary Browser | Notes |
|--------------|----|-----------------|--------------------|-------|
| **NVDA** (free) | Windows | Chrome (latest) | Firefox (latest) | Most common SR for web testing |
| **JAWS** (licensed) | Windows | Chrome (latest) | Edge (latest) | Dominant in enterprise / government |
| **VoiceOver** | macOS / iOS | Safari (latest) | — | Required for Apple ecosystem |
| **TalkBack** | Android | Chrome (latest) | — | Google's Android SR |
| **Narrator** | Windows | Edge (latest) | — | Windows built-in, growing usage |

### Test Scenarios per SR × Browser Pair

For each scenario, navigate using **only the screen reader** (no mouse):

| # | Scenario | Pass Criteria |
|---|----------|--------------|
| 1 | **Page load & navigation** | Correct page title announced; landmark nav available via SR shortcuts; skip link works |
| 2 | **Heading navigation** | All headings announced with correct level; no skipped levels; page hierarchy clear |
| 3 | **Interactive elements** | All buttons/links have accessible names; disabled state announced; icon-only elements labelled |
| 4 | **Form completion** | Every input associated with a label; errors announced on submit; required fields identified |
| 5 | **Modal/dialog** | Focus trapped on open; modal role announced; close button works; focus returned on close |
| 6 | **Dynamic content updates** | Live regions announce status messages; loading states communicated; results count announced |
| 7 | **Images** | Informative images have useful alt text; decorative images ignored; SVG charts have descriptions |
| 8 | **Data tables** | Column and row headers announced; cell context clear; table caption read |
| 9 | **Keyboard traps** | No component traps keyboard; Tab always navigates out except modal (by design) |
| 10 | **WCAG 2.2 new criteria** | Focused elements not obscured; target size adequate; CAPTCHA/auth alternative confirmed |

---

## Manual Test Checklist (POUR Framework)

Run this checklist alongside automated tools — automated tools catch ~30–40% of WCAG issues.

### Perceivable

- [ ] All non-text content has text alternatives (images, icons, charts, audio, video)
- [ ] Decorative images use `alt=""` and `aria-hidden="true"` consistently
- [ ] Data tables have `<caption>` and `scope` on headers
- [ ] Color is not the only means of conveying information (errors, status badges, required fields)
- [ ] Normal body text passes 4.5:1 contrast; large text passes 3:1
- [ ] UI component borders and icons pass 3:1 non-text contrast
- [ ] Page reflows to a single column at 320px CSS width (or 400% zoom)
- [ ] Content survives text-spacing bookmarklet overrides (line-height, letter-spacing, word-spacing)
- [ ] Hover/focus-triggered overlays are dismissible (Escape), hoverable, and persistent (1.4.13)

### Operable

- [ ] All functionality is operable by keyboard alone
- [ ] No keyboard traps (except intentional focus-trapped modals)
- [ ] Skip link is the first focusable element, and works correctly
- [ ] Every page has a unique, descriptive `document.title`
- [ ] Focus order follows the logical reading sequence
- [ ] All interactive elements have a visible focus indicator
- [ ] Focused elements are not covered by sticky headers/footers (2.4.11)
- [ ] All interactive targets are ≥ 24×24 CSS pixels (2.5.8)
- [ ] All dragging interactions have a single-pointer button alternative (2.5.7)
- [ ] Multi-touch gestures have single-pointer alternatives (2.5.1)
- [ ] No functionality activates exclusively on pointer-down (2.5.2)

### Understandable

- [ ] `<html lang="en">` (or correct language) declared
- [ ] All form inputs have visible, programmatically associated labels
- [ ] Errors are identified, described in text, and include correction suggestions where possible
- [ ] Autocomplete attributes present on personal data inputs (1.3.5)
- [ ] Help mechanisms (contact, FAQ, chat) appear in the same position on all pages (3.2.6)
- [ ] Previously entered data is auto-populated in multi-step forms (3.3.7)
- [ ] Authentication allows paste, password manager injection, and offers a cognitive-test-free alternative (3.3.8)

### Robust

- [ ] All interactive components have programmatic name, role, and value
- [ ] States (expanded, selected, pressed, invalid) are communicated via ARIA
- [ ] Status messages use `role="status"` or `aria-live` regions
- [ ] Automated axe audit passes with zero violations on all pages

---

## Automated CI/CD — GitHub Actions

Integrate axe-core Playwright scans into every pull request. Fails the PR if any violations are found.

```yaml
# .github/workflows/accessibility.yml
name: Accessibility Audit

on:
  pull_request:
    branches: [main, develop]
  push:
    branches: [main]

jobs:
  a11y:
    name: WCAG accessibility scan
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: npm

      - name: Install dependencies
        run: npm ci

      - name: Install Playwright browsers
        run: npx playwright install --with-deps chromium

      - name: Build application
        run: npm run build

      - name: Start server
        run: npm run preview &
        env:
          PORT: 4173

      - name: Wait for server
        run: npx wait-on http://localhost:4173 --timeout 30000

      - name: Run accessibility tests
        run: npx playwright test --project=accessibility
        # Fails CI if any axe violations found

      - name: Upload test results
        if: failure()
        uses: actions/upload-artifact@v4
        with:
          name: a11y-test-results
          path: test-results/
          retention-days: 7
```

### Playwright accessibility test file

```typescript
// tests/a11y/pages.spec.ts
import { test, expect } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";

const pages = [
  { name: "Home", path: "/" },
  { name: "Products", path: "/products" },
  { name: "Product detail", path: "/products/1" },
  { name: "Cart", path: "/cart" },
  { name: "Login", path: "/login" },
  { name: "Register", path: "/register" },
  { name: "Checkout", path: "/checkout" },
  { name: "Profile", path: "/profile" },
];

for (const page of pages) {
  test(`${page.name} has no axe violations`, async ({ page: browserPage }) => {
    await browserPage.goto(page.path);

    const results = await new AxeBuilder({ page: browserPage })
      // Target WCAG 2.2 AA rules
      .withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa"])
      // Disable rules that require manual review (color-contrast can have false positives)
      .disableRules(["color-contrast"])
      .analyze();

    // Log violations to help debugging
    if (results.violations.length > 0) {
      console.log("Violations found:");
      results.violations.forEach((v) => {
        console.log(`\n[${v.impact}] ${v.id}: ${v.description}`);
        v.nodes.forEach((n) => console.log("  →", n.html));
      });
    }

    expect(results.violations).toHaveLength(0);
  });
}

// Test authenticated page — login and then scan
test("Dashboard has no axe violations (authenticated)", async ({ page }) => {
  // Log in
  await page.goto("/login");
  await page.getByLabel("Email").fill("test@example.com");
  await page.getByLabel("Password").fill("testpassword");
  await page.getByRole("button", { name: "Sign in" }).click();
  await page.waitForURL("/dashboard");

  const results = await new AxeBuilder({ page })
    .withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa"])
    .analyze();

  expect(results.violations).toHaveLength(0);
});
```

### playwright.config.ts — accessibility project

```typescript
// playwright.config.ts
import { defineConfig, devices } from "@playwright/test";

export default defineConfig({
  projects: [
    {
      name: "accessibility",
      testMatch: "tests/a11y/**/*.spec.ts",
      use: {
        ...devices["Desktop Chrome"],
        baseURL: "http://localhost:4173",
      },
    },
  ],
});
```

---

## Tools Reference

| Tool | Type | Cost | Best Used For |
|------|------|------|--------------|
| **axe DevTools** (browser ext.) | Automated | Free / Paid Pro | Quick page scan in DevTools |
| **WAVE** (browser ext.) | Automated | Free | Visual overlay showing issues |
| **Colour Contrast Analyser** (desktop app) | Manual | Free | Verify oklch/hsl colors vs WCAG ratios |
| **NVDA** | Screen reader | Free | Windows SR testing |
| **JAWS** | Screen reader | Paid | Enterprise SR testing |
| **VoiceOver** | Screen reader | Built-in | macOS/iOS testing |
| **TalkBack** | Screen reader | Built-in | Android testing |
| **@axe-core/playwright** | Automated | Free (OSS) | CI/CD automated scanning |
| **vitest-axe** | Automated | Free (OSS) | Component-level unit tests |
| **Lighthouse** (DevTools) | Automated | Free | General accessibility score |
| **Text Spacing bookmarklet** | Manual test | Free | Verify WCAG 1.4.12 compliance |
| **Deque axe DevTools Pro** | Automated | Paid | Guided manual + automated testing |

---

## VPAT (Voluntary Product Accessibility Template)

### What is a VPAT?

A VPAT is a document that describes how a product conforms to accessibility standards. It is required for selling software to US government agencies (Section 508), many educational institutions, and enterprise procurement. Customers request VPATs to verify accessibility claims.

**Template to use:** VPAT® 2.5 Rev — WCAG 2.2 Edition
- Download from: https://www.itic.org/policy/accessibility/vpat
- Always use the WCAG edition (not the Section 508-only edition)
- Update the VPAT after each major release

### Conformance Levels

| Level | Meaning | When to Use |
|-------|---------|-------------|
| **Supports** | The feature fully meets the success criterion | Only when fully tested and passing |
| **Partially Supports** | Some aspects meet the criterion, others do not | When there are known, bounded gaps |
| **Does Not Support** | The feature does not meet the criterion | Be honest — customers will test it |
| **Not Applicable** | The criterion does not apply to this product | E.g., SC 1.2.x Video Captions for an app with no video |

### VPAT Section Structure

1. **Product Name & Version** — be specific; VPATs are version-specific
2. **Report Date** — date of last audit
3. **Product Description** — one paragraph
4. **Contact Information** — accessibility@yourcompany.com
5. **Notes** — known limitations, software/browser dependencies
6. **Evaluation Methods Used** — tools and manual testing procedures used
7. **Applicable Standards** — check all that apply: WCAG 2.2, Section 508, EN 301 549
8. **WCAG Tables** — one table per principle, list each SC with your conformance level and remarks

### Filling Out WCAG Tables (example rows)

| Criteria | Conformance Level | Remarks |
|---------|-------------------|---------|
| 1.1.1 Non-text Content | Supports | All product images have descriptive alt text. Decorative images use empty alt. Charts have textual data summaries in figcaption. |
| 1.3.5 Identify Input Purpose | Supports | All personal data form inputs include appropriate autocomplete attributes. |
| 2.4.11 Focus Not Obscured | Partially Supports | Most pages comply. Known issue: the Help widget fixed overlay partially obscures focused elements on mobile — scheduled fix in v2.3. |
| 2.5.8 Target Size | Partially Supports | Most interactive elements meet 24×24px minimum. Known issue: filter chip delete buttons in the search bar are 16×16px — fix in progress. |

---

## Accessibility Statement

An accessibility statement is a public commitment to your users about your accessibility goals, known issues, and how to contact you if they encounter problems.

### Required Content

```markdown
# Accessibility Statement for [Product Name]

**Last updated:** [Date]

## Our commitment
[Organization name] is committed to ensuring that [Product Name] is accessible
to people with disabilities. We aim to conform to the [Web Content Accessibility
Guidelines (WCAG) 2.2](https://www.w3.org/TR/WCAG22/) at Level AA.

## Conformance status
[Product Name] version [X.Y] is **partially conformant** with WCAG 2.2 Level AA.
Partially conformant means that some parts of the content do not fully conform
to the accessibility standard.

## Known limitations
The following content may not yet fully conform to WCAG 2.2 AA:

| Issue | WCAG Criterion | Planned Fix |
|-------|---------------|-------------|
| Filter chip delete buttons smaller than 24px | 2.5.8 (AA) Target Size | v2.3 (estimated Q3 2025) |
| PDF reports not screen-reader accessible | 1.1.1 (A) Non-text Content | Under investigation |

## Technical specifications
This website is built with React 19, Tailwind CSS, and Radix UI components.
It relies on the following technologies for conformance:
- HTML, CSS, JavaScript
- WAI-ARIA

## Evaluation approach
We assessed [Product Name] using:
- Self-evaluation against WCAG 2.2 success criteria
- Automated testing with @axe-core/playwright on every pull request
- Manual testing with NVDA + Chrome, VoiceOver + Safari
- Periodic third-party audit (last audit: [Date])

## Feedback and contact
We welcome your feedback on the accessibility of [Product Name].
If you experience barriers or need assistance:

- **Email:** accessibility@[yourcompany.com]
- **Response time:** We aim to respond within 2 business days

If you are not satisfied with our response, you may contact:
[Relevant enforcement authority for your jurisdiction]
```

---

## Audit Cadence

| Activity | Frequency | Who | Tools |
|----------|-----------|-----|-------|
| Automated axe scan | Every PR (CI/CD) | CI system | @axe-core/playwright |
| Component-level unit tests | Every commit | Developer | vitest-axe |
| Manual keyboard navigation check | Every new feature | Developer | Browser only |
| Screen reader spot check (NVDA/VoiceOver) | Every sprint for new UI | Developer or QA | NVDA, VoiceOver |
| Full SR matrix test (5 SR × browser pairs) | Each quarterly release | Dedicated QA or consultant | All 5 SRs |
| WCAG AA audit against full checklist | Annually or major release | Internal or external auditor | Full tool suite |
| VPAT update | Each major release | Product owner + developer | VPAT template |
| Accessibility statement update | Each major release | Product owner | — |

---

## Escalation & Remediation Process

1. **Automated CI failure** → PR cannot merge until violation is fixed or explicitly excluded with justification in code comment
2. **Bug report from user** → P1 severity if blocking task completion for a disability; P2 for workaround available; P3 for cosmetic
3. **External audit finding** → Create a JIRA/GitHub issue immediately; assign to sprint within 2 weeks for High/Critical; add to VPAT known issues if not fixable immediately
4. **Regression** → Revert or hotfix within 24 hours if it affects a WCAG A/AA criterion that was previously passing

---

## Accessibility Champions Program

For organizations maintaining large codebases:

- **Designate 1 champion per squad** — responsible for reviewing PRs for accessibility, running SR tests, and keeping knowledge current
- **Monthly champions meeting** — share lessons learned, test results, and new WCAG guidance
- **Deque University courses** — all champions complete "Accessibility Testing" course (free tier available)
- **Office hours** — accessibility champion holds 30-min bi-weekly drop-in for developers with questions
