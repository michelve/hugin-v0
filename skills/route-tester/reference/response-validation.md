# Response Validation

## Status Codes

```typescript
describe("HTTP Status Codes", () => {
    it("200 OK - Successful GET", async () => {
        const response = await request(app).get("/api/users");
        expect(response.status).toBe(200);
    });

    it("201 Created - Successful POST", async () => {
        const response = await request(app).post("/api/users").send(validData);
        expect(response.status).toBe(201);
    });

    it("204 No Content - Successful DELETE", async () => {
        const response = await request(app).delete("/api/users/123");
        expect(response.status).toBe(204);
    });

    it("400 Bad Request - Invalid input", async () => {
        const response = await request(app).post("/api/users").send({});
        expect(response.status).toBe(400);
    });

    it("401 Unauthorized - Missing auth", async () => {
        const response = await request(app).get("/api/protected");
        expect(response.status).toBe(401);
    });

    it("403 Forbidden - Insufficient permissions", async () => {
        const response = await request(app)
            .delete("/api/admin/users/123")
            .set("Cookie", userCookie);
        expect(response.status).toBe(403);
    });

    it("404 Not Found - Non-existent resource", async () => {
        const response = await request(app).get("/api/users/999999");
        expect(response.status).toBe(404);
    });

    it("500 Internal Server Error - Server failure", async () => {
        // Test error handling
        mockDatabase.findOne.mockRejectedValue(new Error("DB Error"));
        const response = await request(app).get("/api/users/123");
        expect(response.status).toBe(500);
    });
});
```

## Response Schema Validation

```typescript
describe("Response Schema", () => {
    it("should match expected schema", async () => {
        const response = await request(app).get("/api/users/123");

        expect(response.body).toEqual({
            id: expect.any(String),
            name: expect.any(String),
            email: expect.any(String),
            role: expect.stringMatching(/^(user|admin)$/),
            createdAt: expect.any(String),
            updatedAt: expect.any(String),
        });
    });
});
```
