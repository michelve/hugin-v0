---
name: prisma
description: Prisma ORM patterns including Prisma Client usage, queries, mutations, relations, transactions, and schema management. Use when working with Prisma database operations or schema definitions.
user-invocable: true
---

# Prisma ORM Patterns

## When to Use

- Writing database queries with Prisma Client
- Defining or modifying Prisma schema
- Adding database models
- Creating migrations
- Working with relations and associations
- Implementing transactions
- Handling Prisma errors (P2002, P2025)

## Purpose

Complete patterns for using Prisma ORM effectively, including query optimization, transaction handling, and the repository pattern for clean data access.

## When to Use This Skill

- Working with Prisma Client for database queries
- Creating repositories for data access
- Using transactions
- Query optimization and N+1 prevention
- Handling Prisma errors

---

## Basic Prisma Usage

### Core Query Patterns

```typescript
import { prisma } from "@server/lib/prisma";

// Find one
const user = await prisma.user.findUnique({
    where: { id: userId },
});

// Find many with filters
const users = await prisma.user.findMany({
    where: { isActive: true },
    orderBy: { createdAt: "desc" },
    take: 10,
});

// Create
const newUser = await prisma.user.create({
    data: {
        email: "user@example.com",
        name: "John Doe",
    },
});

// Update
const updated = await prisma.user.update({
    where: { id: userId },
    data: { name: "Jane Doe" },
});

// Delete
await prisma.user.delete({
    where: { id: userId },
});
```

### Complex Filtering

```typescript
// Multiple conditions
const users = await prisma.user.findMany({
    where: {
        email: { contains: "@example.com" },
        isActive: true,
        createdAt: { gte: new Date("2024-01-01") },
    },
});

// AND/OR conditions
const posts = await prisma.post.findMany({
    where: {
        AND: [{ published: true }, { author: { isActive: true } }],
        OR: [{ title: { contains: "prisma" } }, { content: { contains: "prisma" } }],
    },
});
```

---

## Repository Pattern

See [repository-pattern.md](reference/repository-pattern.md) for repository template, when to use repositories, and service integration.

---

## Transaction Patterns

See [transactions.md](reference/transactions.md) for simple and interactive transaction patterns with timeout configuration.

---

## Query Optimization

See [query-optimization.md](reference/query-optimization.md) for select vs include, field limiting, and relation fetching.

---

## N+1 Query Prevention

See [n-plus-one.md](reference/n-plus-one.md) for N+1 problem identification and solutions using include and batch queries.

---

## Relations

See [relations.md](reference/relations.md) for one-to-many queries, nested writes, and relation data patterns.

---

## Error Handling

See [error-handling.md](reference/error-handling.md) for Prisma error codes (P2002, P2003, P2025) and error handling patterns.

---

## Advanced Patterns

### Aggregations

```typescript
// Count
const count = await prisma.user.count({
    where: { isActive: true },
});

// Aggregate
const stats = await prisma.post.aggregate({
    _count: true,
    _avg: { views: true },
    _sum: { likes: true },
    where: { published: true },
});

// Group by
const postsByAuthor = await prisma.post.groupBy({
    by: ["authorId"],
    _count: { id: true },
});
```

### Upsert

```typescript
// Update if exists, create if not
const user = await prisma.user.upsert({
    where: { email: "user@example.com" },
    update: { lastLogin: new Date() },
    create: {
        email: "user@example.com",
        name: "John Doe",
    },
});
```

---

## TypeScript Patterns

```typescript
import type { User, Prisma } from "@prisma/client";

// Create input type
const createUser = async (data: Prisma.UserCreateInput): Promise<User> => {
    return prisma.user.create({ data });
};

// Include type
type UserWithProfile = Prisma.UserGetPayload<{
    include: { profile: true };
}>;

const user: UserWithProfile = await prisma.user.findUnique({
    where: { id },
    include: { profile: true },
});
```

---

## Best Practices

1. **Use the Singleton Client** - Import `prisma` from `@server/lib/prisma`, never create new instances
2. **Use Repositories for Complex Queries** - Keep data access organized
3. **Select Only Needed Fields** - Improve performance with select
4. **Prevent N+1 Queries** - Use include or batch queries
5. **Use Transactions** - Ensure atomicity for multi-step operations
6. **Handle Errors** - Check for specific Prisma error codes

---

**Related Skills:**

- **nodejs** - Core Node.js patterns and async handling
- **route-tester** - API route testing patterns
