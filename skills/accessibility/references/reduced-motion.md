# Reduced Motion

## useReducedMotion Hook

Create this hook at `src/client/hooks/useReducedMotion.ts` (`@/hooks/useReducedMotion`):

```ts
// src/client/hooks/useReducedMotion.ts
import { useEffect, useState } from "react";

export function useReducedMotion(): boolean {
    const [prefersReducedMotion, setPrefersReducedMotion] = useState(
        () => window.matchMedia("(prefers-reduced-motion: reduce)").matches,
    );

    useEffect(() => {
        const mq = window.matchMedia("(prefers-reduced-motion: reduce)");
        const handler = (e: MediaQueryListEvent) => setPrefersReducedMotion(e.matches);
        mq.addEventListener("change", handler);
        return () => mq.removeEventListener("change", handler);
    }, []);

    return prefersReducedMotion;
}
```

Usage:

```tsx
import { useReducedMotion } from "@/hooks/useReducedMotion";

function AnimatedComponent() {
    const prefersReducedMotion = useReducedMotion();

    return (
        <div
            style={{
                transition: prefersReducedMotion ? "none" : "transform 0.3s ease",
            }}
        >
            Content
        </div>
    );
}
```

## Tailwind Variant (preferred)

For most cases, use Tailwind's `motion-reduce:` variant directly on the element —
no hook required:

```tsx
<div className="transition-transform duration-300 motion-reduce:transition-none">
  Content
</div>

<div className="animate-spin motion-reduce:animate-none">
  <Spinner />
</div>
```

## CSS Alternative

For project-level CSS overrides, add to `src/client/custom.css`:

```css
@media (prefers-reduced-motion: reduce) {
    .animated {
        animation: none;
        transition: none;
    }
}
```

---

## WCAG 2.3.3 — Animation from Interactions (AAA)

**Criterion:** Motion triggered by user interaction (e.g. hover effects, click
animations, parallax scrolling) can be disabled unless the motion is essential.

This is an **AAA** criterion — meaning it is aspirational, not mandatory for AA
conformance — but it is the right thing to do for users with vestibular disorders.

**Tailwind pattern:**

```tsx
// Suppress all decorative transitions/animations at the component level
<div className="transition-transform duration-300 hover:-translate-y-1
                motion-reduce:transition-none motion-reduce:hover:translate-y-0">
  Hover card
</div>
```

**CSS-level blanket rule** (add to `src/client/index.css`):

```css
@media (prefers-reduced-motion: reduce) {
  /* Kill decorative motion globally — override per-element only when essential */
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

> **Note:** The global override uses `0.01ms` (not `0`) so that JavaScript
> `transitionend` / `animationend` events still fire reliably.

---

## Framer Motion Integration

When Framer Motion is already in use, prefer its built-in `useReducedMotion` hook
over a custom implementation — the library's hook handles edge cases and SSR.

```tsx
import { motion, useReducedMotion } from "framer-motion";

function AnimatedCard({ children }: { children: React.ReactNode }) {
  const shouldReduceMotion = useReducedMotion();

  return (
    <motion.div
      initial={{ opacity: 0, y: shouldReduceMotion ? 0 : 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: shouldReduceMotion ? 0 : -20 }}
      transition={{ duration: shouldReduceMotion ? 0 : 0.3 }}
    >
      {children}
    </motion.div>
  );
}
```

**Framer Motion `MotionConfig` (apply globally):**

```tsx
import { MotionConfig, useReducedMotion } from "framer-motion";

function App() {
  const shouldReduceMotion = useReducedMotion();

  return (
    <MotionConfig reducedMotion={shouldReduceMotion ? "always" : "never"}>
      <Router>
        <Outlet />
      </Router>
    </MotionConfig>
  );
}
```

> `reducedMotion="user"` (the Framer default) also works and respects the OS
> setting automatically, but the explicit hook allows you to combine it with a
> user-level preference toggle in your app settings.

---

## User Preference Toggle (Opt-in / Opt-out)

Some users have motion turned **on** at the OS level but want to reduce it within
your application. Provide an in-app setting that overrides the OS preference.

```tsx
// src/client/hooks/useMotionPreference.ts
import { useEffect, useState } from "react";

type MotionPreference = "system" | "reduce" | "full";

export function useMotionPreference() {
  const [preference, setPreference] = useState<MotionPreference>(
    () => (localStorage.getItem("motion-preference") as MotionPreference) ?? "system",
  );

  const systemReduces = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  const shouldReduce =
    preference === "reduce" || (preference === "system" && systemReduces);

  const update = (p: MotionPreference) => {
    setPreference(p);
    localStorage.setItem("motion-preference", p);
  };

  return { shouldReduce, preference, setPreference: update };
}
```

```tsx
// Settings page
function MotionSetting() {
  const { preference, setPreference } = useMotionPreference();

  return (
    <fieldset>
      <legend>Animation preferences</legend>
      {(["system", "reduce", "full"] as const).map((value) => (
        <label key={value}>
          <input
            type="radio"
            name="motion"
            value={value}
            checked={preference === value}
            onChange={() => setPreference(value)}
          />
          {value === "system" ? "Use system setting" : value === "reduce" ? "Reduce motion" : "Full motion"}
        </label>
      ))}
    </fieldset>
  );
}
```
