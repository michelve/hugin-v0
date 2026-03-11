# Authentication Testing Patterns

## JWT Cookie Authentication

```typescript
// Common pattern across frameworks
describe("Protected Route Tests", () => {
    let authCookie: string;

    beforeEach(async () => {
        // Login and get JWT cookie
        const loginResponse = await request(app)
            .post("/api/auth/login")
            .send({ email: "test@example.com", password: "password123" });

        authCookie = loginResponse.headers["set-cookie"][0];
    });

    it("should access protected route with valid cookie", async () => {
        const response = await request(app)
            .get("/api/protected/resource")
            .set("Cookie", authCookie);

        expect(response.status).toBe(200);
    });

    it("should reject access without cookie", async () => {
        const response = await request(app).get("/api/protected/resource");

        expect(response.status).toBe(401);
    });
});
```

## JWT Bearer Token Authentication

```typescript
describe("Bearer Token Auth", () => {
    let token: string;

    beforeEach(async () => {
        const response = await request(app)
            .post("/api/auth/login")
            .send({ email: "test@example.com", password: "password123" });

        token = response.body.token;
    });

    it("should authenticate with bearer token", async () => {
        const response = await request(app)
            .get("/api/protected/resource")
            .set("Authorization", `Bearer ${token}`);

        expect(response.status).toBe(200);
    });
});
```
