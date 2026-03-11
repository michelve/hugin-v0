# Transaction Patterns

## Simple Transaction

```typescript
const result = await prisma.$transaction(async (tx) => {
    const user = await tx.user.create({
        data: { email: "user@example.com", name: "John" },
    });

    const profile = await tx.userProfile.create({
        data: { userId: user.id, bio: "Developer" },
    });

    return { user, profile };
});
```

## Interactive Transaction

```typescript
const result = await prisma.$transaction(
    async (tx) => {
        const user = await tx.user.findUnique({ where: { id: userId } });
        if (!user) throw new Error("User not found");

        const updated = await tx.user.update({
            where: { id: userId },
            data: { lastLogin: new Date() },
        });

        await tx.auditLog.create({
            data: { userId, action: "LOGIN", timestamp: new Date() },
        });

        return updated;
    },
    {
        maxWait: 5000, // Wait max 5s to start
        timeout: 10000, // Timeout after 10s
    },
);
```
