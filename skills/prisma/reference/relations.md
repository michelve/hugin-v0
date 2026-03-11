# Relations

## One-to-Many

```typescript
// Get user with posts
const user = await prisma.user.findUnique({
    where: { id: userId },
    include: {
        posts: {
            where: { published: true },
            orderBy: { createdAt: "desc" },
            take: 10,
        },
    },
});
```

## Nested Writes

```typescript
// Create user with profile
const user = await prisma.user.create({
    data: {
        email: "user@example.com",
        name: "John Doe",
        profile: {
            create: {
                bio: "Developer",
                avatar: "avatar.jpg",
            },
        },
    },
    include: { profile: true },
});

// Update with nested updates
const user = await prisma.user.update({
    where: { id: userId },
    data: {
        name: "Jane Doe",
        profile: {
            update: { bio: "Senior developer" },
        },
    },
});
```
