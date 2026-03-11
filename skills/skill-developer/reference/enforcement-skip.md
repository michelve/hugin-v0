# Skip Conditions & User Control

## 1. Session Tracking

**Purpose:** Don't nag repeatedly in same session

**How it works:**

- First edit → Hook blocks, updates session state
- Second edit (same session) → Hook allows
- Different session → Blocks again

**State File:** `.claude/hooks/state/skills-used-{session_id}.json`

## 2. File Markers

**Purpose:** Permanent skip for verified files

**Marker:** `// @skip-validation`

**Usage:**

```typescript
// @skip-validation
import { prisma } from "@server/lib/prisma";
// This file has been manually verified
```

**NOTE:** Use sparingly - defeats the purpose if overused

## 3. Environment Variables

**Purpose:** Emergency disable, temporary override

**Global disable:**

```bash
export SKIP_SKILL_GUARDRAILS=true  # Disables ALL PreToolUse blocks
```

**Skill-specific:**

```bash
export SKIP_DB_VERIFICATION=true
export SKIP_ERROR_REMINDER=true
```
