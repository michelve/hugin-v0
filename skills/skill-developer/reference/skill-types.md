# Skill Types

## 1. Guardrail Skills

**Purpose:** Enforce critical best practices that prevent errors

**Characteristics:**

- Type: `"guardrail"`
- Enforcement: `"block"`
- Priority: `"critical"` or `"high"`
- Block file edits until skill used
- Prevent common mistakes (column names, critical errors)
- Session-aware (don't repeat nag in same session)

**Examples:**

- `database-verification` - Verify table/column names before Prisma queries
- `frontend-dev-guidelines` - Enforce React/TypeScript patterns

**When to Use:**

- Mistakes that cause runtime errors
- Data integrity concerns
- Critical compatibility issues

## 2. Domain Skills

**Purpose:** Provide comprehensive guidance for specific areas

**Characteristics:**

- Type: `"domain"`
- Enforcement: `"suggest"`
- Priority: `"high"` or `"medium"`
- Advisory, not mandatory
- Topic or domain-specific
- Comprehensive documentation

**Examples:**

- `backend-dev-guidelines` - Node.js/Express/TypeScript patterns
- `frontend-dev-guidelines` - React/TypeScript best practices
- `error-tracking` - Sentry integration guidance

**When to Use:**

- Complex systems requiring deep knowledge
- Best practices documentation
- Architectural patterns
- How-to guides
