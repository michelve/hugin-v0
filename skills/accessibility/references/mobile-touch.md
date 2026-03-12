# Mobile & Touch Accessibility — Reference

This reference covers WCAG 2.2 success criteria specifically relevant to touch interfaces, pointer interactions, and mobile contexts.

## Contents

- [Target Size Minimum (WCAG 2.5.8 AA)](#target-size-minimum-wcag-258-aa)
- [Pointer Gestures (WCAG 2.5.1 AA)](#pointer-gestures-wcag-251-aa)
- [Pointer Cancellation (WCAG 2.5.2 AA)](#pointer-cancellation-wcag-252-aa)
- [Orientation (WCAG 1.3.4 AA)](#orientation-wcag-134-aa)
- [Motion Actuation (WCAG 2.5.4 AA)](#motion-actuation-wcag-254-aa)
- [Dragging Movements (WCAG 2.5.7 AA)](#dragging-movements-wcag-257-aa)
- [Content on Hover or Focus (WCAG 1.4.13 AA)](#content-on-hover-or-focus-wcag-1413-aa)
- [Reflow (WCAG 1.4.10 AA)](#reflow-wcag-1410-aa)
- [Text Spacing (WCAG 1.4.12 AA)](#text-spacing-wcag-1412-aa)
- [iOS / Android Screen Reader Notes](#ios--android-screen-reader-notes)

---

## Target Size Minimum (WCAG 2.5.8 AA)

### Requirement

Interactive targets must be at least **24×24 CSS pixels**. This applies to the **pointer target area** — not just the visible icon.

**Exceptions (no 24px requirement):**
- Inline text links in a paragraph
- The browser/OS controls the size (system checkboxes, scrollbars)
- Essential — a real-world control that must match its physical dimensions
- Spacing exception — target is smaller but has at least 24px of spacing between it and neighboring targets

> **2.5.5 (AAA) Target Size Enhanced:** Targets should be ≥ 44×44 CSS pixels.

### Tailwind Implementation

```tsx
// ✔ 24×24 minimum (AA) with padding to create hit area larger than visual
<button
  aria-label="Remove filter"
  className="min-h-6 min-w-6 p-1 inline-flex items-center justify-center rounded"
>
  <XIcon aria-hidden="true" className="h-3.5 w-3.5" />
</button>

// ✔ 44×44 recommended (AAA) — primary actions
<button className="min-h-[44px] min-w-[44px] px-4 py-3">
  Save changes
</button>

// ✔ Icon button with invisible extended hit area — stays visually tight
<button
  aria-label="Open menu"
  className={cn(
    // Layout keeps the visual icon tight but the tap target large
    "relative inline-flex h-8 w-8 items-center justify-center",
    // Optional: invisible extended hit area pseudo-element would be in CSS
    // or just increase h/w to meet 24×24
    "rounded-md focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring",
  )}
>
  <MenuIcon aria-hidden="true" className="h-5 w-5" />
</button>
```

### Common Problem Areas Audit

| Component | Typical Visual Size | Fix |
|-----------|-------------------|-----|
| Close (×) button on modal | 16×16px | Add `min-h-6 min-w-6 p-1` |
| Tag/chip delete icon | 12×12px | Wrap in `h-6 w-6` flex container |
| Table row icon actions | 16×16px | Add `p-1` to each icon button |
| Pagination dots | 8×8px | Use `min-h-6 min-w-6 p-1` + `rounded-full` |
| Dropdown menu items | height varies | Use `min-h-9` (36px) for menu items |
| Toggle/switch container | often auto | Ensure the clickable area is ≥ `h-6 w-10` |

---

## Pointer Gestures (WCAG 2.5.1 AA)

### Requirement

All functionality that uses **multi-pointer** (pinch-to-zoom, two-finger swipe) or **path-based** (draw-a-circle, freehand drawing) gestures must have an alternative that works with a **single pointer and no specific path**.

Exception: The gesture is **essential** (e.g., a hand-drawing tool).

### Implementation

```tsx
// ✔ Map with zoom — provide zoom in/out buttons alongside pinch gesture
<div className="relative">
  <MapContainer ref={mapRef} />

  {/* Single-pointer alternatives to pinch-to-zoom */}
  <div
    className="absolute bottom-4 right-4 flex flex-col gap-1"
    role="group"
    aria-label="Map zoom controls"
  >
    <Button
      size="icon"
      variant="secondary"
      aria-label="Zoom in"
      onClick={() => mapRef.current?.zoomIn()}
    >
      <PlusIcon aria-hidden="true" className="h-4 w-4" />
    </Button>
    <Button
      size="icon"
      variant="secondary"
      aria-label="Zoom out"
      onClick={() => mapRef.current?.zoomOut()}
    >
      <MinusIcon aria-hidden="true" className="h-4 w-4" />
    </Button>
  </div>
</div>

// ✔ Swipe-to-dismiss notification — also provide dismiss button
<div className="relative">
  <ToastItem
    // swipe gesture still works for capable users
    onSwipeEnd={() => dismiss(id)}
  />
  {/* Button alternative for users who cannot swipe */}
  <Button
    variant="ghost"
    size="icon"
    aria-label="Dismiss notification"
    onClick={() => dismiss(id)}
    className="absolute right-1 top-1/2 -translate-y-1/2"
  >
    <XIcon aria-hidden="true" className="h-4 w-4" />
  </Button>
</div>
```

---

## Pointer Cancellation (WCAG 2.5.2 AA)

### Requirement

For functionality activated by a single pointer, at least one of the following must be true:
1. **No down-event** — the function is not activated on the down-event (pointer-down / mouse-down)
2. **Abort or undo** — the action is aborted if the pointer moves off the target before up-event
3. **Up reversal** — the up-event reverses any outcome of the down-event
4. **Essential** — completing on down-event is essential (e.g., virtual piano keys)

### Implementation

**The simple rule: use `onClick` (activates on pointer-up), not `onMouseDown` or `onPointerDown`.**

```tsx
// ✔ Correct — onClick is pointer-up based. User can drag away to cancel.
<button onClick={handleDelete}>Delete</button>

// ✗ Incorrect — activates immediately on press, no cancellation possible
<button onMouseDown={handleDelete}>Delete</button>
<button onPointerDown={handleDelete}>Delete</button>

// ✔ Custom drag implementation — cancel if pointer leaves without releasing on target
function DraggableItem({ onDrop }: { onDrop: () => void }) {
  const [pointerDown, setPointerDown] = useState(false);

  return (
    <div
      onPointerDown={() => setPointerDown(true)}
      onPointerUp={() => {
        if (pointerDown) {
          onDrop(); // Only completes on up-event on same element
          setPointerDown(false);
        }
      }}
      onPointerLeave={() => setPointerDown(false)} // Abort if pointer leaves
      onPointerCancel={() => setPointerDown(false)} // Abort on OS cancellation
    >
      Draggable content
    </div>
  );
}
```

---

## Orientation (WCAG 1.3.4 AA)

### Requirement

Content does not restrict its view and operation to a single display orientation (portrait or landscape) unless a specific orientation is **essential** for the content (a piano keyboard layout, a TV remote simulator).

### Implementation

```tsx
// ✔ Support both orientations via responsive CSS — @media orientation is fine for STYLING
// ✗ Never LOCK orientation
```

```tsx
// ✗ FAIL — locks to portrait orientation
if (typeof window !== "undefined" && "screen" in window) {
  // DO NOT DO THIS:
  screen.orientation.lock("portrait"); // Fails WCAG 1.3.4
}
```

```css
/* ✔ CSS-only portrait/landscape adjustments are fine — this is styling, not locking */
@media (orientation: portrait) {
  .controls {
    flex-direction: column;
  }
}
@media (orientation: landscape) {
  .controls {
    flex-direction: row;
  }
}
```

```tsx
// ✔ Show a user-dismissible prompt (not a lock) if landscape is recommended
export function OrientationSuggestion() {
  const [shown, setShown] = useState(false);

  useEffect(() => {
    const mq = window.matchMedia("(orientation: portrait)");
    const handler = (e: MediaQueryListEvent) => setShown(e.matches);
    mq.addEventListener("change", handler);
    return () => mq.removeEventListener("change", handler);
  }, []);

  if (!shown) return null;

  return (
    // ✔ Suggestion only — user can dismiss; the app still works in portrait
    <aside role="note" className="fixed inset-x-0 top-0 z-50 bg-background p-4 text-sm">
      For the best experience, rotate your device to landscape mode.
      <Button variant="ghost" size="sm" onClick={() => setShown(false)}>Dismiss</Button>
    </aside>
  );
}
```

---

## Motion Actuation (WCAG 2.5.4 AA)

### Requirement

Functionality triggered by device motion (shaking, tilting, gesturing the device) must also be operable via UI components, and users must be able to disable the motion trigger to prevent accidental activation.

### Implementation

```tsx
// ✔ Shake-to-undo with UI alternative and opt-out
import { useEffect, useRef } from "react";

export function useShakeToUndo(onUndo: () => void) {
  const lastShakeTime = useRef(0);
  const enabled = useRef(
    // Check if user has opted out of device motion features
    localStorage.getItem("use-device-motion") !== "false"
  );

  useEffect(() => {
    if (!enabled.current) return;
    if (!("DeviceMotionEvent" in window)) return;

    function handleMotion(event: DeviceMotionEvent) {
      const acc = event.acceleration;
      if (!acc) return;
      const magnitude = Math.sqrt((acc.x ?? 0) ** 2 + (acc.y ?? 0) ** 2 + (acc.z ?? 0) ** 2);
      const now = Date.now();
      if (magnitude > 25 && now - lastShakeTime.current > 1000) {
        lastShakeTime.current = now;
        onUndo();
      }
    }

    window.addEventListener("devicemotion", handleMotion);
    return () => window.removeEventListener("devicemotion", handleMotion);
  }, [onUndo]);
}

// Usage — always include UI alternative button
function EditorToolbar({ onUndo }: { onUndo: () => void }) {
  useShakeToUndo(onUndo);

  return (
    <div>
      {/* ✔ UI alternative to shake gesture */}
      <Button variant="ghost" onClick={onUndo} aria-label="Undo last action">
        <UndoIcon aria-hidden="true" />
        Undo
      </Button>
    </div>
  );
}
```

---

## Dragging Movements (WCAG 2.5.7 AA)

See [wcag22-new-criteria.md](wcag22-new-criteria.md#257-dragging-movements--aa-required) for full implementation with the `SortableList` example and slider button alternative.

**Quick recap:**
- Every drag-to-reorder list must have Up/Down buttons
- Every drag-to-resize panel must have keyboard shortcuts or numeric inputs
- Every path-drawing tool must have an alternative unless essential

---

## Content on Hover or Focus (WCAG 1.4.13 AA)

### Requirement

Content that appears on pointer hover or keyboard focus (tooltips, popovers, sub-menus) must be:
1. **Dismissible** — user can dismiss without moving focus/pointer (typically `Escape` key)
2. **Hoverable** — the pointer can move over the appeared content without it disappearing
3. **Persistent** — the content stays visible until the hover/focus trigger is removed, or the user dismisses it, or the information is no longer valid

### Implementation — Tooltip

`@radix-ui/react-tooltip` (bundled in `radix-ui`) meets all three requirements by default. Always prefer it over a custom tooltip.

```tsx
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip";

// ✔ Radix Tooltip — dismissible (Escape), hoverable, persistent
export function ActionButton() {
  return (
    <TooltipProvider>
      <Tooltip>
        <TooltipTrigger asChild>
          <Button size="icon" aria-label="Share page">
            <ShareIcon aria-hidden="true" className="h-4 w-4" />
          </Button>
        </TooltipTrigger>
        <TooltipContent>
          <p>Share this page</p>
        </TooltipContent>
      </Tooltip>
    </TooltipProvider>
  );
}
```

**If building a custom tooltip:**

```tsx
// ✔ Custom tooltip — implement all three requirements manually
function CustomTooltip({ trigger, content }: CustomTooltipProps) {
  const [visible, setVisible] = useState(false);

  return (
    <div className="relative inline-block">
      <div
        onMouseEnter={() => setVisible(true)}
        onMouseLeave={() => setVisible(false)} // persist while hovering tooltip
        onFocus={() => setVisible(true)}
        onBlur={() => setVisible(false)}
        onKeyDown={(e) => {
          // ✔ Dismissible with Escape (1.4.13 requirement 1)
          if (e.key === "Escape") setVisible(false);
        }}
      >
        {trigger}
      </div>

      {visible && (
        <div
          role="tooltip"
          // ✔ Hoverable — the tooltip itself captures pointer events
          // Without this, moving the mouse from trigger to tooltip would hide it
          onMouseEnter={() => setVisible(true)}
          onMouseLeave={() => setVisible(false)}
          className="absolute z-50 rounded-md bg-popover px-3 py-2 text-sm shadow-md"
        >
          {content}
        </div>
      )}
    </div>
  );
}
```

---

## Reflow (WCAG 1.4.10 AA)

### Requirement

Content must reflow to a single column at **320 CSS pixels width** (equivalent to 400% zoom on a 1280px viewport) without requiring two-dimensional scrolling, except for content that requires two-dimensional layout to function (data tables, maps, complex diagrams).

### Implementation

```tsx
// ✔ Responsive layout — never horizontal scrolling at 320px
<div className="w-full max-w-screen-lg mx-auto px-4">
  {/* Content reflows naturally with w-full */}
</div>

// ✔ Card grid — wraps to single column at small viewports
<div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
  {cards.map((card) => (
    <Card key={card.id} {...card} />
  ))}
</div>
```

**Common failures:**

```tsx
// ✗ Fixed width — does not reflow
<div style={{ width: "800px" }}>content</div>

// ✗ min-width larger than 320px — forces horizontal scroll
<div className="min-w-[500px]">content</div>

// ✗ Horizontal scrolling table — needs overflow wrapper with role="region" + tabindex
// ✔ Wrap tables in a scrollable region
<div
  role="region"
  aria-label="Sales data table"
  tabIndex={0}
  className="overflow-x-auto focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
>
  <table>...</table>
</div>
```

**How to test:**

1. In Chrome DevTools, set device width to 320px (or zoom to 400%)
2. Check all content is readable without horizontal scrolling
3. Exception: data tables may scroll horizontally if given `role="region"` + `tabIndex={0}` wrapper

---

## Text Spacing (WCAG 1.4.12 AA)

### Requirement

No loss of content or functionality when the following CSS properties are applied by the user:
- `line-height: 1.5` (times the font size)
- `letter-spacing: 0.12em`
- `word-spacing: 0.16em`
- Space after paragraphs: `2em`

### Implementation

In practice: **do not use `overflow: hidden` on containers that hold text**, and do not use `height` constraints on text without `overflow: auto`.

```tsx
// ✗ Clips text if user increases line-height or letter-spacing
<div className="overflow-hidden h-[3rem]">
  User-entered text content
</div>

// ✔ Allow text to expand
<div className="min-h-[3rem]">
  User-entered text content
</div>

// ✔ Where truncation is truly needed (card titles), use min-h rather than overflow-hidden
<p className="line-clamp-2 min-h-0">
  Card title that is long and may wrap
</p>
```

**Bookmarklet for manual testing:** Search "Text Spacing bookmarklet" — it injects the WCAG text-spacing overrides instantly. Verify no content disappears or overlaps.

---

## iOS / Android Screen Reader Notes

When testing on mobile, these screen readers must be manually confirmed:

| Screen Reader | Platform | Browser | Test Priority |
|--------------|---------|---------|--------------|
| VoiceOver | iOS / iPadOS | Safari | Primary — largest user base |
| TalkBack | Android | Chrome | Primary |

**Common mobile-specific issues:**

- `role="button"` on `<div>` — VoiceOver reads it but TalkBack may not announce "button" in all contexts. Prefer `<button>`.
- Touch-activated roles — `role="slider"` elements need additional touch event handling on mobile if not using a native `<input type="range">`.
- `aria-live` regions — test on real devices; simulators often behave differently for dynamic content.
- Swipe navigation — VoiceOver and TalkBack navigate by swiping through elements; ensure tab/focus order reflects visual reading order.

See [testing-a11y.md](testing-a11y.md) for the full screen reader cross-browser test matrix.
