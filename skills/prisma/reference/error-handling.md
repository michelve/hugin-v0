# Error Handling

## Prisma Error Codes

```typescript
import { Prisma } from "@prisma/client";

try {
    await prisma.user.create({
        data: { email: "user@example.com" },
    });
} catch (error) {
    if (error instanceof Prisma.PrismaClientKnownRequestError) {
        // P2002: Unique constraint violation
        if (error.code === "P2002") {
            throw new ConflictError("Email already exists");
        }

        // P2003: Foreign key constraint failed
        if (error.code === "P2003") {
            throw new ValidationError("Invalid reference");
        }

        // P2025: Record not found
        if (error.code === "P2025") {
            throw new NotFoundError("Record not found");
        }
    }

    console.error(error);
    throw error;
}
```

## Common Error Codes

| Code  | Meaning                       |
| ----- | ----------------------------- |
| P2002 | Unique constraint violation   |
| P2003 | Foreign key constraint failed |
| P2025 | Record not found              |
| P2014 | Relation violation            |
