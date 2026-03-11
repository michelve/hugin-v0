# N+1 Query Prevention

## Problem

```typescript
// ❌ N+1 Query Problem
const users = await prisma.user.findMany(); // 1 query

for (const user of users) {
    // N additional queries
    const profile = await prisma.userProfile.findUnique({
        where: { userId: user.id },
    });
}
```

## Solution 1: Use include

```typescript
// ✅ Single query with include
const users = await prisma.user.findMany({
    include: { profile: true },
});

for (const user of users) {
    console.log(user.profile.bio);
}
```

## Solution 2: Batch Query

```typescript
// ✅ Batch query
const users = await prisma.user.findMany();
const userIds = users.map((u) => u.id);

const profiles = await prisma.userProfile.findMany({
    where: { userId: { in: userIds } },
});

const profileMap = new Map(profiles.map((p) => [p.userId, p]));
```
