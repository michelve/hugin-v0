// =============================================================================
// Assertion Best Practices — Examples
// =============================================================================

// ---------------------------------------------------------------------------
// 1. Assert Specific Values
// ---------------------------------------------------------------------------

// ❌ WEAK - passes even if completely wrong data
expect(result).toBeDefined();
expect(result.items).toHaveLength(2);
expect(user).toBeTruthy();

// ✅ STRONG - catches actual bugs
expect(result).toEqual({ status: "success", items: ["a", "b"] });
expect(user.email).toBe("test@example.com");

// ---------------------------------------------------------------------------
// 2. Match Assertions to Test Title
// ---------------------------------------------------------------------------

// ❌ TEST SAYS "different IDs" BUT ASSERTS COUNT
it("generates different IDs for each call", () => {
    const id1 = generateId();
    const id2 = generateId();
    expect([id1, id2]).toHaveLength(2); // WRONG: doesn't check they're different!
});

// ✅ ACTUALLY VERIFIES DIFFERENT IDs
it("generates different IDs for each call", () => {
    const id1 = generateId();
    const id2 = generateId();
    expect(id1).not.toBe(id2); // RIGHT: verifies the claim
});

// ---------------------------------------------------------------------------
// 3. Avoid Implementation Coupling
// ---------------------------------------------------------------------------

// ❌ BRITTLE - tests implementation details
expect(mockDatabase.query).toHaveBeenCalledWith(
    "SELECT * FROM users WHERE id = 1",
);

// ✅ FLEXIBLE - tests behavior
expect(result.user.name).toBe("Alice");
