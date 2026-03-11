---
name: nodejs
description: Core Node.js backend patterns for TypeScript applications including async/await error handling, middleware concepts, configuration management, testing strategies, and layered architecture principles. Use when building Node.js backend services, APIs, or microservices.
user-invocable: true
---

## Current Project Context

```json
!`cat package.json 2>/dev/null || echo '{"error": "No package.json found."}'`
```

# Node.js Backend Patterns

## When to Use

- Building Express API routes
- Creating middleware
- Configuring Node.js server
- Implementing async/await error handling patterns
- Setting up layered architecture (Controller → Service → Repository)
- Working with Node.js streams or modules

## Purpose

Core patterns for building scalable Node.js backend applications with TypeScript, emphasizing clean architecture, error handling, and testability.

## When to Use This Skill

- Building Node.js backend services
- Implementing async/await patterns
- Error handling and logging
- Configuration management
- Testing backend code
- Layered architecture (routes → controllers → services → repositories)

---

## Quick Start

### Layered Architecture

```
src/
├── api/
│   ├── routes/         # HTTP route definitions
│   ├── controllers/    # Request/response handling
│   ├── services/       # Business logic
│   └── repositories/   # Data access
├── middleware/         # Express middleware
├── types/             # TypeScript types
├── config/            # Configuration
└── utils/             # Utilities
```

**Flow:** Route → Controller → Service → Repository → Database

---

## Async/Await Error Handling

See [resources/async-and-errors.md](resources/async-and-errors.md) for async/await patterns (basic pattern, controller pattern, Promise.all for parallel operations, custom error classes, async error wrapper).

---

## TypeScript Patterns

### Request/Response Types

```typescript
// Request body
interface CreateUserRequest {
    email: string;
    name: string;
    password: string;
}

// Response
interface ApiResponse<T> {
    success: boolean;
    data?: T;
    error?: string;
    message?: string;
}

// Usage
async function createUser(
    req: Request<{}, {}, CreateUserRequest>,
    res: Response<ApiResponse<User>>,
): Promise<void> {
    const { email, name, password } = req.body;

    const user = await userService.create({ email, name, password });

    res.json({
        success: true,
        data: user,
    });
}
```

### Service Layer Types

```typescript
interface IUserService {
    getById(id: string): Promise<User>;
    create(data: CreateUserDto): Promise<User>;
    update(id: string, data: UpdateUserDto): Promise<User>;
    delete(id: string): Promise<void>;
}

class UserService implements IUserService {
    async getById(id: string): Promise<User> {
        // Implementation
    }

    async create(data: CreateUserDto): Promise<User> {
        // Implementation
    }

    async update(id: string, data: UpdateUserDto): Promise<User> {
        // Implementation
    }

    async delete(id: string): Promise<void> {
        // Implementation
    }
}
```

---

## Configuration Management

### Environment Variables

```typescript
// config/env.ts
import { z } from "zod";

const envSchema = z.object({
    NODE_ENV: z.enum(["development", "production", "test"]),
    PORT: z.string().transform(Number),
    DATABASE_URL: z.string().url(),
    JWT_SECRET: z.string().min(32),
    LOG_LEVEL: z.enum(["error", "warn", "info", "debug"]).default("info"),
});

export const env = envSchema.parse(process.env);
```

### Unified Config

```typescript
// config/index.ts
interface Config {
    server: {
        port: number;
        host: string;
    };
    database: {
        url: string;
    };
    auth: {
        jwtSecret: string;
        jwtExpiry: string;
    };
}

export const config: Config = {
    server: {
        port: parseInt(process.env.PORT || "3000"),
        host: process.env.HOST || "localhost",
    },
    database: {
        url: process.env.DATABASE_URL || "",
    },
    auth: {
        jwtSecret: process.env.JWT_SECRET || "",
        jwtExpiry: process.env.JWT_EXPIRY || "7d",
    },
};
```

---

## Layered Architecture (Detailed)

See [resources/architecture-patterns.md](resources/architecture-patterns.md) for detailed controller, service, and repository layer implementations plus dependency injection patterns.

---

## Error Handling

See [resources/async-and-errors.md](resources/async-and-errors.md) for custom error classes (AppError, NotFoundError, ValidationError) and async error wrapper pattern.

---

## Best Practices

### 1. Always Use Async/Await

```typescript
// ✅ Good: async/await
async function getUser(id: string): Promise<User> {
  const user = await userRepository.findById(id);
  return user;
}

// ❌ Avoid: Promise chains
function getUser(id: string): Promise<User> {
  return userRepository.findById(id)
    .then(user => user)
    .catch(error => throw error);
}
```

### 2. Layer Separation

```typescript
// ✅ Good: Separated layers
// Controller handles HTTP
// Service handles business logic
// Repository handles data access

// ❌ Avoid: Business logic in controllers
class UserController {
  async create(req: Request, res: Response) {
    // ❌ Don't put business logic here
    const hashedPassword = await hash(req.body.password);
    const user = await db.user.create({...});
    res.json(user);
  }
}
```

### 3. Type Everything

```typescript
// ✅ Good: Full type coverage
async function updateUser(id: string, data: UpdateUserDto): Promise<User> {
    return userService.update(id, data);
}

// ❌ Avoid: any types
async function updateUser(id: any, data: any): Promise<any> {
    return userService.update(id, data);
}
```

---

## Additional Resources

For more patterns, see:

- [async-and-errors.md](resources/async-and-errors.md) - Advanced error handling
- [testing-guide.md](resources/testing-guide.md) - Comprehensive testing
- [architecture-patterns.md](resources/architecture-patterns.md) - Architecture details
