---
name: web-design-guidelines
version: 1.0.0
description: Review UI code for Web Interface Guidelines compliance. Use when asked to "review my UI", "check accessibility", "audit design", "review UX", or "check my site against best practices".
argument-hint: <file-or-pattern>
user-invocable: true
disable-model-invocation: true
context:
    - resources/web-interface-guidelines.md
metadata:
    author: vercel
    customized: true
    version: "1.0.0"
---

# Web Interface Guidelines

Review files for compliance with Web Interface Guidelines.

## How It Works

1. Read the bundled guidelines from `resources/web-interface-guidelines.md`
2. Read the specified files (or prompt user for files/pattern)
3. Check against all rules in the guidelines
4. Output findings in the terse `file:line` format

## Guidelines Source

The rules are bundled in this skill at `resources/web-interface-guidelines.md`, sourced from:

The resource file is loaded automatically as context when the skill is invoked — no fetching needed.

## Usage

When a user provides a file or pattern argument:

1. Read guidelines from `resources/web-interface-guidelines.md`
2. Read the specified files
3. Apply all rules from the fetched guidelines
4. Output findings using the format specified in the guidelines

If no files specified, ask the user which files to review.

## Arguments

When invoking this skill with arguments:

- `$ARGUMENTS` - File path or glob pattern to review for Web Interface Guidelines compliance
    - Single file: `src/components/Header.tsx`
    - Glob pattern: `src/components/**/*.tsx` (all TypeScript components)
    - Multiple patterns: `src/pages/*.tsx src/components/*.tsx`
    - Example: `/web-design-guidelines src/components/Navigation.tsx`
    - Example: `/web-design-guidelines "src/**/*.tsx"`

The skill will:

1. Read the guidelines from `resources/web-interface-guidelines.md`
2. Expand glob patterns to matching files
3. Read each file and check against all guidelines rules
4. Output findings in `file:line` format

If invoked without arguments, the skill will prompt for which files or patterns to review.
