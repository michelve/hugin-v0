# HTTP Method Testing

## GET Requests

```typescript
describe("GET /api/users", () => {
    it("should return paginated users", async () => {
        const response = await request(app).get("/api/users?page=1&limit=10");

        expect(response.status).toBe(200);
        expect(response.body).toHaveProperty("data");
        expect(response.body).toHaveProperty("pagination");
        expect(Array.isArray(response.body.data)).toBe(true);
    });

    it("should filter users by query params", async () => {
        const response = await request(app).get("/api/users?role=admin");

        expect(response.status).toBe(200);
        expect(response.body.data.every((u) => u.role === "admin")).toBe(true);
    });
});
```

## POST Requests

```typescript
describe("POST /api/users", () => {
    it("should create new user with valid data", async () => {
        const newUser = {
            name: "John Doe",
            email: "john@example.com",
            role: "user",
        };

        const response = await request(app)
            .post("/api/users")
            .set("Cookie", authCookie)
            .send(newUser);

        expect(response.status).toBe(201);
        expect(response.body).toMatchObject(newUser);
        expect(response.body).toHaveProperty("id");
    });

    it("should reject invalid data", async () => {
        const invalidUser = {
            name: "John Doe",
            // Missing required email field
        };

        const response = await request(app)
            .post("/api/users")
            .set("Cookie", authCookie)
            .send(invalidUser);

        expect(response.status).toBe(400);
        expect(response.body).toHaveProperty("errors");
    });
});
```

## PUT/PATCH Requests

```typescript
describe("PATCH /api/users/:id", () => {
    it("should update user fields", async () => {
        const updates = { name: "Jane Doe" };

        const response = await request(app)
            .patch("/api/users/123")
            .set("Cookie", authCookie)
            .send(updates);

        expect(response.status).toBe(200);
        expect(response.body.name).toBe("Jane Doe");
    });

    it("should return 404 for non-existent user", async () => {
        const response = await request(app)
            .patch("/api/users/999999")
            .set("Cookie", authCookie)
            .send({ name: "Test" });

        expect(response.status).toBe(404);
    });
});
```

## DELETE Requests

```typescript
describe("DELETE /api/users/:id", () => {
    it("should delete user and return success", async () => {
        const response = await request(app).delete("/api/users/123").set("Cookie", authCookie);

        expect(response.status).toBe(204);
    });

    it("should prevent unauthorized deletion", async () => {
        const response = await request(app).delete("/api/users/123");
        // No auth cookie

        expect(response.status).toBe(401);
    });
});
```
