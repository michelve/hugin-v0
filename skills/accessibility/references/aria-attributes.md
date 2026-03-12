# ARIA Attributes

## Contents

- [Interactive Elements](#interactive-elements)
- [Form Elements](#form-elements)
- [Live Regions](#live-regions)
- [Combobox (Autocomplete Input + Listbox)](#combobox-autocomplete-input--listbox)
- [Data Grid (Interactive Grid)](#data-grid-interactive-grid)
- [Tree View](#tree-view)
- [Carousel](#carousel)
- [Breadcrumb](#breadcrumb)
- [Pagination](#pagination)
- [Loading / Spinner States](#loading--spinner-states)
- [Reusable Announcement Hook](#reusable-announcement-hook)

---

## Interactive Elements

```tsx
// Button with state
<button
  aria-expanded={isOpen}
  aria-controls="menu-id"
  aria-haspopup="menu"
>
  Menu
</button>

// Menu
<ul
  id="menu-id"
  role="menu"
  aria-labelledby="button-id"
>
  <li role="menuitem" tabIndex={-1}>Option 1</li>
  <li role="menuitem" tabIndex={-1}>Option 2</li>
</ul>
```

## Form Elements

```tsx
// Input with error
<div>
    <label id="email-label" htmlFor="email">
        Email
    </label>
    <input
        id="email"
        type="email"
        aria-labelledby="email-label"
        aria-describedby="email-error"
        aria-invalid={hasError}
    />
    {hasError && (
        <span id="email-error" role="alert">
            Please enter a valid email
        </span>
    )}
</div>
```

## Live Regions

```tsx
// Announce dynamic content
<div aria-live="polite" aria-atomic="true">
  {statusMessage}
</div>

// Urgent announcements
<div role="alert" aria-live="assertive">
  {errorMessage}
</div>
```

---

## Combobox (Autocomplete Input + Listbox)

A combobox is an `<input>` paired with a popup listbox. Screen readers need `aria-expanded`, `aria-autocomplete`, and `aria-activedescendant` to communicate state.

```tsx
export function Combobox({ options, onSelect }: ComboboxProps) {
  const [query, setQuery] = useState("");
  const [open, setOpen] = useState(false);
  const [activeIndex, setActiveIndex] = useState(-1);
  const inputRef = useRef<HTMLInputElement>(null);
  const listId = useId();

  const filtered = options.filter((o) =>
    o.label.toLowerCase().includes(query.toLowerCase()),
  );

  return (
    <div className="relative">
      <input
        ref={inputRef}
        type="text"
        role="combobox"
        aria-expanded={open}
        aria-haspopup="listbox"
        aria-autocomplete="list"
        // Points to the currently highlighted option's id
        aria-activedescendant={
          activeIndex >= 0 ? `${listId}-option-${activeIndex}` : undefined
        }
        aria-controls={listId}
        value={query}
        onChange={(e) => {
          setQuery(e.target.value);
          setOpen(true);
          setActiveIndex(-1);
        }}
        onKeyDown={(e) => {
          if (e.key === "ArrowDown") {
            e.preventDefault();
            setActiveIndex((i) => Math.min(i + 1, filtered.length - 1));
          } else if (e.key === "ArrowUp") {
            e.preventDefault();
            setActiveIndex((i) => Math.max(i - 1, 0));
          } else if (e.key === "Enter" && activeIndex >= 0) {
            onSelect(filtered[activeIndex]);
            setOpen(false);
          } else if (e.key === "Escape") {
            setOpen(false);
            setActiveIndex(-1);
          }
        }}
        className="w-full rounded-md border border-input px-3 py-2"
      />
      {open && filtered.length > 0 && (
        <ul
          id={listId}
          role="listbox"
          aria-label="Suggestions"
          className="absolute z-50 mt-1 w-full rounded-md border bg-popover shadow-md"
        >
          {filtered.map((option, index) => (
            <li
              key={option.value}
              id={`${listId}-option-${index}`}
              role="option"
              aria-selected={index === activeIndex}
              onClick={() => {
                onSelect(option);
                setQuery(option.label);
                setOpen(false);
              }}
              className="cursor-default px-3 py-2 aria-selected:bg-accent"
            >
              {option.label}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
```

---

## Data Grid (Interactive Grid)

A data grid differs from a data table: cells are interactive (editable, selectable, sortable). Use `role="grid"` rather than `role="table"`.

```tsx
<div
  role="grid"
  aria-label="Sales data"
  aria-rowcount={totalRows}        // Total row count including off-screen rows
  aria-colcount={columns.length}   // Total column count
>
  <div role="rowgroup">
    <div role="row">
      {columns.map((col, colIndex) => (
        <div
          key={col.key}
          role="columnheader"
          aria-colindex={colIndex + 1}
          // "ascending" | "descending" | "none" when column is sortable
          aria-sort={sortColumn === col.key ? sortDirection : "none"}
          tabIndex={focusedCell.col === colIndex && focusedCell.row === -1 ? 0 : -1}
          onClick={() => sortBy(col.key)}
          className="px-4 py-2 font-semibold"
        >
          {col.label}
        </div>
      ))}
    </div>
  </div>

  <div role="rowgroup">
    {rows.map((row, rowIndex) => (
      <div
        key={row.id}
        role="row"
        aria-rowindex={rowIndex + 1}
      >
        {columns.map((col, colIndex) => (
          <div
            key={col.key}
            role="gridcell"
            aria-colindex={colIndex + 1}
            // -1 for all cells not currently focused; 0 for the active cell
            tabIndex={
              focusedCell.row === rowIndex && focusedCell.col === colIndex ? 0 : -1
            }
            onFocus={() => setFocusedCell({ row: rowIndex, col: colIndex })}
            className="px-4 py-2"
          >
            {row[col.key]}
          </div>
        ))}
      </div>
    ))}
  </div>
</div>
```

See [keyboard-navigation.md](keyboard-navigation.md) for the 2D Arrow-key grid navigation handler.

---

## Tree View

A tree presents hierarchical data with expandable/collapsible nodes.

```tsx
function TreeItem({ node, level }: { node: TreeNode; level: number }) {
  const [expanded, setExpanded] = useState(false);
  const hasChildren = node.children && node.children.length > 0;

  return (
    <li
      role="treeitem"
      aria-level={level}             // Nesting depth (1-based)
      aria-expanded={hasChildren ? expanded : undefined}
      aria-setsize={node.siblings}   // How many items are in this node's parent
      aria-posinset={node.position}  // This item's position within its sibling set (1-based)
      aria-selected={node.selected}
      tabIndex={node.focused ? 0 : -1}
    >
      <div
        className="flex items-center gap-1 rounded px-2 py-1"
        onClick={() => hasChildren && setExpanded((v) => !v)}
      >
        {hasChildren && (
          <ChevronRightIcon
            aria-hidden="true"
            className={cn("h-4 w-4 transition-transform", expanded && "rotate-90")}
          />
        )}
        {node.label}
      </div>

      {hasChildren && expanded && (
        <ul role="group">
          {node.children.map((child) => (
            <TreeItem key={child.id} node={child} level={level + 1} />
          ))}
        </ul>
      )}
    </li>
  );
}

// Root container
<ul role="tree" aria-label="File explorer">
  {rootNodes.map((node) => (
    <TreeItem key={node.id} node={node} level={1} />
  ))}
</ul>
```

---

## Carousel

```tsx
export function Carousel({ slides, label }: CarouselProps) {
  const [current, setCurrent] = useState(0);
  const [paused, setPaused] = useState(false);
  const liveRef = useRef<HTMLDivElement>(null);

  // Auto-rotation
  useEffect(() => {
    if (paused) return;
    const timer = setInterval(() => {
      setCurrent((c) => (c + 1) % slides.length);
    }, 5000);
    return () => clearInterval(timer);
  }, [paused, slides.length]);

  function goTo(index: number) {
    setCurrent(index);
    // Announce new slide to screen readers
    if (liveRef.current) {
      liveRef.current.textContent = `Slide ${index + 1} of ${slides.length}: ${slides[index].title}`;
    }
  }

  return (
    // role="region" + aria-roledescription announces as "carousel" rather than "region"
    <section
      aria-roledescription="carousel"
      aria-label={label}
    >
      {/* Hidden live region for slide change announcements */}
      <div ref={liveRef} aria-live="polite" aria-atomic="true" className="sr-only" />

      {/* Slides */}
      <div className="overflow-hidden">
        {slides.map((slide, index) => (
          <div
            key={slide.id}
            role="group"
            aria-roledescription="slide"
            aria-label={`Slide ${index + 1} of ${slides.length}: ${slide.title}`}
            // Hide non-current slides from assistive technologies
            aria-hidden={index !== current}
            className={cn("transition-transform", index !== current && "hidden")}
          >
            {slide.content}
          </div>
        ))}
      </div>

      {/* Controls */}
      <div role="group" aria-label="Carousel controls">
        <Button
          variant="outline"
          size="icon"
          onClick={() => goTo((current - 1 + slides.length) % slides.length)}
          aria-label="Previous slide"
        >
          <ChevronLeftIcon aria-hidden="true" className="h-4 w-4" />
        </Button>

        {/* Play/Pause button (required when auto-rotation is present) */}
        <Button
          variant="outline"
          size="icon"
          onClick={() => setPaused((p) => !p)}
          aria-label={paused ? "Play carousel" : "Pause carousel"}
          aria-pressed={paused}
        >
          {paused ? (
            <PlayIcon aria-hidden="true" className="h-4 w-4" />
          ) : (
            <PauseIcon aria-hidden="true" className="h-4 w-4" />
          )}
        </Button>

        <Button
          variant="outline"
          size="icon"
          onClick={() => goTo((current + 1) % slides.length)}
          aria-label="Next slide"
        >
          <ChevronRightIcon aria-hidden="true" className="h-4 w-4" />
        </Button>
      </div>

      {/* Slide indicator dots */}
      <div role="group" aria-label="Slide indicators">
        {slides.map((slide, index) => (
          <button
            key={slide.id}
            onClick={() => goTo(index)}
            aria-label={`Go to slide ${index + 1}: ${slide.title}`}
            aria-current={index === current ? "true" : undefined}
            className={cn(
              "h-2 w-2 rounded-full min-h-6 min-w-6", // ≥ 24×24 target (2.5.8 AA)
              "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring",
              index === current ? "bg-primary" : "bg-muted",
            )}
          />
        ))}
      </div>
    </section>
  );
}
```

---

## Breadcrumb

```tsx
// ✔ Breadcrumb — ordered list (reflects hierarchy) inside a labeled nav landmark
<nav aria-label="Breadcrumb">
  <ol className="flex items-center gap-1 text-sm text-muted-foreground">
    <li>
      <a href="/" className="hover:text-foreground">Home</a>
    </li>
    <li aria-hidden="true" className="select-none">/</li>
    <li>
      <a href="/products" className="hover:text-foreground">Products</a>
    </li>
    <li aria-hidden="true" className="select-none">/</li>
    {/* aria-current="page" on the last item — the current page */}
    <li>
      <span aria-current="page" className="font-medium text-foreground">
        Laptops
      </span>
    </li>
  </ol>
</nav>
```

---

## Pagination

```tsx
<nav aria-label="Pagination">
  <ul className="flex items-center gap-1">
    <li>
      <Button
        variant="outline"
        disabled={currentPage === 1}
        onClick={() => onPageChange(currentPage - 1)}
        aria-label="Go to previous page"
      >
        Previous
      </Button>
    </li>

    {pages.map((page) => (
      <li key={page}>
        <Button
          variant={page === currentPage ? "default" : "outline"}
          onClick={() => onPageChange(page)}
          aria-label={`Go to page ${page}`}
          // Marks the current page for screen readers
          aria-current={page === currentPage ? "page" : undefined}
        >
          {page}
        </Button>
      </li>
    ))}

    <li>
      <Button
        variant="outline"
        disabled={currentPage === totalPages}
        onClick={() => onPageChange(currentPage + 1)}
        aria-label="Go to next page"
      >
        Next
      </Button>
    </li>
  </ul>

  {/* Announce page change to screen readers */}
  <div role="status" aria-live="polite" className="sr-only">
    Page {currentPage} of {totalPages}
  </div>
</nav>
```

---

## Loading / Spinner States

```tsx
// ✔ Inline spinner — role="status" + aria-label describes what is loading
<div
  role="status"
  aria-label="Loading user profile"
  className="flex items-center gap-2"
>
  <LoaderIcon aria-hidden="true" className="h-4 w-4 animate-spin" />
  <span className="text-sm text-muted-foreground">Loading…</span>
</div>

// ✔ Full-page loading — aria-busy on the container being loaded
<main
  id="main-content"
  aria-busy={isLoading}  // Announces to screen readers that content is updating
  tabIndex={-1}
>
  {isLoading ? (
    <div role="status" className="sr-only">Loading page content</div>
  ) : (
    children
  )}
</main>

// ✔ Button loading state
<Button
  disabled={isSubmitting}
  aria-disabled={isSubmitting}
  aria-describedby={isSubmitting ? "submit-status" : undefined}
>
  {isSubmitting ? (
    <>
      <LoaderIcon aria-hidden="true" className="mr-2 h-4 w-4 animate-spin" />
      Saving…
    </>
  ) : (
    "Save changes"
  )}
</Button>
{isSubmitting && (
  <div id="submit-status" className="sr-only" role="status">
    Saving your changes, please wait
  </div>
)}

---

## Reusable Announcement Hook

Use this hook to imperatively announce dynamic events (filter applied, item saved, search complete) without moving focus.

```tsx
// src/client/hooks/useAnnounce.ts
import { useCallback, useRef } from "react";

export function useAnnounce() {
  const politeRef = useRef<HTMLDivElement>(null);
  const assertiveRef = useRef<HTMLDivElement>(null);

  const announce = useCallback(
    (message: string, politeness: "polite" | "assertive" = "polite") => {
      const el = politeness === "assertive" ? assertiveRef.current : politeRef.current;
      if (!el) return;
      // Clear first, then set — forces re-announcement even when text is identical
      el.textContent = "";
      requestAnimationFrame(() => { el.textContent = message; });
    },
    [],
  );

  const LiveRegions = (
    <>
      <div ref={politeRef} role="status" aria-live="polite" aria-atomic="true" className="sr-only" />
      <div ref={assertiveRef} role="alert" aria-live="assertive" aria-atomic="true" className="sr-only" />
    </>
  );

  return { announce, LiveRegions };
}
```

```tsx
// Usage
function SearchResults() {
  const { announce, LiveRegions } = useAnnounce();

  const handleSearch = async (query: string) => {
    const results = await fetchResults(query);
    announce(`${results.length} results found for "${query}"`);
  };

  return (
    <>
      {LiveRegions}
      {/* search UI */}
    </>
  );
}
```

**Rules:**

- Mount `LiveRegions` in the same component that calls `announce` (or in a layout root)
- The live region container must exist in the DOM **before** content is injected
- Use `polite` (default) for most updates; `assertive` only for urgent errors that need immediate interruption
- The clear → rAF → set pattern ensures the same message re-announces if called again
