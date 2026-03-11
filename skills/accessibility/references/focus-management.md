# Focus Management

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
