#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# Git pre-commit hook — validates plugin frontmatter, hooks, and evals.
#
# Install (symlink — recommended):
#   ln -sf ../../scripts/pre-commit-validate.sh .git/hooks/pre-commit
#
# Or copy:
#   cp scripts/pre-commit-validate.sh .git/hooks/pre-commit && chmod +x .git/hooks/pre-commit
#
# Errors block the commit. Warnings are shown but do NOT block.
# Bypass once with: git commit --no-verify
# ---------------------------------------------------------------------------

set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
VALIDATOR="${REPO_ROOT}/.github/scripts/validate-frontmatter.py"

# Pick Python binary
if command -v python3 &>/dev/null; then
    PYTHON=python3
elif command -v python &>/dev/null; then
    PYTHON=python
else
    echo "pre-commit: python not found — skipping validation"
    exit 0
fi

# Ensure validator exists
if [ ! -f "$VALIDATOR" ]; then
    echo "pre-commit: validator not found at $VALIDATOR — skipping"
    exit 0
fi

# Get staged files (added/modified/copied/renamed — index only)
STAGED=$(git diff --cached --name-only --diff-filter=ACMR 2>/dev/null || true)

if [ -z "$STAGED" ]; then
    exit 0
fi

# Patterns that require a full project scan
STRUCTURAL_RE='(hooks/hooks\.json|settings\.json|\.claude-plugin/plugin\.json|skills/.*/evals/.*\.json|skills/.*/skills-rules\.json)'

# Patterns for individual .md file validation
MD_RE='(agents/.*\.md|skills/.*/SKILL\.md|commands/.*\.md|output-styles/.*\.md)$'

# Check if any structural files were staged
if echo "$STAGED" | grep -qE "$STRUCTURAL_RE"; then
    echo "==> Structural plugin files changed — running full validation..."
    cd "$REPO_ROOT"
    $PYTHON "$VALIDATOR"
    exit $?
fi

# Collect staged .md files that match plugin paths
MD_FILES=$(echo "$STAGED" | grep -E "$MD_RE" || true)

if [ -z "$MD_FILES" ]; then
    # No plugin-relevant files staged — nothing to do
    exit 0
fi

echo "==> Validating staged plugin files..."
cd "$REPO_ROOT"
# shellcheck disable=SC2086
$PYTHON "$VALIDATOR" $MD_FILES
exit $?
