# Semantic HTML — Accessibility Reference

Semantic HTML uses the correct HTML element for the content's meaning. It provides built-in accessibility at no cost — screen readers, browsers, search engines, and assistive technologies all understand semantic meaning and expose it correctly to users.

## Contents

- [Images — Alt Text Decision Tree](#images--alt-text-decision-tree)
- [SVG Accessibility](#svg-accessibility)
- [Landmark Regions](#landmark-regions)
- [Heading Hierarchy](#heading-hierarchy)
- [Data Tables](#data-tables)
- [Lists](#lists)
- [Language Declaration](#language-declaration)
- [Interactive vs. Non-Interactive Elements](#interactive-vs-non-interactive-elements)
- [Time and Dates](#time-and-dates)
- [Microdata and Rich Content](#microdata-and-rich-content)

---

## Images — Alt Text Decision Tree

Every `<img>` element must have an `alt` attribute. The value depends on **what the image communicates**.

```
Is the image purely decorative (only adds visual polish, conveys no information)?
├── YES → alt="" AND aria-hidden="true"
└── NO → Does the image have a visible caption nearby that describes it?
         ├── YES → alt="" (caption carries the information)
         └── NO → What is the image's function?
                  ├── INFORMATIVE (photo, illustration, chart, diagram) → Write a brief description alt text
                  ├── FUNCTIONAL (button icon, link that is an image) → Describe the action: alt="Search"
                  └── COMPLEX (chart, map, infographic) → Short alt + long description via <figure><figcaption> or aria-describedby
```

### Informative Images

```tsx
// ✔ Describes what the image shows — "A golden retriever puppy sitting in a meadow"
<img
  src="/hero.jpg"
  alt="A golden retriever puppy sitting in a sunny meadow, looking at the camera"
/>
```

### Decorative Images

```tsx
// ✔ Empty alt + aria-hidden removes the image from the accessibility tree entirely
<img src="/divider-wave.svg" alt="" aria-hidden="true" />

// ✔ Background image via CSS — no alt needed, not in the DOM
<div className="bg-[url('/hero-bg.jpg')] h-64 bg-cover" aria-hidden="true" />
```

### Functional Images (Image is the Entire Link or Button)

```tsx
// ✔ The alt describes the DESTINATION or ACTION, not the image itself
<a href="/">
  <img src="/logo.svg" alt="Acme Inc — go to home page" />
</a>

// ✔ Icon-only button — describe what the button DOES
<button>
  <img src="/search-icon.png" alt="Search products" />
</button>
```

### Complex Images (Charts, Diagrams, Infographics)

```tsx
// ✔ Short summary alt + long description in visible caption
<figure>
  <img
    src="/quarterly-sales-chart.png"
    alt="Bar chart showing quarterly sales — Q4 was highest at $2.1M"
    aria-describedby="chart-description"
  />
  <figcaption id="chart-description">
    Chart description: Quarterly revenue for FY2024. Q1: $1.2M, Q2: $1.4M,
    Q3: $1.7M, Q4: $2.1M. Growth was driven by the enterprise segment in Q4.
  </figcaption>
</figure>
```

---

## SVG Accessibility

Inline SVGs are not automatically accessible. Always choose one of the two approaches below.

### Informative SVG (conveys information)

```tsx
// ✔ role="img" + title + aria-labelledby
<svg
  role="img"
  aria-labelledby="pie-chart-title pie-chart-desc"
  viewBox="0 0 200 200"
>
  <title id="pie-chart-title">Browser market share 2024</title>
  <desc id="pie-chart-desc">
    Chrome 65%, Safari 19%, Firefox 4%, Edge 4%, Other 8%
  </desc>
  {/* SVG paths */}
</svg>
```

### Informative SVG Icon used as a label

```tsx
// ✔ Standalone icon button — aria-label on the button is preferred over title on SVG
<button aria-label="Share this page">
  <ShareIcon aria-hidden="true" className="h-5 w-5" />
</button>
```

### Decorative SVG (purely visual, no information)

```tsx
// ✔ aria-hidden removes from accessibility tree; focusable="false" prevents IE11 tab focus
<svg
  aria-hidden="true"
  focusable="false"
  className="h-4 w-4 text-muted-foreground"
>
  {/* decorative icon paths */}
</svg>
```

### Using lucide-react icons

```tsx
import { SearchIcon, ArrowRightIcon } from "lucide-react";

// ✔ Decorative icon — always aria-hidden when a visible label or aria-label is nearby
<Button>
  <SearchIcon aria-hidden="true" className="mr-2 h-4 w-4" />
  Search
</Button>

// ✔ Icon-only — always add an aria-label to the button
<Button size="icon" aria-label="Next page">
  <ArrowRightIcon aria-hidden="true" className="h-4 w-4" />
</Button>
```

---

## Landmark Regions

Landmark regions are the page's table of contents for screen reader users. Use native HTML5 elements — they have built-in ARIA landmark roles and need no `role` attribute.

| HTML Element | Implicit ARIA Role | Purpose | Per-Page Limit |
|--------------|--------------------|---------|----------------|
| `<header>` (top-level) | `banner` | Site-wide header (logo, primary nav) | 1 |
| `<nav>` | `navigation` | Navigation links | Multiple — must label each |
| `<main>` | `main` | Primary page content | 1 |
| `<aside>` | `complementary` | Supporting, tangentially related content | Multiple — must label each |
| `<footer>` (top-level) | `contentinfo` | Site-wide footer (legal, links) | 1 |
| `<section>` with accessible name | `region` | Named section of content | Multiple |
| `<form>` with accessible name | `form` | Form landmark | Multiple |
| `<search>` | `search` | Search functionality | Multiple |

### Full page structure example

```tsx
export function AppLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      {/* role="banner" — one per page, site-wide */}
      <header className="sticky top-0 z-50 h-16 border-b bg-background">
        {/* role="navigation" — label each nav distinctly */}
        <nav aria-label="Main navigation" className="flex items-center gap-4">
          {/* nav links */}
        </nav>
      </header>

      <div className="flex">
        {/* role="complementary" — supporting content, labeled */}
        <aside aria-label="Filters" className="w-64 border-r p-4">
          {/* filter sidebar */}
        </aside>

        {/* role="main" — one per page, primary content */}
        <main id="main-content" tabIndex={-1} className="flex-1 p-6 outline-none">
          {children}
        </main>
      </div>

      {/* role="contentinfo" — one per page, site-wide */}
      <footer className="border-t py-6">
        <nav aria-label="Footer navigation">
          {/* footer links */}
        </nav>
      </footer>
    </>
  );
}
```

### Section as a named region

```tsx
// ✔ <section> with aria-labelledby creates a "region" landmark
// Use sparingly — only for major content areas that users would want to navigate to directly
<section aria-labelledby="featured-heading">
  <h2 id="featured-heading">Featured articles</h2>
  {/* article list */}
</section>
```

### Rules

- `<header>` and `<footer>` are only landmarks when **direct children of `<body>`** — if nested inside `<main>` or `<article>`, they are not landmarks
- Every `<nav>` on a page must have a unique `aria-label` or `aria-labelledby`
- Every `<aside>` should have `aria-label` describing its complementary purpose
- Never put `<main>` inside another landmark (not inside `<header>`, `<nav>`, or `<aside>`)
- Do not use `<div>` or `<span>` where a semantic element is available

---

## Heading Hierarchy

Headings provide page structure and enable screen reader users to navigate by `H` key.

### Rules

1. **One `<h1>` per page** — describes the page's primary topic
2. **No skipping levels** — never jump from `<h2>` to `<h4>` without an `<h3>` between them
3. **Logical nesting** — headings nest by content section, not by desired font size
4. **Use CSS for appearance** — size is controlled by Tailwind classes, not by heading level choice

```tsx
// ✔ Correct heading hierarchy
<h1>Product Catalog</h1>
  <h2>Electronics</h2>
    <h3>Laptops</h3>
      <h4>Budget category ($0–$500)</h4>
    <h3>Tablets</h3>
  <h2>Clothing</h2>
    <h3>Men's</h3>
    <h3>Women's</h3>

// ✗ Incorrect — never skip heading levels
<h1>Dashboard</h1>
<h3>Performance metrics</h3>  {/* Missing h2 — FAIL */}

// ✗ Incorrect — never choose heading level based on desired size
<h6 className="text-2xl font-bold">Important section</h6>  {/* FAIL */}
```

```tsx
// ✔ Size appearance controlled by className, level by document outline
<h2 className="text-sm font-medium text-muted-foreground">
  Subsection title that should look small
</h2>
```

---

## Data Tables

Use `<table>` for tabular data — rows and columns with headers. Never use tables for layout.

### Simple table

```tsx
<table>
  {/* caption is the table's title — screen readers announce it before the data */}
  <caption className="sr-only">Q4 2024 Sales by Region</caption>
  <thead>
    <tr>
      {/* scope="col" links the header to the entire column */}
      <th scope="col">Region</th>
      <th scope="col">Q3 Revenue</th>
      <th scope="col">Q4 Revenue</th>
      <th scope="col">Growth</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      {/* scope="row" links the header to the entire row */}
      <th scope="row">North America</th>
      <td>$1.2M</td>
      <td>$1.8M</td>
      <td>+50%</td>
    </tr>
    <tr>
      <th scope="row">Europe</th>
      <td>$0.8M</td>
      <td>$1.1M</td>
      <td>+37.5%</td>
    </tr>
  </tbody>
  <tfoot>
    <tr>
      <th scope="row">Total</th>
      <td>$2.0M</td>
      <td>$2.9M</td>
      <td>+45%</td>
    </tr>
  </tfoot>
</table>
```

### Complex table (multi-level headers)

When column headers span multiple rows, or row headers span multiple columns, use `id` / `headers` to link cells:

```tsx
<table>
  <caption>Employee skills matrix</caption>
  <thead>
    <tr>
      <td></td> {/* empty corner cell */}
      <th id="frontend" scope="colgroup" colSpan={2}>Frontend</th>
      <th id="backend" scope="colgroup" colSpan={2}>Backend</th>
    </tr>
    <tr>
      <td></td>
      <th id="react" scope="col">React</th>
      <th id="css" scope="col">CSS</th>
      <th id="node" scope="col">Node.js</th>
      <th id="sql" scope="col">SQL</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="alice" scope="row">Alice</th>
      {/* headers attribute links to both the column-group and specific column headers */}
      <td headers="frontend react alice">Expert</td>
      <td headers="frontend css alice">Proficient</td>
      <td headers="backend node alice">Beginner</td>
      <td headers="backend sql alice">Proficient</td>
    </tr>
  </tbody>
</table>
```

### Sortable table headers

```tsx
<th
  scope="col"
  aria-sort="ascending"        // "ascending" | "descending" | "none" | "other"
  onClick={() => sortBy("name")}
  onKeyDown={(e) => e.key === "Enter" && sortBy("name")}
  tabIndex={0}
  style={{ cursor: "pointer" }}
  className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
>
  Name
  <span aria-hidden="true"> ↑</span>
</th>
```

---

## Lists

Use the correct list type based on the content's meaning:

| Content Type | Element |
|-------------|---------|
| Items where order does not matter | `<ul>` (unordered) |
| Sequential steps / ranked items | `<ol>` (ordered) |
| Terms and their definitions | `<dl>` (description list) |
| Navigation links | `<nav>` + `<ul>` |

```tsx
// ✔ Navigation — always ul inside nav
<nav aria-label="Breadcrumb">
  <ol className="flex gap-2">
    <li><a href="/">Home</a></li>
    <li aria-hidden="true">/</li>
    <li><a href="/products">Products</a></li>
    <li aria-hidden="true">/</li>
    <li aria-current="page">Laptops</li>
  </ol>
</nav>

// ✔ Definition list for key-value pairs
<dl>
  <dt>Author</dt>
  <dd>Jane Smith</dd>
  <dt>Published</dt>
  <dd><time dateTime="2024-03-15">March 15, 2024</time></dd>
  <dt>Category</dt>
  <dd>Technology</dd>
</dl>
```

**Tailwind `list-none` caveat:** Safari + VoiceOver removes list semantics from `<ul>` elements that have `list-style: none`. Fix:

```tsx
// ✔ Restore list semantics when using list-none in Safari VoiceOver
<ul className="list-none p-0" role="list">
  <li>...</li>
</ul>
```

---

## Language Declaration

```html
<!-- src/client/index.html — always declare the page language -->
<html lang="en">

<!-- lang attribute on inline foreign-language text -->
<p>
  The French greeting is
  <span lang="fr">bonjour</span>.
</p>

<!-- Entire block in another language -->
<blockquote lang="de" cite="https://example.com/zitat">
  Alles Gute kommt von oben.
</blockquote>
```

**Common BCP 47 language tags:**

| Language | Tag |
|---------|-----|
| English (US) | `en` or `en-US` |
| French | `fr` |
| German | `de` |
| Spanish | `es` |
| Chinese (Simplified) | `zh-Hans` |
| Japanese | `ja` |
| Arabic | `ar` |

---

## Interactive vs. Non-Interactive Elements

Always use the **native element** that matches the interaction. Native elements provide keyboard support, ARIA semantics, and platform integration for free.

| Task | ✔ Use This | ✗ Not This |
|------|-----------|-----------|
| Submit form | `<button type="submit">` | `<div onClick>` |
| Navigate to URL | `<a href="...">` | `<span onClick>` |
| Toggle a boolean | `<input type="checkbox">` or Radix `Checkbox` | `<div onClick` with manually managed ARIA |
| Select one of many options | `<input type="radio">` or Radix `RadioGroup` | Custom-styled `<div>` list |
| Expand/collapse section | Radix `Accordion`, or `<details>/<summary>` | `<div onClick` with manually toggled ARIA |
| Open a modal | Radix `Dialog` | `<div role="dialog"` custom implementation |
| Choose from a dropdown | Radix `Select` or `<select>` | Custom `<div>` dropdown |

> When you cannot use a native element, see [aria-attributes.md](aria-attributes.md) for the full ARIA role, state, and keyboard pattern to replicate native semantics.

---

## Time and Dates

```tsx
// ✔ Use <time> element with machine-readable dateTime
<time dateTime="2024-03-15">March 15, 2024</time>

// ✔ For relative times, include both formats
<time dateTime="2024-03-15">3 days ago</time>

// ✔ Durations
<time dateTime="PT1H30M">1 hour 30 minutes</time>
```

---

## Microdata and Rich Content

```tsx
// ✔ Use <abbr> for abbreviations
<abbr title="World Wide Web Consortium">W3C</abbr>

// ✔ Use <mark> for highlighted/search-result text (announces as "highlighted")
<p>
  Search results for <strong>React</strong>:{" "}
  <mark>React</mark> is a JavaScript library.
</p>

// ✔ Use <code> and <pre> for code
<p>Use the <code>tabIndex</code> attribute to include elements in the tab order.</p>

// ✔ Use <kbd> for keyboard input
<p>Press <kbd>Ctrl</kbd>+<kbd>C</kbd> to copy.</p>
```
