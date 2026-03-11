# TypeScript Patterns

### Component Props

```typescript
// Basic props
interface ButtonProps {
    label: string;
    onClick: () => void;
    disabled?: boolean;
}

// Props with children
interface CardProps {
    title: string;
    children: React.ReactNode;
}

// Props with specific child types
interface ListProps {
    children: React.ReactElement<ItemProps> | React.ReactElement<ItemProps>[];
}

// Props with event handlers
interface FormProps {
    onSubmit: (data: FormData) => void;
    onChange?: (field: string, value: unknown) => void;
}
```

### Hooks TypeScript

```typescript
// useState with type
const [user, setUser] = useState<User | null>(null);
const [items, setItems] = useState<Item[]>([]);

// useRef with type
const inputRef = useRef<HTMLInputElement>(null);
const timerRef = useRef<number | null>(null);

// Custom hook with return type
function useUser(id: string): { user: User | null; loading: boolean } {
    const [user, setUser] = useState<User | null>(null);
    const [loading, setLoading] = useState(true);

    // ... implementation

    return { user, loading };
}
```
