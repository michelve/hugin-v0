# Common Mistakes to Avoid

### 1. Conditional Hooks

```typescript
// Never do this
function Component({ condition }) {
    if (condition) {
        const [state, setState] = useState(0); // Breaks rules of hooks
    }
}

// Do this instead
function Component({ condition }) {
    const [state, setState] = useState(0);
    // Use state conditionally, not the hook
}
```

### 2. Missing Dependencies

```typescript
// Bad: Missing dependency
useEffect(() => {
    fetchUser(userId);
}, []); // userId should be in deps

// Good: All dependencies listed
useEffect(() => {
    fetchUser(userId);
}, [userId]);
```

### 3. Mutating State

```typescript
// Bad: Mutating state directly
const handleAdd = () => {
    items.push(newItem); // Don't mutate
    setItems(items);
};

// Good: Create new array
const handleAdd = () => {
    setItems([...items, newItem]);
};
```
