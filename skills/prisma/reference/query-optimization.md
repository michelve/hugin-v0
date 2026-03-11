# Query Optimization

## Use select to Limit Fields

```typescript
// ❌ Fetches all fields
const users = await prisma.user.findMany();

// ✅ Only fetch needed fields
const users = await prisma.user.findMany({
    select: {
        id: true,
        email: true,
        name: true,
    },
});

// ✅ Select with relations
const users = await prisma.user.findMany({
    select: {
        id: true,
        email: true,
        profile: {
            select: { firstName: true, lastName: true },
        },
    },
});
```

## Use include Carefully

```typescript
// ❌ Excessive includes
const user = await prisma.user.findUnique({
    where: { id },
    include: {
        posts: { include: { comments: true } },
        workflows: { include: { steps: { include: { actions: true } } } },
    },
});

// ✅ Only include what you need
const user = await prisma.user.findUnique({
    where: { id },
    include: { profile: true },
});
```
