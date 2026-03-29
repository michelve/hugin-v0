#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# Hook Linter
# Checks hook scripts for common issues and best practices.
# Supports both bash (.sh) and Python (.py) hook scripts.
#
# Adapted from anthropics/claude-plugins-official plugin-dev for hugin-v0.
# Extended with Python hook linting.
#
# Usage:
#   ./scripts/hook-linter.sh <hook-script.sh> [hook-script2.py ...]
#   ./scripts/hook-linter.sh scripts/*.py hooks-handlers/*.sh
# ---------------------------------------------------------------------------

set -euo pipefail

# --- Colors ---
if [ -t 1 ]; then
    RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[0;33m'
    CYAN='\033[0;36m'; BOLD='\033[1m'; RESET='\033[0m'
else
    RED='' GREEN='' YELLOW='' CYAN='' BOLD='' RESET=''
fi

# --- Usage ---
if [ $# -eq 0 ]; then
    cat <<'EOF'
Usage: hook-linter.sh <hook-script> [hook-script2 ...]

Checks hook scripts for common issues and best practices.
Supports .sh (bash) and .py (Python) hook scripts.

Checks for shell scripts:
  - Shebang presence
  - set -euo pipefail usage
  - Input reading from stdin
  - jq usage for JSON parsing
  - Variable quoting (injection risk)
  - Hardcoded absolute paths
  - ${CLAUDE_PLUGIN_ROOT} usage
  - Proper exit codes (0 or 2)
  - Long-running code detection
  - Error messages to stderr

Checks for Python scripts:
  - Shebang or encoding header
  - sys.stdin / input() usage
  - json module usage
  - sys.exit() usage
  - Hardcoded absolute paths
  - Exception handling
  - f-string injection patterns

Examples:
  ./scripts/hook-linter.sh scripts/*.py
  ./scripts/hook-linter.sh hooks-handlers/*.sh
  ./scripts/hook-linter.sh scripts/commitlint-enforcer.py hooks-handlers/session-start.sh
EOF
    exit 1
fi

# ---------------------------------------------------------------------------
# Shell script linter
# ---------------------------------------------------------------------------
check_shell_script() {
    local script="$1"
    local warnings=0
    local errors=0

    echo -e "${BOLD}🔍 Linting (bash): $script${RESET}"
    echo ""

    # Check 1: Executable
    if [ ! -x "$script" ]; then
        echo -e "  ${YELLOW}⚠️  Not executable (chmod +x $script)${RESET}"
        ((warnings++))
    fi

    # Check 2: Shebang
    local first_line
    first_line=$(head -1 "$script")
    if [[ ! "$first_line" =~ ^#!/ ]]; then
        echo -e "  ${RED}❌ Missing shebang (#!/bin/bash or #!/usr/bin/env bash)${RESET}"
        ((errors++))
    fi

    # Check 3: set -euo pipefail
    if ! grep -q "set -euo pipefail" "$script"; then
        echo -e "  ${YELLOW}⚠️  Missing 'set -euo pipefail' (recommended for safety)${RESET}"
        ((warnings++))
    fi

    # Check 4: Reads from stdin
    if ! grep -q "cat\|read\|stdin" "$script"; then
        echo -e "  ${YELLOW}⚠️  Doesn't appear to read input from stdin${RESET}"
        ((warnings++))
    fi

    # Check 5: Uses jq for JSON parsing
    if grep -q "tool_input\|tool_name\|hook_event_name\|session_id" "$script" && ! grep -q "jq" "$script"; then
        echo -e "  ${YELLOW}⚠️  Parses hook input fields but doesn't use jq${RESET}"
        ((warnings++))
    fi

    # Check 6: Unquoted variables
    if grep -En '\$[A-Za-z_][A-Za-z0-9_]*[^"}\)]' "$script" | grep -v '^[[:space:]]*#' | grep -qv '^\s*$'; then
        echo -e "  ${YELLOW}⚠️  Potentially unquoted variables detected (injection risk)${RESET}"
        echo -e "     Always use double quotes: \"\$variable\" not \$variable"
        ((warnings++))
    fi

    # Check 7: Hardcoded absolute paths
    if grep -En '^[^#]*/home/|^[^#]*/Users/|^[^#]*/usr/local/|^[^#]*/opt/' "$script" | grep -qv 'CLAUDE_PLUGIN_ROOT\|CLAUDE_PROJECT_DIR'; then
        echo -e "  ${YELLOW}⚠️  Hardcoded absolute paths detected${RESET}"
        echo -e "     Use \$CLAUDE_PROJECT_DIR or \$CLAUDE_PLUGIN_ROOT"
        ((warnings++))
    fi

    # Check 8: Uses CLAUDE_PLUGIN_ROOT
    if ! grep -q "CLAUDE_PLUGIN_ROOT\|CLAUDE_PROJECT_DIR" "$script"; then
        echo -e "  ${CYAN}💡 Tip: Use \$CLAUDE_PLUGIN_ROOT for plugin-relative paths${RESET}"
    fi

    # Check 9: Exit codes
    if ! grep -q "exit 0\|exit 2" "$script"; then
        echo -e "  ${YELLOW}⚠️  No explicit exit codes (hooks should exit 0 or 2)${RESET}"
        ((warnings++))
    fi

    # Check 10: JSON output for decision hooks
    if grep -q "PreToolUse\|Stop" "$script"; then
        if ! grep -q "permissionDecision\|decision\|additionalContext" "$script"; then
            echo -e "  ${CYAN}💡 Tip: PreToolUse/Stop hooks can output decision JSON${RESET}"
        fi
    fi

    # Check 11: Long-running commands
    if grep -En 'sleep [0-9]{3,}|while true' "$script" | grep -v '^[[:space:]]*#' | grep -qv '^\s*$'; then
        echo -e "  ${YELLOW}⚠️  Potentially long-running code detected${RESET}"
        echo -e "     Hooks should complete quickly (< 60s)"
        ((warnings++))
    fi

    # Check 12: Error messages to stderr
    if grep -q 'echo.*".*[Ee]rror\|echo.*".*[Dd]enied\|echo.*".*[Ff]ailed' "$script"; then
        if ! grep -q '>&2' "$script"; then
            echo -e "  ${YELLOW}⚠️  Error messages should be written to stderr (>&2)${RESET}"
            ((warnings++))
        fi
    fi

    # Check 13: Input validation
    if ! grep -q 'if.*empty\|if.*null\|if.*-z\|\[ -z' "$script"; then
        echo -e "  ${CYAN}💡 Tip: Consider validating input fields aren't empty${RESET}"
    fi

    echo ""
    _print_summary "$errors" "$warnings"
    return $errors
}

# ---------------------------------------------------------------------------
# Python script linter
# ---------------------------------------------------------------------------
check_python_script() {
    local script="$1"
    local warnings=0
    local errors=0

    echo -e "${BOLD}🔍 Linting (python): $script${RESET}"
    echo ""

    # Check 1: Executable
    if [ ! -x "$script" ]; then
        echo -e "  ${YELLOW}⚠️  Not executable (chmod +x $script)${RESET}"
        ((warnings++))
    fi

    # Check 2: Shebang or encoding
    local first_line
    first_line=$(head -1 "$script")
    if [[ ! "$first_line" =~ ^#!/ ]] && [[ ! "$first_line" =~ ^#.*coding ]]; then
        echo -e "  ${CYAN}💡 Tip: Consider adding #!/usr/bin/env python3 shebang${RESET}"
    fi

    # Check 3: Reads from stdin
    if ! grep -q "sys\.stdin\|input()\|fileinput" "$script"; then
        echo -e "  ${YELLOW}⚠️  Doesn't appear to read from sys.stdin${RESET}"
        ((warnings++))
    fi

    # Check 4: Uses json module
    if ! grep -q "import json\|from json" "$script"; then
        echo -e "  ${YELLOW}⚠️  Doesn't import json module (hooks receive JSON on stdin)${RESET}"
        ((warnings++))
    fi

    # Check 5: Uses sys.exit
    if ! grep -q "sys\.exit\|exit(" "$script"; then
        echo -e "  ${YELLOW}⚠️  No explicit sys.exit() call (hooks should exit 0 or 2)${RESET}"
        ((warnings++))
    fi

    # Check 6: Hardcoded absolute paths
    if grep -En "'/home/|'/Users/|'/usr/local/|'/opt/" "$script" | grep -v '^[[:space:]]*#' | grep -qv '^\s*$'; then
        echo -e "  ${YELLOW}⚠️  Hardcoded absolute paths detected${RESET}"
        echo -e "     Use os.environ or CLAUDE_PLUGIN_ROOT"
        ((warnings++))
    fi

    # Check 7: Exception handling
    if ! grep -q "try:\|except\|try " "$script"; then
        echo -e "  ${CYAN}💡 Tip: Consider try/except around JSON parsing for robustness${RESET}"
    fi

    # Check 8: Uses subprocess with shell=True (security risk)
    if grep -q "subprocess.*shell=True\|os\.system(" "$script"; then
        echo -e "  ${RED}❌ Uses shell=True or os.system() — command injection risk${RESET}"
        ((errors++))
    fi

    # Check 9: Checks for required fields
    if grep -q "tool_input\|tool_name\|hook_event_name" "$script"; then
        if ! grep -q "\.get(\|KeyError\|in data\|not in" "$script"; then
            echo -e "  ${YELLOW}⚠️  Accesses hook fields without safe .get() or key check${RESET}"
            ((warnings++))
        fi
    fi

    # Check 10: Long-running patterns
    if grep -En 'time\.sleep\([0-9]{3,}\)|while True' "$script" | grep -v '^[[:space:]]*#' | grep -qv '^\s*$'; then
        echo -e "  ${YELLOW}⚠️  Potentially long-running code detected${RESET}"
        echo -e "     Hooks should complete quickly (< 60s)"
        ((warnings++))
    fi

    # Check 11: Prints to stderr for errors
    if grep -q "print.*[Ee]rror\|print.*[Ff]ailed\|print.*[Dd]enied" "$script"; then
        if ! grep -q "sys\.stderr\|file=sys\.stderr" "$script"; then
            echo -e "  ${CYAN}💡 Tip: Write error messages to sys.stderr${RESET}"
        fi
    fi

    echo ""
    _print_summary "$errors" "$warnings"
    return $errors
}

# ---------------------------------------------------------------------------
# Summary printer
# ---------------------------------------------------------------------------
_print_summary() {
    local errors=$1
    local warnings=$2

    echo "  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    if [ "$errors" -eq 0 ] && [ "$warnings" -eq 0 ]; then
        echo -e "  ${GREEN}✅ No issues found${RESET}"
    elif [ "$errors" -eq 0 ]; then
        echo -e "  ${YELLOW}⚠️  $warnings warning(s)${RESET}"
    else
        echo -e "  ${RED}❌ $errors error(s), $warnings warning(s)${RESET}"
    fi
}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
echo -e "${BOLD}🔎 Hook Script Linter${RESET}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

total_errors=0

for script in "$@"; do
    if [ ! -f "$script" ]; then
        echo -e "${RED}❌ File not found: $script${RESET}"
        ((total_errors++))
        continue
    fi

    if [[ "$script" == *.py ]]; then
        if ! check_python_script "$script"; then
            ((total_errors++))
        fi
    elif [[ "$script" == *.sh ]]; then
        if ! check_shell_script "$script"; then
            ((total_errors++))
        fi
    else
        echo -e "${YELLOW}⚠️  Unknown file type: $script (skipping)${RESET}"
    fi
    echo ""
done

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ $total_errors -eq 0 ]; then
    echo -e "${GREEN}${BOLD}✅ All scripts passed linting${RESET}"
    exit 0
else
    echo -e "${RED}${BOLD}❌ $total_errors script(s) had errors${RESET}"
    exit 1
fi
