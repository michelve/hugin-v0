# Keyboard Navigation Patterns

Complete keyboard navigation patterns for draft_v0 components (React 19 + shadcn/ui).

## Focus Management

### Focus Order

```tsx
// Natural tab order (preferred)
<button>First</button>    {/* tabIndex: 0 (default) */}
<button>Second</button>   {/* tabIndex: 0 (default) */}
<button>Third</button>    {/* tabIndex: 0 (default) */}

// Remove from tab order (still programmatically focusable)
<button tabIndex={-1}>Skip</button>

// Never use positive tabIndex values
// ❌ <button tabIndex={1}>Don't do this</button>
```

### Focus Trap Hook

```tsx
import { useEffect, useRef } from "react";

export function useFocusTrap(containerRef: React.RefObject<HTMLElement>, isActive: boolean) {
    useEffect(() => {
        if (!isActive || !containerRef.current) return;

        const container = containerRef.current;
        const focusableElements = container.querySelectorAll<HTMLElement>(
            'button:not([disabled]), [href], input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])',
        );

        const firstFocusable = focusableElements[0];
        const lastFocusable = focusableElements[focusableElements.length - 1];

        // Focus first element
        firstFocusable?.focus();

        const handleKeyDown = (event: KeyboardEvent) => {
            if (event.key !== "Tab") return;

            if (event.shiftKey) {
                // Shift+Tab: wrap from first to last
                if (document.activeElement === firstFocusable) {
                    event.preventDefault();
                    lastFocusable?.focus();
                }
            } else {
                // Tab: wrap from last to first
                if (document.activeElement === lastFocusable) {
                    event.preventDefault();
                    firstFocusable?.focus();
                }
            }
        };

        container.addEventListener("keydown", handleKeyDown);
        return () => container.removeEventListener("keydown", handleKeyDown);
    }, [containerRef, isActive]);
}
```

### Return Focus

```tsx
export function useReturnFocus(isOpen: boolean) {
    const triggerRef = useRef<HTMLElement | null>(null);

    useEffect(() => {
        if (isOpen) {
            // Store the element that triggered the open
            triggerRef.current = document.activeElement as HTMLElement;
        } else if (triggerRef.current) {
            // Return focus when closed
            triggerRef.current.focus();
            triggerRef.current = null;
        }
    }, [isOpen]);
}
```

## Key Event Handlers

### Key Detection Utilities

```tsx
// utils/keyboard.ts
export const isEnterKey = (event: KeyboardEvent | React.KeyboardEvent) => event.key === "Enter";

export const isSpaceKey = (event: KeyboardEvent | React.KeyboardEvent) =>
    event.key === " " || event.key === "Spacebar";

export const isEscapeKey = (event: KeyboardEvent | React.KeyboardEvent) =>
    event.key === "Escape" || event.key === "Esc";

export const isArrowKey = (event: KeyboardEvent | React.KeyboardEvent) =>
    ["ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight"].includes(event.key);

export const isArrowDown = (event: KeyboardEvent | React.KeyboardEvent) =>
    event.key === "ArrowDown";

export const isArrowUp = (event: KeyboardEvent | React.KeyboardEvent) => event.key === "ArrowUp";

export const isArrowLeft = (event: KeyboardEvent | React.KeyboardEvent) =>
    event.key === "ArrowLeft";

export const isArrowRight = (event: KeyboardEvent | React.KeyboardEvent) =>
    event.key === "ArrowRight";

export const isTabKey = (event: KeyboardEvent | React.KeyboardEvent) => event.key === "Tab";

export const isHomeKey = (event: KeyboardEvent | React.KeyboardEvent) => event.key === "Home";

export const isEndKey = (event: KeyboardEvent | React.KeyboardEvent) => event.key === "End";
```

### Menu Keyboard Handler

```tsx
const handleMenuKeyDown = (event: React.KeyboardEvent) => {
    const items = menuRef.current?.querySelectorAll<HTMLElement>('[role="menuitem"]');
    if (!items?.length) return;

    const currentIndex = Array.from(items).findIndex((item) => item === document.activeElement);

    switch (event.key) {
        case "ArrowDown":
            event.preventDefault();
            const nextIndex = (currentIndex + 1) % items.length;
            items[nextIndex].focus();
            break;

        case "ArrowUp":
            event.preventDefault();
            const prevIndex = (currentIndex - 1 + items.length) % items.length;
            items[prevIndex].focus();
            break;

        case "Home":
            event.preventDefault();
            items[0].focus();
            break;

        case "End":
            event.preventDefault();
            items[items.length - 1].focus();
            break;

        case "Escape":
            event.preventDefault();
            closeMenu();
            break;

        case "Enter":
        case " ":
            event.preventDefault();
            (document.activeElement as HTMLElement)?.click();
            break;
    }
};
```

### Tab Keyboard Handler

```tsx
const handleTabKeyDown = (event: React.KeyboardEvent, tabIndex: number) => {
    switch (event.key) {
        case "ArrowRight":
            event.preventDefault();
            const nextTab = (tabIndex + 1) % tabs.length;
            setActiveTab(nextTab);
            tabRefs.current[nextTab]?.focus();
            break;

        case "ArrowLeft":
            event.preventDefault();
            const prevTab = (tabIndex - 1 + tabs.length) % tabs.length;
            setActiveTab(prevTab);
            tabRefs.current[prevTab]?.focus();
            break;

        case "Home":
            event.preventDefault();
            setActiveTab(0);
            tabRefs.current[0]?.focus();
            break;

        case "End":
            event.preventDefault();
            setActiveTab(tabs.length - 1);
            tabRefs.current[tabs.length - 1]?.focus();
            break;
    }
};
```

### Grid/Table Keyboard Handler

```tsx
const handleGridKeyDown = (event: React.KeyboardEvent, row: number, col: number) => {
    switch (event.key) {
        case "ArrowRight":
            event.preventDefault();
            if (col < columns - 1) focusCell(row, col + 1);
            break;

        case "ArrowLeft":
            event.preventDefault();
            if (col > 0) focusCell(row, col - 1);
            break;

        case "ArrowDown":
            event.preventDefault();
            if (row < rows - 1) focusCell(row + 1, col);
            break;

        case "ArrowUp":
            event.preventDefault();
            if (row > 0) focusCell(row - 1, col);
            break;

        case "Home":
            event.preventDefault();
            if (event.ctrlKey) {
                focusCell(0, 0); // First cell
            } else {
                focusCell(row, 0); // First in row
            }
            break;

        case "End":
            event.preventDefault();
            if (event.ctrlKey) {
                focusCell(rows - 1, columns - 1); // Last cell
            } else {
                focusCell(row, columns - 1); // Last in row
            }
            break;
    }
};
```

## Roving TabIndex

For composite widgets where only one element should be in tab order:

```tsx
export function useRovingTabIndex<T extends HTMLElement>(items: T[], activeIndex: number) {
    return items.map((item, index) => ({
        tabIndex: index === activeIndex ? 0 : -1,
        ref: (el: T | null) => {
            if (el) items[index] = el;
        },
    }));
}

// Usage in tabs
function Tabs({ tabs }: TabsProps) {
    const [activeIndex, setActiveIndex] = useState(0);
    const tabRefs = useRef<HTMLButtonElement[]>([]);

    return (
        <div role="tablist">
            {tabs.map((tab, index) => (
                <button
                    key={tab.id}
                    role="tab"
                    ref={(el) => (tabRefs.current[index] = el!)}
                    tabIndex={index === activeIndex ? 0 : -1}
                    aria-selected={index === activeIndex}
                    onClick={() => setActiveIndex(index)}
                    onKeyDown={(e) => handleTabKeyDown(e, index)}
                >
                    {tab.label}
                </button>
            ))}
        </div>
    );
}
```

## Skip Links

```tsx
// Add at the very top of your app
export function SkipLink() {
    return (
        <a
            href="#main-content"
            className="skip-link"
            // CSS: .skip-link { position: absolute; left: -9999px; }
            // CSS: .skip-link:focus { left: 0; }
        >
            Skip to main content
        </a>
    );
}

// Then in your layout:
<main id="main-content" tabIndex={-1}>
    {/* Main content */}
</main>;
```

## Testing Keyboard Navigation

```tsx
describe("Keyboard Navigation", () => {
    it("traps focus in modal", async () => {
        const user = userEvent.setup();
        render(
            <Modal isOpen onClose={() => {}}>
                <button>First</button>
                <button>Second</button>
                <button>Third</button>
            </Modal>,
        );

        // Focus should start on first focusable
        expect(screen.getByText("First")).toHaveFocus();

        // Tab through
        await user.tab();
        expect(screen.getByText("Second")).toHaveFocus();

        await user.tab();
        expect(screen.getByText("Third")).toHaveFocus();

        // Wrap to first
        await user.tab();
        expect(screen.getByText("First")).toHaveFocus();

        // Shift+Tab wraps to last
        await user.tab({ shift: true });
        expect(screen.getByText("Third")).toHaveFocus();
    });

    it("navigates menu with arrow keys", async () => {
        const user = userEvent.setup();
        render(<Menu items={["One", "Two", "Three"]} />);

        await user.click(screen.getByRole("button", { name: "Menu" }));

        // First item focused
        expect(screen.getByRole("menuitem", { name: "One" })).toHaveFocus();

        // Arrow down
        await user.keyboard("{ArrowDown}");
        expect(screen.getByRole("menuitem", { name: "Two" })).toHaveFocus();

        // Arrow down wraps
        await user.keyboard("{ArrowDown}");
        await user.keyboard("{ArrowDown}");
        expect(screen.getByRole("menuitem", { name: "One" })).toHaveFocus();

        // Escape closes
        await user.keyboard("{Escape}");
        expect(screen.queryByRole("menu")).not.toBeInTheDocument();
    });
});
```

## Focus Visible Styles

```css
/* Only show focus ring for keyboard users */
:focus-visible {
    outline: 2px solid var(--color-focus-ring);
    outline-offset: 2px;
}

/* Remove default outline for mouse users */
:focus:not(:focus-visible) {
    outline: none;
}

/* High contrast focus for better visibility */
@media (prefers-contrast: more) {
    :focus-visible {
        outline-width: 3px;
    }
}
```
