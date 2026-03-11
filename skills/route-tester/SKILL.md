---
name: route-tester
description: Framework-agnostic HTTP API route testing patterns, authentication strategies, and integration testing best practices. Supports REST APIs with JWT cookie authentication and other common auth patterns.
argument-hint: "<route-path-to-test>"
user-invocable: true
---

## Current Project Context

```json
!`cat package.json 2>/dev/null || echo '{"error": "No package.json found."}'`
```

# API Route Testing Skill

This skill provides guidance for testing HTTP API routes and endpoints. Primary examples use Express with TypeScript, but patterns adapt to other frameworks.

## When to Use

- Testing API endpoints
- Writing integration tests for Express routes
- Testing authentication flows (JWT cookies, sessions)
- Validating API responses and status codes
- Testing route middleware and error handling
- Creating route test suites

## Core Testing Principles

### 1. Test Types for API Routes

**Unit Tests**

- Test individual route handlers in isolation
- Mock dependencies (database, external APIs)
- Fast execution (< 50ms per test)
- Focus on business logic

**Integration Tests**

- Test full request/response cycle
- Real database (test instance)
- Authentication flow included
- Slower but more comprehensive

**End-to-End Tests**

- Test from client perspective
- Full authentication flow
- Real services (or close replicas)
- Most realistic, slowest execution

### 2. Authentication Testing Patterns

See [authentication-testing.md](examples/authentication-testing.md) for JWT cookie and bearer token authentication test patterns.

### 3. HTTP Method Testing

See [http-method-patterns.md](examples/http-method-patterns.md) for GET, POST, PUT/PATCH, and DELETE request test examples.

### 4. Response Validation

See [response-validation.md](reference/response-validation.md) for status code testing and response schema validation patterns.

### 5. Error Handling Tests

```typescript
describe("Error Handling", () => {
    it("should return structured error response", async () => {
        const response = await request(app).post("/api/users").send({ invalid: "data" });

        expect(response.status).toBe(400);
        expect(response.body).toEqual({
            error: expect.any(String),
            message: expect.any(String),
            errors: expect.any(Array),
        });
    });

    it("should handle database errors gracefully", async () => {
        mockDatabase.findOne.mockRejectedValue(new Error("Connection lost"));

        const response = await request(app).get("/api/users/123");

        expect(response.status).toBe(500);
        expect(response.body.error).toBe("Internal Server Error");
    });

    it("should sanitize error messages in production", async () => {
        process.env.NODE_ENV = "production";

        const response = await request(app).get("/api/error-prone-route");

        expect(response.status).toBe(500);
        expect(response.body.message).not.toContain("stack trace");
        expect(response.body.message).not.toContain("SQL");
    });
});
```

### 6. Test Setup and Teardown

```typescript
describe("API Tests", () => {
    let testDatabase;

    beforeAll(async () => {
        // Initialize test database
        testDatabase = await initTestDatabase();
    });

    afterAll(async () => {
        // Clean up test database
        await testDatabase.close();
    });

    beforeEach(async () => {
        // Seed test data
        await testDatabase.seed();
    });

    afterEach(async () => {
        // Clear test data
        await testDatabase.clear();
    });

    // Tests...
});
```

## Framework-Specific Testing Libraries

While this skill provides framework-agnostic patterns, here are common testing libraries per framework:

- **Express**: supertest, vitest

## Best Practices

1. **Use descriptive test names** - Test names should describe the scenario and expected outcome
2. **Test happy path and edge cases** - Cover both success and failure scenarios
3. **Isolate tests** - Each test should be independent and not rely on other tests
4. **Use realistic test data** - Test data should mimic production data
5. **Clean up after tests** - Always reset state between tests
6. **Mock external dependencies** - Don't call real external APIs in tests
7. **Test authentication edge cases** - Expired tokens, invalid tokens, missing tokens
8. **Validate response schemas** - Ensure APIs return expected structure
9. **Test rate limiting** - Verify rate limits work correctly
10. **Test CORS headers** - Ensure CORS is configured correctly

## Common Pitfalls

❌ **Don't share state between tests**

```typescript
// Bad
let userId;
it("creates user", async () => {
    const response = await request(app).post("/api/users").send(userData);
    userId = response.body.id; // Shared state!
});

it("deletes user", async () => {
    await request(app).delete(`/api/users/${userId}`); // Depends on previous test
});
```

✅ **Do create fresh state for each test**

```typescript
// Good
it("creates user", async () => {
    const response = await request(app).post("/api/users").send(userData);
    expect(response.status).toBe(201);
});

it("deletes user", async () => {
    const user = await createTestUser();
    const response = await request(app).delete(`/api/users/${user.id}`);
    expect(response.status).toBe(204);
});
```

## Additional Resources

See the `resources/` directory for more detailed guides:

- `http-testing-fundamentals.md` - Deep dive into HTTP testing concepts
- `authentication-testing.md` - Authentication strategies and edge cases
- `api-integration-testing.md` - Integration testing patterns and tools

## Quick Reference

**Test Structure**

```typescript
describe('Resource Name', () => {
  describe('HTTP Method /path', () => {
    it('should describe expected behavior', async () => {
      // Arrange
      const testData = {...};

      // Act
      const response = await request(app)
        .method('/path')
        .set('Cookie', authCookie)
        .send(testData);

      // Assert
      expect(response.status).toBe(expectedStatus);
      expect(response.body).toMatchObject(expectedData);
    });
  });
});
```

**Authentication Pattern**

```typescript
let authCookie: string;

beforeEach(async () => {
  const response = await request(app)
    .post('/api/auth/login')
    .send({ email: 'test@example.com', password: 'password123' });

  authCookie = response.headers['set-cookie'][0];
});

// Use authCookie in protected route tests
.set('Cookie', authCookie)
```
