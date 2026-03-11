# Lazy Loading & Code Splitting

### Basic Lazy Loading

```typescript
import React, { Suspense } from 'react';

// Lazy load heavy component
const HeavyChart = React.lazy(() => import('./HeavyChart'));

function Dashboard() {
  return (
    <div>
      <h1>Dashboard</h1>
      <Suspense fallback={<div>Loading chart...</div>}>
        <HeavyChart />
      </Suspense>
    </div>
  );
}
```

### Multiple Lazy Components

```typescript
const AdminPanel = React.lazy(() => import('./AdminPanel'));
const UserSettings = React.lazy(() => import('./UserSettings'));
const Reports = React.lazy(() => import('./Reports'));

function App() {
  return (
    <Suspense fallback={<LoadingSpinner />}>
      <Routes>
        <Route path="/admin" element={<AdminPanel />} />
        <Route path="/settings" element={<UserSettings />} />
        <Route path="/reports" element={<Reports />} />
      </Routes>
    </Suspense>
  );
}
```

### Feature-Based Code Splitting

```typescript
// features/auth/index.tsx
export { default } from './AuthFeature';

// Lazy load entire feature
const AuthFeature = React.lazy(() => import('~/features/auth'));

<Suspense fallback={<FeatureLoader />}>
  <AuthFeature />
</Suspense>
```
