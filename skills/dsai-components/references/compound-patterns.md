# Compound Component Pattern

## Overview
DSAI uses the compound component pattern for complex UI elements. Parent components share state via React Context with child sub-components.

## Architecture
```
Parent Component (Context Provider)
  ├── SubComponent.Header (Consumer)
  ├── SubComponent.Body (Consumer)
  └── SubComponent.Footer (Consumer)
```

## Implementation
```tsx
// 1. Define context
interface CardContextValue {
  variant: CardVariant;
  color?: SemanticColorVariant;
  size?: ComponentSize;
}
const CardContext = createContext<CardContextValue | undefined>(undefined);

// 2. Hook for consumers
function useCardContext() {
  const context = useContext(CardContext);
  if (!context) throw new Error('Card sub-component must be used within <Card>');
  return context;
}

// 3. Parent component
const Card = forwardRef<HTMLDivElement, CardProps>(
  function Card({ variant = 'elevated', color, size = 'md', children, className, ...props }, ref) {
    return (
      <CardContext.Provider value={{ variant, color, size }}>
        <div ref={ref} className={cn('card', `card-${variant}`, color && `card-${color}`, className)} {...props}>
          {children}
        </div>
      </CardContext.Provider>
    );
  }
);
Card.displayName = 'Card';

// 4. Sub-component
const CardHeader = forwardRef<HTMLDivElement, CardHeaderProps>(
  function CardHeader({ children, className, ...props }, ref) {
    const { color } = useCardContext();
    return (
      <div ref={ref} className={cn('card-header', color && `bg-${color}`, className)} {...props}>
        {children}
      </div>
    );
  }
);
CardHeader.displayName = 'Card.Header';

// 5. Attach sub-components
Card.Header = CardHeader;
Card.Body = CardBody;
Card.Footer = CardFooter;
// etc.
```

## Key Rules
1. Sub-components MUST be used inside their parent (enforced by context check)
2. Each sub-component gets its own forwardRef + displayName
3. Context shares variant/color/size — sub-components inherit styling
4. Sub-components are attached to parent as static properties (Card.Header)
5. Always export both the parent and sub-components from index.ts

## Modal-Specific: Focus Management
```tsx
<Modal isOpen={open} onClose={close} initialFocusRef={inputRef} returnFocusRef={buttonRef}>
  <Modal.Header closeButton>Title</Modal.Header>
  <Modal.Body>
    <Input ref={inputRef} label="Name" />
  </Modal.Body>
</Modal>
```
- useFocusTrap locks keyboard focus within modal
- useScrollLock prevents body scroll
- Escape key closes modal (closeOnEscape prop)
- Click outside closes modal (closeOnBackdrop prop)
- Focus returns to trigger on close (returnFocusRef)

## Tabs-Specific: Activation Modes
```tsx
// Automatic: Tab content shows on arrow key navigation
<Tabs activationMode="automatic">

// Manual: Must press Enter/Space to activate a tab
<Tabs activationMode="manual">
```
- useRovingFocus for keyboard arrow navigation
- TabPanel lazy rendering with lazyMount prop
- Unmount inactive panels with unmountOnExit prop
