#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# Standalone plugin validator — run before committing or pushing.
#
# Usage:
#   ./scripts/validate-plugin.sh                            # full scan
#   ./scripts/validate-plugin.sh skills/react/SKILL.md      # specific file(s)
#   ./scripts/validate-plugin.sh --staged                   # staged files only
#   ./scripts/validate-plugin.sh --fix                      # full scan + auto-fix
#   ./scripts/validate-plugin.sh --fix skills/react/SKILL.md  # fix specific skill
#   ./scripts/validate-plugin.sh --help
# ---------------------------------------------------------------------------

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VALIDATOR="${REPO_ROOT}/.github/scripts/validate-frontmatter.py"

# --- Colors (disabled when piped) ---
if [ -t 1 ]; then
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    YELLOW='\033[0;33m'
    BOLD='\033[1m'
    RESET='\033[0m'
else
    RED='' GREEN='' YELLOW='' BOLD='' RESET=''
fi

# --- Python binary ---
if command -v python3 &>/dev/null; then
    PYTHON=python3
elif command -v python &>/dev/null; then
    PYTHON=python
else
    echo -e "${RED}Error: python not found${RESET}" >&2
    exit 1
fi

# --- Ensure validator exists ---
if [ ! -f "$VALIDATOR" ]; then
    echo -e "${RED}Error: validator not found at $VALIDATOR${RESET}" >&2
    exit 1
fi

# --- Help ---
show_help() {
    cat <<'EOF'
Plugin Validator — validate skills, agents, hooks, evals, and plugin structure.

Usage:
  validate-plugin.sh                              Full project scan
  validate-plugin.sh <file.md> [file2.md ...]     Validate specific files
  validate-plugin.sh --staged                     Validate only git-staged files
  validate-plugin.sh --fix                        Full scan + generate missing scaffolds
  validate-plugin.sh --fix <file.md>              Fix specific skill(s)
  validate-plugin.sh --help                       Show this help

Flags:
  --fix       Auto-generate missing evals/, trigger-evals.json, skills-rules.json
  --staged    Validate only files staged for commit (same as pre-commit hook)
  --help      Show this help message

Exit codes:
  0           All files pass (warnings are allowed)
  1           One or more errors found

Install pre-commit hook:
  ln -sf ../../scripts/pre-commit-validate.sh .git/hooks/pre-commit
EOF
}

# --- Parse arguments ---
FIX_FLAG=""
STAGED_MODE=false
POSITIONAL=()

for arg in "$@"; do
    case "$arg" in
        --help|-h)
            show_help
            exit 0
            ;;
        --fix)
            FIX_FLAG="--fix"
            ;;
        --staged)
            STAGED_MODE=true
            ;;
        *)
            POSITIONAL+=("$arg")
            ;;
    esac
done

cd "$REPO_ROOT"

# --- Staged mode ---
if [ "$STAGED_MODE" = true ]; then
    STAGED=$(git diff --cached --name-only --diff-filter=ACMR 2>/dev/null || true)
    if [ -z "$STAGED" ]; then
        echo -e "${GREEN}No staged files — nothing to validate.${RESET}"
        exit 0
    fi

    MD_RE='(agents/.*\.md|skills/.*/SKILL\.md|commands/.*\.md|output-styles/.*\.md)$'
    STRUCTURAL_RE='(hooks/hooks\.json|settings\.json|\.claude-plugin/plugin\.json|skills/.*/evals/.*\.json|skills/.*/skills-rules\.json)'

    if echo "$STAGED" | grep -qE "$STRUCTURAL_RE"; then
        echo -e "${BOLD}Structural plugin files staged — running full validation...${RESET}"
        $PYTHON "$VALIDATOR" $FIX_FLAG
        RC=$?
    else
        MD_FILES=$(echo "$STAGED" | grep -E "$MD_RE" || true)
        if [ -z "$MD_FILES" ]; then
            echo -e "${GREEN}No plugin files staged — nothing to validate.${RESET}"
            exit 0
        fi
        echo -e "${BOLD}Validating staged plugin files...${RESET}"
        # shellcheck disable=SC2086
        $PYTHON "$VALIDATOR" $FIX_FLAG $MD_FILES
        RC=$?
    fi
else
    # --- Full scan or specific files ---
    if [ ${#POSITIONAL[@]} -gt 0 ]; then
        echo -e "${BOLD}Validating ${#POSITIONAL[@]} file(s)...${RESET}"
        # shellcheck disable=SC2086
        $PYTHON "$VALIDATOR" $FIX_FLAG "${POSITIONAL[@]}"
        RC=$?
    else
        echo -e "${BOLD}Running full plugin validation...${RESET}"
        $PYTHON "$VALIDATOR" $FIX_FLAG
        RC=$?
    fi
fi

# --- Hook linter (optional, only on full validation) ---
HOOK_LINTER="$REPO_ROOT/scripts/hook-linter.sh"
HOOKS_JSON="$REPO_ROOT/hooks/hooks.json"

if [ $RC -eq 0 ] && [ "$STAGED_MODE" = false ] && [ -f "$HOOK_LINTER" ] && [ -f "$HOOKS_JSON" ]; then
    # Collect hook scripts from hooks.json
    HOOK_SCRIPTS=()
    if command -v python3 &>/dev/null; then
        while IFS= read -r hs; do
            # Resolve ${CLAUDE_PLUGIN_ROOT} to repo root
            resolved="${hs//\$\{CLAUDE_PLUGIN_ROOT\}/$REPO_ROOT}"
            if [ -f "$resolved" ]; then
                HOOK_SCRIPTS+=("$resolved")
            fi
        done < <(python3 -c "
import json, re, sys
with open(sys.argv[1]) as f:
    data = json.load(f)
for event_handlers in data.get('hooks', {}).values():
    for handler in event_handlers:
        for hook in handler.get('hooks', []):
            cmd = hook.get('command', '')
            if cmd:
                print(cmd)
" "$HOOKS_JSON" 2>/dev/null)
    fi

    if [ ${#HOOK_SCRIPTS[@]} -gt 0 ]; then
        echo ""
        echo -e "${BOLD}Running hook linter...${RESET}"
        bash "$HOOK_LINTER" "${HOOK_SCRIPTS[@]}" || true
    fi
fi

# --- Result ---
echo ""
if [ $RC -eq 0 ]; then
    echo -e "${GREEN}${BOLD}✓ Validation passed${RESET}"
else
    echo -e "${RED}${BOLD}✗ Validation failed — fix errors before committing${RESET}"
fi

exit $RC
