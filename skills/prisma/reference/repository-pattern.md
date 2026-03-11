# Repository Pattern

## When to Use Repositories

✅ **Use repositories when:**

- Complex queries with joins/includes
- Query used in multiple places
- Need to mock for testing

❌ **Skip repositories for:**

- Simple one-off queries
- Prototyping

## Repository Template

```typescript
import { prisma } from "@server/lib/prisma";
import type { User, Prisma } from "@prisma/client";

export class UserRepository {
    async findById(id: string): Promise<User | null> {
        return prisma.user.findUnique({
            where: { id },
            include: { profile: true },
        });
    }

    async findByEmail(email: string): Promise<User | null> {
        return prisma.user.findUnique({
            where: { email },
        });
    }

    async findActive(): Promise<User[]> {
        return prisma.user.findMany({
            where: { isActive: true },
            orderBy: { createdAt: "desc" },
        });
    }

    async create(data: Prisma.UserCreateInput): Promise<User> {
        return prisma.user.create({ data });
    }

    async update(id: string, data: Prisma.UserUpdateInput): Promise<User> {
        return prisma.user.update({ where: { id }, data });
    }

    async delete(id: string): Promise<void> {
        await prisma.user.delete({ where: { id } });
    }
}
```

## Using in Service

```typescript
export class UserService {
    private userRepository: UserRepository;

    constructor() {
        this.userRepository = new UserRepository();
    }

    async getById(id: string): Promise<User> {
        const user = await this.userRepository.findById(id);
        if (!user) {
            throw new Error("User not found");
        }
        return user;
    }
}
```
