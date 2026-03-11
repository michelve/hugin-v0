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
