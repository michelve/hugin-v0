# Advanced Skill Patterns

Patterns discovered and evaluated during skills optimization (Phase 1-5).
Each pattern includes syntax, use cases, recommendations, and troubleshooting.

---

## 1. Ultrathink Keyword

Force extended reasoning for complex analysis by adding `ultrathink` to the skill body.

### Syntax

Place in a dedicated section or inline where deep reasoning is needed:

```markdown
## Analysis Approach

ultrathink

Before generating output, deeply analyze:

1. All existing patterns in the codebase
2. Trade-offs between approaches
3. Edge cases and failure modes
```

### When to Use

- Skills that require multi-step reasoning (architecture analysis, trade-off evaluation)
- Skills that must cross-reference multiple files before acting
- Complex decision-making where shallow analysis leads to poor results

### When NOT to Use

- Template-following workflows (the template provides structure)
- Simple lookup or generation tasks
- Skills already guided by tools (MCP-driven workflows)

### Verification

Test by invoking the skill and observing whether Claude produces deeper analysis
(longer reasoning chains, more considerations, explicit trade-off discussion).

### Skills Using This Pattern

Currently no skills use `ultrathink` — evaluation found that structured templates
and progressive disclosure provide sufficient reasoning depth for all existing skills.

---

## 2. Dynamic Context Injection

Inject live codebase data into skill context using shell command substitution.

### Syntax

```markdown
Available components: `!`ls src/client/components/ui/ | sed 's/\.tsx$//' | sort``
```

The `` `!`command`` `` syntax runs the command and inserts its stdout into the
skill content before Claude processes it. This gives Claude real-time awareness
of project state.

### Safety Rules

- **Read-only commands only** — never use commands that modify files
- **Fast commands only** — must complete in <1s to avoid latency
- **No secrets** — never inject env vars containing credentials
- **Cross-platform** — test on macOS/Linux; Windows may need PowerShell equivalents

### Examples

```markdown
## Available Components

`!`ls src/client/components/ui/ | sed 's/\.tsx$//' | sort``

## Current Database Schema

`!`head -50 prisma/schema.prisma``

## Existing API Routes

`!`grep -r "router\." src/server/routes/ | head -20``

## Current Task Count

`!`ls .tasks/backlog/ 2>/dev/null | wc -l``
```

### Real-World Usage

The `shadcn` skill uses this pattern to show available components:

```markdown
The following shadcn/ui components are already installed:
`!`ls src/client/components/ui/ 2>/dev/null | sed 's/\.tsx$//' | sort | tr '\n' ', '``
```

### Troubleshooting

| Problem                      | Cause                  | Fix                                                        |
| ---------------------------- | ---------------------- | ---------------------------------------------------------- | ------------------------ |
| Command output not appearing | Wrong backtick syntax  | Use `` `!`command`` `` (backtick-bang-backtick)            |
| Empty output                 | Command fails silently | Add `2>/dev/null` or test command manually                 |
| Slow skill loading           | Expensive command      | Use `head`, `tail`, or `                                   | head -N` to limit output |
| Windows incompatibility      | Unix-only command      | Provide PowerShell alternative or use cross-platform tools |

---

## 3. Supporting Files Structure

Extract detailed content from SKILL.md into organized subdirectories to stay under
the 300-line comfortable target (500-line hard limit).

### Directory Conventions

```
.claude/skills/my-skill/
├── SKILL.md                       # Main file (under 300 lines)
├── examples/                      # Worked scenarios
│   ├── basic-usage.md
│   └── advanced-scenarios.md
├── reference/                     # Lookup tables, specs
│   ├── api-reference.md
│   └── troubleshooting.md
├── templates/                     # Reusable templates
│   └── output-template.md
└── scripts/                       # Executable scripts
    └── visualize.py
```

### Reference Syntax in SKILL.md

Replace extracted sections with cross-references:

```markdown
## Examples

See [basic-usage.md](examples/basic-usage.md) for introductory scenarios.
See [advanced-scenarios.md](examples/advanced-scenarios.md) for complex workflows.
```

### Line Count Guidelines

| Threshold | Status      | Action                                     |
| --------- | ----------- | ------------------------------------------ |
| ≤ 300     | Comfortable | No extraction needed                       |
| 301–499   | Warning     | Consider extracting largest sections       |
| ≥ 500     | Hard limit  | Must extract — Claude may truncate content |

### Extraction Decision Framework

Extract a section when:

1. It's ≥ 50 lines AND the SKILL.md is over 300 lines
2. It's reference material (lookup tables, error catalogs, API specs)
3. It's examples/scenarios (detailed step-by-step walkthroughs)
4. It's rarely needed (troubleshooting, edge cases)

Keep inline when:

1. It's < 30 lines (too small to warrant a separate file)
2. It's the core workflow (always needed by Claude)
3. It's the quick-start or decision framework

### Sync Requirement

After editing `.claude/skills/`, always sync to `.github/skills/`:

```powershell
Copy-Item -Path ".claude/skills/<name>/*" -Destination ".github/skills/<name>/" -Recurse -Force
```

---

## 4. Skill-Scoped Hooks

Lifecycle hooks that fire only when a specific skill is active. Unlike global hooks
in `.claude/settings.json` (which run every interaction), skill-scoped hooks are targeted.

### Hypothesized Syntax

Based on global hooks infrastructure (requires Claude Code CLI testing to confirm):

```yaml
---
name: my-skill
hooks:
    UserPromptSubmit:
        - type: command
          command: "python3 ${CLAUDE_SKILL_DIR}/scripts/inject-context.py"
    PreToolUse:
        - matcher: "Write|Edit"
          type: command
          command: "python3 ${CLAUDE_SKILL_DIR}/scripts/validate.py"
---
```

### Hook Types

| Type               | When It Fires             | Can Block?          | Can Inject?  |
| ------------------ | ------------------------- | ------------------- | ------------ |
| `UserPromptSubmit` | Before Claude sees prompt | No                  | Yes (stdout) |
| `PreToolUse`       | Before tool executes      | Yes (non-zero exit) | Yes (stdout) |
| `PostToolUse`      | After tool completes      | No                  | Yes (stdout) |

### Global vs Skill-Scoped

| Aspect      | Global                              | Skill-Scoped              |
| ----------- | ----------------------------------- | ------------------------- |
| Location    | `.claude/settings.json`             | SKILL.md `hooks:` field   |
| Fires       | Every interaction                   | Only when skill is active |
| Use case    | Cross-cutting (commitlint, quality) | Skill-specific validation |
| Performance | Runs every time                     | Only when relevant        |

### Recommended Candidates

Only 2 skills justify the complexity:

1. **adr-writer** — Auto-inject next ADR number and template path
2. **create-tasks** — Auto-inject backlog count and task template

### When NOT to Use

- Skills with template-guided workflows (template provides structure)
- Skills using MCP tools (validation happens tool-side)
- Simple domain knowledge skills (no lifecycle needs)

### Status: DEFERRED

Syntax is hypothesized from global hooks. **Must test in Claude Code CLI before adoption.**
See POC script: `adr-writer/scripts/inject-adr-context.py` for reference implementation.

---

## 5. Model Field

Controls which Claude model handles the skill. Currently no skills use this field.

### Syntax

```yaml
---
name: my-skill
model: claude-opus-4-20250514
---
```

### Evaluation Finding: NOT RECOMMENDED

After evaluating 4 candidate skills (adr-writer, skill-creator, create-design-system-rules,
figma-implement-design), the recommendation is **do not add model field to any skills**.

**Why:**

- All candidates have structural scaffolding (templates, tools, feedback loops)
  that compensates for model capability differences
- Cost/quality trade-off is unfavorable — higher cost, minimal quality improvement
- Hardcoding model names creates maintenance burden when models are updated
- No A/B testing protocol to empirically measure quality differences

### When It Would Be Justified

A skill should use `model` only if ALL three conditions are met:

1. Requires deep reasoning on novel problems (no template guidance)
2. Produces output in a single pass (no iterative refinement)
3. Has high cost of poor quality (irreversible decisions)

### Testing Protocol (If Revisited)

1. Select 3 identical prompts per skill
2. Run each 3× with default model, capture outputs
3. Add `model: claude-opus-4-20250514`
4. Run same prompts 3×, capture outputs
5. Blind comparison — justify only if quality ≥ 20% improvement

---

## 6. Agent Field Optimization

Controls which subagent type runs fork-context skills.

### Available Agent Types

| Agent     | Capabilities            | Best For                     |
| --------- | ----------------------- | ---------------------------- |
| `default` | Full read/write/execute | Tasks requiring file changes |
| `Explore` | Read-only, fast         | Research and Q&A             |
| `Plan`    | Planning-focused        | Strategy development         |

### Syntax

```yaml
---
name: my-skill
context: fork
agent: default # or Explore, Plan, custom
---
```

### Evaluation Finding: Keep Default

All 5 fork-context skills (adr-writer, code-connect-components,
create-design-system-rules, create-tasks, figma-implement-design) require
file write capabilities, which eliminates Explore and Plan.

### Decision Framework

Choose agent type based on workflow outputs:

| Skill produces...                | Agent               |
| -------------------------------- | ------------------- |
| Files (code, docs, configs)      | `default`           |
| Read-only analysis               | `Explore`           |
| Strategic plans (no file output) | `Plan`              |
| Custom tool-heavy workflows      | `default` or custom |

---

## 7. Visual Output Pattern

Bundle scripts in `scripts/` that generate interactive HTML visualizations.

### Directory Structure

```
.claude/skills/my-visualizer/
├── SKILL.md
└── scripts/
    └── visualize.py          # 100-200 LOC
```

### Script Requirements

- **Standalone HTML** — embedded CSS + JS, no external CDN dependencies
- **100-200 LOC** — keep scripts focused on one visualization
- **Portable paths** — reference via `${CLAUDE_SKILL_DIR}/scripts/visualize.py`
- **CLI interface** — accept optional output path argument
- **No pip dependencies** — use Python stdlib only (or Node.js built-ins)

### SKILL.md Reference

```markdown
## Quick Start

Run from project root:
\`\`\`bash
python3 "${CLAUDE_SKILL_DIR}/scripts/visualize-components.py"
\`\`\`
```

### Example: Component Dependency Graph

The `component-visualizer` skill demonstrates this pattern:

- Scans `src/client/components/` and `src/client/routes/` for imports
- Builds a dependency graph from import statements
- Generates interactive force-directed HTML visualization
- Categorizes nodes: routes (blue), components (green), UI/shadcn (purple)
- Features: drag, zoom, hover highlight, category filtering

### POC Evaluation

| Criterion          | Rating | Notes                                                          |
| ------------------ | ------ | -------------------------------------------------------------- |
| User value         | HIGH   | Immediate visual architecture understanding                    |
| Maintenance burden | LOW    | Pure stdlib Python, self-contained HTML                        |
| Performance impact | NONE   | On-demand execution, not in build pipeline                     |
| Extensibility      | HIGH   | Pattern works for API maps, schema diagrams, coverage heatmaps |

### Troubleshooting

| Problem              | Fix                                                                |
| -------------------- | ------------------------------------------------------------------ |
| `python3 not found`  | Install Python 3 or use `python` on Windows                        |
| Empty graph          | Verify `src/client/components/` exists and contains `.tsx` files   |
| Broken HTML          | Check script output for Python errors before opening browser       |
| Imports not detected | Script resolves `@/` alias only; other aliases need manual mapping |
