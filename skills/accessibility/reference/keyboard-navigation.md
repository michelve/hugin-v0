# Keyboard Navigation

## Required Keys by Component Type

| Component     | Keys                                                              |
| ------------- | ----------------------------------------------------------------- |
| Button        | `Enter`, `Space` to activate                                      |
| Link          | `Enter` to navigate                                               |
| Menu/Dropdown | `Arrow Up/Down` to navigate, `Enter` to select, `Escape` to close |
| Tabs          | `Arrow Left/Right` to switch, `Home/End` for first/last           |
| Modal         | `Tab` to cycle focus, `Escape` to close                           |
| Checkbox      | `Space` to toggle                                                 |
| Radio         | `Arrow Up/Down` to change selection                               |

## useKeyPress Hook

Create this hook at `src/client/hooks/useKeyPress.ts` (`@/hooks/useKeyPress`):

```ts
// src/client/hooks/useKeyPress.ts
import { useEffect } from "react";

export function useKeyPress(keys: string[], handler: (e: KeyboardEvent) => void) {
    useEffect(() => {
        const listener = (e: KeyboardEvent) => {
            if (keys.includes(e.key)) {
                handler(e);
            }
        };
        window.addEventListener("keydown", listener);
        return () => window.removeEventListener("keydown", listener);
    }, [keys, handler]);
}
```

Usage example:

```tsx
import { useKeyPress } from "@/hooks/useKeyPress";

function SearchModal() {
    const [isOpen, setIsOpen] = useState(false);

    // Cmd+K or Ctrl+K to open search
    useKeyPress(["k"], (e) => {
        if (e.metaKey || e.ctrlKey) {
            e.preventDefault();
            setIsOpen(true);
        }
    });

    // Escape to close
    useKeyPress(["Escape"], () => setIsOpen(false));

    return isOpen ? <SearchDialog onClose={() => setIsOpen(false)} /> : null;
}
```

## Inline Arrow Key Navigation

For single-use keyboard handlers, use an inline `onKeyDown` - no utility import needed:

```tsx
// Vertical navigation (menus, lists)
const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "ArrowUp") {
        e.preventDefault();
        focusPreviousItem();
    } else if (e.key === "ArrowDown") {
        e.preventDefault();
        focusNextItem();
    } else if (e.key === "Escape") {
        onClose?.();
    } else if (e.key === "Enter") {
        onActivate?.();
    }
};

// Horizontal navigation (tabs, toolbars)
const handleHorizontal = (e: React.KeyboardEvent) => {
    if (e.key === "ArrowLeft") selectPrevious();
    if (e.key === "ArrowRight") selectNext();
};
```

> **Note:** For complex components (menus, comboboxes, data grids), use the shadcn
> `DropdownMenu`, `Select`, or `Combobox` components instead - they handle roving
> tabindex and arrow key navigation automatically via Radix primitives.
