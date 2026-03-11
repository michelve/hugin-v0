# Core Hooks Patterns

### useState

```typescript
// Simple state
const [count, setCount] = useState<number>(0);

// Object state
const [user, setUser] = useState<User | null>(null);

// Array state
const [items, setItems] = useState<Item[]>([]);

// Functional updates when depending on previous state
setCount((prev) => prev + 1);
setItems((prev) => [...prev, newItem]);
```

### useCallback

```typescript
// Wrap functions passed to child components
const handleClick = useCallback((id: string) => {
    console.log("Clicked:", id);
}, []); // Empty deps if no dependencies

// With dependencies
const handleUpdate = useCallback(
    (data: FormData) => {
        apiCall(userId, data);
    },
    [userId],
); // Re-create when userId changes
```

### useMemo

```typescript
// Expensive computation
const sortedItems = useMemo(() => {
    return items.sort((a, b) => a.score - b.score);
}, [items]);

// Derived state
const totalPrice = useMemo(() => {
    return cart.reduce((sum, item) => sum + item.price, 0);
}, [cart]);
```

### useEffect

```typescript
// Run once on mount
useEffect(() => {
    fetchData();
}, []);

// Run when dependency changes
useEffect(() => {
    if (userId) {
        loadUserData(userId);
    }
}, [userId]);

// Cleanup
useEffect(() => {
    const subscription = subscribe(userId);
    return () => subscription.unsubscribe();
}, [userId]);
```
