// =============================================================================
// Test Structure — Examples
// =============================================================================

// ---------------------------------------------------------------------------
// 1. Arrange-Act-Assert
// ---------------------------------------------------------------------------

it("calculates total with tax for non-exempt items", () => {
    // Arrange: Set up test data
    const item = { price: 100, taxExempt: false };
    const taxRate = 0.1;

    // Act: Execute the behavior
    const total = calculateTotal(item, taxRate);

    // Assert: Verify the outcome
    expect(total).toBe(110);
});

// ---------------------------------------------------------------------------
// 2. One Concept Per Test
// ---------------------------------------------------------------------------

// ❌ MULTIPLE CONCEPTS - hard to diagnose failures
it("validates and processes order", () => {
    expect(validate(order)).toBe(true);
    expect(process(order).status).toBe("complete");
    expect(sendEmail).toHaveBeenCalled();
});

// ✅ SINGLE CONCEPT - clear failures
it("accepts valid orders", () => {
    expect(validate(validOrder)).toBe(true);
});

it("rejects orders with negative quantities", () => {
    expect(validate(negativeQuantityOrder)).toBe(false);
});

it("sends confirmation email after processing", () => {
    process(order);
    expect(sendEmail).toHaveBeenCalledWith(order.customerEmail);
});
