---
name: dsai-components
description: >-
  Comprehensive reference for the DSAI component library. Guides AI agents on
  installing, importing, composing, and extending DSAI components in consumer
  projects. Covers the full component catalog (38+), type system, FSM patterns,
  compound components, hooks, utilities, and critical conventions.

---

# DSAI Component Library Reference

## Installation

Components are installed via the `dsai` CLI — **not** npm/yarn/pnpm install.

```bash
dsai add button              # Single component
dsai add button modal card   # Multiple components
dsai add --all               # All components
dsai add --type hook          # All hooks
```

This copies source files into the consumer project at `src/client/components/ui/<name>/`. Components are **local source code** that you own and can modify.

The registry resolves dependencies via BFS + topological sort, transforms relative imports to path aliases (`@/`), and writes to configured alias directories (`components/ui/`, `hooks/`, `utils/`). Existing files are never overwritten unless the `--overwrite` flag is passed.

## Quick Start

After installing a component with `dsai add`, import it, render it, and customize:

```tsx
// 1. Import the component from your local source
import { Button } from '@/components/ui/button';

// 2. Render it
function App() {
  return (
    <Button variant="primary" size="md" onClick={() => alert('Clicked!')}>
      Get Started
    </Button>
  );
}

// 3. Customize with DSAI tokens (see dsai-styling skill)
// Components use Bootstrap 5 classes + --dsai-* CSS custom properties
// Use cn() for conditional classes — NOT tailwind-merge or clsx
```

### Import Patterns

**Components** — import from `@/components/ui/<name>`:

```tsx
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { Modal } from '@/components/ui/modal';
```

**Type imports** — import from the `.types` file:

```tsx
import type { ButtonProps } from '@/components/ui/button/Button.types';
import type { CardProps } from '@/components/ui/card/Card.types';
import type { ModalProps } from '@/components/ui/modal/Modal.types';
```

**Hooks** — import from `@/hooks/`:

```tsx
import { useControllableState } from '@/hooks/useControllableState';
import { useFocusTrap } from '@/hooks/useFocusTrap';
import { useDarkMode } from '@/hooks/useDarkMode';
```

**Utilities** — import from `@/utils/` or `@/lib/`:

```tsx
import { cn } from '@/utils/cn';
import { sanitizeHtml } from '@/utils/sanitize';
```

> **Note:** `@dsai-io/react` is the internal monorepo package. Consumer projects import from `@/components/ui/<name>` — never from `@dsai-io/react`.

> **Styling:** Components use Bootstrap 5 classes and `--dsai-*` CSS custom properties. See the **dsai-styling** skill for token usage, `cn()` patterns, and dark mode.

---

## Component Architecture Pattern

Every component follows `forwardRef` with an explicit `displayName`:

```tsx
export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  function Button(props, ref) {
    /* ... */
  }
);
Button.displayName = 'Button';
```

For performance-optimized components: `memo(forwardRef(function Name(...)))` + `displayName`.

## File Structure Per Component

Each component directory contains:

| File | Purpose |
|---|---|
| `ComponentName.tsx` | Main component with `forwardRef` |
| `ComponentName.types.ts` | TypeScript prop interfaces (always separate) |
| `ComponentName.fsm.ts` | Finite State Machine (interactive components) |
| `ComponentName.test.tsx` | Unit tests (Jest 30 + React Testing Library) |
| `ComponentName.a11y.test.tsx` | Accessibility tests (jest-axe) |
| `index.ts` | Barrel exports |

---

## Complete Component Catalog

### Layout & Structure

#### Accordion
Collapsible sections.

#### Breadcrumb / BreadcrumbItem
Navigation breadcrumbs.

#### Card (compound)
Sub-components: `Card.Header`, `Card.Body`, `Card.Footer`, `Card.Image`, `Card.Title`, `Card.Subtitle`, `Card.Text`, `Card.Link`, `Card.ImgOverlay`

| Prop | Type | Notes |
|---|---|---|
| `variant` | `'elevated' \| 'outlined' \| 'ghost'` | Visual style |
| `color` | `SemanticColorVariant` | Semantic color |
| `size` | `'sm' \| 'md' \| 'lg'` | Component size |
| `horizontal` | `boolean` | Horizontal layout |
| `interactive` | `boolean` | Hover/active states |
| `href` | `string` | Makes card a link |

```tsx
<Card variant="elevated" color="primary">
  <Card.Header>Title</Card.Header>
  <Card.Body>Content</Card.Body>
  <Card.Footer>Actions</Card.Footer>
</Card>
```

#### CardList
List of cards.

#### Carousel
Sub-components: `CarouselItem`, `CarouselControl`, `CarouselIndicators`, `CarouselCaption`, `CarouselPauseButton`

#### Container
Layout container.

#### Modal (compound)
Sub-components: `Modal.Header`, `Modal.Body`, `Modal.Footer`, `Modal.Title`, `Modal.Description`

Portal rendering, focus trap, scroll lock, FSM-driven animations.

| Prop | Type | Notes |
|---|---|---|
| `isOpen` | `boolean` | Controlled open state |
| `onClose` | `() => void` | Close callback |
| `size` | `'sm' \| 'md' \| 'lg' \| 'xl' \| 'fullscreen'` | Modal size |
| `centered` | `boolean` | Vertically centered |
| `backdrop` | `boolean \| 'static'` | Backdrop behavior |
| `closeOnEscape` | `boolean` | ESC key closes modal |
| `initialFocusRef` | `RefObject` | Focus target on open |

```tsx
<Modal isOpen={open} onClose={close}>
  <Modal.Header closeButton>Edit Profile</Modal.Header>
  <Modal.Body>Form content</Modal.Body>
  <Modal.Footer>
    <Button onClick={close}>Save</Button>
  </Modal.Footer>
</Modal>
```

#### Navbar
Navigation bar.

#### Sheet
Side panel overlay.

#### Tabs (compound)
Sub-components: `Tab`, `TabList`, `TabPanel`

| Prop | Type | Notes |
|---|---|---|
| `variant` | `'underline' \| 'pills' \| 'tabs'` | Visual style |
| `orientation` | `'horizontal' \| 'vertical'` | Tab direction |
| `activationMode` | `'automatic' \| 'manual'` | Focus vs click activation |
| `lazyMount` | `boolean` | Lazy render panels |
| `unmountOnExit` | `boolean` | Unmount inactive panels |

```tsx
<Tabs variant="pills" orientation="horizontal">
  <TabList aria-label="Settings">
    <Tab id="general">General</Tab>
    <Tab id="security">Security</Tab>
  </TabList>
  <TabPanel id="general">General settings</TabPanel>
  <TabPanel id="security">Security settings</TabPanel>
</Tabs>
```

#### TabsPro
Enhanced tabs with closable and addable tabs.

### Form Controls

#### Button
FSM-based interactive component.

| Prop | Type | Notes |
|---|---|---|
| `variant` | `SemanticColorVariant \| 'outline-*' \| 'subtle-*' \| 'ghost' \| 'link'` | Visual style |
| `size` | `'sm' \| 'md' \| 'lg' \| 'icon'` | Button size |
| `loading` | `boolean` | Shows spinner, disables interaction |
| `error` | `boolean` | Error visual state |
| `disabled` | `boolean` | Disabled state |
| `startIcon` | `ReactNode` | Icon before label |
| `endIcon` | `ReactNode` | Icon after label |
| `announceText` | `string` | Screen reader announcement |
| `as` | `ElementType` | Polymorphic — renders as `button`, `a`, or custom |

FSM states: `idle → hovered → focused → pressed → disabled → loading → error`

FSM events: `HOVER`, `BLUR`, `FOCUS`, `PRESS`, `RELEASE`, `DISABLE`, `ENABLE`, `START_LOADING`, `STOP_LOADING`, `ERROR`, `CLEAR_ERROR`

#### Checkbox / CheckboxGroup
Check controls.

#### Input
Text input with built-in validation.

| Prop | Type | Notes |
|---|---|---|
| `type` | `'text' \| 'email' \| 'password' \| 'number' \| 'tel' \| 'url' \| 'search'` | Input type |
| `size` | `'sm' \| 'md' \| 'lg'` | Input size |
| `label` | `string` | Associated label |
| `helperText` | `string` | Help text below input |
| `error` | `string \| boolean` | Error message or state |
| `success` | `string \| boolean` | Success state |
| `prefix` | `ReactNode` | Left addon |
| `suffix` | `ReactNode` | Right addon |
| `clearable` | `boolean` | Show clear button |
| `showCount` | `boolean` | Character count |
| `floating` | `boolean` | Floating label |
| `plaintext` | `boolean` | Read-only plain text |

#### Radio / RadioGroup
Radio controls.

#### Select
Generic typed dropdown select.

| Prop | Type | Notes |
|---|---|---|
| `SelectProps<T>` | Generic | Typed to option shape |
| `multiple` | `boolean` | Multi-select |
| `searchable` | `boolean` | Filterable options |
| `clearable` | `boolean` | Clear selection |
| `loading` | `boolean` | Loading state |
| `renderOption` | `(option: T) => ReactNode` | Custom option rendering |
| `renderValue` | `(value: T) => ReactNode` | Custom value rendering |

#### Switch
Toggle switch.

#### SearchSelectField
Searchable select variant.

#### SelectableCard
Card that acts as a selection control.

### Display & Feedback

#### Alert
Notification banners.

#### Avatar / AvatarGroup
User avatars.

#### Badge / BadgeWrapper
Status indicators.

#### Display
Large display text.

#### Heading
`h1`–`h6` elements.

#### Text
Paragraph text.

#### Typography
Combined typography component.

#### ListGroup / ListGroupItem
List displays.

#### Pagination
Page navigation.

#### Popover (compound)
Sub-components: `PopoverHeader`, `PopoverBody`, `PopoverCloseButton`

#### Progress
Progress bars.

#### Scrollspy
Scroll-based navigation highlighting.

#### Spinner
Loading indicators.

#### Table
Data tables.

#### Toast / ToastContainer / ToastProvider
Toast notifications.

#### Tooltip / TooltipProvider / TooltipGroup
Tooltips.

#### Dropdown
Dropdown menus.

---

## Type System

### Core Primitives

Defined in `types/primitives.ts`:

```typescript
type SemanticColorVariant = 'primary' | 'secondary' | 'success' | 'danger' | 'warning' | 'info' | 'light' | 'dark';
type ComponentSize = 'sm' | 'md' | 'lg';
type ExtendedSize = 'xs' | 'sm' | 'md' | 'lg' | 'xl' | '2xl' | 'xxl';
type FeedbackVariant = 'success' | 'error' | 'warning' | 'info' | 'default';
type Alignment = 'start' | 'center' | 'end';
type Orientation = 'horizontal' | 'vertical';
```

### Polymorphic Components

```typescript
type PolymorphicComponentProps<C extends React.ElementType, Props> =
  Props &
  Omit<React.ComponentPropsWithRef<C>, keyof Props> &
  { as?: C };
```

### SafeHTMLAttributes (Security)

**Allowed:** `className`, `style`, `id`, `title`, `tabIndex`, `data-testid`, `role`, and ARIA attributes.

**Blocked:** `onClick`, `onMouseOver`, `onLoad`, `dangerouslySetInnerHTML`, and all event handlers.

Components define their own safe event handler props explicitly. Never spread unknown props.

### FSM Types

```typescript
interface FSMStateBase { status?: string; }
interface FSMEventBase { type: string; }
type FSMReducer<State, Event> = (state: State, event: Event) => State;
interface VisualStateBase { state: string; shouldRender: boolean; modifiers?: string[]; }
```

---

## Patterns

### FSM Pattern (Interactive Components)

Interactive components use `useReducer` with a finite state machine:

```tsx
const [fsmState, dispatch] = useReducer(
  buttonFSMReducer,
  initialProps,
  createInitialButtonFSMState
);
```

Events dispatched: `HOVER`, `BLUR`, `FOCUS`, `PRESS`, `RELEASE`, `DISABLE`, `ENABLE`, `START_LOADING`, `STOP_LOADING`, `ERROR`, `CLEAR_ERROR`

### Compound Component Pattern

Parent and children communicate via React Context:

```tsx
<Card variant="elevated" color="primary">
  <Card.Header>Title</Card.Header>
  <Card.Body>Content</Card.Body>
  <Card.Footer>Actions</Card.Footer>
</Card>
```

### Controlled / Uncontrolled Pattern

Components support both modes via the `useControllableState` hook:

```tsx
// Controlled
<Select value={selected} onChange={setSelected} options={options} />

// Uncontrolled
<Select defaultValue="option1" options={options} />
```

### cn() Utility

Simple class name composition (NOT tailwind-merge). Uses Bootstrap 5 class naming:

```tsx
cn('btn', variant && `btn-${variant}`, size === 'lg' && 'btn-lg', className)
// Filters falsy values, joins with space
```

---

## Hooks (24)

### Accessibility
- `useFocusTrap` — Trap focus within a container
- `useRovingFocus` — Arrow-key focus navigation
- `useReducedMotion` — Detect `prefers-reduced-motion`

### UI
- `useMediaQuery` — Match media queries
- `useIsMobile` / `useIsTablet` / `useIsDesktop` / `useIsLargeDesktop` — Breakpoint hooks
- `useScrollLock` — Prevent body scroll
- `useDarkMode` — Dark mode state

### State
- `useControllableState` — Controlled/uncontrolled state
- `usePrevious` — Previous value
- `useLocalStorage` / `useSessionStorage` — Persisted state
- `useDebounce` / `useThrottle` — Timing

### Form
- `useField` — Field-level state and validation
- `useForm` — Form state management

### Event
- `useClickOutside` — Detect clicks outside element
- `useKeyPress` — Key event handling
- `useHover` — Hover detection
- `useIntersectionObserver` — Visibility detection
- `useResizeObserver` — Size change detection

### Utility
- `useAsync` — Async operation state
- `useCallbackRef` — Stable callback reference
- `useId` — Unique ID generation
- `useMounted` — Mount state tracking

---

## Utilities (21 Categories)

| Category | Functions |
|---|---|
| **Core** | `cn()`, `generateId`, `clamp`, `isBrowser`, `mergeRefs`, `prefersReducedMotion` |
| **Accessibility** | `announceToScreenReader`, `focusableSelectors`, `trapFocus`, `getAnimationDuration`, `shouldAnimate` |
| **Keyboard** | `isEnterKey`, `isEscapeKey` |
| **DOM** | `mergeRefs` |
| **Objects** | `deepMerge`, `omit`, `pick` |
| **String** | `capitalize`, `slugify`, `truncate`, `getVariantClass` |
| **Timing** | `debounce`, `throttle` |
| **Safety** | `sanitizeHtml`, `sanitizeUrl`, `generateCryptoId`, `copyToClipboard` |
| **Validation** | `isValidEmail`, `isValidHref`, `isSafeHref`, `isValidUrl`, `isExternalUrl` |
| **Color** | `getContrastRatio`, `hexToRgb`, `rgbToHsl`, `hslToHex`, `meetsWCAG` |
| **Forms** | `validateField`, `validateForm`, `parseFormData`, `serializeForm` |
| **Misc** | `mapPlacement`, `normalizeTriggers`, `getSafeInputProps`, `ClearIcon` |

---

## Critical Rules

1. **ALWAYS** use `forwardRef` + `displayName` — not optional.
2. Props go in separate `*.types.ts` files.
3. Use `SemanticColorVariant` for colors — never hardcode hex/rgb values.
4. Use `ComponentSize` for sizing (`sm` | `md` | `lg`).
5. Compound sub-components use React Context for parent ↔ child communication.
6. Interactive components use FSM (`useReducer`) for state management.
7. `SafeHTMLAttributes` — never pass event handlers through prop spread; define them explicitly.
8. Use `cn()` for class composition — Bootstrap 5 classes, **not** Tailwind.
9. Test with `jest-axe` (a11y) and React Testing Library.
10. Components are local source code — import from `@/` not `@dsai-io/react` or any npm package.
