# Performance Optimization

### React.memo

```typescript
// Memoize component to prevent unnecessary re-renders
const UserCard = React.memo<UserCardProps>(({ user, onUpdate }) => {
  return (
    <div>
      <h3>{user.name}</h3>
      <button onClick={() => onUpdate(user.id)}>Update</button>
    </div>
  );
});

// Custom comparison function
const UserCard = React.memo(UserCardComponent, (prevProps, nextProps) => {
  return prevProps.user.id === nextProps.user.id;
});
```

### Avoiding Re-renders

```typescript
// Bad: Creates new function on every render
function Parent() {
  return <Child onClick={() => console.log('clicked')} />;
}

// Good: Stable function reference
function Parent() {
  const handleClick = useCallback(() => {
    console.log('clicked');
  }, []);

  return <Child onClick={handleClick} />;
}
```
