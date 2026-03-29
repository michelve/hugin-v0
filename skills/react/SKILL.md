---
name: react
version: 1.0.0
description: Core React 19 patterns for DSAI projects including hooks, Suspense, lazy loading, component structure with forwardRef, TypeScript best practices, and performance optimization. Use when working with React components, hooks, lazy loading, Suspense boundaries, or React-specific TypeScript patterns.
user-invocable: true
---

# React Core Patterns

## When to Use

- Creating React components
- Working with hooks (useState, useEffect, custom hooks)
- Implementing Suspense boundaries
- Setting up lazy loading with React.lazy
- Using React 19 patterns (ref as prop, no forwardRef)
- Structuring component files
- Optimizing component performance

## Purpose

Essential React 19 patterns for building modern applications with hooks, Suspense, lazy loading, and TypeScript.

**Note**: DSAI Component Convention (React 19):

- `forwardRef` is **REQUIRED** for all DSAI components — use `memo(forwardRef(function Name(props, ref)))` pattern
- Every component MUST have a `displayName` property
- Props go in separate `*.types.ts` files
- `propTypes` removed (use TypeScript interfaces)
- New JSX transform required
- `React.FC` type discouraged — use direct function components with typed props

## When to Use This Skill

- Creating React components
- Using React hooks (useState, useEffect, useCallback, useMemo)
- Implementing lazy loading and code splitting
- Working with Suspense boundaries
- React-specific TypeScript patterns
- Performance optimization with React

---

## Quick Start

### Component Structure Template

```typescript
import { forwardRef, memo, useState, useCallback } from 'react';
import { cn } from '@/lib/utils';
import type { UserProfileProps } from './UserProfile.types';

// Props defined in UserProfile.types.ts:
// interface UserProfileProps {
//   userId: string;
//   onUpdate?: (data: UserData) => void;
//   className?: string;
// }

export const UserProfile = memo(
  forwardRef<HTMLDivElement, UserProfileProps>(
    function UserProfile({ userId, onUpdate, className }, ref) {
      const [data, setData] = useState<UserData | null>(null);

      const handleUpdate = useCallback((newData: UserData) => {
        setData(newData);
        onUpdate?.(newData);
      }, [onUpdate]);

      return (
        <div ref={ref} className={cn('user-profile', className)}>
          {/* Component content */}
        </div>
      );
    }
  )
);
UserProfile.displayName = 'UserProfile';
```

### Component Checklist

Creating a React component? Follow this:

- [ ] Use `memo(forwardRef(function Name(props, ref)))` pattern
- [ ] Set `displayName` on every component
- [ ] Props in separate `*.types.ts` file
- [ ] Use `cn()` for class name composition (Bootstrap classes, not Tailwind)
- [ ] Use `useCallback` for event handlers passed to children
- [ ] Use `useMemo` for expensive computations
- [ ] Lazy load if heavy component: `lazy(() => import())`
- [ ] Wrap lazy components in `<Suspense>` with fallback
- [ ] Named export only (no default exports)
- [ ] No conditional hooks (hooks must be called in same order)
- [ ] Import from `@/components/ui/` for DSAI components

---

---

## Core Hooks Patterns

See [hooks-patterns.md](reference/hooks-patterns.md) for useState, useCallback, useMemo, and useEffect patterns with TypeScript examples.

---

## Lazy Loading & Code Splitting

See [lazy-loading.md](examples/lazy-loading.md) for React.lazy, Suspense fallbacks, and feature-based code splitting examples.

---

## Suspense Patterns

### Suspense Boundaries

```typescript
// Wrap data-fetching components
<Suspense fallback={<Skeleton />}>
  <UserProfile userId={id} />
</Suspense>

// Nested Suspense for granular loading
<Suspense fallback={<PageLoader />}>
  <Header />
  <Suspense fallback={<ContentSkeleton />}>
    <MainContent />
  </Suspense>
  <Footer />
</Suspense>
```

### Error Boundaries with Suspense

```typescript
import { ErrorBoundary } from 'react-error-boundary';

<ErrorBoundary fallback={<ErrorFallback />}>
  <Suspense fallback={<Loading />}>
    <DataComponent />
  </Suspense>
</ErrorBoundary>
```

---

---

## TypeScript Patterns

See [typescript-patterns.md](reference/typescript-patterns.md) for component props, hooks typing, and custom hook return types.

---

## Performance Optimization

See [performance.md](reference/performance.md) for React.memo usage, custom comparison functions, and avoiding re-renders.

---

## Common Patterns

### Conditional Rendering

```typescript
// Ternary operator
{isLoading ? <Spinner /> : <Content />}

// Logical AND
{error && <ErrorMessage error={error} />}

// Nullish coalescing
{user ?? <GuestView />}

// Early return for loading states
function Component() {
  const { data } = useSomeHook();

  // ❌ Avoid early returns for loading - breaks hooks rules
  // Use Suspense instead

  return <div>{data.map(...)}</div>;
}
```

### Lists and Keys

```typescript
// Always use stable keys
{items.map(item => (
  <ItemCard key={item.id} item={item} />
))}

// Never use index as key if list can reorder
// ❌ Bad
{items.map((item, index) => (
  <ItemCard key={index} item={item} />
))}
```

---

## File Organization

### Feature-Based Structure

```
src/client/
├── components/
│   ├── ui/              # DSAI components (installed via `dsai add`)
│   │   ├── button/
│   │   │   ├── Button.tsx
│   │   │   ├── Button.types.ts
│   │   │   ├── Button.fsm.ts
│   │   │   └── index.ts
│   │   ├── modal/
│   │   └── card/
│   └── features/        # App-specific feature components
│       ├── auth/
│       └── posts/
├── hooks/               # Shared hooks (DSAI + custom)
├── lib/
│   └── utils/           # Utilities (cn, validators, etc.)
└── types/               # Shared types
```

### Component Co-location

```
components/ui/button/
├── Button.tsx           # Component with forwardRef + displayName
├── Button.types.ts      # TypeScript prop interfaces
├── Button.fsm.ts        # FSM reducer (interactive components)
├── Button.test.tsx       # Unit tests (Jest 30 + RTL)
├── Button.a11y.test.tsx  # Accessibility tests (jest-axe)
└── index.ts             # Barrel exports
```

---

---

## Common Mistakes to Avoid

See [common-mistakes.md](reference/common-mistakes.md) for conditional hooks, missing dependencies, and state mutation anti-patterns.

---

## Additional Resources

For more detailed patterns, see:

- [component-patterns.md](resources/component-patterns.md) - Advanced component patterns
- [performance.md](resources/performance.md) - Performance optimization techniques
- [typescript-patterns.md](resources/typescript-patterns.md) - TypeScript best practices
- [hooks-patterns.md](resources/hooks-patterns.md) - Custom hooks and advanced patterns
