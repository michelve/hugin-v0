# Focus Management

## Contents

- [FocusScope (Radix UI)](#focusscope-radix-ui)
- [Return Focus Pattern](#return-focus-pattern)
- [Focus Not Obscured (WCAG 2.4.11 AA)](#focus-not-obscured-wcag-2411-aa)
- [Skip Link Focus Target](#skip-link-focus-target)
- [Route Change Focus Management](#route-change-focus-management)
- [Dialog Focus Auto-Focus Override](#dialog-focus-auto-focus-override)
- [Skip Links](#skip-links)
- [Page Title Management](#page-title-management)

---

## FocusScope (Radix UI)

The `FocusScope` component from `radix-ui` is the standard way to trap focus in modals and
dialogs. It is already installed (`radix-ui` v1.4.3) - no install required.

```tsx
import { FocusScope } from "radix-ui";

function Modal({ isOpen, onClose, children }: ModalProps) {
    if (!isOpen) return null;

    return (
        <FocusScope loop trapped asChild>
            <div role="dialog" aria-modal="true" onKeyDown={(e) => e.key === "Escape" && onClose()}>
                {children}
            </div>
        </FocusScope>
    );
}
```

**Props:**

| Prop                 | Type          | Description                                                              |
| -------------------- | ------------- | ------------------------------------------------------------------------ |
| `trapped`            | `boolean`     | Prevent focus leaving the container                                      |
| `loop`               | `boolean`     | Tab/Shift+Tab cycles within the container                                |
| `asChild`            | `boolean`     | Merge props onto the child element instead of creating a wrapper `<div>` |
| `onMountAutoFocus`   | `(e) => void` | Override the default auto-focus target                                   |
| `onUnmountAutoFocus` | `(e) => void` | Override where focus returns on unmount                                  |

> **Prefer shadcn `Dialog`** over a manual `FocusScope` whenever possible - the
> shadcn `Dialog` component wraps `FocusScope` and also handles `aria-modal`,
> `role="dialog"`, Escape key dismissal, and return focus automatically.

## Return Focus Pattern

```tsx
function Modal({ open, onClose }) {
    const triggerRef = useRef<HTMLElement | null>(null);

    useEffect(() => {
        if (open) {
            triggerRef.current = document.activeElement as HTMLElement;
        } else {
            triggerRef.current?.focus();
        }
    }, [open]);
}
```

---

## Focus Not Obscured (WCAG 2.4.11 AA)

When a sticky header or fixed toolbar is present, a focused element must not be
**completely** hidden by the overlay. Minimum AA requirement: the focused element
must be at least partially visible. AAA (2.4.12): fully visible.

**Global fix — `scroll-margin-top`:**

```css
/* src/client/index.css  (add inside the :root block or after it) */
:root {
  --header-height: 64px; /* update if the header height changes */
}

*:focus-visible {
  scroll-margin-top: calc(var(--header-height) + 1rem);
}
```

**Dynamic header height with a hook** (when the header can resize):

```tsx
// src/client/hooks/useHeaderHeight.ts
import { useEffect } from "react";

export function useHeaderHeight(headerRef: React.RefObject<HTMLElement | null>) {
  useEffect(() => {
    const header = headerRef.current;
    if (!header) return;

    const update = () => {
      document.documentElement.style.setProperty(
        "--header-height",
        `${header.offsetHeight}px`,
      );
    };

    update();
    const ro = new ResizeObserver(update);
    ro.observe(header);
    return () => ro.disconnect();
  }, [headerRef]);
}
```

```tsx
// AppLayout.tsx
import { useHeaderHeight } from "@/hooks/useHeaderHeight";

export function AppLayout({ children }: { children: React.ReactNode }) {
  const headerRef = useRef<HTMLElement>(null);
  useHeaderHeight(headerRef);

  return (
    <>
      <header ref={headerRef} className="fixed top-0 inset-x-0 z-40 h-16 bg-background border-b">
        {/* nav */}
      </header>
      <main id="main-content" tabIndex={-1} className="outline-none pt-16">
        {children}
      </main>
    </>
  );
}
```

> See [`wcag22-new-criteria.md`](./wcag22-new-criteria.md) for the full 2.4.11 implementation with testing steps.

---

## Skip Link Focus Target

The `<main>` element (or any skip target) must accept programmatic focus so the
skip link actually moves focus there. Add `tabIndex={-1}` to allow it — this does
NOT make the element keyboard-tabbable, only programmatically focusable.

```tsx
// The href="#main-content" skip link jumps here:
<main
  id="main-content"
  tabIndex={-1}
  className="outline-none"   // hide the default focus ring on the container
>
  {children}
</main>
```

> **Anti-pattern:** Omitting `tabIndex={-1}` causes some browsers (Firefox) to
> ignore the scroll-into-view and focus activation triggered by the skip link.

---

## Route Change Focus Management

After a client-side route transition, focus must be moved to an appropriate
landmark so screen reader users know the page has changed.

### Option A — RouteAnnouncer (recommended, covered in SKILL.md)

Renders a visually-hidden `role="status"` region that announces the new page
title. Works well when you also update the document title.

### Option B — Focus the `<main>` element directly

```tsx
// src/client/hooks/useRouteFocus.ts
import { useEffect } from "react";
import { useLocation } from "react-router-dom";

/**
 * After each navigation, move focus to #main-content so screen reader
 * users are positioned at the top of the new page content.
 */
export function useRouteFocus() {
  const { pathname } = useLocation();

  useEffect(() => {
    // Small delay: let the new route's content mount before stealing focus
    const id = setTimeout(() => {
      const main = document.getElementById("main-content");
      main?.focus({ preventScroll: false });
    }, 100);

    return () => clearTimeout(id);
  }, [pathname]);
}
```

```tsx
// App.tsx — call once at the router root
function App() {
  useRouteFocus();
  return <Outlet />;
}
```

| Approach | Pros | Cons |
| -------- | ---- | ---- |
| RouteAnnouncer | Announces page title naturally | Requires consistent `useDocumentTitle` usage |
| `useRouteFocus` | Zero dependencies, works with any router | Moves caret position abruptly for AT users with virtual cursor |
| Both combined | Maximum compatibility | Slight redundancy — test with real screen readers |

---

## Dialog Focus Auto-Focus Override

By default `FocusScope` focuses the first focusable element in the dialog.
Override this to focus a specific element (e.g. the heading or a descriptive paragraph):

```tsx
<FocusScope
  loop
  trapped
  onMountAutoFocus={(e) => {
    e.preventDefault(); // prevent default first-focusable behavior
    headingRef.current?.focus();
  }}
  onUnmountAutoFocus={(e) => {
    e.preventDefault();
    triggerRef.current?.focus();
  }}
>
  <div role="dialog" aria-labelledby="dialog-title">
    <h2 id="dialog-title" tabIndex={-1} ref={headingRef} className="outline-none">
      Confirm deletion
    </h2>
    {/* ... */}
  </div>
</FocusScope>
```

> Focus the heading rather than the first button when the dialog contains
> a destructive action — this gives the user context before they interact.

---

## Skip Links

Skip links let keyboard users bypass repeated navigation — required by WCAG 2.4.1 (Level A).

```tsx
// src/client/components/SkipLink.tsx
export function SkipLink() {
  return (
    <a
      href="#main-content"
      className={[
        "sr-only focus:not-sr-only",       // hidden until focused
        "fixed left-4 top-4 z-[9999]",     // above all other content
        "rounded-md bg-background px-4 py-2",
        "text-sm font-medium text-foreground",
        "ring-2 ring-ring focus-visible:outline-none",
      ].join(" ")}
    >
      Skip to main content
    </a>
  );
}
```

```tsx
// src/client/App.tsx — must be the FIRST focusable element on the page
export function App() {
  return (
    <>
      <SkipLink />
      <RouteAnnouncer />
      <AppLayout>
        <Routes>...</Routes>
      </AppLayout>
    </>
  );
}
```

**Requirements:**

- First focusable element in DOM order
- Visible when focused (`sr-only focus:not-sr-only`)
- Target `#main-content` must have `tabIndex={-1}` so it can receive programmatic focus
- For multi-section pages add more links: "Skip to search", "Skip to filters"

---

## Page Title Management

WCAG 2.4.2 (Level A): each page needs a unique, descriptive `document.title` that updates on every route change.

```tsx
// src/client/hooks/useDocumentTitle.ts
import { useEffect } from "react";

const SITE_NAME = "Your App Name";

export function useDocumentTitle(pageTitle: string) {
  useEffect(() => {
    const previous = document.title;
    // Format: "Most Specific — Site Name"
    document.title = `${pageTitle} — ${SITE_NAME}`;
    return () => { document.title = previous; };
  }, [pageTitle]);
}
```

```tsx
// Usage — call in every route component
function DashboardPage() {
  useDocumentTitle("Dashboard");
  return <main id="main-content" tabIndex={-1}>...</main>;
}

function UserProfilePage({ username }: { username: string }) {
  useDocumentTitle(`${username}'s Profile`);
  return <main id="main-content" tabIndex={-1}>...</main>;
}
```

**Route-change announcer** — tells screen readers the page changed without moving focus:

```tsx
// src/client/components/RouteAnnouncer.tsx
import { useEffect, useRef } from "react";
import { useLocation } from "react-router-dom";

export function RouteAnnouncer() {
  const { pathname } = useLocation();
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // Wait for useDocumentTitle to update document.title first
    const timer = setTimeout(() => {
      if (ref.current) ref.current.textContent = `Navigated to ${document.title}`;
    }, 100);
    return () => clearTimeout(timer);
  }, [pathname]);

  return (
    <div
      ref={ref}
      role="status"
      aria-live="polite"
      aria-atomic="true"
      className="sr-only"
    />
  );
}
```

Add `<RouteAnnouncer />` once inside `<App />`, alongside `<SkipLink />`.
