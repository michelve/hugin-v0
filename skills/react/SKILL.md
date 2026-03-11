---
name: react
description: Core React 19 patterns including hooks, Suspense, lazy loading, component structure, TypeScript best practices, and performance optimization. Use when working with React components, hooks, lazy loading, Suspense boundaries, or React-specific TypeScript patterns.
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

**Note**: React 19 (released December 2024) breaking changes:

- `forwardRef` no longer needed - pass `ref` as a prop directly
- `propTypes` removed (silently ignored)
- New JSX transform required
- `React.FC` type discouraged - use direct function components instead

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
import { useState, useCallback } from 'react';

interface Props {
  userId: string;
  onUpdate?: (data: UserData) => void;
}

interface UserData {
  name: string;
  email: string;
}

function UserProfile({ userId, onUpdate }: Props) {
  const [data, setData] = useState<UserData | null>(null);

  const handleUpdate = useCallback((newData: UserData) => {
    setData(newData);
    onUpdate?.(newData);
  }, [onUpdate]);

  return (
    <div>
      {/* Component content */}
    </div>
  );
}

export default UserProfile;
```

### Component Checklist

Creating a React component? Follow this:

- [ ] Use function components with typed props (not `React.FC`)
- [ ] Define interfaces for Props and local state
- [ ] Use `useCallback` for event handlers passed to children
- [ ] Use `useMemo` for expensive computations
- [ ] Lazy load if heavy component: `lazy(() => import())`
- [ ] Wrap lazy components in `<Suspense>` with fallback
- [ ] Named export only (no default exports)
- [ ] No conditional hooks (hooks must be called in same order)
- [ ] Pass `ref` as a prop (no `forwardRef` needed in React 19)

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
src/
├── features/
│   ├── auth/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── types/
│   │   └── index.tsx
│   └── posts/
│       ├── components/
│       ├── hooks/
│       ├── types/
│       └── index.tsx
├── components/  # Shared components
├── hooks/       # Shared hooks
└── types/       # Shared types
```

### Component Co-location

```
features/posts/
├── components/
│   ├── PostCard.tsx
│   ├── PostList.tsx
│   └── PostForm.tsx
├── hooks/
│   ├── usePost.ts
│   └── usePosts.ts
├── types/
│   └── post.ts
└── index.tsx  # Public API
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
